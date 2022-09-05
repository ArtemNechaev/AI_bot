from email.policy import default
from transformers import pipeline
from PIL import Image
import matplotlib.pyplot as plt
import math
import re
from io import BytesIO
import os


from db_context import  get_translation


from settings import cv_model_path, dialog_model_path, \
    translate_model_enru_path, translate_model_ruen_path,\
    translation_kwargs, dialog_kwargs

#  CV

COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]


def plot_results(pil_img, model_outputs):

    fig, ax = plt.subplots()
    ax.imshow(pil_img)
    uniq_labels = set(m['label'] for m in model_outputs)
    labels2ids = {label: i for i, label in enumerate(uniq_labels)}

    colors = COLORS * math.ceil(len(labels2ids)/6)
    for m in model_outputs:
        xmin, ymin, xmax, ymax = m['box'].values()
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=colors[labels2ids[m["label"]]], linewidth=3))

        text = f'{m["label"]}: {m["score"]:0.2f}'

        ax.text(xmin, ymin, text, fontsize=15, bbox=dict(facecolor='yellow', alpha=0.5))

    plt.axis('off')
    image = BytesIO()
    fig.savefig(image, format='jpg', bbox_inches='tight',pad_inches=0, dpi=600)
    image.seek(0)
    return image


def detect_pipe(image: Image):
    model_pipline = pipeline('object-detection', model=cv_model_path)
    model_outputs = model_pipline(image)

    return plot_results(image, model_outputs)


# NLP
import requests
from collections import deque
import numpy as np
from bs4 import BeautifulSoup


class Generator():

    def __init__(self, model):
        self.pipe = pipeline(task='text2text-generation', model=model)

    def __call__(self, text, **kwargs):
        return [output['generated_text'] for output in self.pipe(text, **kwargs)]

def to_float(any, default=None):
    try:
        return float(any)
    except:
        return default


def dialog_pipe(context, last_message, keyword=None):
    generate = Generator( model=dialog_model_path)

    commands = [ 
        "What can you do?", "What skills do you have?", 
        'translate text to Russian or English', "translate message",
        "What's in picture?", "Who is on photo?",
        "Advice me a movie", "What to watch",
        "translate it", "translate last message"]

    commands = [f"stsb sentence1: {c} sentence2: {last_message}" for c in commands]
    sims = np.array([to_float(c, default=0) for c in generate(commands)])
    
    if sims.max() > 2.3:    
        return int(sims.argmax())//2

    if not keyword:
        keyword = generate('keyword: ' + ' '.join(context), num_beams=2,)[0]

    knowlege = ''
    if keyword != 'no_keywords':
        resp = requests.get(f"https://en.wikipedia.org/wiki/{keyword}")
        root = BeautifulSoup(resp.content, "html.parser")
        knowlege = "knowlege: " +  " ".join([_.text.strip() for _ in root.find("div", class_="mw-body-content mw-content-ltr").find_all("p", limit=2)])

    answ = generate(f'dialog: ' + knowlege + ' '.join(context), **dialog_kwargs)[0]
    return answ, keyword

def translate_pipe(text):
    
    ln = 'ru' if len(re.findall(r'[А-Яа-яёЁ]', text)) > 0.1 * len(text) else 'en'
    translations = get_translation(text, ln)
    
    if translations:
        return ", ".join(translations)

    generate = Generator(model=translate_model_enru_path if ln=='en' else translate_model_ruen_path)

    return generate(text, **translation_kwargs)[0]


