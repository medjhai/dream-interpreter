import os
from openai import OpenAI

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def fast_interpret_dream(dream_text, mood='neutro', style='psicologico'):
    """
    Fast, concise dream interpretation using OpenAI with optimized prompt.
    """
    if not dream_text or len(dream_text.strip()) < 5:
        return "Per favore, fornisci una descrizione più dettagliata del tuo sogno per un'interpretazione accurata."
    
    # Simplified, faster prompt for quick responses
    prompt = f"""
    Analizza questo sogno in modo conciso e pratico (massimo 120 parole):
    
    Sogno: "{dream_text}"
    Mood: {mood}
    Stile: {style}
    
    Fornisci:
    🔍 Simbolo principale e significato
    💭 Connessione emotiva
    💡 Un insight pratico
    
    Scrivi in italiano, tono caldo ma conciso.
    """
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Faster, cheaper model
            messages=[
                {
                    "role": "system",
                    "content": "Sei un analista di sogni esperto. Rispondi in modo conciso e mirato."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=200,  # Reduced for faster response
            temperature=0.7
        )
        
        interpretation = response.choices[0].message.content
        return interpretation.strip() if interpretation else "Interpretazione non disponibile."
        
    except Exception as e:
        return f"Spiacenti, si è verificato un errore durante l'interpretazione: {str(e)}"