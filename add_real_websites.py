import json

with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Show first 20 restaurant names to see the pattern
print("Sample restaurant names in your database:")
for i, r in enumerate(restaurants[:20], 1):
    print(f"{i}. {r.get('name')}")

# Now let's update with better matching
real_websites = {
    "https://www.ippudo.com": ["ippudo"],
    "https://en.ichiran.com": ["ichiran"],
    "https://www.gindaco.com": ["gindaco"],
    "https://www.kanidoraku.co.jp": ["kani doraku", "kani douraku"],
    "https://www.kushikatsu-daruma.com": ["daruma", "kushikatsu daruma"],
    "https://www.okonomiyaki-mizuno.com": ["mizuno"],
    "https://www.chibo.co.jp": ["chibo"],
    "https://www.torikizoku.co.jp": ["torikizoku", "tori kizoku"],
    "https://www.hanamaru-u.co.jp": ["hanamaru"],
}

updated = 0
for restaurant in restaurants:
    name = restaurant.get('name', '').lower()
    
    for url, keywords in real_websites.items():
        for keyword in keywords:
            if keyword in name:
                restaurant['website'] = url
                updated += 1
                print(f"✓ Updated: {restaurant.get('name')} → {url}")
                break

with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"\n✅ Updated {updated} restaurants with real websites!")