#!/usr/bin/env python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import random
import sys
import json


filename = sys.argv[1]
to_store = sys.argv[2]

with open(filename, encoding="utf8") as myfile:
    doc="".join(line.rstrip() for line in myfile)

k=1
topk=200
topp=0.95

lengthh = len(sent_tokenize(doc))

tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")  
model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws")


sentence = doc
if lengthh == 1:
    text =  "paraphrase: " + sentence + " </s>"
    encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    #input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to("cuda")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
    
    outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=256,
        do_sample=True,
        top_k=topk,
        top_p=topp,
        early_stopping=True,
        num_return_sequences=k
    )
    
    for index, output in enumerate(outputs):
        line = tokenizer.decode(output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        print(line)
    
      # what to send    
    output_dictionary = {"paraphrased_text": line}  
    json_results = json.dumps(output_dictionary, indent = 2)

else:
            
  input_text = doc
  lista =[]

  def my_paraphrase(sentence):
    for sent in sent_tokenize(input_text):
      sentence =  "paraphrase: " + sent + " </s>"

      encoding = tokenizer.encode_plus(sentence,pad_to_max_length=True, return_tensors="pt")
      #input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to("cuda")
      input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]

      outputs = model.generate(
          input_ids=input_ids, attention_mask=attention_masks,
          max_length=256,
          do_sample=True,
          top_k=topk,
          top_p=topp,
          early_stopping=True,
          num_return_sequences=k
      )

      for output in outputs:
        line = tokenizer.decode(output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        lista.append(line)

                    
  my_paraphrase(input_text)

  final_res=[]
  for l in range(k):
      listab=[]
      final_list=[]
      j=0
      n=k
      for i in range(len(sent_tokenize(input_text))):
        possible_choices = [item for item in lista[j:n] if item != ""]
        rundfromlista = random.choice(possible_choices)
        listab.append(rundfromlista)
        for l in lista[j:n]:
            if l == rundfromlista:
                l == ""
            break
        n+=k
        j+=k

      final_list.append(' '.join(listab))
      strtext = ' '.join(final_list)
      listab=[]
      final_res.append(strtext)  

  print(final_res)

  # what to send    
  output_dictionary = {"paraphrased_text": final_res}  
  json_results = json.dumps(output_dictionary, indent = 2)

f = open(to_store, "w", encoding='utf-8')
f.write(json_results)
f.close()



