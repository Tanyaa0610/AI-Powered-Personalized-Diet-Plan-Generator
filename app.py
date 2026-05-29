import streamlit as st
import json
import os

# Import your existing functions
from agents.validator import validate_input
from agents.researcher import get_research
from agents.nutritionist import generate_diet
from agents.analyzer import analyze_nutrition
from agents.recipe import generate_recipes
from agents.allergen import filter_allergens
from agents.aggregator import aggregate
from agents.json_validator import validate_json
from agents.file_generator import save_files

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="NutriAI – Personalised Diet Planner",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========================
# CUSTOM CSS
# ========================
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Palette ── */
:root {
    --bg:          #F7F5F0;
    --surface:     #FFFFFF;
    --border:      #E2DDD6;
    --green-deep:  #1E4035;
    --green-mid:   #2D6A4F;
    --green-light: #52B788;
    --green-pale:  #D8F3DC;
    --amber:       #C9A84C;
    --amber-pale:  #FDF3DC;
    --text-dark:   #1A1A18;
    --text-mid:    #4A4A45;
    --text-light:  #8A8A82;
    --red-pale:    #FDECEA;
    --red:         #C0392B;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text-dark);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem !important; max-width: 720px !important; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-pill {
    display: inline-block;
    background: var(--green-pale);
    color: var(--green-mid);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    line-height: 1.15;
    color: var(--green-deep);
    margin: 0 0 0.75rem;
}
.hero h1 em {
    font-style: italic;
    color: var(--green-light);
}
.hero p {
    font-size: 1rem;
    color: var(--text-mid);
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
}

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 12px rgba(30,64,53,0.05);
}
.card-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--green-mid);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}
.card-title::before {
    content: '';
    display: inline-block;
    width: 10px;
    height: 2px;
    background: var(--green-light);
    border-radius: 2px;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text-mid) !important;
    margin-bottom: 0.15rem !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg) !important;
    color: var(--text-dark) !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 0.85rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--green-light) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.15) !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg) !important;
}

/* ── BMI Strip ── */
.bmi-strip {
    background: var(--green-pale);
    border: 1px solid #B7E4C7;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
    color: var(--green-deep);
    margin-top: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.bmi-value { font-weight: 700; font-size: 1rem; }

/* ── Goal Pills ── */
.goal-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.5rem; }
.goal-pill {
    padding: 0.45rem 1rem;
    border-radius: 999px;
    border: 1.5px solid var(--border);
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.15s;
    background: var(--bg);
    color: var(--text-mid);
}

/* ── CTA Button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: var(--green-deep) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s !important;
    box-shadow: 0 4px 16px rgba(30,64,53,0.25) !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--green-mid) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Progress / Spinner ── */
div[data-testid="stSpinner"] {
    background: var(--amber-pale);
    border: 1px solid #F0DC9A;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: var(--text-mid);
    font-size: 0.88rem;
}

/* ── Success Banner ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
}

/* ── Result Sections ── */
.result-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--green-deep);
    margin: 2rem 0 0.25rem;
}
.result-sub {
    font-size: 0.85rem;
    color: var(--text-light);
    margin-bottom: 1.5rem;
}

.result-card {
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid transparent;
}
.result-card.eat {
    background: var(--green-pale);
    border-color: #B7E4C7;
}
.result-card.avoid {
    background: var(--red-pale);
    border-color: #F5C6C0;
}
.result-card h4 {
    margin: 0 0 0.6rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.result-card.eat h4 { color: var(--green-mid); }
.result-card.avoid h4 { color: var(--red); }
.result-card p {
    font-size: 0.93rem;
    color: var(--text-dark);
    line-height: 1.6;
    margin: 0;
}

/* ── Download Buttons ── */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--green-deep) !important;
    border: 1.5px solid var(--green-deep) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.15s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--green-deep) !important;
    color: #fff !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

/* ── Column gap fix ── */
[data-testid="column"] { padding: 0 0.3rem !important; }
</style>
""", unsafe_allow_html=True)

# ========================
# HERO
# ========================
st.markdown("""
<div class="hero">
    <div class="hero-pill">🌿 AI-Powered Nutrition</div>
    <h1>Your <em>personalised</em><br>diet plan, instantly</h1>
    <p>Enter a few details to generate a medically-aware meal plan tailored to your body and goals.</p>
</div>
""", unsafe_allow_html=True)

# ========================
# SECTION 1 — BODY METRICS
# ========================
st.markdown('<div class="card"><div class="card-title">Body Metrics</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=100, value=25, step=1)
with col2:
    weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70, step=1)
with col3:
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, step=1)

# Live BMI
if height > 0 and weight > 0:
    bmi = round(weight / ((height / 100) ** 2), 1)
    if bmi < 18.5:
        bmi_label = "Underweight"
        bmi_color = "#3498DB"
    elif bmi < 25:
        bmi_label = "Healthy weight ✓"
        bmi_color = "#27AE60"
    elif bmi < 30:
        bmi_label = "Overweight"
        bmi_color = "#E67E22"
    else:
        bmi_label = "Obese"
        bmi_color = "#C0392B"

    st.markdown(f"""
    <div class="bmi-strip">
        <span>Body Mass Index (BMI)</span>
        <span class="bmi-value" style="color:{bmi_color}">{bmi} — {bmi_label}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========================
# SECTION 2 — HEALTH PROFILE
# ========================
st.markdown('<div class="card"><div class="card-title">Health Profile</div>', unsafe_allow_html=True)

disease = st.text_input(
    "Medical condition or disease",
    placeholder="e.g. Type 2 Diabetes, Hypertension, PCOS, Obesity…"
)

col_a, col_b = st.columns(2)
with col_a:
    allergies = st.text_input(
        "Food allergies",
        placeholder="e.g. nuts, gluten, dairy…"
    )
with col_b:
    deficiencies = st.text_input(
        "Nutritional deficiencies",
        placeholder="e.g. Vitamin D, Iron, B12…"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ========================
# SECTION 3 — GOAL
# ========================
st.markdown('<div class="card"><div class="card-title">Primary Goal</div>', unsafe_allow_html=True)

goal = st.selectbox(
    "What are you aiming for?",
    ["Weight Loss", "Muscle Gain", "Maintenance"],
    format_func=lambda x: {
        "Weight Loss":  "⚖️  Weight Loss — reduce body fat sustainably",
        "Muscle Gain":  "💪  Muscle Gain — build lean muscle mass",
        "Maintenance":  "🧘  Maintenance — stay balanced and healthy"
    }[x]
)
goal_value = goal.lower()

st.markdown('</div>', unsafe_allow_html=True)

# ========================
# GENERATE BUTTON
# ========================
st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
generate = st.button("✦  Generate My Diet Plan", use_container_width=True)

# ========================
# GENERATION PIPELINE
# ========================
if generate:
    if not disease.strip():
        st.error("⚠️  Please enter a medical condition or disease to continue.")
        st.stop()

    steps = [
        "Validating your health profile…",
        "Researching disease-specific dietary guidelines…",
        "Crafting your personalised meal plan…",
        "Analysing macro & micronutrient balance…",
        "Filtering allergens from your plan…",
        "Aggregating final recommendations…",
        "Validating output integrity…",
        "Generating downloadable files…",
    ]

    progress_bar = st.progress(0)
    status_text  = st.empty()

    def update_progress(step_index, total=len(steps)):
        progress_bar.progress(int((step_index / total) * 100))
        status_text.markdown(
            f"<p style='font-size:0.83rem;color:#4A4A45;margin:0.3rem 0 0.8rem;'>"
            f"Step {step_index}/{total} — {steps[step_index-1]}</p>",
            unsafe_allow_html=True
        )

    try:
        # T1
        update_progress(1)
        user = validate_input(
            disease,
            allergies,
            age=age,
            weight=weight,
            height=height,
            deficiencies=deficiencies,
            goal=goal_value
        )

        # T2
        update_progress(2)
        research = get_research(user["disease"])
        if not research:
            progress_bar.empty()
            status_text.empty()
            st.error("⚠️  Disease not found in our research database. Please try a different term.")
            st.stop()

        # T3
        update_progress(3)
        diet = generate_diet(research, user)

        # T4
        update_progress(4)
        nutrition = analyze_nutrition(user)
        recipes   = generate_recipes()

        # T5
        update_progress(5)
        diet = filter_allergens(diet, user["allergies"])

        # T6
        update_progress(6)
        final = aggregate(user["disease"], diet, nutrition, recipes)

        # T7
        update_progress(7)
        if not validate_json(final):
            progress_bar.empty()
            status_text.empty()
            st.error("⚠️  An error occurred while validating the generated plan. Please try again.")
            st.stop()

        # T8
        update_progress(8)
        json_file, pdf_file = save_files(final)

        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Something went wrong: {e}")
        st.stop()

    # ========================
    # SUCCESS STATE
    # ========================
    st.markdown("""
    <div style="
        background: #D8F3DC;
        border: 1px solid #B7E4C7;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    ">
        <span style="font-size:1.2rem">✅</span>
        <span style="font-size:0.9rem;color:#1E4035;font-weight:500;">
            Your personalised diet plan is ready!
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ========================
    # RESULTS PREVIEW
    # ========================
    st.markdown('<div class="result-header">Your Diet Plan</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-sub">Personalised for {disease.title()} · Goal: {goal} · BMI {bmi}</div>',
        unsafe_allow_html=True
    )

    eat_items   = final.get("diet", {}).get("eat",   [])
    avoid_items = final.get("diet", {}).get("avoid", [])

    eat_text   = ", ".join(eat_items)   if isinstance(eat_items,   list) else str(eat_items)
    avoid_text = ", ".join(avoid_items) if isinstance(avoid_items, list) else str(avoid_items)

    col_eat, col_avoid = st.columns(2)

    with col_eat:
        st.markdown(f"""
        <div class="result-card eat">
            <h4>✅ Recommended Foods</h4>
            <p>{eat_text if eat_text else "See your full plan in the PDF."}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_avoid:
        st.markdown(f"""
        <div class="result-card avoid">
            <h4>🚫 Foods to Avoid</h4>
            <p>{avoid_text if avoid_text else "See your full plan in the PDF."}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Additional insight tiles ──
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    tile_cols = st.columns(3)
    tiles = [
        ("🥗", "Recipes", f"{len(final.get('recipes', []))} personalised recipes included"),
        ("📊", "Nutrition",  "Macro & micronutrient targets calculated"),
        ("🚫", "Allergens",  f"Filtered for: {allergies if allergies else 'none specified'}"),
    ]
    for col, (icon, label, desc) in zip(tile_cols, tiles):
        with col:
            st.markdown(f"""
            <div style="
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
            ">
                <div style="font-size:1.4rem">{icon}</div>
                <div style="font-size:0.78rem;font-weight:600;color:var(--green-mid);
                            margin:0.3rem 0 0.2rem;text-transform:uppercase;letter-spacing:0.08em">{label}</div>
                <div style="font-size:0.78rem;color:var(--text-light);line-height:1.4">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ========================
    # DOWNLOADS
    # ========================
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem;font-weight:600;letter-spacing:0.14em;
                text-transform:uppercase;color:var(--green-mid);margin-bottom:0.9rem;">
        ⬇ Download Your Plan
    </div>
    """, unsafe_allow_html=True)

    dl_col1, dl_col2, spacer = st.columns([1, 1, 1])

    with dl_col1:
        with open(json_file, "rb") as f:
            st.download_button(
                label="📄  JSON Data",
                data=f,
                file_name="diet_plan.json",
                mime="application/json",
                use_container_width=True
            )

    with dl_col2:
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📑  Full PDF Report",
                data=f,
                file_name="diet_plan.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ========================
# FOOTER
# ========================
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;color:#B0AEA8;font-size:0.78rem;">
    NutriAI · 
</div>
""", unsafe_allow_html=True)