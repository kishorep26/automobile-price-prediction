// DOM Elements
const form = document.getElementById('prediction-form');
const analyzeBtn = document.getElementById('analyze-btn');
const resultStandby = document.getElementById('result-standby');
const resultActive = document.getElementById('result-active');
const priceValue = document.getElementById('price-value');
const confidenceBar = document.getElementById('confidence-bar');
const confidencePercent = document.getElementById('confidence-percent');
const accuracyMeter = document.getElementById('accuracy-meter');
const accuracyFill = document.getElementById('accuracy-fill');
const trainStat = document.getElementById('train-stat');
const testStat = document.getElementById('test-stat');
const findingsGrid = document.getElementById('findings-grid');

// Load data on page load
window.addEventListener('DOMContentLoaded', async () => {
    await loadModelStats();
    await loadOptions();
    await loadInsights();
});

// Load model statistics
async function loadModelStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        const testScore = (data.test_score * 100).toFixed(1);
        const trainScore = (data.train_score * 100).toFixed(1);

        // Animate accuracy meter
        animateValue(accuracyMeter, 0, parseFloat(testScore), 2000, '%');
        setTimeout(() => {
            accuracyFill.style.width = `${testScore}%`;
        }, 100);

        // Update quick stats
        animateValue(trainStat, 0, parseFloat(trainScore), 1500, '%');
        animateValue(testStat, 0, parseFloat(testScore), 1500, '%');

    } catch (error) {
        console.error('Error loading stats:', error);
        accuracyMeter.textContent = 'N/A';
        trainStat.textContent = 'N/A';
        testStat.textContent = 'N/A';
    }
}

// Load dropdown options
async function loadOptions() {
    try {
        const response = await fetch('/api/options');
        const options = await response.json();

        populateSelect('make', options['make']);
        populateSelect('fuel_type', options['fuel-type']);
        populateSelect('aspiration', options['aspiration']);
        populateSelect('body_style', options['body-style']);
        populateSelect('drive_wheels', options['drive-wheels']);
        populateSelect('engine_type', options['engine-type']);
        populateSelect('fuel_system', options['fuel-system']);

    } catch (error) {
        console.error('Error loading options:', error);
    }
}

// Load insights from JSON
async function loadInsights() {
    try {
        const response = await fetch('/static/visualizations/insights.json');
        const insights = await response.json();

        // Populate findings
        insights.top_features.forEach(feature => {
            const findingItem = document.createElement('div');
            findingItem.className = 'finding-item';
            findingItem.innerHTML = `
                <div class="finding-name">${feature.name}</div>
                <div class="finding-importance">Importance: ${(feature.importance * 100).toFixed(1)}%</div>
                <div class="finding-desc">${feature.description}</div>
            `;
            findingsGrid.appendChild(findingItem);
        });

    } catch (error) {
        console.error('Error loading insights:', error);
    }
}

// Populate select element
function populateSelect(elementId, options) {
    const select = document.getElementById(elementId);

    // Clear existing options except the first one
    while (select.options.length > 1) {
        select.remove(1);
    }

    // Add new options
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option.toUpperCase();
        select.appendChild(optionElement);
    });

    // Select first option by default
    if (options.length > 0) {
        select.selectedIndex = 1;
    }
}

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Show loading state
    analyzeBtn.classList.add('loading');
    analyzeBtn.disabled = true;
    const btnText = analyzeBtn.querySelector('.btn-text');
    const originalText = btnText.textContent;
    btnText.textContent = 'ANALYZING...';

    try {
        // Gather form data
        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Make prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            displayResult(result.predicted_price);
        } else {
            showError(result.error || 'Prediction failed');
        }

    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server');
    } finally {
        // Reset button state
        analyzeBtn.classList.remove('loading');
        analyzeBtn.disabled = false;
        btnText.textContent = originalText;
    }
});

// Display prediction result
function displayResult(price) {
    // Hide standby, show result
    resultStandby.style.display = 'none';
    resultActive.style.display = 'block';

    // Animate price
    animateValue(priceValue, 0, price, 1500, '', true);

    // Set confidence (based on model accuracy)
    const confidence = 93; // From model test accuracy
    setTimeout(() => {
        confidenceBar.style.width = `${confidence}%`;
        confidencePercent.textContent = `${confidence}%`;
    }, 500);

    // Scroll to result
    document.getElementById('result-display').scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    });
}

// Reset analysis
function resetAnalysis() {
    resultStandby.style.display = 'block';
    resultActive.style.display = 'none';
    confidenceBar.style.width = '0%';

    // Scroll to form
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Show error message
function showError(message) {
    alert(`ERROR: ${message}`);
}

// Animate number value
function animateValue(element, start, end, duration, suffix = '', isPrice = false) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = start + (end - start) * easeOutQuart;

        if (isPrice) {
            element.textContent = formatPrice(current);
        } else {
            element.textContent = current.toFixed(1) + suffix;
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            if (isPrice) {
                element.textContent = formatPrice(end);
            } else {
                element.textContent = end.toFixed(1) + suffix;
            }
        }
    }

    requestAnimationFrame(update);
}

// Format price with commas
function formatPrice(price) {
    return Math.round(price).toLocaleString('en-US');
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add input effects
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('focus', function () {
        this.parentElement.style.transform = 'translateX(3px)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });

    input.addEventListener('blur', function () {
        this.parentElement.style.transform = 'translateX(0)';
    });
});

// Add select effects
document.querySelectorAll('select').forEach(select => {
    select.addEventListener('focus', function () {
        this.parentElement.style.transform = 'translateX(3px)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });

    select.addEventListener('blur', function () {
        this.parentElement.style.transform = 'translateX(0)';
    });
});

// Parallax effect for background
let ticking = false;

window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            const scrolled = window.pageYOffset;
            const speedometerBg = document.querySelector('.speedometer-bg');
            if (speedometerBg) {
                speedometerBg.style.transform = `translate(-50%, -50%) rotate(${scrolled * 0.05}deg)`;
            }
            ticking = false;
        });
        ticking = true;
    }
});

// Initialize
console.log('AutoValuate Pro - ML Model Initialized');
