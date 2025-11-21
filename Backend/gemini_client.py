import google.generativeai as genai

API_KEY = "AIzaSyDG5aiRXnu1T46vfx46y8clYu3aYa9DLWY"

genai.configure(api_key=API_KEY)


async def analyze_sentiment(texto: str) -> str:
    """
    Analiza el sentimiento del texto usando Gemini.
    Retorna: 'positivo', 'negativo' o 'neutro'
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        prompt = f"""Eres un experto analizador de sentimientos. Analiza el siguiente texto y clasifica su sentimiento.

INSTRUCCIONES:
- Si el texto expresa emociones positivas, satisfacción, felicidad, amor, o cosas buenas → Responde: positivo
- Si el texto expresa emociones negativas, tristeza, enojo, decepción, o cosas malas → Responde: negativo  
- Si el texto es completamente neutral, sin emociones claras → Responde: neutro

Texto a analizar: "{texto}"

Sentimiento:"""
        
        response = model.generate_content(prompt)
        sentimiento = response.text.strip().lower()
        
        
        sentimiento = sentimiento.replace(".", "").replace(",", "").replace(":", "").strip()
        
        
        if "positiv" in sentimiento:
            return "positivo"
        elif "negativ" in sentimiento:
            return "negativo"
        elif "neutr" in sentimiento:
            return "neutro"
        
        
        if sentimiento in ["positivo", "negativo", "neutro"]:
            return sentimiento
        
        
        texto_lower = texto.lower()
        
        
        palabras_positivas = ["excelente", "bueno", "genial", "increíble", "fantástico", 
                             "maravilloso", "amor", "feliz", "alegre", "encanta", "perfecto",
                             "hermoso", "lindo", "mejor", "super", "rico", "delicioso"]
        
        palabras_negativas = ["malo", "horrible", "terrible", "pésimo", "triste", 
                             "tristeza", "odio", "feo", "peor", "desagradable", 
                             "deficiente", "decepción", "molesto", "enojado"]
        
        pos_count = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
        neg_count = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
        
        if pos_count > neg_count:
            return "positivo"
        elif neg_count > pos_count:
            return "negativo"
        
        return "neutro"

    except Exception as e:
        print(f"Error analizando sentimiento: {e}")
        texto_lower = texto.lower()
        if any(word in texto_lower for word in ["bueno", "excelente", "amor", "feliz", "encanta"]):
            return "positivo"
        elif any(word in texto_lower for word in ["malo", "horrible", "triste", "odio", "enojo"]):
            return "negativo"
        return "neutro"