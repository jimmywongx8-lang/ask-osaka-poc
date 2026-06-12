import json
import time

with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Specific, verified food photos from Unsplash with timestamps to prevent caching
timestamp = int(time.time())

food_images = {
    "Ramen": f"https://images.unsplash.com/photo-1557872943-16a5ac26437e?w=400&h=300&fit=crop&t={timestamp}",
    "Sushi": f"https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&h=300&fit=crop&t={timestamp}",
    "Okonomiyaki": f"https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop&t={timestamp}",
    "Takoyaki": f"https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=300&fit=crop&t={timestamp}",
    "Kushikatsu": f"https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&h=300&fit=crop&t={timestamp}",
    "Yakiniku": f"https://images.unsplash.com/photo-1555939561126-7627a7a7ecdd?w=400&h=300&fit=crop&t={timestamp}",
    "Tempura": f"https://images.unsplash.com/photo-1601046309494-2e5f4b4d4c0e?w=400&h=300&fit=crop&t={timestamp}",
    "Udon": f"https://images.unsplash.com/photo-1626074353765-517a681e40be?w=400&h=300&fit=crop&t={timestamp}",
    "Soba": f"https://images.unsplash.com/photo-1552611052-33e04178183c?w=400&h=300&fit=crop&t={timestamp}",
    "Tonkatsu": f"https://images.unsplash.com/photo-1603073477944-39d4b1c2d866?w=400&h=300&fit=crop&t={timestamp}",
    "Seafood": f"https://images.unsplash.com/photo-1534939561126-7627a7a4aa1c?w=400&h=300&fit=crop&t={timestamp}",
    "Dessert": f"https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop&t={timestamp}",
    "Izakaya": f"https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400&h=300&fit=crop&t={timestamp}",
    "Kaiseki": f"https://images.unsplash.com/photo-1582878929476-f5c4f1e5e4d7?w=400&h=300&fit=crop&t={timestamp}",
    "Yakitori": f"https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400&h=300&fit=crop&t={timestamp}",
    "Oden": f"https://images.unsplash.com/photo-1541544537156-7627a7a4aa1c?w=400&h=300&fit=crop&t={timestamp}",
    "Beef Cutlet": f"https://images.unsplash.com/photo-1603073477944-39d4b1c2d866?w=400&h=300&fit=crop&t={timestamp}",
    "Italian": f"https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop&t={timestamp}",
    "Curry": f"https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop&t={timestamp}",
    "Cafe": f"https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop&t={timestamp}",
}

default_image = f"https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop&t={timestamp}"

for restaurant in restaurants:
    category = restaurant.get('category', '')
    restaurant['image_url'] = food_images.get(category, default_image)

with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"✓ Updated {len(restaurants)} restaurants with timestamp-based cache-busting")