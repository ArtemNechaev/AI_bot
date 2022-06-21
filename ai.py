from transformers import pipeline
from PIL import Image
import matplotlib.pyplot as plt
import math

from io import BytesIO

COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

def plot_results(pil_img, model_outputs):
    #plt.figure(figsize=(16,10))
    
    fig, ax = plt.subplots()
    ax.imshow(pil_img)
    uniq_labels = set(m['label'] for m in  model_outputs)
    labels2ids ={label: i for i, label in  enumerate(uniq_labels)}
    
    colors = COLORS * math.ceil(len(labels2ids)/6)
    for m in model_outputs:
        xmin, ymin, xmax, ymax = m['box'].values()
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False,color = colors[labels2ids[m["label"]]] , linewidth=3))

        text = f'{m["label"]}: {m["score"]:0.2f}'
        
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    image = BytesIO()
    fig.savefig(image, format='png', bbox_inches='tight', pad_inches=0, dpi=600)
    image.seek(0)
    return image

def detect(image: Image):
    model_pipline = pipeline('object-detection', model ='facebook/detr-resnet-50')
    model_outputs = model_pipline(image)
    

    return  plot_results(image, model_outputs)