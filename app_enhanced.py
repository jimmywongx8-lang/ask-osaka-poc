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
st.set_page_config(page_title="Ask Osaka - AI Travel Planner", page_icon="🏯", layout="wide")

# Premium Wix-like CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.main .block-container {
    max-width: 1400px !important;
    padding: 2.5rem 3rem !important;
    background: linear-gradient(180deg, #fafbfc 0%, #f0f2f5 100%) !important;
}

/* Header Styling */
.main h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stCaption"] {
    font-size: 1.1rem !important;
    color: #64748b !important;
}

/* Restaurant Cards */
div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]) {
    background: white !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid #e2e8f0 !important;
}

div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]):hover {
    transform: translateY(-6px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.12) !important;
}

/* Center and Style Images */
[data-testid="stImage"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}

[data-testid="stImage"] img {
    border-radius: 0 !important;
    width: 100% !important;
    height: 220px !important;
    object-fit: cover !important;
    display: block !important;
}

/* Tags */
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
}

.tag-location { background: #dbeafe; color: #1e40af; }
.tag-cuisine { background: #f3e8ff; color: #7c3aed; }
.tag-price { background: #fef3c7; color: #b45309; }

/* Action Buttons Area */
.actions-bar {
    display: flex;
    gap: 0.75rem;
    padding: 1rem 1.5rem 1.5rem 1.5rem !important;
    border-top: 1px solid #f1f5f9 !important;
    margin-top: 1rem !important;
    align-items: center;
    justify-content: space-between;
}

/* Button 1: Favorite (Pink/Red) */
.actions-bar .stButton:nth-of-type(1) button {
    background-color: #ffeff2 !important;
    color: #e0245e !important;
    border: 1px solid #ffeff2 !important;
    font-size: 1.2rem !important;
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.actions-bar .stButton:nth-of-type(1) button:hover {
    background-color: #e0245e !important;
    color: white !important;
    border-color: #e0245e !important;
}

/* Button 2: Share (Blue) */
.actions-bar .stButton:nth-of-type(2) button {
    background-color: #eff6ff !important;
    color: #2563eb !important;
    border: 1px solid #eff6ff !important;
    font-size: 1.2rem !important;
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.actions-bar .stButton:nth-of-type(2) button:hover {
    background-color: #2563eb !important;
    color: white !important;
    border-color: #2563eb !important;
}

/* Button 3: Report (Orange) */
.actions-bar .stButton:nth-of-type(3) button {
    background-color: #fff7ed !important;
    color: #ea580c !important;
    border: 1px solid #fff7ed !important;
    font-size: 1.2rem !important;
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.actions-bar .stButton:nth-of-type(3) button:hover {
    background-color: #ea580c !important;
    color: white !important;
    border-color: #ea580c !important;
}

/* Button 4: Google Info (Gradient Purple) */
.actions-bar .stButton:nth-of-type(4) button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 15px rgba(118, 75, 162, 0.3) !important;
    flex: 1 !important;
    max-width: 250px !important;
}
.actions-bar .stButton:nth-of-type(4) button:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4) !important;
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
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e2e8f0 !important;
}

/* Chat Container */
.chat-container {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    margin-top: 2rem;
    border: 1px solid #e2e8f0;
}

[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin: 1rem 0 !important;
    background: #f8fafc !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    border: 1px solid #e2e8f0 !important;
}

/* Mobile */
@media (max-width: 768px) {
    .main .block-container { padding: 1rem !important; }
    .main h1 { font-size: 2rem !important; }
    [data-testid="stImage"] img { height: 180px !important; }
    .actions-bar { flex-wrap: wrap; justify-content: center; }
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

# Load data FIRST
@st.cache_data(ttl=300)
def load_osaka_data():
    try:
        with open("osaka_restaurants.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

osaka_data = load_osaka_data()

# Header and Stats
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
    "> Ask Osaka</h1>
    <p style="
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
        font-weight: 400;
    ">Your AI-powered travel planner & dining guide</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;">
        <div style="font-size: 2rem; font-weight: 800; color: #667eea;">{len(osaka_data)}</div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 0.25rem;">Restaurants</div>
    </div>
    """, unsafe_allow_html=True)

all_areas = sorted(list(set(r.get('area', 'Unknown') for r in osaka_data)))
with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;">
        <div style="font-size: 2rem; font-weight: 800; color: #764ba2;">{len(all_areas)}</div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 0.25rem;">Districts</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;">
        <div style="font-size: 2rem; font-weight: 800; color: #f59e0b;">AI</div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 0.25rem;">Powered</div>
    </div>
    """, unsafe_allow_html=True)

all_categories = sorted(list(set(r.get('category', 'Unknown') for r in osaka_data)))
all_prices = sorted(list(set(r.get('price_range', 'Unknown') for r in osaka_data)))

# Sidebar
st.sidebar.header("Search & Filters")
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
        st.sidebar.markdown(f"• {fav_name}")
    if st.sidebar.button("Clear Favorites", key="clear_fav"):
        st.session_state.favorites = []
        st.rerun()
else:
    st.sidebar.info("Click ❤️ to save favorites")

st.sidebar.markdown("---")

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
            <span style="color: #64748b; font-size: 12px;"> {restaurant.get('category', 'N/A')}</span><br>
            <span style="color: #475569; font-size: 12px;">📞 {restaurant.get('phone', 'N/A')}</span>
        </div>
        """
        folium.Marker(coords, popup=folium.Popup(popup_html, max_width=300), tooltip=restaurant.get('name')).add_to(m)
    st_folium(m, width=700, height=500, use_container_width=True)

# === AI CHAT SECTION (MOVED TO TOP) ===
st.markdown("---")
st.subheader("💬 AI Travel Planner")

# Quick Actions for Itinerary Builder
st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
col_q1, col_q2, col_q3 = st.columns(3)
with col_q1:
    if st.button("📅 Plan a 3-Day Trip", type="secondary"):
        st.session_state.messages.append({"role": "user", "content": "Create a 3-day food itinerary for Osaka covering different areas each day."})
        st.rerun()
with col_q2:
    if st.button("❤️ Best Date Night", type="secondary"):
        st.session_state.messages.append({"role": "user", "content": "Recommend the best romantic dinner spots for a date night."})
        st.rerun()
with col_q3:
    if st.button(" Budget Eats", type="secondary"):
        st.session_state.messages.append({"role": "user", "content": "Find the best budget-friendly street food and cheap eats."})
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Context Preparation
context_items = filtered_data[:50] if filtered_data else osaka_data[:50]
context_text = "\n".join([f"{r.get('name')}: {r.get('category')} in {r.get('area')}, {r.get('price_range')} - {r.get('description', '')}" for r in context_items])

# ENHANCED SYSTEM PROMPT FOR ITINERARIES
SYSTEM_PROMPT = f"""You are an expert Osaka travel planner and food guide.

RESTAURANT DATABASE:
{context_text}

INSTRUCTIONS:
1. Answer questions about specific restaurants using ONLY the provided data.
2. If the user asks for an ITINERARY (e.g., "3 day trip", "plan for me", "schedule"), create a structured travel plan:
   - Organize by Day > Meal (Lunch/Dinner).
   - Group restaurants geographically to minimize travel time (e.g., Dotonbori + Shinsaibashi).
   - Include the restaurant name, category, price range, and a "Why go here" tip based on the description.
3. If the user asks for something not in the data, politely say you only know these specific spots.
4. Keep the tone helpful and local (use phrases like "Maido", "Okini" occasionally).
5. Format your response clearly using Markdown headers and lists.
"""

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Groq API Key", type="password")
    if not GROQ_API_KEY:
        st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask for recommendations or 'Plan a 2-day trip'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=1000
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.success(f"✅ {len(osaka_data)} restaurants loaded")

# Pagination
items_per_page = 12
page = st.sidebar.number_input("Page", min_value=1, max_value=max(1, (len(filtered_data) + items_per_page - 1) // items_per_page), value=1)
start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_data = filtered_data[start_idx:end_idx]

# Display restaurants
if page_data:
    st.subheader(f"🍽️ Restaurants (Page {page})")
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
                
                # Tags
                st.markdown(f"""
                <div class="tags-row">
                    <span class="tag tag-location">📍 {restaurant.get('area', 'Unknown')}</span>
                    <span class="tag tag-cuisine">🍴 {restaurant.get('category', 'Unknown')}</span>
                    <span class="tag tag-price">💰 {restaurant.get('price_range', 'N/A')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Details
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
                
                # Actions Bar
                st.markdown('<div class="actions-bar">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
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
                    if st.button("📤", key=f"share_{idx}", help="Share"):
                        st.code(f"{rest_name}\n{restaurant.get('address')}\n{restaurant.get('phone')}")
                
                with col3:
                    if st.button("🚩", key=f"report_{idx}", help="Report"):
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