import json
import requests
import time
import os

# Load your Google API key (or set as env var)
GOOGLE_API_KEY = "AIzaSyAPcWxWwnUQ-JzAlIRsA5PgSsv-AVoCbuw"  # Replace with your actual key

# Load restaurant data
with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

print(f"🔍 Fetching verified websites from Google Places for {len(restaurants)} restaurants...")

updated_count = 0

for i, restaurant in enumerate(restaurants):
    name = restaurant.get('name', '')
    area = restaurant.get('area', '')
    
    print(f"\n[{i+1}/{len(restaurants)}] {name}")
    
    # Search Google Places
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {
        "query": f"{name} {area} Osaka Japan",
        "key": GOOGLE_API_KEY,
        "language": "en"
    }
    
    try:
        search_response = requests.get(search_url, params=search_params).json()
        
        if search_response.get("results"):
            place = search_response["results"][0]
            place_id = place.get("place_id")
            
            # Get detailed info including website
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "fields": "website,name",
                "key": GOOGLE_API_KEY
            }
            
            details_response = requests.get(details_url, params=details_params).json()
            
            if details_response.get("result"):
                website = details_response["result"].get("website")
                
                if website:
                    old_website = restaurant.get('website', 'N/A')
                    restaurant['website'] = website
                    restaurant['website_verified'] = True
                    restaurant['website_source'] = 'Google Places API'
                    
                    if old_website != website:
                        print(f"  ✅ Updated: {old_website} → {website}")
                        updated_count += 1
                    else:
                        print(f"  ✓ Already correct: {website}")
                else:
                    print(f"  ⚠️  No website found on Google")
            else:
                print(f"  ❌ No place details found")
        else:
            print(f"  ❌ Restaurant not found on Google")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Small delay to avoid rate limiting
    time.sleep(0.2)

# Save updated data
with open('osaka_restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"✅ UPDATED {updated_count} restaurants with verified websites!")
print(f"💡 Push to GitHub to update the live app")
print(f"{'='*60}")