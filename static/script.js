// Global state
let currentAngle = 30;
let showTan = true;

// DOM elements
const angleSlider = document.getElementById('angleSlider');
const angleDisplay = document.getElementById('angleDisplay');
const showTanCheckbox = document.getElementById('showTan');
const sinValue = document.getElementById('sinValue');
const cosValue = document.getElementById('cosValue');
const tanValue = document.getElementById('tanValue');
const angleInfo = document.getElementById('angleInfo');
const quadrantInfo = document.getElementById('quadrantInfo');
const pointInfo = document.getElementById('pointInfo');
const circleImageContainer = document.getElementById('circleImageContainer');
const graphImageContainer = document.getElementById('graphImageContainer');

// Update display
async function updateDisplay() {
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                angle: currentAngle,
                show_tan: showTan
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Update metric values
        sinValue.textContent = data.sin.toFixed(3);
        cosValue.textContent = data.cos.toFixed(3);
        tanValue.textContent = data.tan !== null ? data.tan.toFixed(3) : 'undefined';
        
        // Update angle info
        angleInfo.textContent = `${currentAngle}°`;
        quadrantInfo.textContent = `This angle is ${data.quadrant}.`;
        pointInfo.innerHTML = `On the unit circle, the point is <strong>(cos θ, sin θ) = (${data.cos.toFixed(3)}, ${data.sin.toFixed(3)})</strong>.`;
        
        // Update images
        circleImageContainer.innerHTML = `<img src="data:image/png;base64,${data.circle_img}" alt="Unit Circle">`;
        graphImageContainer.innerHTML = `<img src="data:image/png;base64,${data.graph_img}" alt="Trig Functions Graph">`;
        
    } catch (error) {
        console.error('Error updating display:', error);
        circleImageContainer.innerHTML = '<p style="color: red;">Error loading image</p>';
        graphImageContainer.innerHTML = '<p style="color: red;">Error loading image</p>';
    }
}

// Event listeners
angleSlider.addEventListener('input', (e) => {
    currentAngle = parseInt(e.target.value);
    angleDisplay.textContent = `${currentAngle}°`;
    updateDisplay();
});

showTanCheckbox.addEventListener('change', (e) => {
    showTan = e.target.checked;
    updateDisplay();
});

// Initial load
updateDisplay();
