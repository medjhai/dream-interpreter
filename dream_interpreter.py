from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from functools import lru_cache
import hashlib
import json
from datetime import datetime

# Configurazione logging avanzato
logging.basicConfig(
    filename='dream_interpreter.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verifica della chiave API
api_key = os.getenv('OPENAI_API_KEY')
is_test_mode = api_key and api_key.startswith('sk-test-')

class DreamInterpreter:
    def __init__(self, model="gpt-3.5-turbo"):
        if not is_test_mode:
            if not api_key:
                logger.warning("API key non trovata nel file .env")
            self.client = OpenAI(api_key=api_key)
        self.model = model
        self._initialize_cache()

    def _initialize_cache(self):
        self.cache_file = 'dream_cache.json'
        try:
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.cache = {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def _get_cache_key(self, dream_text, mood, style):
        content = f"{dream_text}:{mood}:{style}:{self.model}"
        return hashlib.md5(content.encode()).hexdigest()

    @lru_cache(maxsize=100)
    def get_cached_interpretation(self, cache_key):
        return self.cache.get(cache_key)

    def get_gpt_interpretation(self, dream_text, mood='', style='neutro'):
        try:
            # In modalità test, restituisci un'interpretazione di esempio
            if is_test_mode:
                logger.info("Using test mode interpretation")
                return self._get_test_interpretation(dream_text, mood, style)

            cache_key = self._get_cache_key(dream_text, mood, style)
            cached_result = self.get_cached_interpretation(cache_key)
            if cached_result:
                logger.info(f"Cache hit for dream interpretation: {cache_key[:8]}")
                return cached_result

            logger.info(f"Processing new dream interpretation - Style: {style}, Mood: {mood}, Model: {self.model}")

            style_prompts = {
                "neutro": "Fornisci un'interpretazione professionale e oggettiva",
                "poetico": "Interpreta il sogno in modo poetico e metaforico",
                "scientifico": "Analizza il sogno da una prospettiva psicologica freudiana e junghiana",
                "spirituale": "Offri un'interpretazione spirituale e simbolica",
                "consolatorio": "Fornisci un'interpretazione empatica e rassicurante"
            }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Sei un esperto interprete di sogni specializzato in psicologia junghiana e analisi simbolica."},
                    {"role": "user", "content": self._generate_enhanced_prompt(dream_text, mood, style, style_prompts)}
                ],
                temperature=0.7,
                max_tokens=1200  # Limite più contenuto per GPT-3.5
            )

            interpretation = response.choices[0].message.content
            self.cache[cache_key] = interpretation
            self._save_cache()
            return interpretation

        except Exception as e:
            logger.error(f"Error in GPT interpretation: {str(e)}")
            return self._fallback_interpretation(dream_text, mood, style)

    def _get_test_interpretation(self, dream_text, mood, style):
        """Fornisce un'interpretazione di esempio per la modalità test"""
        return f"""
        <div class='interpretation-section'>
            <h3>🔍 Simboli Principali</h3>
            <p>Il tuo sogno contiene elementi interessanti che potrebbero rappresentare aspetti della tua vita quotidiana.</p>
            
            <h3>🧠 Analisi Psicologica</h3>
            <p>Questo è un esempio di interpretazione in modalità test. L'applicazione sta funzionando correttamente.</p>
            <p>Mood selezionato: {mood}</p>
            <p>Stile interpretativo: {style}</p>
            
            <h3>💡 Suggerimenti</h3>
            <p>Questa è una versione di test dell'applicazione. Per interpretazioni reali, configura una chiave API OpenAI valida.</p>
        </div>
        """

    def _generate_enhanced_prompt(self, dream_text, mood, style, style_prompts):
        return f"""Sei un esperto interprete di sogni con conoscenze approfondite di psicologia del profondo.

Analizza il seguente sogno con particolare attenzione:
"{dream_text}"

Contesto emotivo: {mood if mood else 'non specificato'}
Approccio interpretativo: {style_prompts.get(style, style_prompts['neutro'])}

Fornisci un'interpretazione sintetica ma significativa, includendo:
1. 🔍 Simboli principali e significato archetipico
2. 🧠 Spiegazione psicologica
3. 💡 Riflessione utile per il sognatore

Formatta la risposta in HTML semplice, divisa per sezioni."""

    def _fallback_interpretation(self, dream_text, mood='', style='neutro'):
        logger.warning("Using fallback interpretation")
        return "Mi dispiace, al momento non riesco a interpretare questo sogno. Riprova più tardi."

def interpret_dream(dream_text, mood='', style='neutro', model="gpt-3.5-turbo"):
    interpreter = DreamInterpreter(model=model)
    return interpreter.get_gpt_interpretation(dream_text, mood, style)
