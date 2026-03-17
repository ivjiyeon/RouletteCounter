import streamlit as st

# Define the set of red numbers
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

# The 8 predefined boxes
BOXES = [
    "LowEvenRed", "LowOddRed", "HighEvenRed", "HighOddRed",
    "LowEvenBlack", "LowOddBlack", "HighEvenBlack", "HighOddBlack"
]

# Initialize session state to hold the counts persistently
if "box_counts" not in st.session_state:
    st.session_state.box_counts = {box: 0 for box in BOXES}

def get_box_category(number):
    """Determine the correct box for a given number."""
    is_low = number <= 18
    is_even = (number % 2 == 0)
    is_red = number in RED_NUMBERS
    
    part1 = "Low" if is_low else "High"
    part2 = "Even" if is_even else "Odd"
    part3 = "Red" if is_red else "Black"
    
    return f"{part1}{part2}{part3}"

def record_number(number):
    """Callback function when a number button is pressed."""
    box_category = get_box_category(number)
    st.session_state.box_counts[box_category] += 1

def reset_all():
    """Reset all box counters back to 0."""
    st.session_state.box_counts = {box: 0 for box in BOXES}

# ---------------- UI LAYOUT ----------------

st.set_page_config(page_title="Roulette Tracker", layout="centered")

# --- DYNAMIC CSS INJECTION ---
# Create grouped CSS selectors for the buttons based on their Streamlit keys
red_selectors = ", ".join([f".st-key-btn_{i} button" for i in RED_NUMBERS])
black_selectors = ", ".join([f".st-key-btn_{i} button" for i in range(1, 37) if i not in RED_NUMBERS])

custom_css = f"""
<style>
/* Styling for Red Number Buttons */
{red_selectors} {{
    background-color: #D32F2F !important;
    color: white !important;
    border: 1px solid #D32F2F !important;
    font-weight: bold;
}}
/* Styling for Black Number Buttons */
{black_selectors} {{
    background-color: #1A1D20 !important;
    color: white !important;
    border: 1px solid #1A1D20 !important;
    font-weight: bold;
}}
/* Hover Effects */
{red_selectors}:hover, {black_selectors}:hover {{
    opacity: 0.8 !important;
    border: 1px solid white !important;
}}
/* --- MOBILE-ONLY GRID OVERRIDE --- */
@media (max-width: 600px) 
.stButton {{
        width: 23% !important;  /* roughly 4 per row */
        display: inline-block !important;
        margin: 2px !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# -----------------------------

st.title("Roulette Number Tracker")

# 1. Number Buttons (1-36)
st.subheader("Select a Number")
cols = st.columns(6)
for i in range(1, 37):
    with cols[(i - 1) % 6]:
        # The key parameter here matches the CSS injected above
        st.button(str(i), key=f"btn_{i}", on_click=record_number, args=(i,), use_container_width=True)

# 2. Box Counters
st.subheader("Box Counters")
box_cols = st.columns(4)
for idx, box in enumerate(BOXES):
    with box_cols[idx % 4]:
        st.metric(label=box, value=st.session_state.box_counts[box])

st.button("Reset All", on_click=reset_all, type="primary")

st.divider()

# 3. Betting Logic Evaluation
boxes_above_1 = [box for box, count in st.session_state.box_counts.items() if count >= 1]
has_box_above_2 = [box for box, count in st.session_state.box_counts.items() if count >= 2] #any(count >= 2 for count in st.session_state.box_counts.values())

if len(boxes_above_1) >= 4 and len(has_box_above_2) >= 1:
    # box_list = ", ".join(has_box_above_2)
    st.success(f"Place your bet on: {has_box_above_2}")
else:
    st.info("No Bets")
