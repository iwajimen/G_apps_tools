import re
import demoji
import neologdn
import MeCab

def url_del(texts):
    text = re.sub(r'http?://[\w/:%#\$&\?\(\)~\.=\+\-]+', "", texts)
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', "", text)
    return text

def emoji_del(texts):
    text = demoji.replace(string=texts, repl="")
    return text

def symbol_del(texts):
    text = re.sub(r'[!”#$%&\’\\\\()*+,-./:;?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。,？！｀＋￥％]', "", texts)
    text = re.sub('[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]', "", text)
    return text

def normalize(texts):
    text = neologdn.normalize(texts)
    text = re.sub(r'\b\d{1,3}(,\d{3})*\b', '0', text)
    text = re.sub(r'\d+', '0', text)
    text = text.lower()
    return text

def morphological_analysis(texts):
    tagger = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    target_parts_of_speech = [
           "名詞-サ変接続", 
           "名詞-形容動詞語幹", 
           "名詞-一般", 
           "名詞-固有名詞-一般", 
           "名詞-固有名詞-組織", 
           "形容詞-自立"
           ]

    with open('./japanese_stop_words.txt') as f:
        stop_words = f.read().splitlines()

    result_word_list = []

    try:
        for line in tagger.parse(texts).splitlines():
            if line is None or line == '' or line == 'EOS' or len(line.split()) < 4:
                continue
            for target_part_of_speech in target_parts_of_speech:
                if target_part_of_speech == line.split()[3]:
                    word = line.split()[2]
                    if not word in stop_words:
                        result_word_list.append(word)
    except:
        result_word_list.append("none")
    return result_word_list

def preprocess(texts):
    if texts != "none":
        text = url_del(texts)
        text = emoji_del(text)
        text = symbol_del(text)
        text = normalize(text)
        text = morphological_analysis(text)
        return text
    else:
        return texts

import pandas as pd

texts = pd.read_csv("./data/update_doc_datav2.csv")

texts["all_txt"] = texts.apply(lambda x: x["thema"]+x["doc_text"],axis=1)
texts["pre_text"] = texts["all_txt"].apply(preprocess)

texts.to_csv("./data/update_doc_datav3.csv", index = False)