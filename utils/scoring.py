def calculate_scores(extracted):

    industry = extracted["industry"]
    business_model = extracted["business_model"]

    # -----------------------------
    # 1️⃣ Market Potential
    # -----------------------------
    if industry in ["AI", "FinTech", "HealthTech", "ClimateTech"]:
        market_score = 20
    elif industry in ["EdTech", "E-commerce"]:
        market_score = 16
    else:
        market_score = 12

    # -----------------------------
    # 2️⃣ Competition Density
    # Higher score = more competition (worse)
    # -----------------------------
    if industry in ["Food & Beverage", "E-commerce"]:
        competition_score = 18
    elif industry in ["FinTech", "EdTech"]:
        competition_score = 14
    else:
        competition_score = 10

    # -----------------------------
    # 3️⃣ Scalability
    # -----------------------------
    if business_model == "SaaS":
        scalability_score = 20
    elif business_model in ["Marketplace", "Subscription"]:
        scalability_score = 17
    elif business_model == "Product Sales":
        scalability_score = 13
    else:
        scalability_score = 12

    # -----------------------------
    # 4️⃣ Funding Attractiveness
    # -----------------------------
    if industry in ["AI", "FinTech", "HealthTech", "Web3"]:
        funding_score = 18
    elif industry in ["ClimateTech", "EdTech"]:
        funding_score = 16
    else:
        funding_score = 11

    # -----------------------------
    # 5️⃣ Risk Level (Derived)
    # Lower scalability + high competition = high risk
    # -----------------------------
    risk_score = min(20, 20 - scalability_score + (competition_score // 2))

    # -----------------------------
    # 6️⃣ Innovation Score (NEW)
    # -----------------------------
    if industry in ["AI", "Web3", "ClimateTech"]:
        innovation_score = 20
    elif industry in ["FinTech", "HealthTech"]:
        innovation_score = 16
    else:
        innovation_score = 12

    # -----------------------------
    # 7️⃣ Market Saturation (NEW)
    # Higher = more crowded
    # -----------------------------
    if industry in ["Food & Beverage", "E-commerce"]:
        saturation_score = 18
    elif industry in ["FinTech"]:
        saturation_score = 14
    else:
        saturation_score = 10

    # -----------------------------
    # 8️⃣ Execution Complexity (NEW)
    # -----------------------------
    if business_model == "Product Sales":
        execution_complexity = 18
    elif business_model == "Marketplace":
        execution_complexity = 16
    elif business_model == "SaaS":
        execution_complexity = 12
    else:
        execution_complexity = 14

    # -----------------------------
    # Final Scores Dictionary
    # -----------------------------
    scores = {
        "Market Potential": market_score,
        "Competition Density": competition_score,
        "Scalability": scalability_score,
        "Funding Attractiveness": funding_score,
        "Risk Level": risk_score,
        "Innovation Score": innovation_score,
        "Market Saturation": saturation_score,
        "Execution Complexity": execution_complexity
    }

    total_score = sum(scores.values())

    return scores, total_score


def generate_risk_analysis(extracted, scores):

    industry = extracted["industry"]
    business_model = extracted["business_model"]

    risk_analysis = {}

    # -----------------------------
    # 1️⃣ Market Risk
    # -----------------------------
    if scores["Market Saturation"] >= 16:
        risk_analysis["Market Risk"] = "The industry appears highly saturated, making differentiation challenging."
    elif scores["Market Potential"] >= 18:
        risk_analysis["Market Risk"] = "Strong market growth reduces overall market risk."
    else:
        risk_analysis["Market Risk"] = "Moderate market uncertainty depending on execution strategy."

    # -----------------------------
    # 2️⃣ Competition Risk
    # -----------------------------
    if scores["Competition Density"] >= 16:
        risk_analysis["Competition Risk"] = "High competition could increase customer acquisition costs."
    else:
        risk_analysis["Competition Risk"] = "Competitive pressure appears manageable."

    # -----------------------------
    # 3️⃣ Operational Risk
    # -----------------------------
    if scores["Execution Complexity"] >= 16:
        risk_analysis["Operational Risk"] = "Execution complexity is high and may require strong operational capabilities."
    elif business_model == "SaaS":
        risk_analysis["Operational Risk"] = "SaaS model lowers operational complexity and improves scalability."
    else:
        risk_analysis["Operational Risk"] = "Operational requirements are moderate."

    # -----------------------------
    # 4️⃣ Funding Risk
    # -----------------------------
    if scores["Funding Attractiveness"] >= 17:
        risk_analysis["Funding Risk"] = "Industry trends suggest strong investor interest."
    else:
        risk_analysis["Funding Risk"] = "Funding may require strong traction and differentiation."

    return risk_analysis



import random
import numpy as np


def simulate_survival(total_score, years=5, simulations=500):

    # Convert total score into base probability (normalize)
    base_probability = min(0.9, total_score / 160)

    yearly_survival_rates = []

    for year in range(years):
        survival_count = 0

        for _ in range(simulations):
            shock = random.uniform(-0.08, 0.08)
            adjusted_prob = max(0, min(1, base_probability + shock))

            if random.random() < adjusted_prob:
                survival_count += 1

        yearly_survival = survival_count / simulations
        yearly_survival_rates.append(yearly_survival)

        # small decay over time (realistic startup attrition)
        base_probability *= 0.92

    return yearly_survival_rates



def get_competitor_insights(extracted):

    industry = extracted["industry"]

    COMPETITOR_DATA = {
        "FinTech": ["Stripe", "PayPal", "Razorpay"],
        "EdTech": ["Coursera", "Udemy", "Byju's"],
        "HealthTech": ["Practo", "Teladoc", "Zocdoc"],
        "AI": ["OpenAI", "Anthropic", "Cohere"],
        "E-commerce": ["Amazon", "Shopify", "Flipkart"],
        "Food & Beverage": ["Zomato", "Swiggy", "Uber Eats"],
        "Web3": ["Ethereum", "Solana", "Polygon"],
        "ClimateTech": ["Tesla Energy", "Climeworks", "NextEra Energy"],
        "Gaming": ["Epic Games", "Riot Games", "Valve"]
    }

    competitors = COMPETITOR_DATA.get(industry, ["No major dominant players identified"])

    # Determine market crowdedness level
    if industry in ["Food & Beverage", "E-commerce", "FinTech"]:
        crowdedness = "High"
        pressure_score = 18
    elif industry in ["AI", "HealthTech", "EdTech"]:
        crowdedness = "Medium"
        pressure_score = 14
    else:
        crowdedness = "Low"
        pressure_score = 10

    return {
        "competitors": competitors,
        "market_crowdedness": crowdedness,
        "competitive_pressure_score": pressure_score
    }