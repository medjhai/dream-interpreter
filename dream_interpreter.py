def interpret_dream(dream_text, mood='', style='neutro'):
    """
    Analyze dream text and return a detailed interpretation based on keywords, symbols,
    emotional state, and chosen interpretation style.
    
    Args:
        dream_text (str): The text of the dream to interpret
        mood (str, optional): The emotional state during the dream ('felice', 'triste', etc.)
        style (str, optional): The style of interpretation ('neutro', 'poetico', etc.)
        
    Returns:
        str: The detailed interpretation of the dream with psychological insights,
             adjusted based on mood and interpretation style
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
    
    # Mood-specific insights to add to interpretations
    mood_insights = {
        "felice": {
            "intro": "Hai indicato che ti sentivi felice durante questo sogno. Le emozioni positive nei sogni spesso riflettono stati di benessere, realizzazione o aspirazioni appaganti nella vita cosciente.",
            "connection": "La felicità provata durante il sogno potrebbe amplificare gli aspetti positivi dei simboli onirici, sottolineando potenziali, opportunità e nuove possibilità."
        },
        "triste": {
            "intro": "Hai indicato che ti sentivi triste durante questo sogno. La tristezza nei sogni spesso elabora emozioni represse, perdite non completamente elaborate o bisogni emotivi insoddisfatti.",
            "connection": "La tristezza provata potrebbe indicare un processo di elaborazione emotiva in corso, un lutto simbolico o la necessità di prestare attenzione a ciò che ti manca nella vita quotidiana."
        },
        "ansioso": {
            "intro": "Hai indicato che ti sentivi ansioso durante questo sogno. L'ansia nei sogni riflette spesso preoccupazioni attuali, paure inconsce o situazioni di stress che richiedono attenzione.",
            "connection": "L'ansia provata potrebbe amplificare aspetti di incertezza o preoccupazione nei simboli del sogno, suggerendo aree della tua vita che necessitano di maggiore sicurezza o chiarezza."
        },
        "rabbioso": {
            "intro": "Hai indicato che ti sentivi rabbioso durante questo sogno. La rabbia nei sogni spesso rappresenta frustrazione, confini violati o situazioni di ingiustizia percepita che richiedono riconoscimento.",
            "connection": "La rabbia provata potrebbe indicare energia psichica che cerca espressione, conflitti irrisolti o la necessità di affermare i tuoi bisogni in modo più deciso."
        },
        "confuso": {
            "intro": "Hai indicato che ti sentivi confuso durante questo sogno. La confusione nei sogni spesso riflette periodi di transizione, decisioni complesse o situazioni ambigue nella vita cosciente.",
            "connection": "La confusione provata potrebbe indicare la necessità di integrare diverse parti della tua personalità o esperienza, o il bisogno di maggiore chiarezza in alcune aree della tua vita."
        }
    }
    
    # Style-specific formatting and approaches
    style_approaches = {
        "neutro": {
            "title_format": "<strong>{}</strong>",
            "intro": "",
            "conclusion": "",
            "tone": "neutro"
        },
        "poetico": {
            "title_format": "<strong><em>{}</em></strong>",
            "intro": "Come un pittore di sogni, ti guiderò in un viaggio attraverso il paesaggio onirico che hai condiviso, dove ogni elemento è una pennellata sulla tela dell'inconscio...",
            "conclusion": "E così, come le foglie si abbandonano al vento d'autunno, anche i sogni danzano nella mente per sussurrarci verità che la ragione da sola non potrebbe cogliere.",
            "tone": "poetico"
        },
        "scientifico": {
            "title_format": "<strong>{} - Analisi Psicologica</strong>",
            "intro": "Seguendo il modello di analisi onirica sviluppato da C.G. Jung e approfondito dagli studi contemporanei di neuropsicologia del sonno, questo sogno presenta caratteristiche significative che meritano un'analisi strutturale approfondita.",
            "conclusion": "In conclusione, dall'analisi dei contenuti manifesti e latenti di questo sogno, emerge un quadro complessivo che suggerisce processi psichici di integrazione e risoluzione in linea con la teoria dell'individuazione junghiana.",
            "tone": "scientifico"
        },
        "spirituale": {
            "title_format": "<strong>{} ✨</strong>",
            "intro": "I sogni sono messaggeri dell'anima, ponti tra il mondo materiale e quello spirituale. In questa dimensione sacra, ogni simbolo è un portale verso comprensioni più profonde del tuo cammino esistenziale.",
            "conclusion": "Ricorda che i sogni sono doni sacri, specchi dell'anima che riflettono il tuo viaggio spirituale. Ascoltane i messaggi con il cuore aperto e lascia che illuminino il tuo sentiero interiore.",
            "tone": "spirituale"
        },
        "consolatorio": {
            "title_format": "<strong>{}</strong>",
            "intro": "È importante ricordare che i sogni, anche quelli inquietanti, sono espressioni naturali della nostra mente che ci aiutano a elaborare emozioni e esperienze. Sei al sicuro, e insieme esploreremo con gentilezza i messaggi che il tuo inconscio ti sta comunicando.",
            "conclusion": "Prenditi cura di te mentre elabori questi significati. I sogni, come specchi interiori, ci mostrano parti di noi stessi che meritano compassione e comprensione. Qualunque emozione tu stia provando è valida e preziosa nel tuo percorso di crescita personale.",
            "tone": "consolatorio"
        }
    }
    
    # Determine style approach
    style_approach = style_approaches.get(style, style_approaches["neutro"])
    
    # Add mood insight if provided
    mood_insight = ""
    if mood and mood in mood_insights:
        mood_info = mood_insights[mood]
        mood_insight = f"<strong>Sul tuo stato emotivo:</strong><br><br>{mood_info['intro']}<br><br>{mood_info['connection']}<br><br>"
    
    # Check for multiple keywords in dream text
    found_interpretations = []
    for keyword, details in interpretations.items():
        if keyword in dream_text:
            # Apply style formatting to interpretation
            title = style_approach["title_format"].format(details['title'])
            
            # Create a formatted interpretation with title and detailed sections
            # Adjust tone based on selected style
            formatted_interpretation = f"{title}<br><br>"
            
            # Basic description with adjusted tone based on style
            if style == "poetico":
                formatted_interpretation += f"Come acque che danzano nel letto di un fiume, {details['basic'].lower()}<br><br>"
            elif style == "scientifico":
                formatted_interpretation += f"L'analisi empirica di questo elemento onirico indica che {details['basic'].lower()} Questo fenomeno è stato documentato in molteplici studi longitudinali sulla psicologia del sonno.<br><br>"
            elif style == "spirituale":
                formatted_interpretation += f"Nel linguaggio sacro dei sogni, {details['basic'].lower()} Questo simbolo risuona con l'energia universale che connette tutte le anime.<br><br>"
            elif style == "consolatorio":
                formatted_interpretation += f"{details['basic']} È un'esperienza comune e completamente naturale che molte persone condividono nei loro sogni.<br><br>"
            else:
                formatted_interpretation += f"{details['basic']}<br><br>"
            
            # Psychological meaning with adjusted tone based on style
            if style == "poetico":
                formatted_interpretation += f"<em>La voce dell'inconscio racconta:</em> {details['psychological']}<br><br>"
            elif style == "scientifico":
                formatted_interpretation += f"<em>Analisi psicologica:</em> {details['psychological']} Questo è coerente con il modello teorico dell'inconscio collettivo e la teoria degli archetipi.<br><br>"
            elif style == "spirituale":
                formatted_interpretation += f"<em>Risonanza spirituale:</em> {details['psychological']} In molte tradizioni antiche, questo simbolo rappresenta il dialogo tra l'anima e il cosmo.<br><br>"
            elif style == "consolatorio":
                formatted_interpretation += f"<em>Comprendere con gentilezza:</em> {details['psychological']} Ricorda che questi processi interiori sono normali e ti stanno aiutando a crescere.<br><br>"
            else:
                formatted_interpretation += f"<em>Significato psicologico:</em> {details['psychological']}<br><br>"
            
            # Practical application with adjusted tone based on style
            if style == "poetico":
                formatted_interpretation += f"<em>Il sentiero da esplorare:</em> {details['practical']}"
            elif style == "scientifico":
                formatted_interpretation += f"<em>Applicazione pratica basata sull'evidenza:</em> {details['practical']} L'integrazione consapevole di questi contenuti psichici può contribuire al processo di individuazione e all'equilibrio emotivo."
            elif style == "spirituale":
                formatted_interpretation += f"<em>Guida per il cammino interiore:</em> {details['practical']} Medita su questo simbolo per rivelare ulteriori livelli di comprensione spirituale."
            elif style == "consolatorio":
                formatted_interpretation += f"<em>Passi gentili verso la comprensione:</em> {details['practical']} Sii paziente con te stesso/a mentre esplori questi significati."
            else:
                formatted_interpretation += f"<em>Applicazione pratica:</em> {details['practical']}"
            
            found_interpretations.append(formatted_interpretation)
    
    # Compose the final interpretation
    if found_interpretations:
        # Add style-specific intro if available
        result = ""
        if style_approach["intro"]:
            result += f"{style_approach['intro']}<br><br>"
        
        # Add mood insight if available
        if mood_insight:
            result += f"{mood_insight}<hr>"
            
        # Add all found interpretations
        result += "<hr>".join(found_interpretations)
        
        # Add style-specific conclusion if available
        if style_approach["conclusion"]:
            result += f"<hr><br>{style_approach['conclusion']}"
            
        return result
    
    # Enhanced default interpretation if no specific keywords were found
    default_interpretation = "<strong>Analisi Generale del Sogno</strong><br><br>"
    
    # Add style-specific intro
    if style_approach["intro"]:
        default_interpretation += f"{style_approach['intro']}<br><br>"
    
    # Add mood insight if provided
    if mood_insight:
        default_interpretation += mood_insight
    
    # Base interpretation adjusted by style
    if style == "poetico":
        default_interpretation += """Come un'onda che accarezza una spiaggia sconosciuta, questo sogno porta con sé frammenti di un linguaggio misterioso, simboli che danzano ai margini della comprensione comune. Il tuo sogno è una poesia non scritta, un quadro dipinto con i colori dell'anima.<br><br>
        <em>Sussurri dell'inconscio:</em> I sogni sono come farfalle notturne che trasportano messaggi dall'inconscio alla coscienza. Anche quando il loro linguaggio sembra criptico, stanno tessendo una trama di significati profondamente personali, intrecciando fili di memorie, desideri e intuizioni in un arazzo unico.<br><br>
        <em>Sentieri da esplorare:</em> Per decifrare questo poetico messaggio dell'anima, potresti:<br>
        - Quale melodia emotiva risuonava più forte durante il sogno? Le emozioni sono i colori con cui l'anima dipinge.<br>
        - Quali personaggi o luoghi del sogno echeggiano con particolare intensità nella tua vita attuale?<br>
        - Come un fiume sotterraneo, quali correnti di pensieri o emozioni potrebbero scorrere sotto la superficie della tua consapevolezza?<br>
        - Osserva se questo motivo onirico ritorna in altre notti, come un ritornello in una canzone che l'anima desidera tu ascolti."""
    elif style == "scientifico":
        default_interpretation += """Questo sogno presenta caratteristiche idiosincratiche che non si conformano ai pattern simbolici standardizzati nella letteratura onirica, suggerendo un'elaborazione altamente personalizzata di contenuti psichici.<br><br>
        <em>Analisi neuropsicologica:</em> I sogni rappresentano processi di consolidamento della memoria e integrazione emotiva durante la fase REM del sonno. L'attività dell'amigdala e dell'ippocampo facilita l'elaborazione di stimoli emotivamente salienti e la loro integrazione con memorie episodiche e semantiche, generando narrazioni simboliche altamente individualizzate.<br><br>
        <em>Protocollo di analisi consigliato:</em> Per una valutazione empirica più accurata di questo materiale onirico, si suggerisce di considerare i seguenti parametri:<br>
        - Identificare la valenza emotiva predominante durante l'esperienza onirica, dato il suo ruolo determinante nell'attivazione dell'amigdala.<br>
        - Analizzare le correlazioni statistiche tra elementi onirici e contesti esperienziali recenti (entro 7 giorni dall'evento onirico).<br>
        - Monitorare la frequenza di elementi ricorrenti in un campione longitudinale di esperienze oniriche per identificare pattern significativi.<br>
        - Verificare l'ipotesi nulla che questi elementi simbolici non siano correlati a processi di elaborazione emotiva in corso."""
    elif style == "spirituale":
        default_interpretation += """Questo sogno emerge dalle profondità dell'anima come un messaggio unico e sacro, portando con sé simboli che possono non appartenere alle categorie tradizionali, ma che risuonano con la tua essenza spirituale individuale.<br><br>
        <em>Risonanza cosmica:</em> I sogni sono ponti tra il visibile e l'invisibile, tra la coscienza ordinaria e la saggezza universale. Anche quando i simboli sembrano personali e unici, essi vibrano in armonia con l'energia del cosmo e portano messaggi dalla tua guida interiore.<br><br>
        <em>Percorso dell'anima:</em> Per approfondire il messaggio sacro di questo sogno, considera questi aspetti:<br>
        - Quale energia emotiva ha illuminato il sogno? L'emozione è la voce dell'anima che parla alla mente.<br>
        - Vi sono presenze o luoghi che risuonano con la tua attuale fase del cammino spirituale?<br>
        - Quali parti di te potrebbero cercare guarigione, integrazione o espressione attraverso questo messaggio onirico?<br>
        - Osserva se questo simbolismo si ripresenta in altre visioni o meditazioni, creando un mandala di significato che guida il tuo risveglio interiore."""
    elif style == "consolatorio":
        default_interpretation += """Il tuo sogno contiene elementi unici e personali, e questo è assolutamente normale e positivo. I sogni sono esperienze individuali preziose che riflettono la tua unicità.<br><br>
        <em>Un abbraccio comprensivo:</em> I sogni sono come lettere che scriviamo a noi stessi, espressioni sincere del nostro mondo interiore. Anche quando non riconosciamo immediatamente i simboli, il sogno sta comunicando qualcosa di importante con gentilezza e cura. È perfettamente normale sentirsi confusi o incerti riguardo al significato; fa parte del processo di comprensione di sé.<br><br>
        <em>Passi delicati verso la comprensione:</em> Con pazienza e autocompassione, potresti considerare:<br>
        - Quali emozioni hai provato durante il sogno? Non ci sono emozioni giuste o sbagliate, tutte sono messaggi preziosi.<br>
        - Ci sono elementi del sogno che ti fanno sentire a tuo agio o a disagio? Entrambe le reazioni sono valide e meritano ascolto.<br>
        - Il sogno potrebbe riflettere esperienze recenti o pensieri che ti stanno accompagnando. Va bene prendersi il tempo necessario per elaborarli.<br>
        - Se questo sogno dovesse ripetersi, sappi che è semplicemente un invito a prestare attenzione a qualcosa di importante per il tuo benessere."""
    else:  # neutral style
        default_interpretation += """Questo sogno contiene elementi che non rientrano nelle categorie più comuni di simboli onirici, il che lo rende particolarmente personale e unico.<br><br>
        <em>Significato psicologico:</em> I sogni sono manifestazioni del nostro inconscio che elaborano esperienze, pensieri ed emozioni. Anche quando non riconosciamo simboli evidenti, il sogno sta comunicando qualcosa di significativo attraverso il linguaggio simbolico che è profondamente personale.<br><br>
        <em>Applicazione pratica:</em> Per comprendere meglio questo sogno, considera i seguenti aspetti:<br>
        - Quale era l'emozione predominante durante il sogno? Le emozioni sono spesso la chiave per l'interpretazione.<br>
        - Ci sono persone o luoghi del sogno che hanno un significato particolare nella tua vita attuale?<br>
        - Il sogno potrebbe riflettere preoccupazioni, desideri o conflitti che stai vivendo ma che non hai pienamente riconosciuto.<br>
        - Prova a notare se elementi di questo sogno si ripetono in altri sogni, creando un pattern significativo."""
    
    # Add style-specific conclusion
    if style_approach["conclusion"]:
        default_interpretation += f"<br><br>{style_approach['conclusion']}"
        
    return default_interpretation
