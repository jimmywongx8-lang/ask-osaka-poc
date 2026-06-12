import json

with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Map categories to keywords for Unsplash
category_keywords = {
    "Ramen": "japanese+ramen,noodles",
    "Sushi": "sushi,japanese+food",
    "Okonomiyaki": "okonomiyaki,pancake",
    "Takoyaki": "takoyaki,octopus",
    "Kushikatsu": "kushikatsu,fried+skewer",
    "Yakiniku": "yakiniku,korean+bbq,meat",
    "Tempura": "tempura,fried+shrimp",
    "Udon": "udon,noodles",
    "Soba": "soba,noodles",
    "Tonkatsu": "tonkatsu,fried+pork",
    "Seafood": "seafood,crab,sashimi",
    "Dessert": "mochi,japanese+dessert",
    "Izakaya": "izakaya,japanese+pub,drinks",
    "Kaiseki": "kaiseki,plated+food",
    "Yakitori": "yakitori,chicken+skewer",
    "Oden": "oden,hot+pot",
    "Beef Cutlet": "beef,steak",
    "Italian": "pasta,pizza",
    "Curry": "japanese+curry,rice",
    "Cafe": "coffee,cafe",
}

# Generate the new image URL for every restaurant
for restaurant in restaurants:
    category = restaurant.get('category', 'Restaurant')
    # Get the keyword for this category, default to "japanese+food"
    keyword = category_keywords.get(category, "japanese+food")
    
    # This URL dynamically serves a random photo matching the keyword
    # It prevents caching issues because it's a "featured" query
    restaurant['image_url'] = f"https://source.unsplash.com/featured/?{keyword}"

with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"✓ Updated {len(restaurants)} restaurants with keyword-based images")
print("✓ Ramen will now show Ramen, Sushi will show Sushi!")