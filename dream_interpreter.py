def interpret_dream(dream_text):
    """
    Analyze dream text and return an interpretation based on keywords.
    
    Args:
        dream_text (str): The text of the dream to interpret
        
    Returns:
        str: The interpretation of the dream
    """
    dream_text = dream_text.lower()
    
    # List of keywords and their interpretations
    interpretations = {
        "volare": "Sognare di volare rappresenta il desiderio di libertà o evasione da una situazione opprimente. Potrebbe indicare che stai cercando di superare ostacoli o limiti nella tua vita.",
        "cadere": "Sognare di cadere spesso riflette sensazioni di insicurezza o perdita di controllo in qualche aspetto della tua vita. Potrebbe essere legato a timori di fallimento.",
        "acqua": "L'acqua nei sogni simboleggia le emozioni e l'inconscio. Acqua chiara può rappresentare chiarezza emotiva, mentre acqua torbida potrebbe indicare confusione o problemi emotivi irrisolti.",
        "denti": "Sognare di perdere i denti è comune e spesso legato a paure di perdita, preoccupazioni per l'immagine personale o ansia per un cambiamento imminente.",
        "inseguire": "Essere inseguiti in un sogno può riflettere la sensazione di evitare qualcosa nella vita reale, come una responsabilità o una situazione difficile.",
        "esame": "Sognare di non essere preparati per un esame o di fallirlo può riflettere ansie sulle proprie capacità o paura del giudizio altrui.",
        "casa": "La casa nei sogni rappresenta spesso il sé interiore. Esplorare stanze sconosciute potrebbe indicare la scoperta di nuovi aspetti della propria personalità.",
        "morte": "Sognare la morte raramente è premonitorio; più spesso simboleggia la fine di una fase e l'inizio di un nuovo capitolo nella vita.",
        "nudo": "Sognare di essere nudi in pubblico può riflettere vulnerabilità, paura di essere esposti o ansia sociale.",
        "labirinto": "Trovarsi in un labirinto suggerisce confusione nel percorso di vita o difficoltà nel prendere una decisione importante."
    }
    
    # Check for multiple keywords in dream text
    found_interpretations = []
    for keyword, interpretation in interpretations.items():
        if keyword in dream_text:
            found_interpretations.append(interpretation)
    
    # If specific keywords were found, return their interpretations
    if found_interpretations:
        # Join with line breaks if multiple keywords were found
        return " ".join(found_interpretations)
    
    # Default interpretation if no specific keywords were found
    return "Questo sogno potrebbe riflettere emozioni nascoste o desideri repressi. " \
           "I sogni spesso elaborano esperienze recenti e pensieri subconsci. " \
           "Considera gli elementi emotivi che erano presenti e come potrebbero collegarsi alla tua vita attuale."
