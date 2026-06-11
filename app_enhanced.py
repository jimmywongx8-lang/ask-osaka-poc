import streamlit as st
import json
import os
from groq import Groq
import folium
from streamlit_folium import st_folium
import requests
import time
import csv
from datetime import datetime

# Initialize session state for favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Page config - Mobile-optimized
st.set_page_config(page_title="Ask Osaka AI Concierge", page_icon="🏯")

# Mobile-responsive CSS
st.markdown("""
<style>
/* Fix horizontal scrolling on mobile */
.main .block-container {
    max-width: 100% !important;
    padding-top: 2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Stack columns on mobile */
@media (max-width: 768px) {
    div[data-testid="column"] {
        width: 100% !important;
        flex-basis: 100% !important;
    }
    
    /* Make images fill card width */
    .element-container img {
        width: 100% !important;
        height: auto !important;
        border-radius: 8px;
    }
    
    /* Adjust map for mobile */
    iframe[title="streamlit_folium.st_folium"] {
        width: 100% !important;
        height: 250px !important;
    }
    
    /* Sidebar takes 85% width on mobile */
    section[data-testid="stSidebar"] {
        width: 85% !important;
    }
    
    /* Make text smaller on mobile */
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.1rem !important; }
}

/* Desktop optimizations */
@media (min-width: 769px) {
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
}

/* Google badge styling */
.google-badge {
    background: linear-gradient(135deg, #4285F4, #34A853, #FBBC05, #EA4335);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    display: inline-block;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# Function to save feedback
def save_feedback(restaurant_name, issue_type, description):
    """Save user feedback to CSV"""
    file_exists = os.path.isfile('user_feedback.csv')
    with open('user_feedback.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'restaurant', 'issue_type', 'description'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'restaurant': restaurant_name,
            'issue_type': issue_type,
            'description': description
        })

# Google Places API Functions
def get_google_places_data(restaurant_name, area):
    """Fetch live data from Google Places API"""
    
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_PLACES_API_KEY", os.getenv("GOOGLE_PLACES_API_KEY", ""))
    
    if not GOOGLE_API_KEY:
        return None
    
    try:
        # Search for the place
        search_query = f"{restaurant_name} {area} Osaka Japan"
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            "query": search_query,
            "key": GOOGLE_API_KEY,
            "language": "en"
        }
        
        search_response = requests.get(search_url, params=search_params, timeout=5).json()
        
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
        
        details_response = requests.get(details_url, params=details_params, timeout=5).json()
        
        if details_response.get("result"):
            result = details_response["result"]
            
            # Get photo URL if available
            photo_url = None
            if result.get("photos"):
                photo_reference = result["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
            
            return {
                "rating": result.get("rating"),
                "total_ratings": result.get("user_ratings_total", 0),
                "open_now": result.get("opening_hours", {}).get("open_now", False),
                "website": result.get("website", ""),
                "phone": result.get("international_phone_number", ""),
                "address": result.get("formatted_address", ""),
                "price_level": result.get("price_level", 0),
                "photo_url": photo_url
            }
    
    except Exception as e:
        print(f"Google Places API Error: {e}")
    
    return None

# Cache Google Places data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_google_data(restaurant_name, area):
    """Cached version of Google Places lookup"""
    return get_google_places_data(restaurant_name, area)

# App Header
st.title("🏯 Ask Osaka")
st.caption("Your AI local guide. Ask about food, events, transit, or hidden gems.")

# Load restaurant data
@st.cache_data(ttl=300)
def load_osaka_data():
    try:
        with open("osaka_restaurants.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

osaka_data = load_osaka_data()

# Sidebar controls
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Search restaurants...", placeholder="e.g., ramen, namba, cheap")

all_areas = sorted(list(set(r.get('area', 'Unknown') for r in osaka_data)))
all_categories = sorted(list(set(r.get('category', 'Unknown') for r in osaka_data)))
all_prices = sorted(list(set(r.get('price_range', 'Unknown') for r in osaka_data)))

selected_areas = st.sidebar.multiselect("Area", all_areas, default=[])
selected_categories = st.sidebar.multiselect("Cuisine Type", all_categories, default=[])
selected_prices = st.sidebar.multiselect("Price Range", all_prices, default=[])

# Advanced filtering + search
def filter_data(data):
    filtered = data.copy()
    if selected_areas:
        filtered = [r for r in filtered if r.get('area') in selected_areas]
    if selected_categories:
        filtered = [r for r in filtered if r.get('category') in selected_categories]
    if selected_prices:
        filtered = [r for r in filtered if r.get('price_range') in selected_prices]
    if search_query:
        query = search_query.lower()
        filtered = [r for r in filtered if any(query in str(v).lower() for v in r.values())]
    return filtered

filtered_data = filter_data(osaka_data)
st.sidebar.success(f"Showing {len(filtered_data)} of {len(osaka_data)} restaurants")

# Sidebar - Favorites Section
st.sidebar.markdown("---")
st.sidebar.header("⭐ My Favorites")

if st.session_state.favorites:
    st.sidebar.success(f"{len(st.session_state.favorites)} saved")
    
    # Show favorite restaurant names
    for fav_name in st.session_state.favorites[:5]:  # Show first 5
        st.sidebar.markdown(f"• {fav_name}")
    
    if len(st.session_state.favorites) > 5:
        st.sidebar.markdown(f"...and {len(st.session_state.favorites) - 5} more")
    
    if st.sidebar.button("Clear Favorites"):
        st.session_state.favorites = []
        st.rerun()
else:
    st.sidebar.info("Click ❤️ on restaurants to save them")

st.sidebar.markdown("---")

# Pagination
items_per_page = 12
page = st.sidebar.number_input("Page", min_value=1, max_value=max(1, (len(filtered_data) + items_per_page - 1) // items_per_page), value=1)
start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_data = filtered_data[start_idx:end_idx]

# Map
st.sidebar.header("🗺️ Map View")
show_map = st.sidebar.checkbox("Show Restaurant Map", value=False)

if show_map and filtered_data:
    st.subheader("📍 Restaurant Locations")
    m = folium.Map(location=[34.6937, 135.5023], zoom_start=13, tiles="CartoDB positron")
    
    area_coords = {
        "Dotonbori": [34.6686, 135.5023], "Namba": [34.6660, 135.5000],
        "Umeda": [34.7024, 135.4959], "Shinsekai": [34.6520, 135.5060],
        "Yodoyabashi": [34.6880, 135.5050], "Tennouji": [34.6456, 135.5066],
        "Shinsaibashi": [34.6720, 135.5020], "Kuromon Market": [34.6660, 135.5080],
        "Kitashinchi": [34.6970, 135.4980], "Tsuruhashi": [34.6650, 135.5300],
        "Tennoji": [34.6456, 135.5066], "Nakazakicho": [34.6850, 135.5100],
        "Americamura": [34.6730, 135.5010], "Honmachi": [34.6850, 135.4950],
        "Kyobashi": [34.6980, 135.5350], "Imamiya": [34.6400, 135.5050],
        "Sumiyoshi": [34.6100, 135.4900], "Abeno": [34.6300, 135.5000]
    }
    
    map_data = filtered_data[:50]
    for restaurant in map_data:
        area = restaurant.get('area', 'Dotonbori')
        coords = area_coords.get(area, [34.6937, 135.5023])
        
        popup_html = f"""
        <div style="width: 220px; padding: 8px; font-family: Arial;">
            <b style="font-size: 14px;">{restaurant.get('name', 'N/A')}</b><br>
            🍴 {restaurant.get('category', 'N/A')}<br>
            💰 {restaurant.get('price_range', 'N/A')}<br>
            📞 {restaurant.get('phone', 'N/A')}<br>
            📮 {restaurant.get('address', 'Address N/A')}<br>
            🕐 {restaurant.get('hours', 'Hours N/A')}
        </div>
        """
        
        folium.Marker(
            coords, 
            popup=folium.Popup(popup_html, max_width=300), 
            tooltip=restaurant.get('name')
        ).add_to(m)
    
    st_folium(m, width=700, height=500, use_container_width=True)

# Display current page
if page_data:
    st.subheader(f"🍽️ Restaurants (Page {page})")
    cols = st.columns(3)
    for idx, restaurant in enumerate(page_data):
        with cols[idx % 3]:
            with st.container():
                # Display image with error handling
                image_url = restaurant.get('image_url', '')
                
                if image_url:
                    try:
                        st.image(image_url, use_container_width=True)
                    except:
                        st.image("https://loremflickr.com/400/300/japanese?lock=9999", 
                                use_container_width=True, caption="Restaurant")
                else:
                    st.image("https://loremflickr.com/400/300/japanese?lock=9999", 
                            use_container_width=True, caption="Restaurant")
                
                st.markdown(f"### {restaurant.get('name')}")
                st.markdown(f"**📍 {restaurant.get('area')}**")
                st.markdown(f"**🍴 {restaurant.get('category')}**")
                st.markdown(f"**💰 {restaurant.get('price_range')}**")
                
                # Contact Information
                st.markdown("---")
                if restaurant.get('address'):
                    st.markdown(f"📮 {restaurant.get('address')}")
                if restaurant.get('phone'):
                    st.markdown(f"📞 {restaurant.get('phone')}")
                if restaurant.get('hours'):
                    closed = restaurant.get('closed', 'None')
                    st.markdown(f"🕐 {restaurant.get('hours')} (Closed: {closed})")
                
                st.markdown("---")
                st.markdown(f"*{restaurant.get('description')}*")
                
                highlights = restaurant.get('highlights', [])
                if isinstance(highlights, list):
                    st.markdown(f"⭐ {', '.join(highlights)}")
                else:
                    st.markdown(f"⭐ {highlights}")
                
                # Website link
                website = restaurant.get('website', '')
                if website and website.startswith('http'):
                    st.markdown(f"[🌐 Website]({website})")
                
                # Action Buttons Row
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Favorite Button
                    rest_name = restaurant.get('name', '')
                    is_favorite = rest_name in st.session_state.favorites
                    
                    if st.button("❤️" if is_favorite else "🤍", 
                                key=f"fav_{idx}",
                                help="Save to favorites"):
                        if is_favorite:
                            st.session_state.favorites.remove(rest_name)
                            st.toast(f"Removed {rest_name} from favorites")
                        else:
                            st.session_state.favorites.append(rest_name)
                            st.toast(f"Saved {rest_name} to favorites!")
                        st.rerun()
                
                with col2:
                    # Share Button
                    if st.button("📤", key=f"share_{idx}", help="Share restaurant"):
                        share_text = f"Check out {rest_name} in {restaurant.get('area', 'Osaka')}!\n{restaurant.get('category')} • {restaurant.get('price_range')}\n📍 {restaurant.get('address', '')}\n📞 {restaurant.get('phone', '')}"
                        st.code(share_text, language=None)
                        st.success("Copy the text above to share!")
                
                with col3:
                    # Report Issue Button
                    if st.button("🚩", key=f"report_{idx}", help="Report incorrect info"):
                        st.session_state[f"show_report_{idx}"] = True
                
                # Report Form (shows when triggered)
                if st.session_state.get(f"show_report_{idx}"):
                    with st.form(f"report_form_{idx}"):
                        st.markdown("**Report Issue for:** " + rest_name)
                        issue_type = st.selectbox("What's wrong?", 
                                                  ["Wrong hours", "Wrong phone", "Wrong address", 
                                                   "Restaurant closed", "Wrong website", "Other"])
                        description = st.text_area("Details (optional)")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            submitted = st.form_submit_button("Submit")
                        with col_b:
                            cancel = st.form_submit_button("Cancel")
                        
                        if submitted:
                            save_feedback(rest_name, issue_type, description)
                            st.success("✅ Thanks for the feedback!")
                            st.session_state[f"show_report_{idx}"] = False
                            st.rerun()
                        elif cancel:
                            st.session_state[f"show_report_{idx}"] = False
                            st.rerun()
                
                # Google Places Live Data Button
                if st.button("🔍 Google Info", key=f"google_{idx}", type="secondary", use_container_width=True):
                    with st.spinner("Fetching live data..."):
                        google_data = get_cached_google_data(restaurant.get('name'), restaurant.get('area'))
                        
                        if google_data:
                            st.success("✅ Live from Google!")
                            
                            if google_data.get('rating'):
                                stars = "⭐" * int(google_data['rating'])
                                st.markdown(f"<div class='google-badge'>Google: {stars} {google_data['rating']}/5 ({google_data['total_ratings']} reviews)</div>", unsafe_allow_html=True)
                            
                            if google_data.get('open_now') is not None:
                                status = "🟢 Open Now" if google_data['open_now'] else "🔴 Closed"
                                st.markdown(status)
                            
                            if google_data.get('photo_url'):
                                st.image(google_data['photo_url'], caption="Latest from Google", use_container_width=True)
                            
                            if google_data.get('website'):
                                st.markdown(f"[🔗 Official Website]({google_data['website']})")
                            
                            if google_data.get('phone'):
                                st.markdown(f"📞 {google_data['phone']}")
                            
                            if google_data.get('address'):
                                st.markdown(f"📍 {google_data['address']}")
                            
                            if google_data.get('price_level'):
                                price_symbols = "💰" * google_data['price_level']
                                st.markdown(f"Price: {price_symbols}")
                        else:
                            st.warning("⚠️ No Google data found")
                
                st.divider()

# AI Chat Section
st.divider()
st.subheader("💬 Ask for Recommendations")

context_items = filtered_data[:20] if filtered_data else osaka_data[:20]
context_text = "\n\n".join([
    f"Name: {r.get('name')}\nCategory: {r.get('category')}\nArea: {r.get('area')}\nPrice: {r.get('price_range')}\nDescription: {r.get('description')}\nHighlights: {r.get('highlights')}"
    for r in context_items
])

SYSTEM_PROMPT = f"""You are a friendly Osaka local guide with access to verified restaurant data.

Use ONLY these restaurants for recommendations:

{context_text}

When recommending, mention:
- Restaurant name and location
- Price range
- Special features or highlights
- Practical tips (hours, reservations, etc.)

If the user asks about something not in this list, politely say you only have information on the provided restaurants.
Keep responses concise and helpful. Use Osaka dialect occasionally (Maido!, Okini!).
"""

# API Keys
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Enter your Groq API Key", type="password", key="groq_key_input")
    if not GROQ_API_KEY:
        st.warning("⚠️ Please enter your Groq API Key to use the AI concierge")
        st.stop()

groq_client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Osaka restaurants, events, transit, or tips..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Checking local Osaka guide..."):
            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

if len(osaka_data) >= 50:
    st.sidebar.success(f"✅ Loaded {len(osaka_data)} Osaka items")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <b>Ask Osaka</b> - Your AI-powered Osaka restaurant guide<br>
    🍜 900+ verified restaurants • 🗺️ Interactive maps • 💬 AI recommendations
</div>
""", unsafe_allow_html=True)