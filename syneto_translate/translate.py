# Imports the Google Cloud Translation library
from google.cloud import translate
from google.oauth2 import service_account
import json


def load_credentials() -> service_account.Credentials:
    with open('syneto_translate/account_cred.json') as file:
        credentials_json = json.load(file)
        return service_account.Credentials.from_service_account_info(credentials_json)


def translate_text(text, dest_lang: str, project_id="syneto-test-343021") -> str:
    """Translating Text."""
    client = translate.TranslationServiceClient(credentials=load_credentials())

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

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
