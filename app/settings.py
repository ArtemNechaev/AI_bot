import os
import json

if not os.environ.get('BOT_TOKEN'):
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

TOKEN = os.environ['BOT_TOKEN']
IS_PROD = os.environ.get('IS_PROD', None)

# webhook settings
WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')

#database
DB_CONNECTION = os.environ.get('DB_CONNECTION')

#models settings
dialog_model_path = os.environ.get('DIALOG_MODEL', 'artemnech/dialoT5-base')
translate_model_enru_path = os.environ.get('TRANSLATE_MODEL_ENRU', 'artemnech/enrut5-base')
translate_model_ruen_path = os.environ.get('TRANSLATE_MODEL_RUEN', 'artemnech/enrut5-base')
cv_model_path = os.environ.get('CV_MODEL', 'facebook/detr-resnet-50')
translation_kwargs = json.loads(os.environ.get('TRANSLATION_KWARGS', "{}"))
dialog_kwargs = json.loads(os.environ.get('DIALOG_KWARGS', "{}"))