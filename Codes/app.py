import streamlit as st
import pandas as pd
import joblib
import os
import random
import base64
import streamlit.components.v1 as components

# ======================================================
# 1. PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="Enna Look uh",
    page_icon="⚔️",
    layout="wide"
)

# ======================================================
# 2. SESSION STATE (For Start Screen)
# ======================================================
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# ======================================================
# 3. GLOBAL CSS (THE NEW PREMIUM WHITE THEME + WIDGET FIXES)
# ======================================================
st.markdown("""
<style>
/* IMPORT GOOGLE FONT - POPPINS */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');

/* APPLY FONT & BOLD GLOBALLY */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* 1px TEXT BORDER SHADOW MASK (For Readability) */
h1, h2, h3, p, div, span, button, .poke-name, .subtitle, label {
    text-shadow: 
        -1px -1px 0 #000,  
         1px -1px 0 #000,
        -1px  1px 0 #000,
         1px  1px 0 #000 !important;
}

.block-container { padding-top: 1rem !important; }

/* MAIN TITLES */
h1 { 
    margin-top: -20px !important; 
    text-align: center; 
    color: #FFCB05 !important;
    font-weight: 800 !important;
    text-shadow: -2px -2px 0 #3B4CCA, 2px -2px 0 #3B4CCA, -2px 2px 0 #3B4CCA, 2px 2px 0 #3B4CCA !important;
}

.subtitle { 
    text-align: center; 
    color: #fff !important; 
    margin-bottom: 30px; 
    background: rgba(255,255,255,0.2); 
    padding: 15px; 
    border-radius: 15px; 
    display: inline-block; 
    backdrop-filter: blur(10px); 
    border: 2px solid rgba(255,255,255,0.4); 
    font-size: 1.2rem !important;
}

/* 🔥 WHITE GLASS CARD STYLE */
.poke-card {
    background: rgba(255, 255, 255, 0.15); 
    border-radius: 25px;
    padding: 25px;
    border: 3px solid rgba(255, 255, 255, 0.5); 
    margin-bottom: 20px;
    transition: all 0.3s ease;
    text-align: center;
    backdrop-filter: blur(20px); 
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}
.poke-card:hover { 
    transform: translateY(-8px) scale(1.02); 
    border-color: #ffffff; 
    background: rgba(255, 255, 255, 0.35); 
    box-shadow: 0 15px 40px rgba(255, 255, 255, 0.4);
}

/* WINNER GLOW */
.winner-card { 
    border: 4px solid #ffd700 !important; 
    box-shadow: 0 0 60px rgba(255, 215, 0, 0.9) !important; 
    animation: pulse 1.5s infinite alternate; 
    background: rgba(255, 215, 0, 0.2) !important;
}
@keyframes pulse { from { box-shadow: 0 0 20px rgba(255, 215, 0, 0.6); } to { box-shadow: 0 0 70px rgba(255, 215, 0, 1.0); } }

/* TEXT STYLES */
.poke-name { font-size: 1.8rem !important; font-weight: 800 !important; color: #fff !important; margin-top: 15px; }
.poke-type { color: #eee !important; font-size: 1.1rem; margin-bottom: 10px; }
.power-badge { background: rgba(0,0,0,0.5); color: #FFCB05 !important; padding: 8px 20px; border-radius: 30px; font-weight: 800; font-size: 1.2rem; margin-top: 10px; display: inline-block; border: 3px solid #FFCB05; }

/* 🔥 FIX: CUSTOMIZE SELECTBOX (POKEMON SELECTOR) TO WHITE GLASS */
/* The Container */
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border-color: rgba(255, 255, 255, 0.6) !important;
    border-radius: 10px !important;
    backdrop-filter: blur(10px);
}
/* The Text inside */
div[data-baseweb="select"] span {
    color: white !important;
    font-weight: 700 !important;
}
/* The Dropdown Icon */
div[data-baseweb="select"] svg {
    fill: white !important;
}
/* The Dropdown Menu List */
div[data-baseweb="popover"] {
    background-color: rgba(20, 20, 30, 0.95) !important; /* Dark BG for list */
    border: 1px solid rgba(255, 255, 255, 0.3);
}
div[data-baseweb="menu"] li {
    color: white !important;
}

/* 🔥 FIX: PROGRESS BARS (HP/ATK/DEF) */
.stProgress > div > div > div > div {
    background-color: #3B4CCA !important; /* Pokemon Blue */
}
.stProgress p {
    font-size: 1rem !important;
    font-weight: 800 !important;
    color: white !important;
    margin-bottom: 5px !important;
}

/* PURPLE BUTTON */
div.stButton > button { 
    width: 100%; 
    background-color: #8A2BE2; 
    color: white !important; 
    font-weight: 800 !important; 
    font-size: 22px !important; 
    padding: 15px; 
    border-radius: 12px; 
    border: 3px solid #6A0DAD; 
    transition: all 0.3s; 
    box-shadow: 0 6px 20px rgba(138, 43, 226, 0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}
div.stButton > button:hover { 
    background-color: #9932CC; 
    transform: scale(1.03); 
    box-shadow: 0 10px 30px rgba(138, 43, 226, 0.8); 
    border-color: #fff;
}
</style>
""", unsafe_allow_html=True)


# ======================================================
# 4. BACKGROUND VIDEO FUNCTION
# ======================================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_video(video_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, video_filename)
    
    if not os.path.exists(video_path):
        st.warning(f"⚠️ Machi, '{video_filename}' file kaanom!")
        return

    bin_str = get_base64_of_bin_file(video_path)
    
    video_html = f"""
    <style>
    .stApp {{
        background: none;
    }}
    #myVideo {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -1;
    }}
    header {{
        background-color: rgba(0,0,0,0) !important;
    }}
    </style>
    
    <video autoplay loop id="myVideo">
        <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
    </video>
    
    <script>
        var video = document.getElementById("myVideo");
        video.muted = false;
        video.volume = 1.0;
        video.play();
    </script>
    """
    st.markdown(video_html, unsafe_allow_html=True)

# ======================================================
# 5. SPLASH SCREEN (CLICK TO START)
# ======================================================
if not st.session_state.game_started:
    st.markdown("""
    <style>
        .stApp { background-color: #000; }
        .start-container { text-align: center; margin-top: 25vh; }
        .big-title {
            font-size: 90px !important;
            font-weight: 900 !important;
            color: #FFCB05 !important;
            text-shadow: -3px -3px 0 #3B4CCA, 3px -3px 0 #3B4CCA, -3px 3px 0 #3B4CCA, 3px 3px 0 #3B4CCA !important;
        }
        .start-btn-container div.stButton > button {
            font-size: 35px !important;
            padding: 25px 60px !important;
            background-color: #8A2BE2 !important;
            border-radius: 60px !important;
            border: 4px solid #fff !important;
            box-shadow: 0 0 40px rgba(138, 43, 226, 1.0) !important;
        }
         .start-btn-container div.stButton > button:hover {
             transform: scale(1.1) !important;
             background-color: #9932CC !important;
         }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='start-container'><h1 class='big-title'>POKÉMON<br>BATTLE ARENA</h1></div>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        with st.container():
             st.markdown('<div class="start-btn-container">', unsafe_allow_html=True)
             if st.button("🔊 CLICK TO ENTER ARENA 🔊", use_container_width=True):
                 st.session_state.game_started = True
                 st.rerun()
             st.markdown('</div>', unsafe_allow_html=True)
            
    st.stop()

# ======================================================
# 🚀 MAIN APP (Runs ONLY after 'Start' is clicked)
# ======================================================

# 1. LOAD VIDEO
set_background_video('background.mp4')

# 2. LOAD DATA & MODEL
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'pokemon_data.csv')
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df['type2'] = df['type2'].fillna("None")
    return df

@st.cache_resource
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'pokemon_battle_model_ultra.pkl')
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

df = load_data()
model = load_model()

# 4. MULTIPLIER LOGIC
type_chart = {
    'fire': {'grass': 2.0, 'water': 0.5, 'bug': 2.0, 'ice': 2.0, 'dragon': 0.5, 'steel': 2.0, 'rock': 0.5, 'ground': 0.5},
    'water': {'fire': 2.0, 'ground': 2.0, 'rock': 2.0, 'grass': 0.5, 'dragon': 0.5},
    'grass': {'water': 2.0, 'ground': 2.0, 'rock': 2.0, 'fire': 0.5, 'flying': 0.5, 'poison': 0.5, 'bug': 0.5, 'dragon': 0.5, 'steel': 0.5},
    'electric': {'water': 2.0, 'flying': 2.0, 'ground': 0.0, 'grass': 0.5, 'dragon': 0.5, 'electric': 0.5},
    'ice': {'grass': 2.0, 'ground': 2.0, 'flying': 2.0, 'dragon': 2.0, 'fire': 0.5, 'water': 0.5, 'ice': 0.5, 'steel': 0.5},
    'fighting': {'normal': 2.0, 'ice': 2.0, 'rock': 2.0, 'dark': 2.0, 'steel': 2.0, 'psychic': 0.5, 'flying': 0.5, 'bug': 0.5, 'poison': 0.5, 'fairy': 0.5},
    'poison': {'grass': 2.0, 'fairy': 2.0, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0.0},
    'ground': {'fire': 2.0, 'electric': 2.0, 'poison': 2.0, 'rock': 2.0, 'steel': 2.0, 'grass': 0.5, 'bug': 0.5, 'flying': 0.0},
    'flying': {'grass': 2.0, 'fighting': 2.0, 'bug': 2.0, 'electric': 0.5, 'rock': 0.5, 'steel': 0.5},
    'psychic': {'fighting': 2.0, 'poison': 2.0, 'psychic': 0.5, 'steel': 0.5, 'dark': 0.0},
    'bug': {'grass': 2.0, 'psychic': 2.0, 'dark': 2.0, 'fire': 0.5, 'fighting': 0.5, 'flying': 0.5, 'ghost': 0.5, 'steel': 0.5, 'fairy': 0.5},
    'rock': {'fire': 2.0, 'ice': 2.0, 'flying': 2.0, 'bug': 2.0, 'fighting': 0.5, 'ground': 0.5, 'steel': 0.5},
    'ghost': {'psychic': 2.0, 'ghost': 2.0, 'dark': 0.5, 'normal': 0.0},
    'dragon': {'dragon': 2.0, 'steel': 0.5, 'fairy': 0.0},
    'steel': {'ice': 2.0, 'rock': 2.0, 'fairy': 2.0, 'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'steel': 0.5},
    'dark': {'psychic': 2.0, 'ghost': 2.0, 'fighting': 0.5, 'dark': 0.5, 'fairy': 0.5},
    'fairy': {'fighting': 2.0, 'dragon': 2.0, 'dark': 2.0, 'fire': 0.5, 'poison': 0.5, 'steel': 0.5},
    'normal': {'rock': 0.5, 'ghost': 0.0, 'steel': 0.5},
    'None': {}
}
def get_multiplier(atk, d1, d2):
    m1 = type_chart.get(atk, {}).get(d1, 1.0)
    m2 = 1.0 if d2 == "None" else type_chart.get(atk, {}).get(d2, 1.0)
    return m1 * m2

# ======================================================
# 5. FIREWORKS FUNCTION
# ======================================================
def run_fullscreen_fireworks():
    fireworks_html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <style> .fireworks-container { position: fixed; inset: 0; z-index: 99999; pointer-events: none; } </style>
    <div class="fireworks-container">
        <lottie-player src="https://assets5.lottiefiles.com/packages/lf20_tiviyc3p.json" background="transparent" speed="1" style="width:100%; height:100%;" autoplay></lottie-player>
    </div>
    """
    components.html(fireworks_html, height=0, width=0)

# ======================================================
# 6. SESSION STATE & CELEBRATION
# ======================================================
if "winner" not in st.session_state: st.session_state.winner = None
if "celebrate" not in st.session_state: st.session_state.celebrate = False

if st.session_state.celebrate:
    random.choice([st.balloons, run_fullscreen_fireworks])()
    st.session_state.celebrate = False

# ======================================================
# 7. UI LAYOUT
# ======================================================
with st.container():
    st.markdown("<h1>⚡ POKÉMON BATTLE PREDICTOR ⚡</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><p class='subtitle'>Select two Pokémon and let the <b>AI Model</b> predict the winner!</p></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 0.2, 1])

with col1:
    st.markdown("<h2 style='text-align:center; color: white;'>PLAYER 1</h2>", unsafe_allow_html=True)
    p1 = st.selectbox("Choose Pokémon 1", df['name'].unique(), index=24)
    d1 = df[df['name'] == p1].iloc[0]
    card_class = "winner-card" if st.session_state.winner == p1 else ""
    st.markdown(f"""
    <div class="poke-card {card_class}">
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{d1['id']}.png" width="160">
        <div class="poke-name">{p1.upper()}</div>
        <div class="poke-type">{d1['type1']} / {d1['type2']}</div>
        <div class="power-badge">⚡ POWER: {d1['total_power']}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(int(d1['hp']/255*100), f"HP: {d1['hp']}")
    st.progress(int(d1['attack']/190*100), f"ATK: {d1['attack']}")
    st.progress(int(d1['defense']/230*100), f"DEF: {d1['defense']}")

with col2:
    # Adjusted VS text size and padding for bold font
    st.markdown("<h1 style='text-align:center; margin-left:20px; padding-top:240px; font-size:60px; color:#FF5733 !important;'>VS</h1>", unsafe_allow_html=True)

with col3:
    st.markdown("<h2 style='text-align:center; color: white;'>PLAYER 2</h2>", unsafe_allow_html=True)
    p2 = st.selectbox("Choose Pokémon 2", df['name'].unique(), index=5)
    d2 = df[df['name'] == p2].iloc[0]
    card_class = "winner-card" if st.session_state.winner == p2 else ""
    st.markdown(f"""
    <div class="poke-card {card_class}">
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{d2['id']}.png" width="160">
        <div class="poke-name">{p2.upper()}</div>
        <div class="poke-type">{d2['type1']} / {d2['type2']}</div>
        <div class="power-badge">⚡ POWER: {d2['total_power']}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(int(d2['hp']/255*100), f"HP: {d2['hp']}")
    st.progress(int(d2['attack']/190*100), f"ATK: {d2['attack']}")
    st.progress(int(d2['defense']/230*100), f"DEF: {d2['defense']}")

# ======================================================
# 8. PREDICTION LOGIC
# ======================================================
st.write("")
st.write("")
st.write("") # Extra spacing before button

if st.button("⚔️ SEE WHO IS GOING TO WIN THE BATTLE ⚔️", use_container_width=True):
    if p1 == p2:
        st.error("⚠️ bro, onnaku arivu funda iruka rendum same pokemon da vera ethavathu choose pannu")
        st.stop()
    
    m1 = get_multiplier(d1['type1'], d2['type1'], d2['type2'])
    m2 = get_multiplier(d2['type1'], d1['type1'], d1['type2'])
    
    input_data = pd.DataFrame([{
        'hp_diff': d1['hp'] - d2['hp'], 'atk_diff': d1['attack'] - d2['attack'],
        'def_diff': d1['defense'] - d2['defense'], 'spd_diff': d1['speed'] - d2['speed'],
        'total_power_diff': d1['total_power'] - d2['total_power'],
        'p1_real_advantage': m1, 'p2_real_advantage': m2
    }])
    
    prediction = model.predict(input_data)[0]
    winner = p1 if prediction == 0 else p2
    st.session_state.winner = winner
    st.session_state.celebrate = True 
    st.rerun()

if st.session_state.winner:
    # Updated Winner box to match white glass theme with green tint
    st.markdown(f"""
    <div style="text-align:center; margin-top:20px; margin-bottom:10px; padding:15px; background:rgba(76, 175, 80, 0.3); border-radius:20px; border:3px solid #4CAF50; backdrop-filter: blur(15px); box-shadow: 0 0 30px rgba(76, 175, 80, 0.5);">
        <h2 style="color:#fff; margin:0; font-size: 2rem; text-shadow: 2px 2px 0 #000;">🏆 THE BATTLE IS WON BY : {st.session_state.winner.upper()} 🏆</h2>
    </div>
    <h3 style="text-align:center; color:white; margin-top:10px; font-size: 1.5rem;">AI Confidence: {99.0}%</h3>
    """, unsafe_allow_html=True)
