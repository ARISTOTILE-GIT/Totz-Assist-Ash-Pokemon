import streamlit as st
import pandas as pd
import joblib
import os
import requests
import random
import streamlit.components.v1 as components 

# 1. SETUP & LOADING
st.set_page_config(page_title="AI Pokémon Battle Arena", page_icon="⚔️", layout="wide")

# ==========================================
# 🎨 CUSTOM CSS FOR UI
# ==========================================
st.markdown("""
    <style>
    /* 1. Reduce Top White Space */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* 2. Center Title and Subtitle */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #FFCB05; 
        text-shadow: 2px 2px #3B4CCA;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 30px;
    }
    
    /* 3. VS Text Centered */
    .vs-text {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        padding-top: 140px;
        color: #FF5733;
    }

    /* 4. BUTTON STYLE (FULL SCREEN WIDTH) */
    div.stButton > button {
        background-color: #8A2BE2; /* Purple */
        color: white;
        font-weight: bold;
        font-size: 20px;
        border-radius: 8px;
        border: 2px solid #4B0082;
        width: 100% !important; /* 🔥 FORCES FULL WIDTH */
        height: 60px;
        margin-top: 10px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #4B0082;
        color: #FFCB05;
        border-color: #FFCB05;
        transform: scale(1.01);
    }
    
    /* 5. Winner Box */
    .winner-box {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        color: #4CAF50;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    /* 6. Center Images & Text */
    [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .centered-text {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🛠️ LOAD DATA & MODEL
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'pokemon_data.csv')
    if not os.path.exists(csv_path):
        st.error(f"❌ Error: Could not find file at {csv_path}")
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df['type2'] = df['type2'].fillna('None')
    return df

@st.cache_resource
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'pokemon_battle_model_ultra.pkl') 
    if not os.path.exists(model_path):
        st.error(f"❌ Error: Could not find model at {model_path}")
        return None
    return joblib.load(model_path)

df = load_data()
model = load_model()

# ==========================================
# 🎆 FULL SCREEN FIREWORKS FUNCTION
# ==========================================
def run_fullscreen_fireworks():
    fireworks_html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <style>
        .fireworks-container {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 999999; pointer-events: none; display: flex;
            justify-content: center; align-items: center; background: transparent;
        }
    </style>
    <div class="fireworks-container">
        <lottie-player 
            src="https://assets5.lottiefiles.com/packages/lf20_tiviyc3p.json" 
            background="transparent" speed="1" style="width: 100%; height: 100%;" autoplay>
        </lottie-player>
    </div>
    """
    components.html(fireworks_html, height=0, width=0)

# ==========================================
# 🧠 TYPE CHART LOGIC
# ==========================================
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

def get_dual_type_multiplier(atk_type, def_type1, def_type2):
    mult1 = type_chart.get(atk_type, {}).get(def_type1, 1.0)
    mult2 = 1.0 if def_type2 == 'None' else type_chart.get(atk_type, {}).get(def_type2, 1.0)
    return mult1 * mult2

# ==========================================
# 📱 UI LAYOUT
# ==========================================

st.markdown('<h1 class="main-title">⚡ AI Pokémon Battle Predictor ⚡</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Select two Pokémon and let the <b>AI Model</b> predict the winner!</p>', unsafe_allow_html=True)

# Selection Columns
col1, col2, col3 = st.columns([1, 0.3, 1]) 

with col1:
    st.markdown("<h2 style='text-align: center;'>Player 1</h2>", unsafe_allow_html=True)
    p1_name = st.selectbox("Choose Pokémon 1", df['name'].unique(), index=24) # Pikachu
    p1_data = df[df['name'] == p1_name].iloc[0]
    
    st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p1_data['id']}.png", width=200)
    
    st.info(f"**{p1_data['name'].upper()}**")
    st.markdown(f"<div class='centered-text'>Type: {p1_data['type1']} / {p1_data['type2']}</div>", unsafe_allow_html=True)
    st.progress(int(p1_data['hp']/255*100), text=f"HP: {p1_data['hp']}")
    st.markdown(f"<div class='centered-text'><b>Total Power: {p1_data['total_power']}</b></div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)

with col3:
    st.markdown("<h2 style='text-align: center;'>Player 2</h2>", unsafe_allow_html=True)
    p2_name = st.selectbox("Choose Pokémon 2", df['name'].unique(), index=5) # Charizard
    p2_data = df[df['name'] == p2_name].iloc[0]
    
    st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p2_data['id']}.png", width=200)
    
    st.info(f"**{p2_data['name'].upper()}**")
    st.markdown(f"<div class='centered-text'>Type: {p2_data['type1']} / {p2_data['type2']}</div>", unsafe_allow_html=True)
    st.progress(int(p2_data['hp']/255*100), text=f"HP: {p2_data['hp']}")
    st.markdown(f"<div class='centered-text'><b>Total Power: {p2_data['total_power']}</b></div>", unsafe_allow_html=True)

# ==========================================
# 🔥 PREDICTION BUTTON (FULL WIDTH)
# ==========================================
st.write("")
st.write("") 

# NO COLUMNS HERE -> This makes the button take 100% width of the container
if st.button("🔥 PREDICT WINNER 🔥"):
    
    # Mirror Match Check
    if p1_name == p2_name:
        st.error("⚠️ Machi, rendume onnu! Vera ethavathu select pannu!")
        st.stop()
    
    # Feature Calculation
    p1_mult = get_dual_type_multiplier(p1_data['type1'], p2_data['type1'], p2_data['type2'])
    p2_mult = get_dual_type_multiplier(p2_data['type1'], p1_data['type1'], p1_data['type2'])
    
    input_data = pd.DataFrame([{
        'hp_diff': p1_data['hp'] - p2_data['hp'],
        'atk_diff': p1_data['attack'] - p2_data['attack'],
        'def_diff': p1_data['defense'] - p2_data['defense'],
        'spd_diff': p1_data['speed'] - p2_data['speed'],
        'total_power_diff': p1_data['total_power'] - p2_data['total_power'],
        'p1_real_advantage': p1_mult,
        'p2_real_advantage': p2_mult
    }])
    
    prediction = model.predict(input_data)[0]
    probs = model.predict_proba(input_data)[0]
    
    winner_name = p1_name if prediction == 0 else p2_name
    confidence = probs[0] if prediction == 0 else probs[1]
    
    # Large Centered Winner Box
    st.markdown(f'<div class="winner-box">🏆 THE WINNER IS: {winner_name.upper()} 🏆</div>', unsafe_allow_html=True)
    
    # Confidence Score
    st.markdown(f"<h3 style='text-align: center; color: white; margin-bottom: 30px;'>AI Confidence: {confidence*100:.1f}%</h3>", unsafe_allow_html=True)
    
    # Full Screen Celebration
    celebration = random.choice(["balloons", "fireworks"])
    if celebration == "balloons":
        st.balloons()
    else:
        run_fullscreen_fireworks()
