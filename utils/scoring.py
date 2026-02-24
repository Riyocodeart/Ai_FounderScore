import random

def calculate_scores():
    scores = {
        "Market Potential": random.randint(10, 20),
        "Competition Density": random.randint(5, 20),
        "Scalability": random.randint(10, 20),
        "Funding Attractiveness": random.randint(5, 20),
        "Risk Level": random.randint(5, 20),
    }

    total_score = sum(scores.values())
    return scores, total_score