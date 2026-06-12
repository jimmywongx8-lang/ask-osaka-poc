import json

# Load existing data
with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Add image URLs (using Unsplash for demo)
image_mapping = {
    "Ramen": "https://images.unsplash.com/photo-1557872943-16a5ac26437e?w=400",
    "Sushi": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400",
    "Okonomiyaki": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400",
    "Takoyaki": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400",
    "Kushikatsu": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400",
    "Yakiniku": "https://images.unsplash.com/photo-1555939561126-855b8675edd7?w=400",
    "Tempura": "https://images.unsplash.com/photo-1601046309494-2e5f4b4d4c0e?w=400",
    "Udon": "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=400",
    "Soba": "https://images.unsplash.com/photo-1552611052-33e04178183c?w=400",
    "Tonkatsu": "https://images.unsplash.com/photo-1603073477944-39d4b1c2d866?w=400",
    "Seafood": "https://images.unsplash.com/photo-1534939561126-7627a7a7ecdd?w=400",
    "Dessert": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400",
    "Izakaya": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400",
    "Kaiseki": "https://images.unsplash.com/photo-1582878929476-f5c4f1e5e4d7?w=400",
    "Yakitori": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400",
    "Oden": "https://images.unsplash.com/photo-1541544537156-7627a7a4aa1c?w=400",
    "Beef Cutlet": "https://images.unsplash.com/photo-1603073477944-39d4b1c2d866?w=400",
    "French/Japanese": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400",
    "Fusion": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400",
}

# Add image_url to each restaurant
for restaurant in restaurants:
    category = restaurant.get('category', '')
    restaurant['image_url'] = image_mapping.get(category, "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400")

# Save updated data
with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"✓ Added images to {len(restaurants)} restaurants")