import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trig Tutor: Sine, Cosine & Tangent", layout="wide")

# --- SIDEBAR CONTROLS ---
st.sidebar.title("Controls")
angle_deg = st.sidebar.slider(
    "Angle (degrees)",
    min_value=0,
    max_value=360,
    value=30,
    step=1,
    help="Move the slider to see how sin, cos and tan change with the angle."
)

show_tan = st.sidebar.checkbox("Show tangent on the graph", value=True)

# Convert to radians
angle_rad = np.deg2rad(angle_deg)

# Current trig values
sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)
tan_val = np.tan(angle_rad)

# --- MAIN TITLE & INTRO ---
st.title("📐 Trig Tutor: Sine, Cosine & Tangent")
st.markdown(
    """
Use the angle slider in the sidebar to see how **sine**, **cosine**, and **tangent**
change. The app shows:
- A **unit circle** with your angle and the point (cos θ, sin θ)
- A **graph of sin, cos (and tan)** from 0° to 360°
- Live numeric values and a short explanation
"""
)

# --- VALUE DISPLAY ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("sin(θ)", f"{sin_val:.3f}")

with col2:
    st.metric("cos(θ)", f"{cos_val:.3f}")

with col3:
    if np.isfinite(tan_val):
        st.metric("tan(θ)", f"{tan_val:.3f}")
    else:
        st.metric("tan(θ)", "undefined")

# Quadrant / explanation
def angle_quadrant(deg: float) -> str:
    # Normalize to [0, 360)
    a = deg % 360
    # Handle axes exactly
    axes = {0: "on the positive x-axis",
            90: "on the positive y-axis",
            180: "on the negative x-axis",
            270: "on the negative y-axis"}
    rounded = int(round(a))
    if rounded in axes and abs(a - rounded) < 1e-6:
        return axes[rounded]

    if 0 < a < 90:
        return "in Quadrant I (sin > 0, cos > 0)"
    elif 90 < a < 180:
        return "in Quadrant II (sin > 0, cos < 0)"
    elif 180 < a < 270:
        return "in Quadrant III (sin < 0, cos < 0)"
    elif 270 < a < 360:
        return "in Quadrant IV (sin < 0, cos > 0)"
    else:
        return "at a special angle on one of the axes"

st.markdown(
    f"""
### Angle: {angle_deg}°

- This angle is **{angle_quadrant(angle_deg)}**.
- On the unit circle, the point is **(cos θ, sin θ) = ({cos_val:.3f}, {sin_val:.3f})**.
- Tangent is defined as **tan θ = sin θ / cos θ**.
"""
)

# --- VISUALS: LAYOUT ---
circle_col, graph_col = st.columns(2)

# --- UNIT CIRCLE PLOT ---
with circle_col:
    st.subheader("Unit Circle View")

    fig1, ax1 = plt.subplots()
    # Draw unit circle
    theta = np.linspace(0, 2 * np.pi, 400)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax1.plot(x_circle, y_circle)

    # Axes
    ax1.axhline(0, linewidth=0.5)
    ax1.axvline(0, linewidth=0.5)

    # Point on circle
    x = cos_val
    y = sin_val
    ax1.scatter([x], [y])
    ax1.plot([0, x], [0, y])  # radius line

    # Projections for sine and cosine
    # cosine projection to x-axis
    ax1.plot([x, x], [0, y], linestyle="--", linewidth=1)
    # sine projection to y-axis
    ax1.plot([0, x], [y, y], linestyle="--", linewidth=1)

    ax1.set_aspect("equal", "box")
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_xlabel("x (cos θ)")
    ax1.set_ylabel("y (sin θ)")
    ax1.set_title(f"Unit Circle – θ = {angle_deg}°")
    ax1.grid(alpha=0.3)

    st.pyplot(fig1)

# --- TRIG FUNCTION PLOT ---
with graph_col:
    st.subheader("Graphs of sin θ, cos θ and tan θ")

    x_deg = np.linspace(0, 360, 1000)
    x_rad = np.deg2rad(x_deg)

    sin_y = np.sin(x_rad)
    cos_y = np.cos(x_rad)
    tan_y = np.tan(x_rad)

    # Limit tangent so the plot doesn't blow up near 90°, 270°
    tan_y_plot = tan_y.copy()
    tan_y_plot[np.abs(tan_y_plot) > 4] = np.nan

    fig2, ax2 = plt.subplots()
    ax2.plot(x_deg, sin_y, label="sin θ")
    ax2.plot(x_deg, cos_y, label="cos θ")

    if show_tan:
        ax2.plot(x_deg, tan_y_plot, label="tan θ", linestyle=":")

    # Vertical line at current angle
    ax2.axvline(angle_deg, color="k", linewidth=1, linestyle="--", label=f"θ = {angle_deg}°")

    ax2.set_xlim(0, 360)
    ax2.set_xlabel("Angle θ (degrees)")
    ax2.set_ylabel("Value")
    ax2.set_title("Trig Functions from 0° to 360°")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="upper right")

    st.pyplot(fig2)

st.markdown(
    """
#### How to read this:
- On the **left**, the unit circle shows the point corresponding to your angle.
  - The **x-coordinate** is **cos θ**.
  - The **y-coordinate** is **sin θ**.
- On the **right**, the graph shows how sin θ, cos θ and (optionally) tan θ vary from 0° to 360°.
- The dashed vertical line marks your current angle.
"""
)
