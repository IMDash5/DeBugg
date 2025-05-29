import PyPDF2
from gigachat import GigaChat
from gigachat.models import Chat, Messages
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import logging
import pdfplumber
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTFigure 
from config import GIGACHAT_API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик ошибок, если понадобится
def get_feedback_from_user():
    while True:
        print("Вам нравится ответ? (да/нет)")
        feedback = input().strip().lower()
        if feedback == 'да':
            return True
        elif feedback == 'нет':
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")


def text_extraction(element):
    line_text = element.get_text()
    
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    
    return (line_text, format_per_line)

def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    
    return table

def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    table_string = table_string[:-1]
    return table_string

def is_element_inside_any_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

def find_table_for_element(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i 
    return None  

def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1] 
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

def convert_to_images(input_file):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = 'PDF_image.png'
    image.save(output_file, 'PNG')

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='rus+eng')
    return text

def pdf_parser(pdf_path: str) -> str:
    text_per_page = {}
    image_flag = False
    temp_files = []  # Собираем пути для последующей очистки

    pdfFileObj = open(pdf_path, "rb")
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)
    
    try:
        for pagenum, page in enumerate(extract_pages(pdf_path)):
            pageObj = pdfReaded.pages[pagenum]
            page_text = []
            text_from_images = []
            text_from_tables = []
            page_content = []
            table_in_page = -1

            with pdfplumber.open(pdf_path) as pdf:
                page_tables = pdf.pages[pagenum]
                tables = page_tables.find_tables()

                if len(tables) != 0:
                    table_in_page = 0

                for table_num in range(len(tables)):
                    table = extract_table(pdf_path, pagenum, table_num)
                    table_string = table_converter(table)
                    text_from_tables.append(table_string)

            page_elements = [(element.y1, element) for element in page._objs]
            page_elements.sort(key=lambda a: a[0], reverse=True)

            for i, component in enumerate(page_elements):
                element = component[1]

                if table_in_page != -1 and is_element_inside_any_table(element, page, tables):
                    if find_table_for_element(element, page, tables) == table_in_page:
                        page_content.append(text_from_tables[table_in_page])
                        table_in_page += 1
                    continue

                if isinstance(element, LTTextContainer):
                    line_text, _ = text_extraction(element)
                    page_text.append(line_text)
                    page_content.append(line_text)

                if isinstance(element, LTFigure):
                    cropped_path = f"cropped_image_{pagenum}_{i}.pdf"
                    image_path = f"PDF_image_{pagenum}_{i}.png"
                    temp_files.extend([cropped_path, image_path])

                    # Обрезаем и сохраняем как PDF
                    pageObj.mediabox.lower_left = (element.x0, element.y0)
                    pageObj.mediabox.upper_right = (element.x1, element.y1)
                    cropped_pdf_writer = PyPDF2.PdfWriter()
                    cropped_pdf_writer.add_page(pageObj)
                    with open(cropped_path, 'wb') as cropped_pdf_file:
                        cropped_pdf_writer.write(cropped_pdf_file)

                    # Конвертируем PDF в изображение
                    images = convert_from_path(cropped_path)
                    images[0].save(image_path, 'PNG')

                    # Извлекаем текст из изображения
                    image_text = image_to_text(image_path)
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    image_flag = True

            text_per_page[f'Страница {pagenum}'] = [
                page_text,
                [],  # line_format больше не нужен
                text_from_images,
                text_from_tables,
                page_content
            ]
    finally:
        pdfFileObj.close()

        # Удаляем все временные файлы
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)

    full_text = []
    for page_num in text_per_page:
        page_content = text_per_page[page_num][4]
        full_text.append('\n'.join(page_content))

    return '\n\n'.join(full_text)


class ResumeAnalyzer:
    
    def __init__(self, gigachat_api_key: str, model: str = "GigaChat-Pro"):
        if not gigachat_api_key:
            raise ValueError("API ключ GigaChat не может быть пустым")
        
        self.api_key = gigachat_api_key
        self.model = model
        
        self.embedding_model = SentenceTransformer('cointegrated/LaBSE-en-ru')
        
        self.query_templates = {
            "summary": ("краткое содержание", "сделай выжимку", "основные моменты"),
            "strengths": ("сильные стороны", "преимущества", "что умеет"),
            "weaknesses": ("слабые стороны", "недостатки", "что улучшить"),
            "positions": ("подходящие должности", "вакансии", "какие позиции")
        }
        
        self.template_vectors = {}
        for key, phrases in self.query_templates.items():
            self.template_vectors[key] = self.embedding_model.encode(phrases)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Файл {pdf_path} не найден")
            
        # Заменили старый парсер на ваш
        text = pdf_parser(pdf_path)
        if not text:
            raise ValueError("Не удалось извлечь текст из PDF")
        return text

    def _classify_query(self, user_query: str) -> str:
        query_vector = self.embedding_model.encode([user_query.lower()])
        
        max_similarity = -1
        best_match = None
        
        for key, template_vectors in self.template_vectors.items():
            similarities = cosine_similarity(query_vector, template_vectors)
            current_max = np.max(similarities)
            
            if current_max > max_similarity:
                max_similarity = current_max
                best_match = key
        
        if max_similarity > 0.7:
            return best_match
        return "general"

    def _generate_prompt(self, query_type: str) -> str:
        prompts = {
            "summary": """Сделай аналитическую выжимку из резюме. Выдели:
1. Ключевые навыки (Hard Skills)
2. Опыт работы (компании, сроки, должности)
3. Образование и сертификации
4. Рекомендуемые должности""",
            
            "strengths": """Проанализируй сильные стороны кандидата:
1. Технические компетенции
2. Уникальный опыт
3. Карьерные достижения
4. Потенциал развития""",
            
            "weaknesses": """Выяви слабые места в резюме и дай рекомендации:
1. Недостающие навыки для целевых позиций
2. Проблемы в оформлении
3. Рекомендации по улучшению
4. Курсы/сертификации для восполнения пробелов""",
            
            "positions": """Рекомендуй подходящие должности для этого кандидата:
1. Основные варианты (по опыту)
2. Альтернативные варианты (смежные области)
3. Перспективные направления развития
4. Требования к каждой позиции""",
            
            "general": """Ты профессиональный HR-аналитик. Проанализируй резюме и дай развернутый ответ на запрос пользователя.""" 
        }
        
        return prompts.get(query_type, prompts["general"])

    def analyze_resume(self, resume_text: str, user_query: str) -> str:
        try:
            query_type = self._classify_query(user_query)
            logger.info(f"Запрос классифицирован как: {query_type}")
            
            prompt = self._generate_prompt(query_type)
            
            if query_type == "general":
                prompt += f"\n\nЗапрос пользователя: {user_query}"
            
            giga = GigaChat(
                credentials=self.api_key,
                model=self.model,
                verify_ssl_certs=False,
                timeout=60
            )
            
            messages = [
                Messages(role="system", content="Ты профессиональный HR-аналитик."),
                Messages(role="user", content=f"{prompt}\n\nРезюме:\n{resume_text}")
            ]
            
            response = giga.chat(Chat(messages=messages))
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка запроса к GigaChat: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        api_key = GIGACHAT_API
        
        analyzer = ResumeAnalyzer(gigachat_api_key=api_key)
        
        pdf_path = "resume.pdf"
        resume_text = analyzer.extract_text_from_pdf(pdf_path)
        
        while True:
            print("\nВведите ваш запрос к резюме (или 'exit' для выхода):")
            user_query = input().strip()
            
            if user_query.lower() == 'exit':
                break
                
            if not user_query:
                print("Запрос не может быть пустым!")
                continue
                
            print("\nРезультат анализа:")
            result = analyzer.analyze_resume(resume_text, user_query)
            print(result)

            # Запросить обратную связь
            if not get_feedback_from_user():
                print("\nПереработаем ответ...")
                # Здесь можно добавить логику для переработки ответа на основе обратной связи от пользователя
                result = analyzer.analyze_resume(resume_text, user_query)
                print(result)
                continue
            
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
