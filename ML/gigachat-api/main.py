import logging
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pdfplumber
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTFigure, LTTextContainer
from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from gigachat import GigaChat
from gigachat.models import Chat, Messages

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_feedback_from_user() -> bool:
    """Запрашивает у человека «да/нет», возвращает True/False."""
    while True:
        answer = input("Вам нравится ответ? (да/нет): ").strip().lower()
        if answer in {"да", "нет"}:
            return answer == "да"
        print("Пожалуйста, введите 'да' или 'нет'.")


def text_extraction(element) -> Tuple[str, List]:
    """Получает текст и список (шрифты, размер) из LTTextContainer."""
    line_text = element.get_text()
    line_formats: list = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    return line_text, list(set(line_formats))


def extract_table(pdf_path: str, page_num: int, table_num: int) -> List[List[str]]:
    with pdfplumber.open(pdf_path) as pdf:
        return pdf.pages[page_num].extract_tables()[table_num]


def table_converter(table: List[List[str]]) -> str:
    """Конвертирует таблицу в Markdown-строки."""
    rows = []
    for row in table:
        cleaned = [
            "None" if cell is None else cell.replace("\n", " ") for cell in row
        ]
        rows.append("|" + "|".join(cleaned) + "|")
    return "\n".join(rows)


def is_inside_table(element, page, tables) -> bool:
    x0, y0up, x1, y1up = element.bbox
    y0, y1 = page.bbox[3] - y1up, page.bbox[3] - y0up
    for tb in tables:
        tx0, ty0, tx1, ty1 = tb.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False


def which_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0, y1 = page.bbox[3] - y1up, page.bbox[3] - y0up
    for idx, tb in enumerate(tables):
        tx0, ty0, tx1, ty1 = tb.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return idx
    return None


def crop_image(element, page_obj) -> Path:
    """Сохраняет figure-объект в temp PDF, возвращает путь."""
    pdf_writer = PyPDF2.PdfWriter()
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    page_obj.mediabox.lower_left = (element.x0, element.y0)
    page_obj.mediabox.upper_right = (element.x1, element.y1)
    pdf_writer.add_page(page_obj)
    with open(tmp_pdf.name, "wb") as f:
        pdf_writer.write(f)
    return Path(tmp_pdf.name)


def pdf_page_to_png(pdf_path: Path) -> Path:
    """Конвертирует первую страницу temp-PDF в temp-PNG и возвращает путь."""
    image = convert_from_path(str(pdf_path), first_page=1, last_page=1)[0]
    tmp_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(tmp_png.name, "PNG")
    return Path(tmp_png.name)


def image_to_text(img_path: Path) -> str:
    return pytesseract.image_to_string(Image.open(img_path), lang="rus+eng")


def pdf_parser(pdf_path: str) -> str:
    """Извлекает текст/таблицы/картинки из PDF."""
    temp_files: List[Path] = []
    pages_content: Dict[int, List[str]] = {}

    with open(pdf_path, "rb") as pdf_obj:
        pdf_reader = PyPDF2.PdfReader(pdf_obj)

        for pagenum, page in enumerate(extract_pages(pdf_path)):
            page_obj = pdf_reader.pages[pagenum]
            page_parts: list = []

            with pdfplumber.open(pdf_path) as pdf:
                tables = pdf.pages[pagenum].find_tables()
                table_strings = [
                    table_converter(extract_table(pdf_path, pagenum, i))
                    for i in range(len(tables))
                ]

            table_cursor = 0
            elements = sorted(page._objs, key=lambda el: el.y1, reverse=True)

            for element in elements:
                # таблицы
                if tables and is_inside_table(element, page, tables):
                    if which_table(element, page, tables) == table_cursor:
                        page_parts.append(table_strings[table_cursor])
                        table_cursor += 1
                    continue

                # текст
                if isinstance(element, LTTextContainer):
                    text, _ = text_extraction(element)
                    page_parts.append(text)
                    continue

                # изображения
                if isinstance(element, LTFigure):
                    cropped_pdf = crop_image(element, page_obj)
                    temp_files.append(cropped_pdf)
                    png_path = pdf_page_to_png(cropped_pdf)
                    temp_files.append(png_path)
                    page_parts.append(image_to_text(png_path))

            pages_content[pagenum] = page_parts

    # очистка
    for fp in temp_files:
        try:
            fp.unlink(missing_ok=True)
        except Exception as e:
            logger.debug(f"Не удалось удалить {fp}: {e}")

    return "\n\n".join("\n".join(pages_content[p]) for p in sorted(pages_content))


# ──────────────────────────────────────────── main class
class ResumeAnalyzer:
    """Основной класс: классифицирует запрос и вызывает GigaChat."""

    def __init__(self, gigachat_api_key: str, model: str = "GigaChat-Pro") -> None:
        if not gigachat_api_key:
            raise ValueError("API-ключ GigaChat не может быть пустым")

        self.api_key = gigachat_api_key
        self.model = model
        self.sim_threshold = 0.7

        self.embedding_model = SentenceTransformer("cointegrated/LaBSE-en-ru")

        self.query_templates: Dict[str, Tuple[str, ...]] = {
            "summary": ("краткое содержание", "сделай выжимку", "основные моменты"),
            "strengths": ("сильные стороны", "преимущества", "что умеет"),
            "weaknesses": ("слабые стороны", "недостатки", "что улучшить"),
            "positions": ("подходящие должности", "вакансии", "какие позиции"),
            "questions": (
                "вопросы для собеседования",
                "interview questions",
                "какие вопросы зададут",
                "список вопросов",
            ),
            "skills_check": (
                "проверка навыков",
                "skills check",
                "оценка навыков",
                "соответствие навыков",
                "skills vs experience",
            ),
            "hidden_jobs": (
                "скрытые вакансии",
                "hidden jobs",
                "неочевидные вакансии",
                "альтернативные должности",
                "незаполненные роли",
                "latent opportunities",
            ),
        }

        # кэшируем эмбеддинги
        self.template_vectors = {
            key: self.embedding_model.encode(list(phrases))
            for key, phrases in self.query_templates.items()
        }

    # ────────────────────────────── public API

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"Файл {pdf_path} не найден")
        text = pdf_parser(pdf_path)
        if not text:
            raise ValueError("Не удалось извлечь текст из PDF")
        return text

    # ────────────────────────────── helpers

    def _classify_query(self, query: str) -> str:
        query_vec = self.embedding_model.encode([query.lower()])
        best_key, best_score = "general", -1.0

        for key, tmpl_vecs in self.template_vectors.items():
            score = cosine_similarity(query_vec, tmpl_vecs).max()
            if score > best_score:
                best_key, best_score = key, score

        return best_key if best_score >= self.sim_threshold else "general"

    def _generate_prompt(self, qtype: str) -> str:
        prompts = {
            "summary": """Сделай аналитическую выжимку из резюме. Выдели:
1. Ключевые навыки (Hard Skills)
2. Опыт работы (компании, сроки, должности)
3. Образование и сертификации
4. Рекомендуемые должности
5. Самые значимые KPI/результаты (цифры, рост %, экономия $)""",

            "strengths": """Проанализируй сильные стороны кандидата:
1. Технические компетенции
2. Уникальный опыт
3. Карьерные достижения
4. Потенциал развития
5. Что отличает кандидата от 80-го перцентиля рынка""",

            "weaknesses": """Выяви слабые места в резюме и дай рекомендации:
1. Недостающие навыки для целевых позиций
2. Проблемы в оформлении
3. Рекомендации по улучшению
4. Курсы/сертификации для восполнения пробелов
5. Потенциальные «red flags» для рекрутёра (частые переходы, однотипные задачи)""",

            "positions": """Рекомендуй подходящие должности для этого кандидата:
1. Основные варианты (по опыту)
2. Альтернативные варианты (смежные области)
3. Перспективные направления развития
4. Требования к каждой позиции
5. Две позиции stretch-уровня (на 1–2 грейда выше текущего)""",

            "questions": """Ты - профессиональный HR-специалист с 10-летним опытом проведения собеседований.
Проанализируй предоставленное резюме и сгенерируй список вероятных вопросов для собеседования.

Формат ответа ДОЛЖЕН быть строго следующим:

**Категория: [Название категории]**
- [Тип вопроса]: "[Текст вопроса]"
  • Зачем задают: [Цель]
  • Что проверяют: [Навыки/качества]
  • Пример хорошего ответа: "[Пример]"

Категории:
1. Общие вопросы
2. Вопросы по опыту работы
3. Технические/профессиональные вопросы
4. Поведенческие вопросы (по STAR)
5. Вопросы о компании
(Добавь по 2-3 вопроса в каждую категорию.)""",

            "skills_check": """Проанализируй резюме кандидата и оцени, насколько указанные навыки и уровень квалификации соответствуют описанию профессионального опыта. 
Выяви риски, несоответствия и возможное завышение компетенций.

1. Определи заявленные навыки (блоки “Skills/Навыки”).  
2. Сопоставь навыки с фактическими проектами/достижениями.  
3. Отметь неподтверждённые навыки.  
4. Проверь завышение уровня (Senior vs junior-задачи).  
5. Найди временные и содержательные противоречия.

**Формат вывода:**  
Обнаруженные риски:  
1. …  
2. …""",

            "hidden_jobs": """Ты – карьерный консультант по «скрытому рынку» труда.
На основе резюме предложи **скрытые или малоафишируемые вакансии**.

Для каждой рекомендации укажи:
• **Название роли/проекта**  
• **Почему подходит** (2-3 факта)  
• **Где искать** (канал, коммьюнити)  
• **Как привлечь внимание** (ракурс опыта, pet-project, реферал)

Скрытые возможности:
1. **…**  
   • Почему подходит: …  
   • Где искать: …  
   • Как привлечь внимание: …  
2. … (3–6 позиций)""",

            "general": "Ты профессиональный HR-аналитик. Проанализируй резюме и дай развернутый ответ на запрос пользователя.",
        }
        return prompts.get(qtype, prompts["general"])


    def analyze_resume(self, resume_text: str, user_query: str) -> str:
        """Возвращает ответ GigaChat согласно классифицированному запросу."""
        try:
            qtype = self._classify_query(user_query)
            logger.info("Классификация запроса: %s", qtype)

            prompt = self._generate_prompt(qtype)
            if qtype == "general":
                prompt += f"\n\nЗапрос пользователя: {user_query}"

            giga = GigaChat(
                credentials=self.api_key,
                model=self.model,
                verify_ssl_certs=False,
                timeout=60,
            )

            messages = [
                Messages(role="system", content="Ты профессиональный HR-аналитик."),
                Messages(role="user", content=f"{prompt}\n\nРезюме:\n{resume_text}"),
            ]
            reply = giga.chat(Chat(messages=messages))
            return reply.choices[0].message.content

        except Exception as exc:
            logger.error("Ошибка запроса к GigaChat: %s", exc)
            raise


if __name__ == "__main__":
    API_KEY = (
        "NDBkYzg5OTQtNTI1ZC00N2FkLWIyMjEtZDk2ZjQzZDU2MDM3Ojk5ZDUxZGMwLWZhYTMt"
        "NGFlYi05ODRjLTI1NGYzNTBiMGNhZg=="
    )

    analyzer = ResumeAnalyzer(gigachat_api_key=API_KEY)

    pdf_path = input("Укажите путь к резюме (PDF): ").strip()
    text = analyzer.extract_text_from_pdf(pdf_path)

    while True:
        query = input("\nВведите запрос (или 'exit'): ").strip()
        if query.lower() == "exit":
            break
        if not query:
            print("Запрос не может быть пустым!")
            continue

        print("\nРезультат анализа:")
        print(analyzer.analyze_resume(text, query))

        if not get_feedback_from_user():
            print("\nПерегенерируем ответ...")
            print(analyzer.analyze_resume(text, query))
