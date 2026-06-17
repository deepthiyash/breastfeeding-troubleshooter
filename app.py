import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="LatchCare Assistant",
    page_icon="🤱",
    layout="centered"
)

DATA_PATH = Path(__file__).parent / "data" / "guidance.json"

@st.cache_data
def load_guidance():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

guidance = load_guidance()

st.title("🤱 LatchCare Assistant")
st.caption("Educational breastfeeding support. Not a medical diagnosis.")

st.warning(
    "This tool gives general education only. If mother or baby has fever, severe pain, poor feeding, dehydration signs, "
    "blood in milk, breathing difficulty, jaundice, or baby has fewer wet diapers than expected, contact a doctor or lactation consultant."
)

issue = st.selectbox("What is the main issue?", list(guidance.keys()))

st.subheader("Quick questions")

pain_level = st.slider("Pain level during feeding", 0, 10, 3)

baby_age = st.selectbox(
    "Baby age",
    ["0–7 days", "1–4 weeks", "1–3 months", "3+ months"]
)

wet_diapers = st.selectbox(
    "Wet diapers in the last 24 hours",
    ["Less than 4", "4–5", "6 or more", "Not sure"]
)

feeding_frequency = st.selectbox(
    "How many times is baby feeding in 24 hours?",
    ["Less than 6", "6–8", "8–12", "More than 12", "Not sure"]
)

baby_weight = st.radio(
    "Any concern about baby weight gain?",
    ["No", "Yes", "Not sure"]
)

nipple_shape = st.selectbox(
    "How does the nipple look after feeding?",
    ["Normal/round", "Pinched/lipstick shape", "Cracked/bleeding", "Not sure"]
)

fever = st.radio(
    "Any fever, red painful breast area, or flu-like symptoms?",
    ["No", "Yes"]
)

baby_sleepy = st.radio(
    "Is baby too sleepy or not actively sucking?",
    ["No", "Yes"]
)

if st.button("Get guidance"):
    item = guidance[issue]
    red_flags = []

    if feeding_frequency == "Less than 6":
        red_flags.append("Very low feeding frequency may affect milk intake, especially in newborns.")

    if baby_weight == "Yes":
        red_flags.append("Weight gain concerns should be reviewed by a pediatrician or lactation consultant.")

    if nipple_shape in ["Pinched/lipstick shape", "Cracked/bleeding"]:
        red_flags.append("Nipple damage often means latch needs to be assessed.")

    if fever == "Yes":
        red_flags.append("Fever, red painful breast area, or flu-like symptoms can need medical review.")

    if wet_diapers == "Less than 4":
        red_flags.append("Fewer than 4 wet diapers can be a dehydration warning sign, especially in a young baby.")

    if pain_level >= 7:
        red_flags.append("Severe pain is not something to ignore. Latch, nipple trauma, infection, or other causes should be checked.")

    if baby_sleepy == "Yes":
        red_flags.append("A very sleepy baby who is not feeding actively should be assessed, especially in the first weeks.")

    st.subheader("What this may mean")
    st.write(item["meaning"])

    st.subheader("What you can try")
    for step in item["steps"]:
        st.write(f"• {step}")

    st.subheader("When to get help")

    if red_flags:
        for flag in red_flags:
            st.error(flag)
        st.write("Please contact a pediatrician, OB/GYN, or certified lactation consultant.")
    else:
        for flag in item["when_to_get_help"]:
            st.write(f"• {flag}")

    st.info(
        "Tip: Track feeding times, diaper counts, baby weight checks, and pain patterns. These details help a lactation consultant quickly identify the real problem."
    )

st.divider()

st.markdown("### Get your free breastfeeding guide")
st.write("Want a free guide and optional 15-minute consultation? Submit your details below.")
st.markdown("[Submit your email here](https://docs.google.com/forms/d/e/1FAIpQLSeyxiQqgo6i3jGkx1OkCfOrZNA1Qdy6jykaac11TPRabBlTHw/viewform?usp=header)")
