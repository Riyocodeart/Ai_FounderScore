import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# Industry keywords
INDUSTRY_KEYWORDS = {
    "Food & Beverage": ["juice", "restaurant", "food", "snack", "beverage"],
    "FinTech": ["finance", "payment", "bank", "crypto", "loan"],
    "EdTech": ["education", "learning", "course", "students"],
    "HealthTech": ["health", "medical", "fitness", "hospital"],
    "E-commerce": ["online store", "marketplace", "ecommerce", "sell products"]
}

BUSINESS_MODELS = {
    "Subscription": ["subscription", "monthly plan", "yearly plan"],
    "Marketplace": ["marketplace", "platform connecting"],
    "SaaS": ["software", "app", "saas", "web platform"],
    "Product Sales": ["sell", "product brand", "manufacture"]
}

def detect_industry(text):
    text_lower = text.lower()
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for word in keywords:
            if word in text_lower:
                return industry
    return "Other"

def detect_business_model(text):
    text_lower = text.lower()
    for model, keywords in BUSINESS_MODELS.items():
        for word in keywords:
            if word in text_lower:
                return model
    return "Unknown"

def extract_target_market(doc):
    for ent in doc.ents:
        if ent.label_ in ["NORP", "ORG", "PERSON"]:
            return ent.text
    return "General Consumers"

def extract_problem_statement(doc):
    for sent in doc.sents:
        if "problem" in sent.text.lower() or "lack" in sent.text.lower():
            return sent.text.strip()
    return list(doc.sents)[0].text.strip()

def extract_startup_info(idea_text):
    doc = nlp(idea_text)

    industry = detect_industry(idea_text)
    business_model = detect_business_model(idea_text)
    target_market = extract_target_market(doc)
    problem_statement = extract_problem_statement(doc)

    return {
        "industry": industry,
        "target_market": target_market,
        "business_model": business_model,
        "problem_statement": problem_statement
    }