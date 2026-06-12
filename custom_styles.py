# Modern Wix-like Design System
MODERN_CSS = """
<style>
/* ========== GLOBAL STYLES ========== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main container */
.main .block-container {
    max-width: 1200px !important;
    padding: 2rem 3rem !important;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 20px;
    margin: 2rem auto;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* ========== HEADER ========== */
.main h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem !important;
    letter-spacing: -1px;
}

.main h2 {
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: #2d3748 !important;
    margin: 2rem 0 1rem 0 !important;
}

.main h3 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #4a5568 !important;
}

/* Caption */
[data-testid="stCaption"] {
    font-size: 1.1rem !important;
    color: #718096 !important;
    font-weight: 400 !important;
}

/* ========== CARDS ========== */
div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]) {
    background: white !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.3s ease !important;
    border: 1px solid rgba(255, 255, 255, 0.8) !important;
}

div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]):hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15) !important;
}

/* Images */
[data-testid="stImage"] img {
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    transition: transform 0.3s ease !important;
}

[data-testid="stImage"] img:hover {
    transform: scale(1.02) !important;
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Secondary buttons */
.stButton > button[type="secondary"] {
    background: white !important;
    color: #667eea !important;
    border: 2px solid #667eea !important;
}

/* ========== SIDEBAR ========== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%) !important;
    border-right: 1px solid #e2e8f0 !important;
}

section[data-testid="stSidebar"] h2 {
    color: #2d3748 !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}

/* Sidebar inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stMultiselect"] select {
    border-radius: 8px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 0.6rem !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stSelectbox"] select:focus,
[data-testid="stMultiselect"] select:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* ========== BADGES & TAGS ========== */
.google-badge {
    background: linear-gradient(135deg, #4285F4, #34A853, #FBBC05, #EA4335) !important;
    color: white !important;
    padding: 6px 12px !important;
    border-radius: 20px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    display: inline-block !important;
    margin: 8px 0 !important;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3) !important;
}

/* Custom badges */
[data-testid="stMarkdown"] p:has(.price-badge) {
    display: inline-block;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.85rem;
}

/* ========== CHAT SECTION ========== */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 1rem 0 !important;
}

[data-testid="stChatMessage"]:nth-child(odd) {
    background: rgba(255, 255, 255, 0.9) !important;
}

/* ========== ALERTS & NOTIFICATIONS ========== */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
    padding: 1rem !important;
    font-weight: 500 !important;
}

[data-testid="stSuccess"] {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
    color: #155724 !important;
}

[data-testid="stInfo"] {
    background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%) !important;
    color: #0c5460 !important;
}

/* ========== DIVIDERS ========== */
[data-testid="stHorizontalLine"] {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
    margin: 2rem 0 !important;
}

/* ========== MAP CONTAINER ========== */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* ========== MOBILE OPTIMIZATION ========== */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
        margin: 0.5rem !important;
    }
    
    .main h1 {
        font-size: 2rem !important;
    }
    
    .main h2 {
        font-size: 1.5rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]) {
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }
}

/* ========== ANIMATIONS ========== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

[data-testid="stVerticalBlock"] {
    animation: fadeIn 0.5s ease-out;
}

/* ========== LOADING STATES ========== */
[data-testid="stSpinner"] {
    color: #667eea !important;
}

/* ========== SUCCESS STATES ========== */
[data-testid="stToast"] {
    border-radius: 10px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
}
</style>
"""

def apply_modern_styles():
    """Apply modern Wix-like styling to the app"""
    st.markdown(MODERN_CSS, unsafe_allow_html=True)