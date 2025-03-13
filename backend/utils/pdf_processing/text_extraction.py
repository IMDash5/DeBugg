# Функция для извлечения текста
def text_extraction(element):
    # Извлечение текста из текстового элемента
    line_text = element.get_text()
    
    # Определение форматов текста
    # Создание списка всех форматов, использованных в строке
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Перебор каждого символа в строке текста
            for character in text_line:
                if isinstance(character, LTChar):
                    # Добавление имени шрифта символа
                    line_formats.append(character.fontname)
                    # Добавление размера шрифта символа
                    line_formats.append(character.size)
    # Определение уникальных размеров и названий шрифтов
    format_per_line = list(set(line_formats))
    
    # Возвращает кортеж с текстом строки и его форматом
    return (line_text, format_per_line)