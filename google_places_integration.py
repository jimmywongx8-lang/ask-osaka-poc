import requests
import os

def get_place_details(restaurant_name, area):
    """
    Fetch live data from Google Places API
    Returns: rating, total_ratings, current_status, photos, website
    """
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
    
    # Search for the place
    search_query = f"{restaurant_name} {area} Osaka Japan"
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {
        "query": search_query,
        "key": GOOGLE_API_KEY,
        "language": "en"
    }
    
    try:
        search_response = requests.get(search_url, params=search_params).json()
        
        if not search_response.get("results"):
            return None
        
        place = search_response["results"][0]
        place_id = place.get("place_id")
        
        # Get detailed info
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            "place_id": place_id,
            "fields": "rating,user_ratings_total,opening_hours,current_opening_hours,photos,website,international_phone_number,formatted_address,price_level",
            "key": GOOGLE_API_KEY
        }
        
        details_response = requests.get(details_url, params=details_params).json()
        
        if details_response.get("result"):
            result = details_response["result"]
            
            # Get photo reference if available
            photo_url = None
            if result.get("photos"):
                photo_reference = result["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
            
            return {
                "rating": result.get("rating", "N/A"),
                "total_ratings": result.get("user_ratings_total", 0),
                "current_status": "Open Now" if result.get("opening_hours", {}).get("open_now") else "Closed",
                "website": result.get("website", ""),
                "phone": result.get("international_phone_number", ""),
                "address": result.get("formatted_address", ""),
                "price_level": result.get("price_level", 0),  # 1-4 ($ to $$$$)
                "google_photo": photo_url
            }
    
    except Exception as e:
        print(f"Error fetching place details: {e}")
    
    return None