""" from https://github.com/keithito/tacotron """

"""
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
"""

import re
from unidecode import unidecode
from text.thai import thai_text_to_phonemes
from text.japanese import japanese_to_ipa2
from text.english import normalize_numbers

# Regular expression matching whitespace:
_whitespace_re = re.compile(r"\s+")

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [
    (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
    for x in [
        ("mrs", "misess"),
        ("mr", "mister"),
        ("dr", "doctor"),
        ("st", "saint"),
        ("co", "company"),
        ("jr", "junior"),
        ("maj", "major"),
        ("gen", "general"),
        ("drs", "doctors"),
        ("rev", "reverend"),
        ("lt", "lieutenant"),
        ("hon", "honorable"),
        ("sgt", "sergeant"),
        ("capt", "captain"),
        ("esq", "esquire"),
        ("ltd", "limited"),
        ("col", "colonel"),
        ("ft", "fort"),
        ("&", " and ")
    ]
]


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def expand_numbers(text):
    return normalize_numbers(text)


def lowercase(text):
    return text.lower()


def collapse_whitespace(text):
    return re.sub(_whitespace_re, " ", text)


def convert_to_ascii(text):
    return unidecode(text)


def basic_cleaners(text):
    """Basic pipeline that lowercases and collapses whitespace without transliteration."""
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def transliteration_cleaners(text):
    """Pipeline for non-English text that transliterates to ASCII."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def english_cleaners(text):
    """Pipeline for English text, including abbreviation expansion."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_abbreviations(text)
    # phonemes = phonemize(text, language="en-us", backend="espeak", strip=True)
    # phonemes = collapse_whitespace(phonemes)
    return text


def english_cleaners2(text):
    """Pipeline for English text, including abbreviation expansion. + punctuation + stress"""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_abbreviations(text)
    text = expand_numbers(text)
    return text
    # phonemes = phonemize(
    #     text,
    #     language="en-us",
    #     backend="espeak",
    #     strip=True,
    #     preserve_punctuation=True,
    #     with_stress=True,
    # )
    # phonemes = collapse_whitespace(phonemes)
    # return phonemes


# def english_cleaners3(text):
#     """Pipeline for English text, including abbreviation expansion. + punctuation + stress"""
#     text = convert_to_ascii(text)
#     text = lowercase(text)
#     text = expand_abbreviations(text)
#     phonemes = backend.phonemize([text], strip=True)[0]
#     phonemes = collapse_whitespace(phonemes)
#     return phonemes

def tag_jke(text,prev_sentence=None):
    zh_pattern = re.compile(r'[\u4e00-\u9fa5]')
    en_pattern = re.compile(r'[a-zA-Z]')
    jp_pattern = re.compile(r'[\u3040-\u30ff\u31f0-\u31ff]')
    th_pattern = re.compile(r'[\u0e00-\u0e7f]')
    tags={'ZH':'[ZH]','EN':'[EN]','JP':'[JA]','KR':'[KR]', 'TH': "[TH]"}

    tagged_text = ""
    prev_lang = None
    tagged=0
    lang = ""

    for char in text:

        if jp_pattern.match(char):
            lang = "JP"
        elif zh_pattern.match(char):
            lang = "JP"
        # elif en_pattern.match(char):
        #     lang = "EN"
        elif th_pattern.match(char):
            lang = "TH"
        # else:
        #     lang = "None"
        #     tagged_text += char

        if lang:
            return lang
        
    return "SHIT"

    #     if lang != prev_lang:
    #         tagged=1
    #         if prev_lang==None:
    #             tagged_text =tags[lang]+tagged_text
    #         else:
    #             tagged_text =tagged_text+tags[prev_lang]+tags[lang]

    #         prev_lang = lang

    #     tagged_text += char
    
    # if prev_lang:
    #         tagged_text += tags[prev_lang]
    # if not tagged:
    #     prev_lang=prev_sentence
    #     tagged_text =tags[prev_lang]+tagged_text+tags[prev_lang]

    return prev_lang,tagged_text

def cjke_cleaners2(text):
    
    # if tag_jke(text) == "JP":
    #     text = japanese_to_ipa2(text)
    # elif tag_jke(text) == "TH":
    #     text = thai_text_to_phonemes(text)
    # else:
    #     text = english_cleaners2(text)

    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[TH\](.*?)\[TH\]',
                  lambda x: thai_text_to_phonemes(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_cleaners2(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    text = text.replace("...", "…")

    remove_chars = "()\{\}"
    for rc in remove_chars:
        text = text.replace(rc, "")
    return text