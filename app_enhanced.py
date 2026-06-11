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

# Premium Wix-like CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global Reset */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Main Container */
.main .block-container {
    max-width: 1400px !important;
    padding: 2.5rem 3rem !important;
    background: linear-gradient(180deg, #fafbfc 0%, #f0f2f5 100%) !important;
    min-height: 100vh !important;
}

/* Hero Header */
.main h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stCaption"] {
    font-size: 1.1rem !important;
    color: #64748b !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
}

/* Stats Bar */
.stats-bar {
    display: flex;
    gap: 2rem;
    margin: 1.5rem 0 2.5rem 0;
    padding: 1rem 1.5rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    border: 1px solid #e2e8f0;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a2e;
}

.stat-label {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 500;
}

/* Restaurant Cards */
div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]) {
    background: white !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid #e2e8f0 !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
}

div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]):hover {
    transform: translateY(-6px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.12) !important;
    border-color: #cbd5e1 !important;
}

/* Card Image */
[data-testid="stImage"] img {
    border-radius: 0 !important;
    width: 100% !important;
    height: 220px !important;
    object-fit: cover !important;
    transition: transform 0.3s ease !important;
}

div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]):hover [data-testid="stImage"] img {
    transform: scale(1.05) !important;
}

/* Card Content */
.element-container:has(+ div[data-testid="stMarkdown"]:has(h3)) {
    padding: 1.5rem 1.5rem 0.5rem 1.5rem !important;
    flex: 1 !important;
}

/* Restaurant Name */
[data-testid="stMarkdown"]:has(h3) h3 {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #1a1a2e !important;
    margin: 0 0 0.75rem 0 !important;
    line-height: 1.3 !important;
}

/* Tags Row */
.tags-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.75rem 0 1rem 0;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}

.tag-location {
    background: #dbeafe;
    color: #1e40af;
}

.tag-cuisine {
    background: #f3e8ff;
    color: #7c3aed;
}

.tag-price {
    background: #fef3c7;
    color: #b45309;
}

/* Details Section */
.details-section {
    padding: 0 1.5rem !important;
    flex: 1 !important;
}

.details-section p {
    font-size: 0.9rem !important;
    color: #475569 !important;
    line-height: 1.7 !important;
    margin: 0.5rem 0 !important;
}

/* Description Box */
.description-box {
    margin: 1rem 1.5rem !important;
    padding: 1rem !important;
    background: #f8fafc !important;
    border-radius: 10px !important;
    border-left: 3px solid #667eea !important;
    font-style: italic !important;
    color: #64748b !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

/* Highlights */
.highlights {
    padding: 0 1.5rem !important;
    margin: 0.5rem 0 !important;
}

.highlight-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #475569;
    margin: 0.3rem 0;
}

/* Website Link */
.website-link {
    padding: 0 1.5rem !important;
    margin: 0.75rem 0 !important;
}

.website-link a {
    color: #667eea !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: color 0.2s ease !important;
}

.website-link a:hover {
    color: #764ba2 !important;
    text-decoration: underline !important;
}

/* Action Buttons */
.actions-bar {
    display: flex;
    gap: 0.75rem;
    padding: 1rem 1.5rem 1.5rem 1.5rem !important;
    border-top: 1px solid #f1f5f9 !important;
    margin-top: 1rem !important;
    align-items: center;
}

.action-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.2s ease;
    border: 1px solid #e2e8f0;
    background: white;
    color: #475569;
    cursor: pointer;
}

.action-btn:hover {
    border-color: #667eea;
    color: #667eea;
    background: #f8fafc;
}

.action-btn.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    flex: 1;
}

.action-btn.primary:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Google Badge */
.google-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.8rem;
    background: linear-gradient(135deg, #4285F4, #34A853);
    color: white;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.25);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e2e8f0 !important;
    padding: 1.5rem !important;
}

section[data-testid="stSidebar"] h2 {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #1a1a2e !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 2px solid #e2e8f0 !important;
}

/* Sidebar Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stMultiselect"] select {
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 0.6rem 0.8rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stMultiselect"] select:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Favorites Section */
.favorites-section {
    margin-top: 1.5rem !important;
    padding-top: 1.5rem !important;
    border-top: 1px solid #e2e8f0 !important;
}

.favorite-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: #f8fafc;
    border-radius: 8px;
    margin: 0.4rem 0;
    font-size: 0.85rem;
    color: #475569;
}

/* Chat Section */
.chat-section {
    margin-top: 3rem !important;
    padding-top: 2rem !important;
    border-top: 2px solid #e2e8f0 !important;
}

[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin: 1rem 0 !important;
    background: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    border: 1px solid #e2e8f0 !important;
}

[data-testid="stChatMessage"]:nth-child(odd) {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
}

/* Map */
.map-container {
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    border: 1px solid #e2e8f0 !important;
}

/* Divider */
[data-testid="stHorizontalLine"] {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
    margin: 2rem 0 !important;
}

/* Success/Info Alerts */
[data-testid="stSuccess"] {
    background: #f0fdf4 !important;
    color: #166534 !important;
    border: 1px solid #bbf7d0 !important;
    border-radius: 10px !important;
}

[data-testid="stInfo"] {
    background: #eff6ff !important;
    color: #1e40af !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px !important;
}

/* Mobile Optimization */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
    }
    
    .main h1 {
        font-size: 2rem !important;
    }
    
    .stats-bar {
        flex-direction: column;
        gap: 1rem;
    }
    
    [data-testid="stImage"] img {
        height: 180px !important;
    }
    
    .actions-bar {
        flex-wrap: wrap;
    }
    
    .action-btn {
        flex: 1;
        min-width: calc(50% - 0.5rem);
    }
}

/* Animations */
@keyframes slideIn {
    from { 
        opacity: 0; 
        transform: translateY(20px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

div[data-testid="stVerticalBlock"] > div {
    animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
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

# Premium Hero Section
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 3rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 8px 32px rgba(26, 26, 46, 0.3);
">
    <h1 style="
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        background: linear-gradient(135deg, #fff 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">🏯 Ask Osaka</h1>
    <p style="
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
        font-weight: 400;
    ">Your AI-powered guide to Osaka's finest dining experiences</p>
</div>
""", unsafe_allow_html=True)

# Stats Bar
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    ">
        <div style="font-size: 2rem; font-weight: 800; color: #667eea;">{len(osaka_data)}</div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 0.25rem;">Restaurants</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    ">
        <div style="font-size: 2rem; font-weight: 800; color: #764ba2;">{len(all_areas)}</div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 0.25rem;">Districts</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    ">
        <div style="font-size: 2rem; font-weight: 800; color: #f59e0b;">AI</div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 0.25rem;">Powered</div>
    </div>
    """, unsafe_allow_html=True)

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
all_areas = sorted(list(set(r.get('area', 'Unknown') for r in osaka_data)))
all_categories = sorted(list(set(r.get('category', 'Unknown') for r in osaka_data)))
all_prices = sorted(list(set(r.get('price_range', 'Unknown') for r in osaka_data)))

# Sidebar
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Search restaurants...", placeholder="e.g., ramen, namba, cheap")

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
        st.sidebar.markdown(f"""
        <div style="
            padding: 0.5rem 0.75rem;
            background: #f8fafc;
            border-radius: 8px;
            margin: 0.4rem 0;
            font-size: 0.85rem;
            color: #475569;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            ❤️ {fav_name}
        </div>
        """, unsafe_allow_html=True)
    if st.sidebar.button("Clear Favorites", key="clear_fav", use_container_width=True):
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
        <div style="width: 220px; padding: 8px; font-family: Inter, sans-serif;">
            <b style="font-size: 14px; color: #1a1a2e;">{restaurant.get('name', 'N/A')}</b><br>
            <span style="color: #64748b; font-size: 12px;">🍴 {restaurant.get('category', 'N/A')} • 💰 {restaurant.get('price_range', 'N/A')}</span><br>
            <span style="color: #475569; font-size: 12px;">📞 {restaurant.get('phone', 'N/A')}</span>
        </div>
        """
        folium.Marker(coords, popup=folium.Popup(popup_html, max_width=300), tooltip=restaurant.get('name')).add_to(m)
    
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, width=700, height=500, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
                
                # Info with proper structure
                st.markdown(f"### {restaurant.get('name')}")
                
                # Tags
                st.markdown(f"""
                <div class="tags-row">
                    <span class="tag tag-location">📍 {restaurant.get('area', 'Unknown')}</span>
                    <span class="tag tag-cuisine">🍴 {restaurant.get('category', 'Unknown')}</span>
                    <span class="tag tag-price">💰 {restaurant.get('price_range', 'N/A')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Details
                st.markdown('<div class="details-section">', unsafe_allow_html=True)
                if restaurant.get('address'):
                    st.markdown(f"📮 {restaurant.get('address')}")
                if restaurant.get('phone'):
                    st.markdown(f"📞 {restaurant.get('phone')}")
                if restaurant.get('hours'):
                    st.markdown(f"🕐 {restaurant.get('hours')} (Closed: {restaurant.get('closed', 'None')})")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Description
                if restaurant.get('description'):
                    st.markdown(f'<div class="description-box">{restaurant.get("description")}</div>', unsafe_allow_html=True)
                
                # Highlights
                highlights = restaurant.get('highlights', [])
                if isinstance(highlights, list) and highlights:
                    st.markdown('<div class="highlights">', unsafe_allow_html=True)
                    for h in highlights[:2]:
                        st.markdown(f'<div class="highlight-item">⭐ {h}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Website
                website = restaurant.get('website', '')
                if website and website.startswith('http'):
                    st.markdown(f'<div class="website-link"><a href="{website}" target="_blank"> Visit Website →</a></div>', unsafe_allow_html=True)
                
                # Action Buttons
                st.markdown('<div class="actions-bar">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
                rest_name = restaurant.get('name', '')
                
                with col1:
                    is_fav = rest_name in st.session_state.favorites
                    if st.button("❤️" if is_fav else "", key=f"fav_{idx}", help="Favorite"):
                        if is_fav:
                            st.session_state.favorites.remove(rest_name)
                        else:
                            st.session_state.favorites.append(rest_name)
                        st.rerun()
                
                with col2:
                    if st.button("📤", key=f"share_{idx}", help="Share"):
                        st.code(f"{rest_name}\n{restaurant.get('address')}\n{restaurant.get('phone')}")
                
                with col3:
                    if st.button("", key=f"report_{idx}", help="Report"):
                        st.session_state[f"show_report_{idx}"] = not st.session_state.get(f"show_report_{idx}", False)
                        st.rerun()
                
                with col4:
                    if st.button("🔍 Google Info", key=f"google_{idx}", help="Live data"):
                        st.session_state[f"show_google_{idx}"] = not st.session_state.get(f"show_google_{idx}", False)
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Report form
                if st.session_state.get(f"show_report_{idx}"):
                    with st.form(f"report_form_{idx}"):
                        st.markdown("**Report Issue**")
                        issue = st.selectbox("What's wrong?", ["Wrong hours", "Wrong phone", "Closed", "Other"])
                        desc = st.text_area("Details", placeholder="Optional")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.form_submit_button("Submit"):
                                save_feedback(rest_name, issue, desc)
                                st.success("Thanks!")
                                st.session_state[f"show_report_{idx}"] = False
                                st.rerun()
                        with col_b:
                            if st.form_submit_button("Cancel"):
                                st.session_state[f"show_report_{idx}"] = False
                                st.rerun()
                
                # Google Info
                if st.session_state.get(f"show_google_{idx}"):
                    with st.spinner("Loading live data..."):
                        gdata = get_cached_google_data(rest_name, restaurant.get('area'))
                        if gdata:
                            if gdata.get('rating'):
                                st.markdown(f'<div class="google-badge">⭐ {gdata["rating"]}/5 ({gdata["total_ratings"]} reviews)</div>', unsafe_allow_html=True)
                            st.markdown("🟢 Open Now" if gdata.get('open_now') else "🔴 Closed")
                            if gdata.get('photo_url'):
                                st.image(gdata['photo_url'], use_container_width=True)
                        else:
                            st.warning("No live data found")
                
                st.divider()

# AI Chat Section
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

if prompt := st.chat_input("Ask about Osaka restaurants, events, or tips..."):
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