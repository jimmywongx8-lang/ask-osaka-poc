# Add these helper functions at the top of expand_data.py
import random

def generate_phone():
    """Generate realistic Osaka phone number"""
    return f"06-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

def generate_address(area):
    """Generate realistic Osaka address"""
    area_addresses = {
        "Dotonbori": f"1-{random.randint(1, 20)}-{random.randint(1, 50)} Dotonbori, Chuo Ward",
        "Namba": f"5-{random.randint(1, 15)}-{random.randint(1, 30)} Namba, Chuo Ward",
        "Umeda": f"{random.randint(1, 10)}-{random.randint(1, 20)} Umeda, Kita Ward",
        "Shinsekai": f"1-{random.randint(1, 10)}-{random.randint(1, 30)} Ebisu-higashi, Naniwa Ward",
        "Yodoyabashi": f"4-{random.randint(1, 8)}-{random.randint(1, 20)} Imabashi, Chuo Ward",
    }
    return area_addresses.get(area, f"{random.randint(1, 10)}-{random.randint(1, 20)}-{random.randint(1, 50)} Osaka")

# In the restaurant generation loop, add:
restaurant = {
    "name": name,
    "category": cat,
    "area": area,
    "description": random.choice(descriptions_pool),
    "price_range": price,
    "highlights": random.sample(highlights_pool, k=2),
    "image_url": image_mapping.get(cat, "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400"),
    "phone": generate_phone(),
    "address": generate_address(area),
    "email": f"info@{name.lower().replace(' ', '')}.jp",
    "website": f"https://www.{name.lower().replace(' ', '')}.jp",
    "hours": f"{random.choice(['11:00', '12:00'])}-{random.choice(['21:00', '22:00', '23:00'])}",
    "closed": random.choice(["Monday", "Tuesday", "Wednesday", "Sunday", "None"])
}