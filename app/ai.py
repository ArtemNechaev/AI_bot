from transformers import pipeline
from PIL import Image
import matplotlib.pyplot as plt
import math
import re
from io import BytesIO
import os
import json

from settings import model_name, translation_kwargs, dialog_kwargs

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

        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    image = BytesIO()
    fig.savefig(image, format='jpg', bbox_inches='tight',
                pad_inches=0, dpi=600)
    image.seek(0)
    return image


def detect(image: Image):
    model_pipline = pipeline(
        'object-detection', model='facebook/detr-resnet-50')
    model_outputs = model_pipline(image)

    return plot_results(image, model_outputs)


#################################


def sec2sec(text, mode):
    ln = 'ru' if len(re.findall(r'[А-Яа-яёЁ]', text)
                     ) > 0.1 * len(text) else 'en'
    ln2 = 'en' if ln == 'ru' else 'ru'

    pipe = pipeline(task='text2text-generation', model=model_name)

    if mode == 'translate':
        text = f"translate {ln} to {ln2}: " + text
        return pipe(text, **translation_kwargs)[0]['generated_text']

    elif mode == 'dialog':
        text = pipe("dialog: " + text, **dialog_kwargs)[0]['generated_text']
        if ln == 'ru':
            return (
                pipe(f"translate {ln2} to {ln}:" + text, **translation_kwargs)[0]['generated_text'],
                text
            )
        elif ln == 'en':
            return text, text
