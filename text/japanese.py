# import re
# from unidecode import unidecode
# import pyopenjtalk


# # Regular expression matching Japanese without punctuation marks:
# _japanese_characters = re.compile(
#     r'[A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# # Regular expression matching non-Japanese characters or punctuation marks:
# _japanese_marks = re.compile(
#     r'[^A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# # List of (symbol, Japanese) pairs for marks:
# _symbols_to_japanese = [(re.compile('%s' % x[0]), x[1]) for x in [
#     ('％', 'パーセント')
# ]]

# # List of (romaji, ipa) pairs for marks:
# _romaji_to_ipa = [(re.compile('%s' % x[0]), x[1]) for x in [
#     ('ts', 'ʦ'),
#     ('u', 'ɯ'),
#     ('j', 'ʥ'),
#     ('y', 'j'),
#     ('ni', 'n^i'),
#     ('nj', 'n^'),
#     ('hi', 'çi'),
#     ('hj', 'ç'),
#     ('f', 'ɸ'),
#     ('I', 'i*'),
#     ('U', 'ɯ*'),
#     ('r', 'ɾ')
# ]]

# # List of (romaji, ipa2) pairs for marks:
# _romaji_to_ipa2 = [(re.compile('%s' % x[0]), x[1]) for x in [
#     ('u', 'ɯ'),
#     ('ʧ', 'tʃ'),
#     ('j', 'dʑ'),
#     ('y', 'j'),
#     ('ni', 'n^i'),
#     ('nj', 'n^'),
#     ('hi', 'çi'),
#     ('hj', 'ç'),
#     ('f', 'ɸ'),
#     ('I', 'i*'),
#     ('U', 'ɯ*'),
#     ('r', 'ɾ')
# ]]

# # List of (consonant, sokuon) pairs:
# _real_sokuon = [(re.compile('%s' % x[0]), x[1]) for x in [
#     (r'Q([↑↓]*[kg])', r'k#\1'),
#     (r'Q([↑↓]*[tdjʧ])', r't#\1'),
#     (r'Q([↑↓]*[sʃ])', r's\1'),
#     (r'Q([↑↓]*[pb])', r'p#\1')
# ]]

# # List of (consonant, hatsuon) pairs:
# _real_hatsuon = [(re.compile('%s' % x[0]), x[1]) for x in [
#     (r'N([↑↓]*[pbm])', r'm\1'),
#     (r'N([↑↓]*[ʧʥj])', r'n^\1'),
#     (r'N([↑↓]*[tdn])', r'n\1'),
#     (r'N([↑↓]*[kg])', r'ŋ\1')
# ]]


# def symbols_to_japanese(text):
#     for regex, replacement in _symbols_to_japanese:
#         text = re.sub(regex, replacement, text)
#     return text


# def japanese_to_romaji_with_accent(text):
#     '''Reference https://r9y9.github.io/ttslearn/latest/notebooks/ch10_Recipe-Tacotron.html'''
#     text = symbols_to_japanese(text)
#     sentences = re.split(_japanese_marks, text)
#     marks = re.findall(_japanese_marks, text)
#     text = ''
#     for i, sentence in enumerate(sentences):
#         if re.match(_japanese_characters, sentence):
#             if text != '':
#                 text += ' '
#             labels = pyopenjtalk.extract_fullcontext(sentence)
#             for n, label in enumerate(labels):
#                 phoneme = re.search(r'\-([^\+]*)\+', label).group(1)
#                 if phoneme not in ['sil', 'pau']:
#                     text += phoneme.replace('ch', 'ʧ').replace('sh',
#                                                                'ʃ').replace('cl', 'Q')
#                 else:
#                     continue
#                 # n_moras = int(re.search(r'/F:(\d+)_', label).group(1))
#                 a1 = int(re.search(r"/A:(\-?[0-9]+)\+", label).group(1))
#                 a2 = int(re.search(r"\+(\d+)\+", label).group(1))
#                 a3 = int(re.search(r"\+(\d+)/", label).group(1))
#                 if re.search(r'\-([^\+]*)\+', labels[n + 1]).group(1) in ['sil', 'pau']:
#                     a2_next = -1
#                 else:
#                     a2_next = int(
#                         re.search(r"\+(\d+)\+", labels[n + 1]).group(1))
#                 # Accent phrase boundary
#                 if a3 == 1 and a2_next == 1:
#                     text += ' '
#                 # Falling
#                 elif a1 == 0 and a2_next == a2 + 1:
#                     text += '↓'
#                 # Rising
#                 elif a2 == 1 and a2_next == 2:
#                     text += '↑'
#         if i < len(marks):
#             text += unidecode(marks[i]).replace(' ', '')
#     return text


# def get_real_sokuon(text):
#     for regex, replacement in _real_sokuon:
#         text = re.sub(regex, replacement, text)
#     return text


# def get_real_hatsuon(text):
#     for regex, replacement in _real_hatsuon:
#         text = re.sub(regex, replacement, text)
#     return text


# def japanese_to_ipa(text):
#     text = japanese_to_romaji_with_accent(text).replace('...', '…')
#     text = re.sub(
#         r'([aiueo])\1+', lambda x: x.group(0)[0]+'ː'*(len(x.group(0))-1), text)
#     text = get_real_sokuon(text)
#     text = get_real_hatsuon(text)
#     for regex, replacement in _romaji_to_ipa:
#         text = re.sub(regex, replacement, text)
#     return text


# def japanese_to_ipa2(text):
#     text = japanese_to_romaji_with_accent(text).replace('...', '…')
#     text = get_real_sokuon(text)
#     text = get_real_hatsuon(text)
#     for regex, replacement in _romaji_to_ipa2:
#         text = re.sub(regex, replacement, text)
#     return text


# def japanese_to_ipa3(text):
#     text = japanese_to_ipa2(text).replace('n^', 'ȵ').replace(
#         'ʃ', 'ɕ').replace('*', '\u0325').replace('#', '\u031a')
#     text = re.sub(
#         r'([aiɯeo])\1+', lambda x: x.group(0)[0]+'ː'*(len(x.group(0))-1), text)
#     text = re.sub(r'((?:^|\s)(?:ts|tɕ|[kpt]))', r'\1ʰ', text)
#     return text


























# Convert Japanese text to phonemes which is
# compatible with Julius https://github.com/julius-speech/segmentation-kit

import re
import unicodedata

try:
    import MeCab
except ImportError as e:
    raise ImportError("Japanese requires mecab-python3 and unidic-lite.") from e
from num2words import num2words
import re
from unidecode import unidecode
# import pyopenjtalk


# Regular expression matching Japanese without punctuation marks:
_japanese_characters = re.compile(
    r'[A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# Regular expression matching non-Japanese characters or punctuation marks:
_japanese_marks = re.compile(
    r'[^A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# List of (symbol, Japanese) pairs for marks:
_symbols_to_japanese = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('％', 'パーセント')
]]

def symbols_to_japanese(text):
    for regex, replacement in _symbols_to_japanese:
        text = re.sub(regex, replacement, text)
    return text


# def japanese_to_romaji_with_accent(text):
#     '''Reference https://r9y9.github.io/ttslearn/latest/notebooks/ch10_Recipe-Tacotron.html'''
#     text = symbols_to_japanese(text)
#     sentences = re.split(_japanese_marks, text)
#     marks = re.findall(_japanese_marks, text)
#     text = ''
#     for i, sentence in enumerate(sentences):
#         if re.match(_japanese_characters, sentence):
#             if text != '':
#                 text += ' '
#             labels = pyopenjtalk.extract_fullcontext(sentence)
#             for n, label in enumerate(labels):
#                 phoneme = re.search(r'\-([^\+]*)\+', label).group(1)
#                 if phoneme not in ['sil', 'pau']:
#                     text += phoneme.replace('ch', 'ʧ').replace('sh',
#                                                                'ʃ').replace('cl', 'Q')
#                 else:
#                     continue
#                 # n_moras = int(re.search(r'/F:(\d+)_', label).group(1))
#                 a1 = int(re.search(r"/A:(\-?[0-9]+)\+", label).group(1))
#                 a2 = int(re.search(r"\+(\d+)\+", label).group(1))
#                 a3 = int(re.search(r"\+(\d+)/", label).group(1))
#                 if re.search(r'\-([^\+]*)\+', labels[n + 1]).group(1) in ['sil', 'pau']:
#                     a2_next = -1
#                 else:
#                     a2_next = int(
#                         re.search(r"\+(\d+)\+", labels[n + 1]).group(1))
#                 # Accent phrase boundary
#                 if a3 == 1 and a2_next == 1:
#                     text += ' '
#                 # Falling
#                 elif a1 == 0 and a2_next == a2 + 1:
#                     text += '↓'
#                 # Rising
#                 elif a2 == 1 and a2_next == 2:
#                     text += '↑'
#         if i < len(marks):
#             text += unidecode(marks[i]).replace(' ', '')
#     return text


_CONVRULES = [
    # Conversion of 2 letters
    "アァ/ a a",
    "イィ/ i i",
    "イェ/ i e",
    "イャ/ y a",
    "ウゥ/ u:",
    "エェ/ e e",
    "オォ/ o:",
    "カァ/ k a:",
    "キィ/ k i:",
    "クゥ/ k u:",
    "クャ/ ky a",
    "クュ/ ky u",
    "クョ/ ky o",
    "ケェ/ k e:",
    "コォ/ k o:",
    "ガァ/ g a:",
    "ギィ/ g i:",
    "グゥ/ g u:",
    "グャ/ gy a",
    "グュ/ gy u",
    "グョ/ gy o",
    "ゲェ/ g e:",
    "ゴォ/ g o:",
    "サァ/ s a:",
    "シィ/ sh i:",
    "スゥ/ s u:",
    "スャ/ sh a",
    "スュ/ sh u",
    "スョ/ sh o",
    "セェ/ s e:",
    "ソォ/ s o:",
    "ザァ/ z a:",
    "ジィ/ j i:",
    "ズゥ/ z u:",
    "ズャ/ zy a",
    "ズュ/ zy u",
    "ズョ/ zy o",
    "ゼェ/ z e:",
    "ゾォ/ z o:",
    "タァ/ t a:",
    "チィ/ ch i:",
    "ツァ/ ts a",
    "ツィ/ ts i",
    "ツゥ/ ts u:",
    "ツャ/ ch a",
    "ツュ/ ch u",
    "ツョ/ ch o",
    "ツェ/ ts e",
    "ツォ/ ts o",
    "テェ/ t e:",
    "トォ/ t o:",
    "ダァ/ d a:",
    "ヂィ/ j i:",
    "ヅゥ/ d u:",
    "ヅャ/ zy a",
    "ヅュ/ zy u",
    "ヅョ/ zy o",
    "デェ/ d e:",
    "ドォ/ d o:",
    "ナァ/ n a:",
    "ニィ/ n i:",
    "ヌゥ/ n u:",
    "ヌャ/ ny a",
    "ヌュ/ ny u",
    "ヌョ/ ny o",
    "ネェ/ n e:",
    "ノォ/ n o:",
    "ハァ/ h a:",
    "ヒィ/ h i:",
    "フゥ/ f u:",
    "フャ/ hy a",
    "フュ/ hy u",
    "フョ/ hy o",
    "ヘェ/ h e:",
    "ホォ/ h o:",
    "バァ/ b a:",
    "ビィ/ b i:",
    "ブゥ/ b u:",
    "フャ/ hy a",
    "ブュ/ by u",
    "フョ/ hy o",
    "ベェ/ b e:",
    "ボォ/ b o:",
    "パァ/ p a:",
    "ピィ/ p i:",
    "プゥ/ p u:",
    "プャ/ py a",
    "プュ/ py u",
    "プョ/ py o",
    "ペェ/ p e:",
    "ポォ/ p o:",
    "マァ/ m a:",
    "ミィ/ m i:",
    "ムゥ/ m u:",
    "ムャ/ my a",
    "ムュ/ my u",
    "ムョ/ my o",
    "メェ/ m e:",
    "モォ/ m o:",
    "ヤァ/ y a:",
    "ユゥ/ y u:",
    "ユャ/ y a:",
    "ユュ/ y u:",
    "ユョ/ y o:",
    "ヨォ/ y o:",
    "ラァ/ r a:",
    "リィ/ r i:",
    "ルゥ/ r u:",
    "ルャ/ ry a",
    "ルュ/ ry u",
    "ルョ/ ry o",
    "レェ/ r e:",
    "ロォ/ r o:",
    "ワァ/ w a:",
    "ヲォ/ o:",
    "ディ/ d i",
    "デェ/ d e:",
    "デャ/ dy a",
    "デュ/ dy u",
    "デョ/ dy o",
    "ティ/ t i",
    "テェ/ t e:",
    "テャ/ ty a",
    "テュ/ ty u",
    "テョ/ ty o",
    "スィ/ s i",
    "ズァ/ z u a",
    "ズィ/ z i",
    "ズゥ/ z u",
    "ズャ/ zy a",
    "ズュ/ zy u",
    "ズョ/ zy o",
    "ズェ/ z e",
    "ズォ/ z o",
    "キャ/ ky a",
    "キュ/ ky u",
    "キョ/ ky o",
    "シャ/ sh a",
    "シュ/ sh u",
    "シェ/ sh e",
    "ショ/ sh o",
    "チャ/ ch a",
    "チュ/ ch u",
    "チェ/ ch e",
    "チョ/ ch o",
    "トゥ/ t u",
    "トャ/ ty a",
    "トュ/ ty u",
    "トョ/ ty o",
    "ドァ/ d o a",
    "ドゥ/ d u",
    "ドャ/ dy a",
    "ドュ/ dy u",
    "ドョ/ dy o",
    "ドォ/ d o:",
    "ニャ/ ny a",
    "ニュ/ ny u",
    "ニョ/ ny o",
    "ヒャ/ hy a",
    "ヒュ/ hy u",
    "ヒョ/ hy o",
    "ミャ/ my a",
    "ミュ/ my u",
    "ミョ/ my o",
    "リャ/ ry a",
    "リュ/ ry u",
    "リョ/ ry o",
    "ギャ/ gy a",
    "ギュ/ gy u",
    "ギョ/ gy o",
    "ヂェ/ j e",
    "ヂャ/ j a",
    "ヂュ/ j u",
    "ヂョ/ j o",
    "ジェ/ j e",
    "ジャ/ j a",
    "ジュ/ j u",
    "ジョ/ j o",
    "ビャ/ by a",
    "ビュ/ by u",
    "ビョ/ by o",
    "ピャ/ py a",
    "ピュ/ py u",
    "ピョ/ py o",
    "ウァ/ u a",
    "ウィ/ w i",
    "ウェ/ w e",
    "ウォ/ w o",
    "ファ/ f a",
    "フィ/ f i",
    "フゥ/ f u",
    "フャ/ hy a",
    "フュ/ hy u",
    "フョ/ hy o",
    "フェ/ f e",
    "フォ/ f o",
    "ヴァ/ b a",
    "ヴィ/ b i",
    "ヴェ/ b e",
    "ヴォ/ b o",
    "ヴュ/ by u",
    # Conversion of 1 letter
    "ア/ a",
    "イ/ i",
    "ウ/ u",
    "エ/ e",
    "オ/ o",
    "カ/ k a",
    "キ/ k i",
    "ク/ k u",
    "ケ/ k e",
    "コ/ k o",
    "サ/ s a",
    "シ/ sh i",
    "ス/ s u",
    "セ/ s e",
    "ソ/ s o",
    "タ/ t a",
    "チ/ ch i",
    "ツ/ ts u",
    "テ/ t e",
    "ト/ t o",
    "ナ/ n a",
    "ニ/ n i",
    "ヌ/ n u",
    "ネ/ n e",
    "ノ/ n o",
    "ハ/ h a",
    "ヒ/ h i",
    "フ/ f u",
    "ヘ/ h e",
    "ホ/ h o",
    "マ/ m a",
    "ミ/ m i",
    "ム/ m u",
    "メ/ m e",
    "モ/ m o",
    "ラ/ r a",
    "リ/ r i",
    "ル/ r u",
    "レ/ r e",
    "ロ/ r o",
    "ガ/ g a",
    "ギ/ g i",
    "グ/ g u",
    "ゲ/ g e",
    "ゴ/ g o",
    "ザ/ z a",
    "ジ/ j i",
    "ズ/ z u",
    "ゼ/ z e",
    "ゾ/ z o",
    "ダ/ d a",
    "ヂ/ j i",
    "ヅ/ z u",
    "デ/ d e",
    "ド/ d o",
    "バ/ b a",
    "ビ/ b i",
    "ブ/ b u",
    "ベ/ b e",
    "ボ/ b o",
    "パ/ p a",
    "ピ/ p i",
    "プ/ p u",
    "ペ/ p e",
    "ポ/ p o",
    "ヤ/ y a",
    "ユ/ y u",
    "ヨ/ y o",
    "ワ/ w a",
    "ヰ/ i",
    "ヱ/ e",
    "ヲ/ o",
    "ン/ N",
    "ッ/ q",
    "ヴ/ b u",
    "ー/:",
    # Try converting broken text
    "ァ/ a",
    "ィ/ i",
    "ゥ/ u",
    "ェ/ e",
    "ォ/ o",
    "ヮ/ w a",
    "ォ/ o",
    # Symbols
    "、/ ,",
    "。/ .",
    "！/ !",
    "？/ ?",
    "・/ ,",
]

_COLON_RX = re.compile(":+")
_REJECT_RX = re.compile("[^ a-zA-Z:,.?]")


def _makerulemap():
    l = [tuple(x.split("/")) for x in _CONVRULES]
    return tuple({k: v for k, v in l if len(k) == i} for i in (1, 2))


_RULEMAP1, _RULEMAP2 = _makerulemap()


def kata2phoneme(text: str) -> str:
    """Convert katakana text to phonemes."""
    text = text.strip()
    res = ""
    while text:
        if len(text) >= 2:
            x = _RULEMAP2.get(text[:2])
            if x is not None:
                text = text[2:]
                res += x
                continue
        x = _RULEMAP1.get(text[0])
        if x is not None:
            text = text[1:]
            res += x
            continue
        res += " " + text[0]
        text = text[1:]
    res = _COLON_RX.sub(":", res)
    return res[1:]


_KATAKANA = "".join(chr(ch) for ch in range(ord("ァ"), ord("ン") + 1))
_HIRAGANA = "".join(chr(ch) for ch in range(ord("ぁ"), ord("ん") + 1))
_HIRA2KATATRANS = str.maketrans(_HIRAGANA, _KATAKANA)


def hira2kata(text: str) -> str:
    text = text.translate(_HIRA2KATATRANS)
    return text.replace("う゛", "ヴ")


_SYMBOL_TOKENS = set(list("・、。？！"))
_NO_YOMI_TOKENS = set(list("「」『』―（）［］[]　…"))
_TAGGER = MeCab.Tagger()


def text2kata(text: str) -> str:
    parsed = _TAGGER.parse(text)
    res = []
    for line in parsed.split("\n"):
        if line == "EOS":
            break
        parts = line.split("\t")

        word, yomi = parts[0], parts[1]
        if yomi:
            res.append(yomi)
        else:
            if word in _SYMBOL_TOKENS:
                res.append(word)
            elif word in ("っ", "ッ"):
                res.append("ッ")
            elif word in _NO_YOMI_TOKENS:
                pass
            else:
                res.append(word)
    return hira2kata("".join(res))


_ALPHASYMBOL_YOMI = {
    "#": "シャープ",
    "%": "パーセント",
    "&": "アンド",
    "+": "プラス",
    "-": "マイナス",
    ":": "コロン",
    ";": "セミコロン",
    "<": "小なり",
    "=": "イコール",
    ">": "大なり",
    "@": "アット",
    "a": "エー",
    "b": "ビー",
    "c": "シー",
    "d": "ディー",
    "e": "イー",
    "f": "エフ",
    "g": "ジー",
    "h": "エイチ",
    "i": "アイ",
    "j": "ジェー",
    "k": "ケー",
    "l": "エル",
    "m": "エム",
    "n": "エヌ",
    "o": "オー",
    "p": "ピー",
    "q": "キュー",
    "r": "アール",
    "s": "エス",
    "t": "ティー",
    "u": "ユー",
    "v": "ブイ",
    "w": "ダブリュー",
    "x": "エックス",
    "y": "ワイ",
    "z": "ゼット",
    "α": "アルファ",
    "β": "ベータ",
    "γ": "ガンマ",
    "δ": "デルタ",
    "ε": "イプシロン",
    "ζ": "ゼータ",
    "η": "イータ",
    "θ": "シータ",
    "ι": "イオタ",
    "κ": "カッパ",
    "λ": "ラムダ",
    "μ": "ミュー",
    "ν": "ニュー",
    "ξ": "クサイ",
    "ο": "オミクロン",
    "π": "パイ",
    "ρ": "ロー",
    "σ": "シグマ",
    "τ": "タウ",
    "υ": "ウプシロン",
    "φ": "ファイ",
    "χ": "カイ",
    "ψ": "プサイ",
    "ω": "オメガ",
    "♪":"~",
    "̩":',',
    "“":"\"",
    "”": "\"",
    "★":"",
    "☆":"",
    "】":"",
    "【":""
}


_NUMBER_WITH_SEPARATOR_RX = re.compile("[0-9]{1,3}(,[0-9]{3})+")
_CURRENCY_MAP = {"$": "ドル", "¥": "円", "£": "ポンド", "€": "ユーロ"}
_CURRENCY_RX = re.compile(r"([$¥£€])([0-9.]*[0-9])")
_NUMBER_RX = re.compile(r"[0-9]+(\.[0-9]+)?")


def japanese_convert_numbers_to_words(text: str) -> str:
    res = _NUMBER_WITH_SEPARATOR_RX.sub(lambda m: m[0].replace(",", ""), text)
    res = _CURRENCY_RX.sub(lambda m: m[2] + _CURRENCY_MAP.get(m[1], m[1]), res)
    res = _NUMBER_RX.sub(lambda m: num2words(m[0], lang="ja"), res)
    return res


def japanese_convert_alpha_symbols_to_words(text: str) -> str:
    return "".join([_ALPHASYMBOL_YOMI.get(ch, ch) for ch in text.lower()])

def japanese_text_to_phonemes(text: str) -> str:
    """Convert Japanese text to phonemes."""

    # text = japanese_convert_numbers_to_words(text)
    # text = japanese_to_romaji_with_accent(text)
    # text = re.sub(r'([A-Za-z])$', r'\1.', text)
    # return text
    res = unicodedata.normalize("NFKC", text)
    res = japanese_convert_numbers_to_words(res)
    res = japanese_convert_alpha_symbols_to_words(res)
    res = text2kata(res)
    res = kata2phoneme(res)

    return res.replace(" ", "")
