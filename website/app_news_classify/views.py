from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence
import pickle
import jieba
import numpy as np

jieba.set_dictionary('jieba_big_chinese_dict/dict.txt.big')

# We don't use GPU
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

model = load_model('app_news_classify/trained_model/classify_best_model.hdf5')

# Load tokenizer news_classify_tokenizer.pickle
#app_news_classify\news_classify_model\news_classify_tokenizer.pickle
#tokenizer = pickle.load(open('app_news_classify/news_classify_model/news_classify_tokenizer.pickle', 'rb'))
tokenizer = pickle.load(open('app_news_classify/trained_model/classify_tokenizer.pickle', 'rb'))

# category index
news_categories=['電腦應用綜合討論','電視遊樂器綜合討論','智慧型手機']
idx2cate = { i : item for i, item in enumerate(news_categories)}

# home
def home(request):
    return render(request, "app_news_classify/home.html")

from django.http import JsonResponse
import json



# api: get news class given user input text
@csrf_exempt
def api_get_news_cate(request):
    
    new_text = request.POST.get('input_text')
    #print(new_text)

    news_cate = get_cate_proba(new_text)

    response = {
        'classifies': news_cate,
    }

    return JsonResponse(response)


# get category probability
def get_cate_proba(new_text):
    tokens = jieba.lcut(new_text, cut_all=False)
    tokens = [tokens]
    
    new_text_seq = tokenizer.texts_to_sequences(tokens)
    new_text_pad = sequence.pad_sequences(new_text_seq, maxlen=350)

    result = model.predict(new_text_pad)
    print(result)

    label = ['電腦應用綜合討論','電視遊樂器綜合討論','智慧型手機']
    proba = [round(float(result[0, 0]), 3), round(float(result[0, 1]), 3), round(float(result[0, 2]), 3)]
    # Note that result is numpy format and it should be convert to float
    print(label)
    print(proba)
    return {'label': label, 'proba': proba}

print("classification was loaded!")
