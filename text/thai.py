import re
import unicodedata

from num2words import num2words
from pythainlp.transliterate import transliterate
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize

_ALPHASYMBOL_YOMI = {
    'a': 'เอ',
    'b':'บี',
    'c':'ซี',
    'd':'ดี',
    'e':'อี',
    'f':'เอฟ',
    'g':'จี',
    'h':'เอช',
    'i':'ไอ',
    'j':'เจ',
    'k':'เค',
    'l':'แอล',
    'm':'เอ็ม',
    'n':'เอ็น',
    'o':'โอ',
    'p':'พี',
    'q':'คิว',
    'r':'แอร์',
    's':'เอส',
    't':'ที',
    'u':'ยู',
    'v':'วี',
    'w':'ดับเบิลยู',
    'x':'เอ็กซ์',
    'y':'วาย',
    'z':'ซี',
    '%':'เปอร์เซ็น'
}

_NUMBER_WITH_SEPARATOR_RX = re.compile("[0-9]{1,3}(,[0-9]{3})+")
_CURRENCY_MAP = {"$": "ดอลล่า", "¥": "เยน", "£": "ปอนด์", "€": "ยูโร", "฿": "บาท"}
_CURRENCY_RX = re.compile(r"([$¥£€])([0-9.]*[0-9])")
_NUMBER_RX = re.compile(r"[0-9]+(\.[0-9]+)?")


def thai_convert_numbers_to_words(text: str) -> str:
    res = _NUMBER_WITH_SEPARATOR_RX.sub(lambda m: m[0].replace(",", ""), text)
    res = _CURRENCY_RX.sub(lambda m: m[2] + _CURRENCY_MAP.get(m[1], m[1]), res)
    res = _NUMBER_RX.sub(lambda m: num2words(m[0], lang="th"), res)
    return res


def thai_convert_alpha_symbols_to_words(text: str) -> str:
    return "".join([_ALPHASYMBOL_YOMI.get(ch, ch) for ch in text.lower()])

def parse_tone_to_number(phoneme):
    dictionaries = {
        "t͡ɕ": "c",
        "˧": "1",
        "˨˩": "2",
        "˥˩": "3",
        "˦˥": "4",
        "˩˩˦": "5",
        # I don't know we is this 2 shit doing?, So just make it empty
        "̯":"",
        "̚": ""
    }

    for key, value in dictionaries.items():
        phoneme = phoneme.replace(key, value)

    return phoneme.replace(" ", "")

def is_have_predictionaries_in(text):
    for key in pre_dictionaries.keys():
        if key in text:
            return True
    return False

def transliterate_with_dict(text):
    text = normalize(text)
    if text in pre_dictionaries:
        return pre_dictionaries[text]
    
    if text.strip() == "":
        return text

    text_ipa = transliterate(text, "tltk_ipa")
    if text_ipa.strip() == "":
        print("Fuck damn it!", text, "is got empty")
        print("let's try thaig2p")
        text_ipa = parse_tone_to_number(transliterate("อ่ะ", engine="thaig2p"))
        print("we got", text, ":", text_ipa)

    return text_ipa

def clean_maiyamok(text):
    words = maiyamok(text, "attacut")
    return"".join(words)

def get_some_char_in(text, char_set):
    for c in char_set:
        if c in text:
            return True, c
    return False, None

def is_have_punctuation_in(text):
    for c in "\"!@#$%^&*()-+?_=,<>/\"'.:;~‘’“”… ":
        if c in text:
            return True
    return False

def maiyamok(sent, engine):
    if isinstance(sent, str):
        sent = word_tokenize(sent, engine=engine)
    _list_word = []
    i = 0
    for j, text in enumerate(sent):
        if text.isspace() and "ๆ" in sent[j + 1]:
            continue
        if " ๆ" in text:
            text = text.replace(" ๆ", "ๆ")
        if "ๆ" == text:
            text = _list_word[i - 1]
        elif "ๆ" in text:
            text = text.replace("ๆ", "")
            _list_word.append(text)
            i += 1
        _list_word.append(text)
        i += 1
    return _list_word

def remove_all_character(word, special_characters):
    newWorld = word
    for c in special_characters:
        newWorld = newWorld.replace(c, "")
    return newWorld

def clean_with_dict(text, special_characters):
    new_text = text
    for s in special_characters:
        new_text = new_text.replace(s, "")
    return new_text

def thai_text_to_phonemes(text: str) -> str:
    """Convert thai text to phonemes."""
    res = text.strip().replace("  ", "...").replace("...","…")
    res = thai_convert_numbers_to_words(res)
    res = thai_convert_alpha_symbols_to_words(res)
    res = clean_maiyamok(res)
    return res