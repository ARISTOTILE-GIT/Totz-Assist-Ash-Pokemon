import streamlit as st
import pandas as pd
import joblib
import os
import random
import streamlit.components.v1 as components

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Pokémon Battle Arena",
    page_icon="⚔️",
    layout="wide"
)

# ======================================================
# GLOBAL CSS (SPACING + CARD UI + ANIMATIONS)
# ======================================================
st.markdown("""
<style>
.block-container {
    padding-top: 1rem !important;
}

h1 {
    margin-top: -25px !important;
}

.poke-card {
    background: linear-gradient(145deg, #0e1117, #161b22);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #222;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.poke-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 0 30px rgba(77,163,255,0.45);
}

.winner-card {
    border: 2px solid #ffd700 !important;
    box-shadow: 0 0 45px rgba(255,215,0,0.9) !important;
    animation: winnerPulse 1.6s infinite alternate;
}

@keyframes winnerPulse {
    from { box-shadow: 0 0 25px rgba(255,215,0,0.6); }
    to { box-shadow: 0 0 55px rgba(255,215,0,1); }
}

.poke-title {
    background-color: #0d253f;
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    color: #4da3ff;
    margin-bottom: 10px;
}

.poke-img {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

.power-badge {
    background: #162f46;
    color: #ffd166;
    text-align: center;
    padding: 6px;
    border-radius: 8px;
    font-weight: bold;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA & MODEL
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_csv("pokemon_data.csv")
    df['type2'] = df['type2'].fillna("None")
    return df

@st.cache_resource
def load_model():
    return joblib.load("pokemon_battle_model_ultra.pkl")

df = load_data()
model = load_model()

# ======================================================
# FIREWORKS
# ======================================================
def run_fullscreen_fireworks():
    fireworks_html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <style>
        .fireworks-container {
            position: fixed;
            inset: 0;
            z-index: 99999;
            pointer-events: none;
        }
    </style>
    <div class="fireworks-container">
        <lottie-player 
            src="https://assets5.lottiefiles.com/packages/lf20_tiviyc3p.json"
            background="transparent"
            speed="1"
            style="width:100%; height:100%;"
            autoplay>
        </lottie-player>
    </div>
    """
    components.html(fireworks_html, height=0, width=0)

# ======================================================
# TYPE CHART
# ======================================================
type_chart = {
    'fire': {'grass': 2.0, 'water': 0.5},
    'water': {'fire': 2.0, 'grass': 0.5},
    'grass': {'water': 2.0, 'fire': 0.5},
    'electric': {'water': 2.0, 'ground': 0.0},
    'None': {}
}

def get_multiplier(atk, d1, d2):
    m1 = type_chart.get(atk, {}).get(d1, 1.0)
    m2 = 1.0 if d2 == "None" else type_chart.get(atk, {}).get(d2, 1.0)
    return m1 * m2

# ======================================================
# SESSION STATE
# ======================================================
if "winner" not in st.session_state:
    st.session_state.winner = None

# ======================================================
# HEADER
# ======================================================
st.markdown("""
<h1 style="text-align:center;">⚡ AI Pokémon Battle Predictor ⚡</h1>
<p style="text-align:center; color:#cfcfcf;">
Select two Pokémon and let the <b>AI Model</b> predict the winner!
</p>
""", unsafe_allow_html=True)

# ======================================================
# LAYOUT
# ======================================================
col1, col2, col3 = st.columns([1, 0.2, 1])

# ---------------- PLAYER 1 ----------------
with col1:
    st.header("Player 1")
    p1 = st.selectbox("Choose Pokémon 1", df['name'], index=24)
    d1 = df[df['name'] == p1].iloc[0]

    glow1 = "winner-card" if st.session_state.winner == p1 else ""

    st.markdown(f"""
    <div class="poke-card {glow1}">
        <div class="poke-img">
            <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{d1['id']}.png" width="160">
        </div>
        <div class="poke-title">{p1.upper()}</div>
        <div>Type: {d1['type1']} / {d1['type2']}</div>
        <div class="power-badge">⚡ TOTAL POWER: {d1['total_power']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(int(d1['hp']/255*100), f"HP: {d1['hp']}")
    st.progress(int(d1['attack']/190*100), f"Attack: {d1['attack']}")
    st.progress(int(d1['defense']/230*100), f"Defense: {d1['defense']}")

# ---------------- VS ----------------
with col2:
    st.markdown("<h1 style='text-align:center; margin-top:130px;'>VS</h1>", unsafe_allow_html=True)

# ---------------- PLAYER 2 ----------------
with col3:
    st.header("Player 2")
    p2 = st.selectbox("Choose Pokémon 2", df['name'], index=5)
    d2 = df[df['name'] == p2].iloc[0]

    glow2 = "winner-card" if st.session_state.winner == p2 else ""

    st.markdown(f"""
    <div class="poke-card {glow2}">
        <div class="poke-img">
            <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{d2['id']}.png" width="160">
        </div>
        <div class="poke-title">{p2.upper()}</div>
        <div>Type: {d2['type1']} / {d2['type2']}</div>
        <div class="power-badge">⚡ TOTAL POWER: {d2['total_power']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(int(d2['hp']/255*100), f"HP: {d2['hp']}")
    st.progress(int(d2['attack']/190*100), f"Attack: {d2['attack']}")
    st.progress(int(d2['defense']/230*100), f"Defense: {d2['defense']}")

# ======================================================
# PREDICTION
# ======================================================
st.divider()

if st.button("🔥 PREDICT WINNER 🔥", use_container_width=True):
    if p1 == p2:
        st.error("⚠️ Machi rendume same Pokémon da!")
        st.stop()

    m1 = get_multiplier(d1['type1'], d2['type1'], d2['type2'])
    m2 = get_multiplier(d2['type1'], d1['type1'], d1['type2'])

    X = pd.DataFrame([{
        "hp_diff": d1['hp'] - d2['hp'],
        "atk_diff": d1['attack'] - d2['attack'],
        "def_diff": d1['defense'] - d2['defense'],
        "spd_diff": d1['speed'] - d2['speed'],
        "total_power_diff": d1['total_power'] - d2['total_power'],
        "p1_real_advantage": m1,
        "p2_real_advantage": m2
    }])

    pred = model.predict(X)[0]
    probs = model.predict_proba(X)[0]

    winner = p1 if pred == 0 else p2
    confidence = probs[pred] * 100

    st.session_state.winner = winner

    st.success(f"🏆 WINNER: **{winner.upper()}**")
    st.metric("AI Confidence", f"{confidence:.1f}%")

    random.choice([st.balloons, run_fullscreen_fireworks])()
