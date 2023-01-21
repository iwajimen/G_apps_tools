import pandas as pd
import re

def find_id(doc):
    file_id = re.findall('/d/(.*)/', doc)
    try:
        return file_id[0]
    except:
        return "none"

def extract_fileid(doc_list):
    doc_list["file_id"] = doc_list["link"].apply(find_id)
    return doc_list
        
