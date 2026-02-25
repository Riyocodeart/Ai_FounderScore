def generate_strategic_recommendations(extracted, scores):

    industry = extracted["industry"]
    business_model = extracted["business_model"]

    strengths = []
    weaknesses = []
    recommendations = []

    # -------------------------
    # Strength Logic
    # -------------------------

    if scores["Innovation Score"] >= 18:
        strengths.append("Highly innovative positioning within the industry.")

    if scores["Scalability"] >= 18:
        strengths.append("Strong scalability potential due to business model.")

    if scores["Funding Attractiveness"] >= 17:
        strengths.append("High investor interest potential in this sector.")

    # -------------------------
    # Weakness Logic
    # -------------------------

    if scores["Competition Density"] >= 16:
        weaknesses.append("High competitive pressure may increase CAC.")

    if scores["Market Saturation"] >= 16:
        weaknesses.append("Market appears saturated; differentiation is critical.")

    if scores["Execution Complexity"] >= 17:
        weaknesses.append("Operational complexity could slow early growth.")

    # -------------------------
    # Recommendations Logic
    # -------------------------

    if business_model == "SaaS":
        recommendations.append("Focus on reducing churn and optimizing recurring revenue.")
        recommendations.append("Invest early in product-led growth strategies.")

    if scores["Competition Density"] >= 16:
        recommendations.append("Build a strong niche positioning strategy.")

    if industry in ["AI", "FinTech", "Web3"]:
        recommendations.append("Leverage innovation narrative for fundraising advantage.")

    if scores["Risk Level"] >= 15:
        recommendations.append("Start with a lean MVP to minimize early-stage burn.")

    # fallback if empty
    if not strengths:
        strengths.append("Balanced startup structure with moderate risk exposure.")

    if not weaknesses:
        weaknesses.append("No major structural weaknesses detected at early stage.")

    if not recommendations:
        recommendations.append("Focus on customer validation and traction building.")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }