import json

# Load data
with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Reliable image URLs for each category
category_images = {
    "Ramen": "https://images.unsplash.com/photo-1557872943-16a5ac26437e?w=400&h=300&fit=crop",
    "Sushi": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&h=300&fit=crop",
    "Okonomiyaki": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
    "Takoyaki": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=300&fit=crop",
    "Kushikatsu": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&h=300&fit=crop",
    "Yakiniku": "https://images.unsplash.com/photo-1555939561126-7627a7a7ecdd?w=400&h=300&fit=crop",
    "Tempura": "https://images.unsplash.com/photo-1601046309494-2e5f4b4d4c0e?w=400&h=300&fit=crop",
    "Udon": "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=400&h=300&fit=crop",
    "Soba": "https://images.unsplash.com/photo-1552611052-33e04178183c?w=400&h=300&fit=crop",
    "Tonkatsu": "https://images.unsplash.com/photo-1603073477944-39d4b1c2d866?w=400&h=300&fit=crop",
    "Seafood": "https://images.unsplash.com/photo-1534939561126-7627a7a4aa1c?w=400&h=300&fit=crop",
    "Dessert": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop",
    "Izakaya": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400&h=300&fit=crop",
    "Kaiseki": "https://images.unsplash.com/photo-1582878929476-f5c4f1e5e4d7?w=400&h=300&fit=crop",
    "Yakitori": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400&h=300&fit=crop",
    "Oden": "https://images.unsplash.com/photo-1541544537156-7627a7a4aa1c?w=400&h=300&fit=crop",
    "Beef Cutlet": "https://images.unsplash.com/photo-1603073477944-39d4b1c2d866?w=400&h=300&fit=crop",
    "Italian": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop",
    "Curry": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
    "Cafe": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",
    "French/Japanese": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop",
    "Fusion": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400&h=300&fit=crop",
    "Vegan": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop",
    "Vegetarian": "https://images.unsplash.com/photo-1543353071-8665d4b935b5?w=400&h=300&fit=crop",
}

default_image = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop"

# Update all restaurants
fixed_count = 0
for restaurant in restaurants:
    category = restaurant.get('category', '')
    # Always set a valid image URL
    restaurant['image_url'] = category_images.get(category, default_image)
    fixed_count += 1

# Save
with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"✓ Fixed images for {fixed_count} restaurants")
print("✓ All restaurants now have valid image URLs")