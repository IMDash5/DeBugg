from PyPDF2 import PdfReader
from gigachat import GigaChat
from gigachat.models import Chat, Message
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ResumeAnalyzer:
    
    def __init__(self, gigachat_api_key: str, model: str = "GigaChat-Pro"):
        self.api_key = gigachat_api_key
        self.model = model
        self.embeddings = HuggingFaceEmbeddings(model_name="cointegrated/LaBSE-en-ru")

    # Извлекаем текст из PDF файла        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    # Разбиваем текст на фрагменты
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len
        )
        return splitter.split_text(text)
    
    # Создаем векторное хранилище для семантического поиска
    def create_vector_store(self, chunks: list[str]) -> FAISS:
        return FAISS.from_texts(chunks, embedding=self.embeddings)
    
    # Отправляем запрос в gigachat-api
    def analyze_with_gigachat(self, prompt: str, context: str) -> str:
        giga = GigaChat(
            credentials=self.api_key,
            model=self.model,
            verify_ssl_certs=False
        )
        
        messages = [
            Message(role="system", content="Ты профессиональный HR-аналитик."),
            Message(role="user", content=f"{prompt}\n\nКонтекст:\n{context}")
        ]
        
        response = giga.chat(Chat(messages=messages))
        return response.choices[0].message.content
    
    # Генерируем краткое содержание резюмк
    def generate_summary(self, resume_text: str) -> str:
        prompt = """Сделай аналитическую выжимку из резюме. Выдели:
1. Ключевые навыки
2. Опыт работы
3. Образование
4. Рекомендуемые должности"""
        return self.analyze_with_gigachat(prompt, resume_text)
    
    # Анализ сильных сторон
    def analyze_strengths(self, resume_text: str) -> str:
        prompt = """Выдели сильные стороны кандидата:
1. Технические навыки
2. Уникальный опыт
3. Карьерные достижения"""
        return self.analyze_with_gigachat(prompt, resume_text)
    
    # Анализ слабых сторон
    def analyze_weaknesses(self, resume_text: str) -> str:
        prompt = """Выяви слабые места и дай рекомендации:
1. Недостающие навыки
2. Проблемы в оформлении
3. Советы по улучшению"""
        return self.analyze_with_gigachat(prompt, resume_text)
    
    # Рекомендация подходящих должностей
    def suggest_job_titles(self, resume_text: str) -> str:
        prompt = """Подбери 5 подходящих должностей. Для каждой укажи:
- Уровень (Junior/Middle/Senior)
- Ключевые требования
- Совпадение с навыками"""
        return self.analyze_with_gigachat(prompt, resume_text)

# Надо затестить:
# 1. подкл. апи ключ
# 2. резюмешку сохранить
# 3. маин дописать для теста