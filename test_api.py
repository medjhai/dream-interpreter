from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

print(f"API Key trovata: {'Sì' if api_key else 'No'}")
print(f"Lunghezza API Key: {len(api_key) if api_key else 0} caratteri")
print(f"Formato corretto: {'Sì' if api_key and api_key.startswith('sk-') else 'No'}")

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Usiamo un modello più economico per il test
        messages=[{"role": "user", "content": "Test"}],
        max_tokens=10
    )
    print("✅ API Key valida e funzionante!")
except Exception as e:
    print(f"❌ Errore: {str(e)}")