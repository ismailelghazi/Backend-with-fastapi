import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL_TEMPLATE = "https://router.huggingface.co/hf-inference/models/{model}"

MODELS = {
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr"
}

def translate_text(text: str, direction: str):
    if direction not in MODELS:
        raise ValueError("Invalid direction")
    
    model = MODELS[direction]
    api_url = API_URL_TEMPLATE.format(model=model)
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 503:
             # Model loading
             return {"error": "Model is loading, please try again shortly", "status": 503}

        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0 and 'translation_text' in result[0]:
            return result[0]['translation_text']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"HF API Error: {e}")
        return None
