from flask import Flask, render_template, jsonify, request
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    angle_deg = float(data.get('angle', 30))
    show_tan = data.get('show_tan', True)
    
    # Convert to radians
    angle_rad = np.deg2rad(angle_deg)
    
    # Current trig values
    sin_val = float(np.sin(angle_rad))
    cos_val = float(np.cos(angle_rad))
    tan_val = float(np.tan(angle_rad))
    
    # Generate unit circle plot
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    theta = np.linspace(0, 2 * np.pi, 400)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax1.plot(x_circle, y_circle, 'b-', linewidth=2)
    
    # Axes
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    
    # Point on circle
    x = cos_val
    y = sin_val
    ax1.scatter([x], [y], color='red', s=100, zorder=5)
    ax1.plot([0, x], [0, y], 'r-', linewidth=2, label=f'θ = {angle_deg}°')
    
    # Projections for sine and cosine
    ax1.plot([x, x], [0, y], 'g--', linewidth=1, label=f'sin θ = {sin_val:.3f}')
    ax1.plot([0, x], [y, y], 'b--', linewidth=1, label=f'cos θ = {cos_val:.3f}')
    
    ax1.set_aspect('equal', 'box')
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_xlabel('x (cos θ)', fontsize=12)
    ax1.set_ylabel('y (sin θ)', fontsize=12)
    ax1.set_title(f'Unit Circle – θ = {angle_deg}°', fontsize=14, fontweight='bold')
    ax1.grid(alpha=0.3)
    ax1.legend(loc='upper right')
    
    # Convert plot to base64
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', dpi=100, bbox_inches='tight')
    buf1.seek(0)
    circle_img = base64.b64encode(buf1.read()).decode('utf-8')
    plt.close(fig1)
    
    # Generate trig function plot
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    x_deg = np.linspace(0, 360, 1000)
    x_rad = np.deg2rad(x_deg)
    
    sin_y = np.sin(x_rad)
    cos_y = np.cos(x_rad)
    tan_y = np.tan(x_rad)
    
    # Limit tangent so the plot doesn't blow up
    tan_y_plot = tan_y.copy()
    tan_y_plot[np.abs(tan_y_plot) > 4] = np.nan
    
    ax2.plot(x_deg, sin_y, label='sin θ', linewidth=2)
    ax2.plot(x_deg, cos_y, label='cos θ', linewidth=2)
    
    if show_tan:
        ax2.plot(x_deg, tan_y_plot, label='tan θ', linestyle=':', linewidth=2)
    
    # Vertical line at current angle
    ax2.axvline(angle_deg, color='k', linewidth=2, linestyle='--', label=f'θ = {angle_deg}°')
    
    ax2.set_xlim(0, 360)
    ax2.set_xlabel('Angle θ (degrees)', fontsize=12)
    ax2.set_ylabel('Value', fontsize=12)
    ax2.set_title('Trig Functions from 0° to 360°', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.legend(loc='upper right')
    
    # Convert plot to base64
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', dpi=100, bbox_inches='tight')
    buf2.seek(0)
    graph_img = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close(fig2)
    
    # Determine quadrant
    def angle_quadrant(deg):
        a = deg % 360
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
    
    return jsonify({
        'sin': sin_val,
        'cos': cos_val,
        'tan': tan_val if np.isfinite(tan_val) else None,
        'quadrant': angle_quadrant(angle_deg),
        'circle_img': circle_img,
        'graph_img': graph_img
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
