import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# -------------------------
# Expanded Industry Keywords
# -------------------------
INDUSTRY_KEYWORDS = {
    "Food & Beverage": ["juice", "restaurant", "food", "snack", "beverage"],
    "FinTech": ["finance", "payment", "bank", "crypto", "loan"],
    "EdTech": ["education", "learning", "course", "students"],
    "HealthTech": ["health", "medical", "fitness", "hospital"],
    "E-commerce": ["online store", "marketplace", "ecommerce", "sell products"],
    "AI": ["artificial intelligence", "ai", "machine learning"],
    "Cybersecurity": ["security", "cyber", "data protection", "encryption"],
    "Logistics": ["delivery", "supply chain", "logistics", "transport"],
    "ClimateTech": ["climate", "carbon", "sustainability", "renewable"],
    "AgriTech": ["agriculture", "farming", "crop", "agritech"],
    "Creator Economy": ["creator", "influencer", "content platform"],
    "Gaming": ["game", "gaming", "esports"],
    "Web3": ["blockchain", "web3", "decentralized", "nft"]
}

# -------------------------
# Expanded Business Models
# -------------------------
BUSINESS_MODELS = {
    "Subscription": ["subscription", "monthly plan", "yearly plan"],
    "Marketplace": ["marketplace", "platform connecting"],
    "SaaS": ["software", "app", "saas", "web platform"],
    "Product Sales": ["sell", "product brand", "manufacture"],
    "Freemium": ["free tier", "premium upgrade"],
    "B2B Services": ["services for businesses", "enterprise solution"]
}

# -------------------------
# Detection Functions
# -------------------------

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


def detect_target_market(text, doc):
    text_lower = text.lower()

    # Keyword-based detection
    if "students" in text_lower:
        return "Students"
    if "small businesses" in text_lower:
        return "Small Businesses"
    if "enterprises" in text_lower:
        return "Enterprises"
    if "rural" in text_lower:
        return "Rural Population"
    if "gen z" in text_lower:
        return "Gen Z"

    # Named entity fallback
    for ent in doc.ents:
        if ent.label_ in ["NORP", "ORG", "PERSON"]:
            return ent.text

    return "General Consumers"


def detect_problem_statement(doc):
    for sent in doc.sents:
        sentence_lower = sent.text.lower()
        if any(keyword in sentence_lower for keyword in 
               ["problem", "lack", "struggle", "difficulty", "due to", "because"]):
            return sent.text.strip()

    # fallback to first sentence
    return list(doc.sents)[0].text.strip()


# -------------------------
# Confidence Score
# -------------------------

def calculate_confidence(industry, business_model, problem_statement, target_market):
    score = 0

    if industry != "Other":
        score += 30
    if business_model != "Unknown":
        score += 30
    if problem_statement:
        score += 20
    if target_market != "General Consumers":
        score += 20

    return score


# -------------------------
# Main Extraction Function
# -------------------------

def extract_startup_info(idea_text):
    doc = nlp(idea_text)

    industry = detect_industry(idea_text)
    business_model = detect_business_model(idea_text)
    target_market = detect_target_market(idea_text, doc)
    problem_statement = detect_problem_statement(doc)

    confidence = calculate_confidence(
        industry,
        business_model,
        problem_statement,
        target_market
    )

    return {
        "industry": industry,
        "target_market": target_market,
        "business_model": business_model,
        "problem_statement": problem_statement,
        "analysis_confidence_score": confidence
    }