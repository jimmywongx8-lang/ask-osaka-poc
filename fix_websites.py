import json

with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Mapping of fake URLs to real URLs
url_corrections = {
    "https://www.ippudoramen.jp": "https://www.ippudo.com",
    "https://www.ramenippudo.jp": "https://www.ippudo.com",
    "https://www.kushikatsudaruma.jp": "https://www.kushikatsu-daruma.com",
    "https://www.okonomiyakimizuno.jp": "https://www.okonomiyaki-mizuno.com",
    "https://www.okonomiyakichibo.jp": "https://www.chibo.co.jp",
    "https://www.kanidoraku.jp": "https://www.kanidoraku.co.jp",
    "https://www.gindacotakoyaki.jp": "https://www.gindaco.com",
}

# Real URLs for chains we haven't captured yet
chain_real_urls = {
    "ippudo": "https://www.ippudo.com",
    "ichiran": "https://en.ichiran.com",
    "gindaco": "https://www.gindaco.com",
    "daruma": "https://www.kushikatsu-daruma.com",
    "kani doraku": "https://www.kanidoraku.co.jp",
    "mizuno": "https://www.okonomiyaki-mizuno.com",
    "chibo": "https://www.chibo.co.jp",
    "torikizoku": "https://www.torikizoku.co.jp",
    "hanamaru": "https://www.hanamaru-u.co.jp",
    "marugame": "https://www.marugame-seimen.com",
    "sushi zanmai": "https://www.kiyomura.co.jp",
}

updated = 0

for r in restaurants:
    current_url = r.get('website', '')
    name = r.get('name', '').lower()
    
    # First, check if it's a known fake URL
    if current_url in url_corrections:
        new_url = url_corrections[current_url]
        r['website'] = new_url
        updated += 1
        print(f"✓ {r.get('name')}: {current_url} → {new_url}")
        continue
    
    # If URL doesn't look real, try to find the correct one
    if current_url.endswith('.jp') and not any(real in current_url for real in ['.co.jp', '.or.jp', '.ne.jp']):
        # It's likely a fake auto-generated URL
        for chain, real_url in chain_real_urls.items():
            if chain in name:
                r['website'] = real_url
                updated += 1
                print(f"✓ {r.get('name')}: {current_url} → {real_url}")
                break

# Save
with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"\n✅ Updated {updated} restaurants with real websites!")
print("💡 Restart Streamlit to see changes: python -m streamlit run app_enhanced.py")