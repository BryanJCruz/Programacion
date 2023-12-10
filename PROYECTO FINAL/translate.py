import boto3

def traductor(texto,code):

    target_language_code = code
    source_language_code = 'auto'  # Auto-detect source language
    translate = boto3.client('translate', region_name='us-east-1')
    response = translate.translate_text(
    Text=texto,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code)
    print('Traducción:', response['TranslatedText'])

traductor('car','es')