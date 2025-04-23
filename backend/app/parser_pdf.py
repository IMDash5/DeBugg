import PyPDF2  
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTFigure  
import pdfplumber  
from PIL import Image  
from pdf2image import convert_from_path  
import pytesseract  

# Функция для извлечения текста
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

# Функция для извлечения таблицы из PDF
def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    
    return table

# Функция для конвертации таблицы в строковый формат
def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    table_string = table_string[:-1]
    return table_string

# Функция для проверки, находится ли элемент внутри таблицы
def is_element_inside_any_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

# Функция для поиска таблицы, в которой находится элемент
def find_table_for_element(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i 
    return None  

# Функция для обрезки изображений из PDF
def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1] 
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Функция для преобразования PDF в изображения
def convert_to_images(input_file):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = 'PDF_image.png'
    image.save(output_file, 'PNG')

# Функция для извлечения текста из изображения
def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='rus+eng')
    return text


def pdf_parser(pdf_path: str) -> str:
    text_per_page = {}
    image_flag = False
    
    pdfFileObj = open(pdf_path, "rb")
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)
    
    for pagenum, page in enumerate(extract_pages(pdf_path)):
        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        line_format = []
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

            # обработка таблицы
            if table_in_page != -1 and is_element_inside_any_table(element, page, tables):
                if find_table_for_element(element, page, tables) == table_in_page:
                    page_content.append(text_from_tables[table_in_page])
                    table_in_page += 1
                continue

            # Обработка текста
            if isinstance(element, LTTextContainer):
                line_text, format_per_line = text_extraction(element)
                page_text.append(line_text)
                page_content.append(line_text)

            # Обработка изображений
            if isinstance(element, LTFigure):
                crop_image(element, pageObj)
                convert_to_images('cropped_image.pdf')
                image_text = image_to_text('PDF_image.png')
                text_from_images.append(image_text)
                page_content.append(image_text)
                image_flag = True

        text_per_page[f'Страница {pagenum}'] = [
            page_text,
            line_format,
            text_from_images,
            text_from_tables,
            page_content
        ]

    full_text = []
    for page_num in text_per_page:
        page_content = text_per_page[page_num][4]
        full_text.append('\n'.join(page_content))

    # Закрытие файла и очистка
    pdfFileObj.close()
    if image_flag:
        import os
        os.remove('cropped_image.pdf')
        os.remove('PDF_image.png')

    return '\n\n'.join(full_text)
