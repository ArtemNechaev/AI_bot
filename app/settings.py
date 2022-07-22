import os
import json

if not os.environ.get('BOT_TOKEN'):
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

TOKEN = os.environ['BOT_TOKEN']

# webhook settings
WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')

#models settings
model_name = os.environ['MODEL_NAME']
translation_kwargs = json.loads(os.environ.get('TRANSLATION_KWARGS', "{}"))
dialog_kwargs = json.loads(os.environ.get('DIALOG_KWARGS', "{}"))