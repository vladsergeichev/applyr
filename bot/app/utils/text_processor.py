import re


def extract_vacancy_name(text: str) -> str:
    """Извлекает название вакансии из первой строки текста"""
    lines = text.strip().split("\n")
    if lines:
        # Убираем лишние пробелы
        first_line = lines[0].strip()

        # Убираем только эмодзи и некоторые специальные символы, но сохраняем пунктуацию
        # Удаляем эмодзи (расширенный диапазон Unicode emoji)
        # Включаем все основные диапазоны эмодзи
        emoji_pattern = re.compile(
            r"[\U0001F600-\U0001F64F"  # Emoticons
            r"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
            r"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
            r"\U0001F1E0-\U0001F1FF"  # Regional Indicator Symbols
            r"\U00002600-\U000027BF"  # Miscellaneous Symbols
            r"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            r"\U0001F018-\U0001F270"  # Miscellaneous Symbols
            r"\U0000231A-\U0000231B"  # Clock symbols
            r"\U000023E9-\U000023EC"  # Arrow symbols
            r"\U000023F0"  # Alarm clock
            r"\U000023F3"  # Hourglass
            r"\U000025FD-\U000025FE"  # White/black squares
            r"\U00002614-\U00002615"  # Umbrella
            r"\U00002648-\U00002653"  # Zodiac symbols
            r"\U0000267F"  # Wheelchair
            r"\U00002692-\U00002697"  # Tools
            r"\U00002699"  # Gear
            r"\U000026A0-\U000026A1"  # Warning symbols
            r"\U000026AA-\U000026AB"  # White/black circles
            r"\U000026B0-\U000026B1"  # Coffin
            r"\U000026C4-\U000026C5"  # Snowman
            r"\U000026CE"  # Ophiuchus
            r"\U000026D4"  # No entry
            r"\U000026EA"  # Church
            r"\U000026F2-\U000026F3"  # Fountain
            r"\U000026F5"  # Sailboat
            r"\U000026FA"  # Tent
            r"\U000026FD"  # Fuel pump
            r"\U00002705"  # White check mark
            r"\U0000270A-\U0000270B"  # Fist
            r"\U00002728"  # Sparkles
            r"\U0000274C"  # Cross mark
            r"\U0000274E"  # Negative squared cross mark
            r"\U00002753-\U00002755"  # Question/exclamation marks
            r"\U00002757"  # Heavy exclamation mark
            r"\U00002795-\U00002797"  # Plus/minus
            r"\U000027B0"  # Curly loop
            r"\U000027BF"  # Double curly loop
            r"\U00002B1B-\U00002B1C"  # White/black large squares
            r"\U00002B50"  # White medium star
            r"\U00002B55"  # Heavy large circle
            r"\U0001F004"  # Mahjong tile
            r"\U0001F0CF"  # Joker
            r"\U0001F170-\U0001F171"  # Negative squared letters
            r"\U0001F17E-\U0001F17F"  # Negative squared letters
            r"\U0001F18E"  # Negative squared AB
            r"\U0001F191-\U0001F19A"  # Squared symbols
            r"\U0001F1E6-\U0001F1FF"  # Regional indicators
            r"\U0001F201-\U0001F202"  # Squared katakana
            r"\U0001F21A"  # Squared CJK
            r"\U0001F22F"  # Squared CJK
            r"\U0001F232-\U0001F23A"  # Squared CJK
            r"\U0001F250-\U0001F251"  # Circled ideographs
            r"\U0001F300-\U0001F321"  # Weather symbols
            r"\U0001F324-\U0001F393"  # Weather and objects
            r"\U0001F396-\U0001F397"  # Military symbols
            r"\U0001F399-\U0001F39B"  # Music symbols
            r"\U0001F39E-\U0001F3F0"  # Buildings
            r"\U0001F3F3-\U0001F3F5"  # Flags
            r"\U0001F3F7-\U0001F3FA"  # Objects
            r"\U0001F400-\U0001F4FD"  # Animals and objects
            r"\U0001F4FF-\U0001F53D"  # Objects and symbols
            r"\U0001F549-\U0001F54E"  # Religious symbols
            r"\U0001F550-\U0001F567"  # Clock faces
            r"\U0001F56F-\U0001F570"  # Objects
            r"\U0001F573-\U0001F57A"  # Objects
            r"\U0001F587"  # Paperclip
            r"\U0001F58A-\U0001F58D"  # Writing implements
            r"\U0001F590"  # Hand
            r"\U0001F595-\U0001F596"  # Hands
            r"\U0001F5A4-\U0001F5A5"  # Computer
            r"\U0001F5A8"  # Printer
            r"\U0001F5B1-\U0001F5B2"  # Computer
            r"\U0001F5BC"  # Picture frame
            r"\U0001F5C2-\U0001F5C4"  # Card files
            r"\U0001F5D1-\U0001F5D3"  # Wastebasket
            r"\U0001F5DC-\U0001F5DE"  # Compress
            r"\U0001F5E1"  # Knife
            r"\U0001F5E3"  # Speaking head
            r"\U0001F5E8"  # Left speech bubble
            r"\U0001F5EF"  # Right anger bubble
            r"\U0001F5F3"  # Ballot box
            r"\U0001F5FA-\U0001F64F"  # Map and people
            r"\U0001F680-\U0001F6C5"  # Transport
            r"\U0001F6CB-\U0001F6D2"  # Furniture
            r"\U0001F6E0-\U0001F6E5"  # Tools
            r"\U0001F6E9"  # Airplane
            r"\U0001F6EB-\U0001F6EC"  # Airplane
            r"\U0001F6F0"  # Satellite
            r"\U0001F6F3-\U0001F6F9"  # Transport
            r"\U0001F910-\U0001F93A"  # People
            r"\U0001F93C-\U0001F93E"  # Sports
            r"\U0001F940-\U0001F945"  # Sports
            r"\U0001F947-\U0001F970"  # Sports and people
            r"\U0001F973-\U0001F976"  # People
            r"\U0001F97A"  # Face
            r"\U0001F97C-\U0001F9A2"  # Animals
            r"\U0001F9B0-\U0001F9B9"  # Hair
            r"\U0001F9C0-\U0001F9C2"  # Food
            r"\U0001F9D0-\U0001F9FF"  # People and objects
            r"\U0001FA70-\U0001FA73"  # Objects
            r"\U0001FA78-\U0001FA7A"  # Objects
            r"\U0001FA80-\U0001FA82"  # Objects
            r"\U0001FA90-\U0001FA95"  # Objects
            r"\U0001FA96-\U0001FAA8"  # Objects
            r"\U0001FAB0-\U0001FAB6"  # Objects
            r"\U0001FAC0-\U0001FAC2"  # People
            r"\U0001FAD0-\U0001FAD6"  # Food
            r"\U0001FAD8-\U0001FADA"  # Objects
            r"\U0001FADC-\U0001FADE"  # Objects
            r"\U0001FAE0-\U0001FAE7"  # Objects
            r"\U0001FAF0-\U0001FAF6"  # Hands
            r"\U0001FAF8-\U0001FAFA"  # Objects
            r"\U0001FAFB-\U0001FAFF"  # Objects
            r"]+",
            flags=re.UNICODE,
        )

        first_line = emoji_pattern.sub("", first_line)

        # Убираем лишние пробелы
        first_line = re.sub(r"\s+", " ", first_line).strip()

        return first_line[:200]  # Ограничиваем длину
    return "Неизвестная вакансия"


def generate_link(chat_id: int, message_id: int) -> str:
    """Генерирует ссылку на оригинальный пост"""
    return f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"
