// DOM Elements
const form = document.getElementById('prediction-form');
const predictBtn = document.getElementById('predict-btn');
const resultCard = document.getElementById('result-card');
const resultContent = document.getElementById('result-content');
const predictedPrice = document.getElementById('predicted-price');
const confidenceFill = document.getElementById('confidence-fill');
const confidenceValue = document.getElementById('confidence-value');
const accuracyStat = document.getElementById('accuracy-stat');
const trainAccuracy = document.getElementById('train-accuracy');
const testAccuracy = document.getElementById('test-accuracy');

// Load model stats on page load
window.addEventListener('DOMContentLoaded', async () => {
    await loadModelStats();
    await loadOptions();
});

// Load model statistics
async function loadModelStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        const testScore = (data.test_score * 100).toFixed(1);
        const trainScore = (data.train_score * 100).toFixed(1);

        accuracyStat.textContent = `${testScore}%`;
        trainAccuracy.textContent = `${trainScore}%`;
        testAccuracy.textContent = `${testScore}%`;

        // Animate the stats
        animateValue(accuracyStat, 0, parseFloat(testScore), 1500, '%');
        animateValue(trainAccuracy, 0, parseFloat(trainScore), 1500, '%');
        animateValue(testAccuracy, 0, parseFloat(testScore), 1500, '%');

    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load dropdown options
async function loadOptions() {
    try {
        const response = await fetch('/api/options');
        const options = await response.json();

        // Populate dropdowns
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

// Populate select element
function populateSelect(elementId, options) {
    const select = document.getElementById(elementId);
    const currentValue = select.value;

    // Clear existing options except the first one
    while (select.options.length > 1) {
        select.remove(1);
    }

    // Add new options
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option.charAt(0).toUpperCase() + option.slice(1);
        select.appendChild(optionElement);
    });

    // Restore previous value if it exists
    if (currentValue && options.includes(currentValue)) {
        select.value = currentValue;
    } else if (options.length > 0) {
        select.selectedIndex = 1; // Select first actual option
    }
}

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Show loading state
    predictBtn.classList.add('loading');
    predictBtn.disabled = true;
    const btnText = predictBtn.querySelector('.btn-text');
    const originalText = btnText.textContent;
    btnText.textContent = 'Predicting...';

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
        predictBtn.classList.remove('loading');
        predictBtn.disabled = false;
        btnText.textContent = originalText;
    }
});

// Display prediction result
function displayResult(price) {
    // Hide placeholder, show result
    const placeholder = resultCard.querySelector('.result-placeholder');
    placeholder.style.display = 'none';
    resultContent.style.display = 'block';

    // Animate price
    animateValue(predictedPrice, 0, price, 1000, '', true);

    // Set confidence (based on model accuracy)
    const confidence = 85; // You can calculate this based on model stats
    confidenceFill.style.width = `${confidence}%`;
    confidenceValue.textContent = `${confidence}%`;

    // Scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Add success animation
    resultCard.style.animation = 'none';
    setTimeout(() => {
        resultCard.style.animation = 'priceReveal 0.6s ease-out';
    }, 10);
}

// Show error message
function showError(message) {
    alert(`Error: ${message}`);
}

// Reset form
function resetForm() {
    form.reset();
    const placeholder = resultCard.querySelector('.result-placeholder');
    placeholder.style.display = 'block';
    resultContent.style.display = 'none';

    // Scroll to form
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

// Add input validation and formatting
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function () {
        // Remove invalid characters
        this.value = this.value.replace(/[^0-9.]/g, '');

        // Ensure only one decimal point
        const parts = this.value.split('.');
        if (parts.length > 2) {
            this.value = parts[0] + '.' + parts.slice(1).join('');
        }
    });

    // Add focus effect
    input.addEventListener('focus', function () {
        this.parentElement.style.transform = 'scale(1.02)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });

    input.addEventListener('blur', function () {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Add hover effects to form sections
document.querySelectorAll('.form-section').forEach(section => {
    section.addEventListener('mouseenter', function () {
        this.style.transition = 'all 0.3s ease';
        this.style.transform = 'translateX(5px)';
    });

    section.addEventListener('mouseleave', function () {
        this.style.transform = 'translateX(0)';
    });
});

// Parallax effect for background
let ticking = false;

window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            const scrolled = window.pageYOffset;
            const bgGradient = document.querySelector('.bg-gradient');
            if (bgGradient) {
                bgGradient.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
            ticking = false;
        });
        ticking = true;
    }
});

// Add loading skeleton for stats
function showStatsSkeleton() {
    accuracyStat.textContent = '--';
    trainAccuracy.textContent = '--';
    testAccuracy.textContent = '--';
}

// Initialize
showStatsSkeleton();

// Add form auto-save to localStorage (optional enhancement)
const STORAGE_KEY = 'automobile_prediction_form';

function saveFormData() {
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function loadFormData() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        try {
            const data = JSON.parse(saved);
            Object.keys(data).forEach(key => {
                const element = form.elements[key];
                if (element) {
                    element.value = data[key];
                }
            });
        } catch (error) {
            console.error('Error loading saved form data:', error);
        }
    }
}

// Auto-save form data on change
form.addEventListener('change', saveFormData);

// Load saved form data on page load (optional - commented out by default)
// loadFormData();
