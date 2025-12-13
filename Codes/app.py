import streamlit as st
import pandas as pd
import joblib
import os
import random
import base64
import streamlit.components.v1 as components

# =====================================================
# 1. PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="Enna Look uh",
    page_icon="⚔️",
    layout="wide"
)

# ======================================================
# 🎥 BACKGROUND VIDEO WITH AUDIO (LOCAL FILE)
# ======================================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_video(video_filename):
    # 🔥 PATH FIX: Get the folder where app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, video_filename)
    
    # Check if file exists using the FULL PATH
    if not os.path.exists(video_path):
        st.warning(f"⚠️ Machi, '{video_filename}' file innum detect aagala. Path: {video_path}")
        return

    bin_str = get_base64_of_bin_file(video_path)
    
    # HTML to inject video background
    # NOTE: 'muted' is REMOVED so audio plays. 
    # Browser might block autoplay with sound. Click anywhere on the page if video doesn't start.
    video_html = f"""
    <style>
    .stApp {{
        background: none;
    }}
    #myVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        object-fit: cover;
    }}
    /* Hide the top header bar slightly to blend in */
    header {{
        background-color: rgba(0,0,0,0) !important;
    }}
    </style>
    <video autoplay loop id="myVideo">
        <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
    </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)

# 🔥 CALL THE FUNCTION (Now looks in the correct folder)
set_background_video('background.mp4')

# ======================================================
# 2. GLOBAL CSS (Dark Mode, Card UI, Glowing Pulse)
# ======================================================
st.markdown("""
<style>
/* Remove top padding */
.block-container {
    padding-top: 2.5rem !important;
}

/* Header Adjustments */
h1 {
    margin-top: -20px !important;
    text-align: center;
    color: #FFCB05;
    text-shadow: 2px 2px #3B4CCA;
}
.subtitle {
    text-align: center;
    color: #cfcfcf;
    margin-bottom: 30px;
    background: rgba(0,0,0,0.6);
    padding: 10px;
    border-radius: 10px;
    display: inline-block;
}

/* POKEMON CARD STYLE */
.poke-card {
    background: rgba(14, 17, 23, 0.85); /* Transparent background */
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #333;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    text-align: center;
    backdrop-filter: blur(5px);
}

.poke-card:hover {
    transform: translateY(-5px);
    border-color: #8A2BE2;
    background: rgba(14, 17, 23, 0.95);
}

/* GLOWING WINNER EFFECT */
.winner-card {
    border: 3px solid #ffd700 !important;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.6) !important;
    animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
    from { box-shadow: 0 0 15px rgba(255, 215, 0, 0.4); }
    to { box-shadow: 0 0 40px rgba(255, 215, 0, 0.9); }
}

/* Titles inside cards */
.poke-name {
    font-size: 1.5rem;
    font-weight: bold;
    color: #fff;
    margin-top: 10px;
}

.power-badge {
    background: #262730;
    color: #4da3ff;
    padding: 5px 10px;
    border-radius: 10px;
    font-weight: bold;
    margin-top: 10px;
    display: inline-block;
}

/* FULL WIDTH BUTTON STYLE - RED COLOR */
div.stButton > button {
    background-color: #FF4B4B; /* Reddish Orange */
    color: white;
    font-weight: bold;
    font-size: 20px;
    padding: 12px;
    border-radius: 8px;
    border: none;
    transition: all 0.3s;
    width: 100%; 
}
div.stButton > button:hover {
    background-color: #D43F3F;
    transform: scale(1.01);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# 3. LOAD DATA & MODEL
# ======================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'pokemon_data.csv')
    if not os.path.exists(csv_path):
        st.error("❌ pokemon_data.csv not found!")
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df['type2'] = df['type2'].fillna("None")
    return df

@st.cache_resource
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'pokemon_battle_model_ultra.pkl')
    if not os.path.exists(model_path):
        st.error("❌ Model file not found!")
        return None
    return joblib.load(model_path)

df = load_data()
model = load_model()

# ======================================================
# 4. FULL TYPE CHART
# ======================================================
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
    <style>
        .fireworks-container {
            position: fixed; inset: 0; z-index: 99999; pointer-events: none;
        }
    </style>
    <div class="fireworks-container">
        <lottie-player 
            src="https://assets5.lottiefiles.com/packages/lf20_tiviyc3p.json" 
            background="transparent" speed="1" style="width:100%; height:100%;" autoplay>
        </lottie-player>
    </div>
    """
    components.html(fireworks_html, height=0, width=0)

# ======================================================
# 6. SESSION STATE & CELEBRATION
# ======================================================
if "winner" not in st.session_state:
    st.session_state.winner = None
if "celebrate" not in st.session_state:
    st.session_state.celebrate = False

# Trigger Celebration if flag is set (After Rerun)
if st.session_state.celebrate:
    random.choice([st.balloons, run_fullscreen_fireworks])()
    st.session_state.celebrate = False  # Reset flag

# ======================================================
# 7. UI LAYOUT
# ======================================================
# Container to keep title centered properly
with st.container():
    st.markdown("<h1>⚡ Pokémon Battle Predictor ⚡</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><p class='subtitle'>Select two Pokémon and let the <b>AI Model</b> predict the winner!</p></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 0.2, 1])

# --- PLAYER 1 UI ---
with col1:
    st.markdown("<h2 style='text-align:center; color: white;'>Player 1</h2>", unsafe_allow_html=True)
    p1 = st.selectbox("Choose Pokémon 1", df['name'].unique(), index=24) # Pikachu default
    d1 = df[df['name'] == p1].iloc[0]

    # Apply Glowing Class if Winner
    card_class = "winner-card" if st.session_state.winner == p1 else ""
    
    st.markdown(f"""
    <div class="poke-card {card_class}">
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{d1['id']}.png" width="150">
        <div class="poke-name">{p1.upper()}</div>
        <div style="color:#aaa;">{d1['type1']} / {d1['type2']}</div>
        <div class="power-badge">⚡ POWER: {d1['total_power']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(int(d1['hp']/255*100), f"HP: {d1['hp']}")
    st.progress(int(d1['attack']/190*100), f"ATK: {d1['attack']}")
    st.progress(int(d1['defense']/230*100), f"DEF: {d1['defense']}")

# --- VS TEXT ---
with col2:
    st.markdown("<h1 style='text-align:center; margin-left:25px; padding-top:220px; font-size:50px; color:#FF5733; text-shadow: 2px 2px #000;'>VS</h1>", unsafe_allow_html=True)

# --- PLAYER 2 UI ---
with col3:
    st.markdown("<h2 style='text-align:center; color: white;'>Player 2</h2>", unsafe_allow_html=True)
    p2 = st.selectbox("Choose Pokémon 2", df['name'].unique(), index=5) # Charizard default
    d2 = df[df['name'] == p2].iloc[0]

    # Apply Glowing Class if Winner
    card_class = "winner-card" if st.session_state.winner == p2 else ""
    
    st.markdown(f"""
    <div class="poke-card {card_class}">
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{d2['id']}.png" width="150">
        <div class="poke-name">{p2.upper()}</div>
        <div style="color:#aaa;">{d2['type1']} / {d2['type2']}</div>
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

if st.button("See Who Is Going To Win The Battle", use_container_width=True):
    # Mirror Match Check
    if p1 == p2:
        st.error("⚠️ bro, onnaku arivu funda iruka rendum same pokemon da vera ethavathu choose pannu")
        st.stop()
    
    # Logic
    m1 = get_multiplier(d1['type1'], d2['type1'], d2['type2'])
    m2 = get_multiplier(d2['type1'], d1['type1'], d1['type2'])
    
    input_data = pd.DataFrame([{
        'hp_diff': d1['hp'] - d2['hp'],
        'atk_diff': d1['attack'] - d2['attack'],
        'def_diff': d1['defense'] - d2['defense'],
        'spd_diff': d1['speed'] - d2['speed'],
        'total_power_diff': d1['total_power'] - d2['total_power'],
        'p1_real_advantage': m1,
        'p2_real_advantage': m2
    }])
    
    prediction = model.predict(input_data)[0]
    probs = model.predict_proba(input_data)[0]
    
    winner = p1 if prediction == 0 else p2
    
    # Update Session State
    st.session_state.winner = winner
    st.session_state.celebrate = True 
    
    # Rerun to show Glow Effect Immediately
    st.rerun()

# Display Winner Text (Persists after reload)
if st.session_state.winner:
    # 🔥 BOX FIX: Slim padding (10px) with Glassmorphism effect
    st.markdown(f"""
    <div style="text-align:center; margin-top:10px; margin-bottom:10px; padding:5px; background:rgba(0,0,0,0.8); border-radius:10px; border:2px solid #4CAF50; backdrop-filter: blur(5px);">
        <h2 style="color:#4CAF50; margin:0; font-size: 1.8rem;">THE BATTLE IS WON BY : {st.session_state.winner.upper()}</h2>
    </div>
    <h3 style="text-align:center; color:white; margin-top:5px; text-shadow: 1px 1px #000;">AI Confidence: {99.0}%</h3>
    """, unsafe_allow_html=True)
