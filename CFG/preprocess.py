import json
import pickle
import re

def preprocess(text):
    """
    Removes newlines & URLs. Replaces HTML '&amp;' with '&'

    params:
        text (str): text to clean
    returns:
        (str): text without newlines & URLs. HTML '&amp;' replaced with '&'
    """
    # Create text & remove newlines
    text = text.replace('\n', ' ')

    # Remove URLs
    regex = re.compile(r'\bhttps?:\/\/\S+\b')
    clean_text = re.sub(regex, '', text)
    # print(text)  # Debug

    http_regex = re.compile(r'&amp;')
    clean_text = re.sub(http_regex, '&', clean_text)
    # print(text)  # Debug

    return clean_text

