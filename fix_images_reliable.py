import json

with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Map categories to keywords for LoremFlickr (very reliable)
category_keywords = {
    "Ramen": "ramen",
    "Sushi": "sushi",
    "Okonomiyaki": "okonomiyaki",
    "Takoyaki": "takoyaki",
    "Kushikatsu": "skewers",
    "Yakiniku": "bbq",
    "Tempura": "tempura",
    "Udon": "udon",
    "Soba": "soba",
    "Tonkatsu": "pork",
    "Seafood": "seafood",
    "Dessert": "dessert",
    "Izakaya": "izakaya",
    "Kaiseki": "japanese",
    "Yakitori": "yakitori",
    "Oden": "oden",
    "Beef Cutlet": "beef",
    "Italian": "pasta",
    "Curry": "curry",
    "Cafe": "coffee",
}

import random
# Add random lock to prevent same image for same category
for i, restaurant in enumerate(restaurants):
    category = restaurant.get('category', 'Restaurant')
    keyword = category_keywords.get(category, "restaurant")
    # Add random number to get different images for same category
    random_num = random.randint(1, 1000)
    restaurant['image_url'] = f"https://loremflickr.com/400/300/{keyword}?lock={random_num}"

with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"✓ Updated {len(restaurants)} restaurants with LoremFlickr images")
print("✓ These images are very reliable and category-specific!")