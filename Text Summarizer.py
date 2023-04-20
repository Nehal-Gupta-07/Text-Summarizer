import spacy #latest version
import re
from heapq import nlargest
import gensim #version 3.8.3 or older
from spacy.lang.en.stop_words import STOP_WORDS
import pdb
nlp = spacy.load("en_core_web_sm")


def is_float(string):
  try:
    return float(string) and '.' in string  # True if string is a number contains a dot
  except ValueError:  # String is not a number
    return False
  
def summarizer(): #creates 2 summaries , first using spacy and second using gensim
    text = input("Enter the text to be summarized: ")
    
    ratio= input("Enter ratio of summary(Between 0 and 1):") #Ratio of length of the summaries to the length of the actual text
    if(is_float(ratio) and (float(ratio)>0 and float(ratio)<=1)): #checks if ratio is valid , default ratio = 0.2
        ratio=float(ratio)
    else:
        print("Ratio invalid, using 0.2 as ratio")
        ratio=0.2
    doc = nlp(text)
    processed_txt=[token.text for token in doc if not token.is_stop and not token.is_punct and token.text!="\n"] 

    l=set(processed_txt) #getting the unique words of the text
    words={i:processed_txt.count(i)for i in l} #frequency of each unique word

    max_freq=max(words.values())

    for word in words.keys():
        words[word]=words[word]/max_freq #score given to each word based on usage
    
    sentence_tokens=[sent for sent in doc.sents]
    
    sentence_scores={}
    # finding score of each sentence
    for sent in sentence_tokens:
        for word in sent:
            if word.text in words.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = words[word.text]
                else:
                    sentence_scores[sent]+= words[word.text]
    
    select_length = int(len(sentence_tokens)*ratio) #length of summaries in number of sentences

    summary1 = nlargest(select_length, sentence_scores, key = sentence_scores.get) #finding most important sentences

    final_summary1 = [word.text for word in summary1]
    final_summary1 = " ".join(final_summary1)
    final_summary1 = re.sub("\n"," ",final_summary1) #final summary 1


    ltext=[text]

    summary2 = [gensim.summarization.summarize(txt,  
                    ratio=ratio) for txt in ltext]  
    
    final_summary2=" ".join(summary2)

    final_summary2=re.sub("\n"," ",final_summary2) #final summary 2

    if len(final_summary1)>0:
        print("\nSummary created using spacy:\n",final_summary1)
        print("\n")
        print("Summary created using gensim:\n",final_summary2)
    else:
        print("Text invalid or too short")

summarizer()