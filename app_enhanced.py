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

# Initialize session state
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Page config
st.set_page_config(page_title="Ask Osaka - AI Restaurant Guide", page_icon="🏯", layout="wide")

# Clean Modern CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Main container */
.main .block-container {
    max-width: 1200px !important;
    padding: 2rem !important;
    background: #f8f9fa !important;
}

/* Header */
.main h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem !important;
}

/* Restaurant Cards */
div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]) {
    background: white !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    margin-bottom: 1.5rem !important;
}

div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]):hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
}

/* Images */
[data-testid="stImage"] img {
    border-radius: 0 !important;
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
}

/* Card content padding */
.element-container:has(+ div[data-testid="stMarkdown"]:has(h3)) {
    padding: 1rem !important;
}

/* Buttons - Clean Icon Style */
.stButton > button {
    background: transparent !important;
    border: 2px solid #e2e8f0 !important;
    color: #4a5568 !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.8rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    min-width: 40px !important;
}

.stButton > button:hover {
    border-color: #667eea !important;
    color: #667eea !important;
    background: rgba(102, 126, 234, 0.05) !important;
}

/* Google Info Button - Accent Style */
.stButton > button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    width: 100% !important;
    padding: 0.6rem !important;
}

.stButton > button[data-testid="baseButton-secondary"]:hover {
    opacity: 0.9 !important;
    transform: none !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e2e8f0 !important;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stMultiselect"] select {
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 0.5rem !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stMultiselect"] select:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1) !important;
}

/* Google Badge */
.google-badge {
    background: linear-gradient(135deg, #4285F4, #34A853, #FBBC05, #EA4335) !important;
    color: white !important;
    padding: 4px 10px !important;
    border-radius: 16px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    display: inline-block !important;
    margin: 6px 0 !important;
}

/* Chat */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    background: white !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}

/* Mobile */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
    }
    .main h1 {
        font-size: 1.8rem !important;
    }
    [data-testid="stImage"] img {
        height: 150px !important;
    }
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

[data-testid="stVerticalBlock"] > div {
    animation: fadeIn 0.4s ease-out;
}
</style>
""", unsafe_allow_html=True)

# Function to save feedback
def save_feedback(restaurant_name, issue_type, description):
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

# Google Places API
def get_google_places_data(restaurant_name, area):
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_PLACES_API_KEY", os.getenv("GOOGLE_PLACES_API_KEY", ""))
    if not GOOGLE_API_KEY:
        return None
    
    try:
        search_query = f"{restaurant_name} {area} Osaka Japan"
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {"query": search_query, "key": GOOGLE_API_KEY, "language": "en"}
        search_response = requests.get(search_url, params=search_params, timeout=5).json()
        
        if not search_response.get("results"):
            return None
        
        place = search_response["results"][0]
        place_id = place.get("place_id")
        
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            "place_id": place_id,
            "fields": "rating,user_ratings_total,opening_hours,current_opening_hours,photos,website,international_phone_number,formatted_address,price_level",
            "key": GOOGLE_API_KEY
        }
        details_response = requests.get(details_url, params=details_params, timeout=5).json()
        
        if details_response.get("result"):
            result = details_response["result"]
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

@st.cache_data(ttl=3600)
def get_cached_google_data(restaurant_name, area):
    return get_google_places_data(restaurant_name, area)

# Hero Section
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏯 Ask Osaka")
    st.caption("Your AI-powered guide to Osaka's best restaurants • 900+ verified spots")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2331/2331966.png", width=80)

# Load data
@st.cache_data(ttl=300)
def load_osaka_data():
    try:
        with open("osaka_restaurants.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

osaka_data = load_osaka_data()

# Sidebar
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Search restaurants...", placeholder="e.g., ramen, namba, cheap")

all_areas = sorted(list(set(r.get('area', 'Unknown') for r in osaka_data)))
all_categories = sorted(list(set(r.get('category', 'Unknown') for r in osaka_data)))
all_prices = sorted(list(set(r.get('price_range', 'Unknown') for r in osaka_data)))

selected_areas = st.sidebar.multiselect("Area", all_areas, default=[])
selected_categories = st.sidebar.multiselect("Cuisine Type", all_categories, default=[])
selected_prices = st.sidebar.multiselect("Price Range", all_prices, default=[])

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

# Favorites in sidebar
st.sidebar.markdown("---")
st.sidebar.header("⭐ My Favorites")
if st.session_state.favorites:
    st.sidebar.success(f"{len(st.session_state.favorites)} saved")
    for fav_name in st.session_state.favorites[:5]:
        st.sidebar.markdown(f"• {fav_name}")
    if st.sidebar.button("Clear Favorites", key="clear_fav"):
        st.session_state.favorites = []
        st.rerun()
else:
    st.sidebar.info("Click ❤️ to save favorites")

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
            📞 {restaurant.get('phone', 'N/A')}
        </div>
        """
        folium.Marker(coords, popup=folium.Popup(popup_html, max_width=300), tooltip=restaurant.get('name')).add_to(m)
    st_folium(m, width=700, height=500, use_container_width=True)

# Display restaurants
if page_data:
    st.subheader(f"️ Restaurants (Page {page})")
    cols = st.columns(3)
    for idx, restaurant in enumerate(page_data):
        with cols[idx % 3]:
            with st.container():
                # Image
                image_url = restaurant.get('image_url', '')
                if image_url:
                    try:
                        st.image(image_url, use_container_width=True)
                    except:
                        st.image("https://loremflickr.com/400/300/japanese?lock=9999", use_container_width=True)
                else:
                    st.image("https://loremflickr.com/400/300/japanese?lock=9999", use_container_width=True)
                
                # Info
                st.markdown(f"### {restaurant.get('name')}")
                st.markdown(f"**📍 {restaurant.get('area')}** | **🍴 {restaurant.get('category')}** | **💰 {restaurant.get('price_range')}**")
                
                st.markdown("---")
                if restaurant.get('address'):
                    st.markdown(f"📮 {restaurant.get('address')}")
                if restaurant.get('phone'):
                    st.markdown(f"📞 {restaurant.get('phone')}")
                if restaurant.get('hours'):
                    st.markdown(f" {restaurant.get('hours')} (Closed: {restaurant.get('closed', 'None')})")
                
                st.markdown("---")
                if restaurant.get('description'):
                    st.markdown(f"*{restaurant.get('description')}*")
                
                highlights = restaurant.get('highlights', [])
                if isinstance(highlights, list):
                    for h in highlights[:2]:
                        st.markdown(f"⭐ {h}")
                
                # Website
                website = restaurant.get('website', '')
                if website and website.startswith('http'):
                    st.markdown(f"[🌐 Website]({website})")
                
                # Action buttons - Clean layout
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                rest_name = restaurant.get('name', '')
                
                with col1:
                    is_fav = rest_name in st.session_state.favorites
                    if st.button("❤️" if is_fav else "🤍", key=f"fav_{idx}", help="Favorite"):
                        if is_fav:
                            st.session_state.favorites.remove(rest_name)
                        else:
                            st.session_state.favorites.append(rest_name)
                        st.rerun()
                
                with col2:
                    if st.button("", key=f"share_{idx}", help="Share"):
                        st.code(f"{rest_name}\n{restaurant.get('address')}\n{restaurant.get('phone')}")
                
                with col3:
                    if st.button("🚩", key=f"report_{idx}", help="Report"):
                        st.session_state[f"show_report_{idx}"] = not st.session_state.get(f"show_report_{idx}", False)
                        st.rerun()
                
                # Report form - Inline
                if st.session_state.get(f"show_report_{idx}"):
                    with st.form(f"report_form_{idx}"):
                        st.markdown("**Report Issue**")
                        issue = st.selectbox("What's wrong?", ["Wrong hours", "Wrong phone", "Closed", "Other"])
                        desc = st.text_area("Details", placeholder="Optional")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            submitted = st.form_submit_button("Submit")
                        with col_b:
                            cancel = st.form_submit_button("Cancel")
                        
                        if submitted:
                            save_feedback(rest_name, issue, desc)
                            st.success("Thanks!")
                            st.session_state[f"show_report_{idx}"] = False
                            st.rerun()
                        if cancel:
                            st.session_state[f"show_report_{idx}"] = False
                            st.rerun()
                
                # Google Info Button
                if st.button("🔍 Show Live Google Info", key=f"google_{idx}", type="secondary", use_container_width=True):
                    with st.spinner("Loading..."):
                        gdata = get_cached_google_data(rest_name, restaurant.get('area'))
                        if gdata:
                            if gdata.get('rating'):
                                st.markdown(f"<div class='google-badge'>⭐ {gdata['rating']}/5 ({gdata['total_ratings']} reviews)</div>", unsafe_allow_html=True)
                            st.markdown("🟢 Open Now" if gdata.get('open_now') else "🔴 Closed")
                            if gdata.get('photo_url'):
                                st.image(gdata['photo_url'], use_container_width=True)
                        else:
                            st.warning("No data found")
                
                st.markdown("</div>", unsafe_allow_html=True)

# AI Chat
st.markdown("---")
st.subheader("💬 Ask AI for Recommendations")

context_items = filtered_data[:20] if filtered_data else osaka_data[:20]
context_text = "\n".join([f"{r.get('name')}: {r.get('category')} in {r.get('area')}, {r.get('price_range')}" for r in context_items])

SYSTEM_PROMPT = f"""You are a friendly Osaka guide. Recommend from these restaurants:\n{context_text}\nBe helpful and concise."""

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Groq API Key", type="password")
    if not GROQ_API_KEY:
        st.stop()

client = Groq(api_key=GROQ_API_KEY)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Osaka restaurants..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.success(f"✅ {len(osaka_data)} restaurants loaded")