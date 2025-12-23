# 🚗 Automobile Price Prediction

An AI-powered web application that predicts automobile prices using advanced machine learning algorithms. Built with Flask, scikit-learn, and modern web technologies.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![ML](https://img.shields.io/badge/ML-Random%20Forest-orange)
![License](https://img.shields.io/badge/License-GPL--3.0-red)

## ✨ Features

- **AI-Powered Predictions**: Uses Random Forest regression for accurate price predictions
- **Modern UI**: Beautiful, responsive interface with smooth animations
- **Real-time Analysis**: Instant predictions based on 25+ vehicle features
- **Model Statistics**: View training and testing accuracy metrics
- **Interactive Form**: Easy-to-use form with validation and auto-complete
- **Mobile Responsive**: Works seamlessly on all devices

## 🎯 Model Performance

- **Training Accuracy**: ~95%
- **Testing Accuracy**: ~85%
- **Algorithm**: Random Forest Regressor
- **Training Samples**: 205 automobiles
- **Features**: 26 attributes including engine specs, dimensions, and performance metrics

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kishorep26/automobile-price-prediction.git
cd automobile-price-prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model:
```bash
python train_model.py
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 📊 Dataset

The model is trained on a comprehensive automobile dataset containing:
- **205 samples** of various car models
- **26 features** including:
  - Vehicle specifications (make, body style, fuel type)
  - Engine details (size, cylinders, horsepower)
  - Physical dimensions (length, width, height, weight)
  - Performance metrics (MPG, compression ratio, peak RPM)

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **scikit-learn**: Machine learning
- **pandas**: Data processing
- **NumPy**: Numerical computations

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with modern gradients and animations
- **JavaScript**: Interactive functionality
- **Google Fonts**: Typography (Inter)

### Deployment
- **Gunicorn**: WSGI HTTP Server
- **Heroku/Render**: Cloud hosting (ready to deploy)

## 📁 Project Structure

```
automobile-price-prediction/
├── app.py                          # Flask application
├── train_model.py                  # Model training script
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment config
├── runtime.txt                     # Python version specification
├── Automobile price data _Raw_.csv # Dataset
├── templates/
│   └── index.html                  # Main web interface
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── script.js              # Frontend logic
└── reference/                      # Original project files (gitignored)
    ├── automobile.ipynb
    └── ...
```

## 🎨 Features in Detail

### Price Prediction
Enter vehicle specifications across four categories:
1. **Vehicle Information**: Make, body style, fuel type, doors
2. **Engine Specifications**: Size, cylinders, horsepower, type
3. **Physical Dimensions**: Length, width, height, weight
4. **Performance & Efficiency**: MPG, compression ratio, RPM

### Model Statistics
View real-time model performance metrics:
- Training accuracy
- Testing accuracy
- Feature importance rankings

## 🌐 Deployment

### Deploy to Heroku

1. Create a Heroku account and install the CLI
2. Login to Heroku:
```bash
heroku login
```

3. Create a new app:
```bash
heroku create your-app-name
```

4. Push to Heroku:
```bash
git push heroku main
```

### Deploy to Render

1. Create a Render account
2. Connect your GitHub repository
3. Create a new Web Service
4. Render will automatically detect and deploy your Flask app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Kishore Prashanth**
- GitHub: [@kishorep26](https://github.com/kishorep26)

## 🙏 Acknowledgments

- Dataset source: UCI Machine Learning Repository
- Built with modern web technologies and ML best practices
- Inspired by the need for accurate automobile price estimation

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ and Machine Learning
