import json

# Load data
with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Simple, reliable image URLs - using Unsplash source URLs that always work
category_images = {
    "Ramen": "https://source.unsplash.com/400x300/?ramen,noodles",
    "Sushi": "https://source.unsplash.com/400x300/?sushi,japanese",
    "Okonomiyaki": "https://source.unsplash.com/400x300/?okonomiyaki,japanese+food",
    "Takoyaki": "https://source.unsplash.com/400x300/?takoyaki",
    "Kushikatsu": "https://source.unsplash.com/400x300/?kushikatsu,skewers",
    "Yakiniku": "https://source.unsplash.com/400x300/?yakiniku,bbq",
    "Tempura": "https://source.unsplash.com/400x300/?tempura",
    "Udon": "https://source.unsplash.com/400x300/?udon,noodles",
    "Soba": "https://source.unsplash.com/400x300/?soba,noodles",
    "Tonkatsu": "https://source.unsplash.com/400x300/?tonkatsu",
    "Seafood": "https://source.unsplash.com/400x300/?seafood",
    "Dessert": "https://source.unsplash.com/400x300/?dessert,japanese+dessert",
    "Izakaya": "https://source.unsplash.com/400x300/?izakaya,japanese+pub",
    "Kaiseki": "https://source.unsplash.com/400x300/?kaiseki",
    "Yakitori": "https://source.unsplash.com/400x300/?yakitori",
    "Oden": "https://source.unsplash.com/400x300/?oden",
    "Beef Cutlet": "https://source.unsplash.com/400x300/?beef,cutlet",
    "Italian": "https://source.unsplash.com/400x300/?italian,pasta",
    "Curry": "https://source.unsplash.com/400x300/?curry,japanese+curry",
    "Cafe": "https://source.unsplash.com/400x300/?cafe,coffee",
    "French/Japanese": "https://source.unsplash.com/400x300/?fine+dining",
    "Fusion": "https://source.unsplash.com/400x300/?fusion+food",
    "Vegan": "https://source.unsplash.com/400x300/?vegan",
    "Vegetarian": "https://source.unsplash.com/400x300/?vegetarian",
}

# Fallback for any category
default_image = "https://source.unsplash.com/400x300/?restaurant,japanese+food"

# Update all restaurants
for restaurant in restaurants:
    category = restaurant.get('category', '')
    restaurant['image_url'] = category_images.get(category, default_image)

# Save
with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"✓ Updated {len(restaurants)} restaurants with reliable images")