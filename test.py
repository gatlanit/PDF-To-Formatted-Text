from spellchecker import SpellChecker

spell = SpellChecker()

def correct_text(text):
    words = text.split()
    corrected_words = [spell.correction(word) if word not in spell else word for word in words]
    return ' '.join(corrected_words)

text = "i1t\"s really upto you at this point im time."
fixed_text = correct_text(text)
print(fixed_text)

####

import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def correct_with_language_tool(text):
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

text = "i1t\"s really upto you at this point im time."
corrected_text = correct_with_language_tool(text)
print(corrected_text)