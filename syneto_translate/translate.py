# Imports the Google Cloud Translation library
from google.cloud import translate
from google.oauth2 import service_account
import json

from syneto_translate import PROJECT_ID, SERVICE_ACCOUNT_FILE


def load_credentials() -> service_account.Credentials:
    print(PROJECT_ID, SERVICE_ACCOUNT_FILE)
    with open(SERVICE_ACCOUNT_FILE) as file:
        credentials_json = json.load(file)
        return service_account.Credentials.from_service_account_info(credentials_json)


def translate_text(text: str, dest_lang: str) -> str:
    """Translating Text."""
    client = translate.TranslationServiceClient(credentials=load_credentials())

    location = "global"

    parent = f"projects/{PROJECT_ID}/locations/{location}"

    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "target_language_code": dest_lang,
        }
    )

    # Display the translation for each input text provided
    return ' '.join([translation.translated_text for translation in response.translations])
