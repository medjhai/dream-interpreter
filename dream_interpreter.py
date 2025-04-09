def interpret_dream(dream_text):
    """
    Analyze dream text and return a detailed interpretation based on keywords and symbols.
    
    Args:
        dream_text (str): The text of the dream to interpret
        
    Returns:
        str: The detailed interpretation of the dream with psychological insights
    """
    dream_text = dream_text.lower()
    
    # Enhanced list of keywords and their detailed interpretations
    interpretations = {
        "volare": {
            "title": "Il Volo e la Libertà",
            "basic": "Sognare di volare rappresenta il desiderio profondo di libertà o evasione da una situazione opprimente.",
            "psychological": "Dal punto di vista psicologico, il volo nei sogni è collegato alla trascendenza dei limiti quotidiani e rappresenta una profonda aspirazione all'autonomia emotiva e spirituale.",
            "practical": "Questo simbolo potrebbe indicare che stai cercando di superare ostacoli significativi nella tua vita, o che desideri elevarti al di sopra di circostanze difficili. Considera quali aree della tua vita ti fanno sentire limitato/a o vincolato/a."
        },
        "cadere": {
            "title": "La Caduta e la Perdita di Controllo",
            "basic": "Sognare di cadere riflette sensazioni di insicurezza o perdita di controllo in qualche aspetto della tua vita.",
            "psychological": "Secondo l'interpretazione junghiana, la caduta simboleggia la discesa nell'inconscio e il confronto con aspetti repressi del sé. La sensazione di caduta può anche rappresentare il timore di cedere agli impulsi o alle emozioni incontrollate.",
            "practical": "Questo sogno potrebbe essere collegato a timori di fallimento o a situazioni in cui ti senti sopraffatto/a. Rifletti su quali decisioni o responsabilità recenti ti hanno fatto sentire vulnerabile o impreparato/a."
        },
        "acqua": {
            "title": "L'Acqua e il Mondo Emotivo",
            "basic": "L'acqua nei sogni simboleggia le emozioni e l'inconscio collettivo.",
            "psychological": "Nella psicologia dei sogni, l'acqua è l'archetipo per eccellenza delle emozioni profonde e del flusso della vita psichica. La sua forma e stato (calma, agitata, limpida, torbida) riflette direttamente lo stato emotivo del sognatore e il suo rapporto con il proprio mondo interiore.",
            "practical": "Acqua chiara può rappresentare chiarezza emotiva e insight, mentre acqua torbida potrebbe indicare confusione o problemi emotivi irrisolti. Considera la qualità dell'acqua nel sogno: era un oceano vasto (emozioni travolgenti), un fiume (flusso di vita), un lago (riflessione interiore) o pioggia (purificazione)?"
        },
        "denti": {
            "title": "I Denti e l'Identità Personale",
            "basic": "Sognare di perdere i denti è comune e spesso legato a paure di perdita o preoccupazioni per l'immagine personale.",
            "psychological": "I denti nei sogni sono collegati all'autostima, alla capacità di assimilare nuove esperienze e all'ansia sociale. La loro perdita può simboleggiare timori riguardanti il deterioramento, l'invecchiamento o la paura di apparire inadeguati agli occhi altrui.",
            "practical": "Questo simbolo onirico potrebbe riflettere ansia per un cambiamento imminente, preoccupazioni legate alla comunicazione o al modo in cui ti presenti agli altri. Potresti stare attraversando una fase di trasformazione personale che causa incertezza sulla tua identità."
        },
        "inseguire": {
            "title": "L'Inseguimento e la Fuga",
            "basic": "Essere inseguiti in un sogno riflette spesso la sensazione di evitare qualcosa nella vita reale.",
            "psychological": "Dal punto di vista psicanalitico, l'inseguimento nei sogni può rappresentare parti rifiutate o proiettate della propria personalità che cercano integrazione. Ciò che fuggiamo nei sogni è frequentemente ciò che non vogliamo affrontare nella veglia.",
            "practical": "Questo sogno suggerisce che potresti star evitando una responsabilità, un'emozione difficile o una situazione complessa. Considera cosa o chi ti stava inseguendo, poiché questo elemento potrebbe offrire indizi su ciò che stai cercando di evitare."
        },
        "esame": {
            "title": "Gli Esami e la Valutazione di Sé",
            "basic": "Sognare di affrontare un esame o di fallirlo riflette ansie sulle proprie capacità o paura del giudizio altrui.",
            "psychological": "Questi sogni spesso persistono anche molti anni dopo il periodo scolastico, indicando come il tema della valutazione e del giudizio rimanga centrale nell'inconscio umano. Rappresentano il confronto con standard interiorizzati e la paura di non essere all'altezza delle aspettative, proprie o altrui.",
            "practical": "Rifletti su quali situazioni nella tua vita attuale ti fanno sentire giudicato/a o messo/a alla prova. Potresti essere sottoposto/a a pressioni professionali o personali che riattivano antiche insicurezze."
        },
        "casa": {
            "title": "La Casa e il Sé Interiore",
            "basic": "La casa nei sogni rappresenta spesso il sé interiore e la psiche del sognatore.",
            "psychological": "Nella tradizione junghiana, la casa è un simbolo potente della totalità psichica e dell'identità personale. Ogni stanza può rappresentare un aspetto diverso della personalità, mentre lo stato della casa (nuova, vecchia, in rovina, in costruzione) riflette la percezione che il sognatore ha del proprio sviluppo interiore.",
            "practical": "Esplorare stanze sconosciute potrebbe indicare la scoperta di nuovi aspetti della tua personalità o talenti inespressi. Presta attenzione alle condizioni delle stanze: erano luminose, buie, in ordine o disordinate? Questi elementi offrono indizi sui tuoi stati emotivi e sulle potenzialità ancora inesplorate."
        },
        "morte": {
            "title": "La Morte e la Trasformazione",
            "basic": "Sognare la morte raramente è premonitorio; più spesso simboleggia la fine di una fase e l'inizio di un nuovo capitolo nella vita.",
            "psychological": "Nella simbologia onirica, la morte rappresenta il processo di trasformazione psichica, la necessità di abbandonare vecchi schemi per far spazio a nuove possibilità. È un archetipo universale che riflette il ciclo naturale di conclusione e rinnovamento presente in ogni aspetto dell'esistenza.",
            "practical": "Considera quali aspetti della tua vita potrebbero essere pronti per una profonda trasformazione. Chi muore nel sogno è significativo: se eri tu, potrebbe indicare un desiderio di reinventarti; se era qualcun altro, potrebbe riflettere cambiamenti nella relazione con quella persona o con ciò che essa rappresenta per te."
        },
        "nudo": {
            "title": "La Nudità e la Vulnerabilità",
            "basic": "Sognare di essere nudi in pubblico riflette vulnerabilità, paura di essere esposti o ansia sociale.",
            "psychological": "La nudità nei sogni è collegata al timore che le nostre imperfezioni, fisiche o psicologiche, vengano rivelate agli altri. Rappresenta uno stato di totale autenticità, privo delle 'maschere sociali' che indossiamo quotidianamente, e la paura associata a tale esposizione.",
            "practical": "Questo sogno potrebbe emergere in momenti in cui ti senti particolarmente esposto/a o vulnerabile in una situazione sociale o professionale. Rifletti su quali aspetti di te stesso/a temi che possano essere scoperti o giudicati dagli altri."
        },
        "labirinto": {
            "title": "Il Labirinto e la Ricerca Interiore",
            "basic": "Trovarsi in un labirinto suggerisce confusione nel percorso di vita o difficoltà nel prendere una decisione importante.",
            "psychological": "Il labirinto è un antico simbolo del viaggio iniziatico e della ricerca spirituale. Rappresenta il percorso complesso dell'individuazione, con le sue svolte, vicoli ciechi e ripetizioni, che conduce infine al centro del sé autentico.",
            "practical": "Questo sogno potrebbe riflettere una fase di confusione o incertezza che stai attraversando. La tua reazione all'interno del labirinto è significativa: cercavi disperatamente una via d'uscita o esploravi con curiosità? Questa distinzione può rivelare il tuo atteggiamento attuale verso le complessità della vita."
        },
        "serpente": {
            "title": "Il Serpente e la Trasformazione",
            "basic": "Il serpente nei sogni rappresenta spesso la trasformazione, la guarigione e l'energia vitale.",
            "psychological": "Nella psicologia dei sogni, il serpente è un simbolo ambivalente che unisce l'energia ctonia (terrestre) con la saggezza primordiale. La sua capacità di mutare pelle lo rende un potente simbolo di rinascita e trasformazione personale. Può rappresentare anche l'integrazione degli opposti e la riconciliazione con aspetti repressi del sé.",
            "practical": "Considera il comportamento del serpente nel sogno: era minaccioso, neutrale o amichevole? La tua reazione emotiva al serpente rivela il tuo rapporto con i processi di cambiamento nella tua vita e con l'energia vitale che cerca espressione."
        },
        "fuoco": {
            "title": "Il Fuoco e la Passione Trasformativa",
            "basic": "Il fuoco nei sogni rappresenta passione, energia creativa e potere trasformativo.",
            "psychological": "Come elemento purificatore e distruttore, il fuoco simboleggia nei sogni la capacità di bruciare il vecchio per far spazio al nuovo. Rappresenta l'intensità emotiva, la libido psichica e la forza vitale che può essere sia creativa che distruttiva.",
            "practical": "Questo simbolo potrebbe indicare un risveglio di passione o creatività nella tua vita, o la necessità di purificare e liberarti da situazioni o relazioni che non ti servono più. Rifletti su come il fuoco si manifestava: era controllato, selvaggio, riscaldante o minaccioso?"
        },
        "bambino": {
            "title": "Il Bambino e il Potenziale di Rinnovamento",
            "basic": "Sognare un bambino spesso rappresenta nuovi inizi, innocenza e potenziale di crescita.",
            "psychological": "Nella psicologia junghiana, il bambino è un archetipo che simboleggia il Sé nascente, la totalità psichica in formazione. Rappresenta la parte più autentica e creativa della personalità, nonché la capacità di meravigliarsi e di vedere il mondo con occhi nuovi.",
            "practical": "La presenza di un bambino nei tuoi sogni potrebbe indicare l'emergere di nuove possibilità, progetti nascenti o una rinnovata vitalità. Potrebbe anche richiamare l'attenzione sulla tua infanzia o su qualità infantili che necessitano integrazione nella tua personalità adulta."
        }
    }
    
    # Check for multiple keywords in dream text
    found_interpretations = []
    for keyword, details in interpretations.items():
        if keyword in dream_text:
            # Create a formatted interpretation with title and detailed sections
            formatted_interpretation = f"<strong>{details['title']}</strong><br><br>"
            formatted_interpretation += f"{details['basic']}<br><br>"
            formatted_interpretation += f"<em>Significato psicologico:</em> {details['psychological']}<br><br>"
            formatted_interpretation += f"<em>Applicazione pratica:</em> {details['practical']}"
            found_interpretations.append(formatted_interpretation)
    
    # If specific keywords were found, return their interpretations
    if found_interpretations:
        # Join with horizontal separators for clear distinction
        return "<hr>".join(found_interpretations)
    
    # Enhanced default interpretation if no specific keywords were found
    return """<strong>Analisi Generale del Sogno</strong><br><br>
           Questo sogno contiene elementi che non rientrano nelle categorie più comuni di simboli onirici, il che lo rende particolarmente personale e unico.<br><br>
           <em>Significato psicologico:</em> I sogni sono manifestazioni del nostro inconscio che elaborano esperienze, pensieri ed emozioni. Anche quando non riconosciamo simboli evidenti, il sogno sta comunicando qualcosa di significativo attraverso il linguaggio simbolico che è profondamente personale.<br><br>
           <em>Applicazione pratica:</em> Per comprendere meglio questo sogno, considera i seguenti aspetti:<br>
           - Quale era l'emozione predominante durante il sogno? Le emozioni sono spesso la chiave per l'interpretazione.<br>
           - Ci sono persone o luoghi del sogno che hanno un significato particolare nella tua vita attuale?<br>
           - Il sogno potrebbe riflettere preoccupazioni, desideri o conflitti che stai vivendo ma che non hai pienamente riconosciuto.<br>
           - Prova a notare se elementi di questo sogno si ripetono in altri sogni, creando un pattern significativo."""
