#!/usr/bin/env python
import sys
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, AutoTokenizer, AutoModelForTokenClassification, pipeline
import json

stopwords_ = set(stopwords.words('english'))

filename = sys.argv[1]
with open(filename, encoding="utf8") as myfile:
    text="".join(line.rstrip() for line in myfile)


def extract_keywords(text):
    key_tokenizer = AutoTokenizer.from_pretrained("yanekyuk/bert-uncased-keyword-extractor")
    key_model = AutoModelForTokenClassification.from_pretrained("yanekyuk/bert-uncased-keyword-extractor")
    nlp = pipeline("ner", model=key_model, tokenizer=key_tokenizer)
    result = list()
    keyword = ""
    for token in nlp(text):
        if token['entity'] == 'I-KEY':
            keyword += token['word'][2:] if \
            token['word'].startswith("##") else f" {token['word']}"
        else:
            if keyword:
                result.append(keyword)
            keyword = token['word']
    result.append(keyword)
    return list(set(result))


def extract_summary():
    model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    inputs = tokenizer([text],return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length = (int(len(text)*0.7)), num_beams = 4)
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return summary


def keypoints(text):
    sentences = sent_tokenize(text)
    word_frequencies = {}
    for word in word_tokenize(text):
        if word not in stopwords_:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    return summary_sentences

#print(extract_keywords(text))
#print("\n")
#print(extract_summary())
#print("\n")
#print(keypoints(text))

# what to send    
output_dictionary = {"extract_keywords": extract_keywords(text),
                        "extract_summary": extract_summary(),
                        "extract_keypoints": keypoints(text)
                    }
   

json_results = json.dumps(output_dictionary, indent = 2)
print(json_results)

to_store = sys.argv[2]

f = open(to_store, "w", encoding='utf-8')
f.write(json_results)
f.close()
