#! /usr/bin/python

#
# Description: https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
# ================================================================
# Time-stamp: "2023-01-25 02:19:15 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from newspaper import Article
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import os

url="https://www.symmetrymagazine.org/article/a-universe-is-born"

def grabText(url):

    print(" "*4,url)
    try:
        article = Article(url)
        article.download()
        article.parse()
        return summarize(article.text, 0.10)
    #except article.ArticleException as arex:
    except:
        print("ERROR: Likely 505...")
        return ""
    

def summarize(text, per):
    #nlp = spacy.load('en_core_web_sm')
    #nlp = spacy.load('en_core_web_md')
    nlp = spacy.load('en_core_web_lg')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary
