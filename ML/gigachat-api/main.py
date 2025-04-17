# конект с парсером 
# добавить промптов
# расширить шаблоны
# добавить комментарии к функциям 
# логику для вывода только нужной части

from PyPDF2 import PdfReader
from gigachat import GigaChat
from gigachat.models import Chat, Messages
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
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
        api_key = "NDBkYzg5OTQtNTI1ZC00N2FkLWIyMjEtZDk2ZjQzZDU2MDM3Ojk5ZDUxZGMwLWZhYTMtNGFlYi05ODRjLTI1NGYzNTBiMGNhZg=="  # Замените на реальный ключ
        
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
                
            # 3. Анализируем и выводим результат
            print("\nРезультат анализа:")
            result = analyzer.analyze_resume(resume_text, user_query)
            print(result)
            
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")