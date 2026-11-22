import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from energy_predictor import predict_demand

st.set_page_config(
    page_title="GreenGrid AI | Smart Energy Manager",
    page_icon="🌱",
    layout="wide"
)

# ---------- Page styling ----------
st.markdown("""
<style>
    .main-title {font-size: 2.25rem; font-weight: 800; margin-bottom: 0;}
    .sub-title {color: #7b8794; margin-top: 0.2rem;}
    .metric-card {
        background: rgba(120, 130, 140, 0.10);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(120, 130, 140, 0.18);
    }
    .source-pill {
        display: inline-block; padding: 7px 13px; border-radius: 20px;
        font-weight: 700; background: rgba(25, 135, 84, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# ---------- Decision engine ----------
def choose_source(solar_w, demand_w, battery_soc, grid_available, mode, manual_source):
    """Simulation decision logic. This is not a trained ML model."""
    solar_can_supply = solar_w >= demand_w and solar_w > 0
    battery_available = battery_soc > 10

    if mode == "Manual":
        if manual_source == "Solar" and solar_can_supply:
            return "Solar", "Manual selection: solar can meet the simulated load."
        if manual_source == "Battery" and battery_available:
            return "Battery", "Manual selection: battery output is available."
        if manual_source == "Grid" and grid_available:
            return "Grid", "Manual selection: grid supply is available."
        # Safe fallback if requested source is unavailable
        if solar_can_supply:
            return "Solar", "Requested source unavailable; fallback to solar."
        if battery_available:
            return "Battery", "Requested source unavailable; fallback to battery."
        if grid_available:
            return "Grid", "Requested source unavailable; fallback to grid."
        return "No source", "No source is currently available."

    if mode == "Solar-first":
        if solar_can_supply:
            return "Solar", "Solar generation is sufficient for the simulated load."
        if battery_available:
            return "Battery", "Solar is insufficient; battery is available."
        if grid_available:
            return "Grid", "Solar and battery cannot supply the load; using grid."
        return "No source", "No source is currently available."

    if mode == "Grid-first":
        if grid_available:
            return "Grid", "Grid-first mode is enabled and grid supply is available."
        if solar_can_supply:
            return "Solar", "Grid is unavailable; solar can supply the load."
        if battery_available:
            return "Battery", "Grid and solar are unavailable; using battery."
        return "No source", "No source is currently available."

    # AUTO mode: renewable source first, then battery, then grid
    if solar_can_supply:
        return "Solar", "Solar generation is sufficient; renewable energy is prioritised."
    if battery_available:
        return "Battery", "Solar is insufficient; battery is used before grid power."
    if grid_available:
        return "Grid", "Solar and battery are unavailable; switching to grid."
    return "No source", "No source is currently available."

# ---------- Header ----------
st.markdown('<p class="main-title">🌱 GreenGrid AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Smart Energy Source Selection & Management — Software Prototype</p>',
    unsafe_allow_html=True
)
st.divider()

# ---------- Sidebar controls ----------
st.sidebar.header("⚙️ Energy Inputs")
st.sidebar.caption("Change these values to simulate different energy conditions.")

solar_w = st.sidebar.slider("Solar generation (W)", 0, 600, 250, 10)
battery_soc = st.sidebar.slider("Battery charge (%)", 0, 100, 75, 5)
demand_w = st.sidebar.slider("Household demand (W)", 50, 500, 150, 10)
grid_available = st.sidebar.toggle("Grid supply available", value=True)

st.sidebar.divider()
mode = st.sidebar.selectbox(
    "Operating mode",
    ["Auto", "Solar-first", "Grid-first", "Manual"],
    help="Auto prioritises solar, then battery, then grid."
)
manual_source = "Solar"
if mode == "Manual":
    manual_source = st.sidebar.selectbox("Choose source", ["Solar", "Battery", "Grid"])

# ---------- Compute selected source ----------
selected_source, reason = choose_source(
    solar_w, demand_w, battery_soc, grid_available, mode, manual_source
)

if selected_source == "Solar":
    source_color = "green"
    source_icon = "☀️"
elif selected_source == "Battery":
    source_color = "orange"
    source_icon = "🔋"
elif selected_source == "Grid":
    source_color = "blue"
    source_icon = "⚡"
else:
    source_color = "red"
    source_icon = "⛔"

# Approximate illustrative values for the software demonstration only
grid_tariff = 8.0  # ₹ per kWh, editable project assumption
solar_cost = 0.0
battery_cost = 2.0  # illustrative wear-cost assumption, not a market tariff
if selected_source == "Solar":
    estimated_cost_per_hour = (demand_w / 1000) * solar_cost
elif selected_source == "Battery":
    estimated_cost_per_hour = (demand_w / 1000) * battery_cost
elif selected_source == "Grid":
    estimated_cost_per_hour = (demand_w / 1000) * grid_tariff
else:
    estimated_cost_per_hour = 0.0

# ---------- Session history ----------
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("➕ Record this simulation", type="primary"):
    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Solar (W)": solar_w,
        "Battery (%)": battery_soc,
        "Demand (W)": demand_w,
        "Selected source": selected_source,
        "Estimated cost (₹/hour)": round(estimated_cost_per_hour, 2)
    })
    st.success("Simulation recorded.")

# ---------- Main metrics ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Solar generation", f"{solar_w} W")
c2.metric("Battery level", f"{battery_soc}%")
c3.metric("Household demand", f"{demand_w} W")
c4.metric("Selected source", f"{source_icon} {selected_source}")

st.markdown("### 🔌 Energy source decision")
if selected_source == "No source":
    st.error(reason)
else:
    st.success(f"**{selected_source} selected.** {reason}")

left, right = st.columns([1.15, 1])
with left:
    st.markdown("#### Source availability")
    availability = pd.DataFrame({
        "Source": ["Solar", "Battery", "Grid"],
        "Status": [
            "Can meet load" if solar_w >= demand_w and solar_w > 0 else "Insufficient",
            "Available" if battery_soc > 10 else "Low / unavailable",
            "Available" if grid_available else "Unavailable"
        ],
        "Illustrative value": [solar_w, battery_soc, int(grid_available)]
    })
    st.dataframe(availability[["Source", "Status"]], use_container_width=True, hide_index=True)

with right:
    st.markdown("#### Estimated operating cost")
    st.metric("Estimated cost per hour", f"₹{estimated_cost_per_hour:.2f}")
    st.caption(
        "Illustrative assumptions: solar ₹0/kWh, battery wear ₹2/kWh, "
        "grid ₹8/kWh. Replace these with locally researched project values."
    )

st.divider()

# ---------- Charts ----------
chart_left, chart_right = st.columns(2)
with chart_left:
    st.markdown("### Energy availability")
    energy_df = pd.DataFrame({
        "Input": ["Solar generation", "Household demand"],
        "Power (W)": [solar_w, demand_w]
    })
    fig = px.bar(
        energy_df, x="Input", y="Power (W)", color="Input",
        title="Solar generation compared with demand"
    )
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, use_container_width=True)

with chart_right:
    st.markdown("### Battery status")
    battery_df = pd.DataFrame({
        "Status": ["Charge available", "Remaining to 100%"],
        "Percentage": [battery_soc, 100 - battery_soc]
    })
    fig2 = px.pie(
        battery_df, names="Status", values="Percentage", hole=0.58,
        title="Simulated battery state of charge"
    )
    fig2.update_layout(margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig2, use_container_width=True)

# ---------- History ----------
st.divider()
st.markdown("### 📊 Simulation history")
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download history as CSV",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="greengrid_simulation_history.csv",
        mime="text/csv"
    )
    if st.button("Clear simulation history"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("No simulations recorded yet. Change the inputs and click 'Record this simulation'.")

# ---------- Project notes ----------
with st.expander("About this prototype — useful for project evaluation"):
    st.write(
        "This first software version demonstrates energy-source selection using "
        "transparent decision rules and simulated inputs. It is not yet a trained "
        "machine-learning model and it does not control physical hardware. "
        "The next development stage is to connect sensor readings from an ESP32, "
        "then add data-based solar/demand forecasting and evaluate the model."
    )

st.caption("GreenGrid AI | Academic prototype | Simulated values — not live electrical measurements")
# ---------- AI Demand Prediction ----------

st.header("🤖 AI Energy Demand Prediction")

st.write("Predict household energy demand using a Random Forest model.")

col1, col2, col3 = st.columns(3)

with col1:
    hour = st.slider("Hour of the day", 0, 23, 18)

with col2:
    temperature = st.slider("Temperature (°C)", 10, 45, 27)

with col3:
    previous_demand = st.number_input(
        "Previous demand (W)",
        min_value=0,
        max_value=1000,
        value=300
    )

if st.button("Predict Energy Demand"):
    prediction = predict_demand(hour, temperature, previous_demand)

    st.success(f"Predicted Energy Demand: {prediction} W")