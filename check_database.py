import json

with open('osaka_restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

print("="*60)
print("DATABASE DIAGNOSTIC REPORT")
print("="*60)
print(f"Total restaurants: {len(restaurants)}\n")

# Check first 10 restaurants
print("SAMPLE RESTAURANTS (First 10):")
print("-" * 60)
for i, r in enumerate(restaurants[:10], 1):
    print(f"\n{i}. {r.get('name')}")
    print(f"   Category: {r.get('category')}")
    print(f"   Website: {r.get('website', 'N/A')}")
    print(f"   Image: {r.get('image_url', 'N/A')[:60]}...")
    print(f"   Phone: {r.get('phone', 'N/A')}")
    print(f"   Hours: {r.get('hours', 'N/A')}")

# Check for famous chains
print("\n" + "="*60)
print("SEARCHING FOR FAMOUS CHAINS:")
print("-" * 60)

famous_chains = ["ippudo", "ichiran", "gindaco", "daruma", "kani doraku", "mizuno", "chibo"]

for r in restaurants:
    name = r.get('name', '').lower()
    for chain in famous_chains:
        if chain in name:
            print(f"\n✓ Found: {r.get('name')}")
            print(f"  Current website: {r.get('website', 'N/A')}")
            print(f"  Current image: {r.get('image_url', 'N/A')[:50]}...")
            break

# Count issues
print("\n" + "="*60)
print("ISSUE COUNT:")
print("-" * 60)
no_website = sum(1 for r in restaurants if not r.get('website'))
fake_website = sum(1 for r in restaurants if r.get('website', '').startswith('http') and not any(x in r.get('website', '') for x in ['.com', '.jp', '.org']))
no_image = sum(1 for r in restaurants if not r.get('image_url'))
no_phone = sum(1 for r in restaurants if not r.get('phone'))

print(f"Restaurants without website: {no_website}")
print(f"Restaurants with fake website: {fake_website}")
print(f"Restaurants without image: {no_image}")
print(f"Restaurants without phone: {no_phone}")
print("="*60)