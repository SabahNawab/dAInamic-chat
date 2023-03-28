from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import openai
import numpy as np
import pandas as pd
import random
import os
import gradio as gr
tokenizer = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-base-seq2seq")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-base-seq2seq")
#custom training left
# textual testing phase 1
#full code underprogress
def chat_with_dainamic(input, old_convo=[]):
    Guide = 'Instruction: Given a prompt you need to respond creatively and be innovative each time'
    ans = '  '
    word_limit_lower = 10
    word_limit_higher = 500
    lst = []
    for convo in old_convo:
        lst += convo
    lst.append(input)
    sentence = ''
    for i in lst:
        sentence += i + ' EOS '
    sentence = sentence.rstrip(' EOS ')
    question = "{} [CONTEXT] {} {}".format(Guide, sentence, ans)
    p = 0.9
    encoded_question = tokenizer.encode(question)
    recent_input = torch.tensor(encoded_question).unsqueeze(0)
    gen = model.generate(recent_input,min_length=int(word_limit_lower),max_length=int(word_limit_higher),top_p=p,do_sample=True)
    reply = tokenizer.decode(gen[0], skip_special_tokens=True)
    old_convo.extend([(input, reply)])
    return (old_convo, old_convo)
gr.Interface(chat_with_dainamic,["text",'state'],["chatbot",'state']).launch(debug = True, share = True)