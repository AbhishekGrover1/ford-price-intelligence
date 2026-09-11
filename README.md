# 🚗 Ford Price Intelligence

### End-to-End Machine Learning System for Used Ford Vehicle Price Prediction

**Ford Price Intelligence** is an end-to-end machine learning application designed to estimate the market price of used Ford vehicles based on vehicle specifications and usage characteristics.

The system uses a **Random Forest Regression** model trained on Ford vehicle listings and exposes the trained model through a **FastAPI REST API**, with a lightweight web interface for making real-time predictions.

---

## ✨ Overview

Used vehicle pricing depends on several factors including vehicle age, mileage, engine size, fuel type, transmission, fuel efficiency, and model.

This project applies machine learning to learn relationships between these attributes and historical vehicle prices, allowing users to enter vehicle specifications and receive an estimated price.

### What the system does

* 📊 Performs exploratory data analysis
* 🧹 Handles data preprocessing and missing/invalid values
* 🔤 Encodes categorical vehicle attributes
* 🛠️ Performs feature preparation for machine learning
* 🌲 Trains a Random Forest regression model
* 🔍 Performs hyperparameter optimization using `RandomizedSearchCV`
* 📈 Evaluates model performance using regression metrics
* 💾 Serializes the trained model for production inference
* ⚡ Serves predictions through a FastAPI REST API
* 🌐 Provides a browser-based prediction interface
* 🚀 Supports deployment-oriented project structure

---

## 🧠 Machine Learning Pipeline

```text
Ford Vehicle Dataset
        │
        ▼
Data Exploration
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Categorical Encoding
        │
        ▼
Train / Test Split
        │
        ▼
Random Forest Regressor
        │
        ▼
Hyperparameter Optimization
        │
        ▼
Model Evaluation
        │
        ▼
Model Serialization
        │
        ▼
FastAPI REST API
        │
        ▼
Web Prediction Interface
```

---

## 📌 Input Features

The model uses the following vehicle attributes:

| Feature        | Description                                |
| -------------- | ------------------------------------------ |
| `model`        | Ford vehicle model                         |
| `year`         | Manufacturing year                         |
| `transmission` | Automatic, Manual, or Semi-Auto            |
| `mileage`      | Vehicle mileage in miles                   |
| `fuelType`     | Petrol, Diesel, Hybrid, Electric, or Other |
| `tax`          | Vehicle tax in GBP                         |
| `mpg`          | Fuel efficiency                            |
| `engineSize`   | Engine displacement in litres              |

### Supported Ford Models

The application supports Ford models including:

`Fiesta` · `Focus` · `Mustang` · `Kuga` · `Puma` · `Mondeo` · `Ranger` · `EcoSport` · `Edge` · `Galaxy` · `S-MAX` · `C-MAX` · `B-MAX` · `Ka+` · `KA` · `Fusion` · `Escort` · `Tourneo Connect` · `Tourneo Custom` · `Grand C-MAX` · `Grand Tourneo Connect` · `Transit Tourneo` · `Streetka`

---

## 🌲 Machine Learning Model

The prediction engine is based on a **Random Forest Regressor**.

Random Forest was selected because it can model nonlinear relationships between vehicle characteristics and price while handling a mixture of numerical and categorical-derived features effectively.

The training workflow includes:

* `Train/Test Split`
* `RandomForestRegressor`
* `RandomizedSearchCV`
* 3-fold cross-validation during hyperparameter search
* Model evaluation on held-out test data

### Hyperparameter Search

The optimization process explores:

* `n_estimators`
* `max_depth`
* `min_samples_split`

The best estimator discovered during randomized search is saved as the production prediction model.

---

## 📊 Model Evaluation

The model is evaluated using standard regression metrics:

### Mean Absolute Error — MAE

Measures the average absolute difference between actual and predicted prices.

### Root Mean Squared Error — RMSE

Penalizes larger prediction errors more heavily than MAE.

### R² Score

Measures how much of the variation in vehicle prices is explained by the model.

> Model performance should be reported using the actual evaluation values generated during training rather than estimated or placeholder numbers.

---

## 🔬 Exploratory Data Analysis

The training notebook includes analysis of:

* Price distribution
* Ford model frequency
* Fuel type distribution
* Transmission distribution
* Mileage vs. price relationship
* Numerical feature correlations
* Price distribution across transmission types
* Price distribution across fuel types
* Feature importance
* Actual vs. predicted prices
* Worst prediction errors

These analyses help identify patterns in the dataset and understand which vehicle characteristics influence the model's predictions.

---

## ⚙️ Data Preprocessing

The project performs preprocessing before model training and inference.

### Engine Size Handling

Records where `engineSize` is `0.0` are replaced with the median engine size of the training data.

### Categorical Encoding

Categorical variables such as:

* Model
* Transmission
* Fuel Type

are transformed using one-hot encoding.

The resulting feature-column structure is saved separately in:

```text
model_columns.pkl
```

This ensures that incoming API requests can be transformed into the same feature structure expected by the trained model.

---

## 🏗️ Project Architecture

```text
                    ┌──────────────────────┐
                    │    Web Interface     │
                    │     HTML / CSS / JS   │
                    └──────────┬───────────┘
                               │
                               │ POST /api/predict
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │    REST API Layer    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Feature Preparation  │
                    │ One-Hot Encoding     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Random Forest Model  │
                    │  ford_price_         │
                    │  predictor.pkl       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Predicted Ford Price │
                    └──────────────────────┘
```

---

## 🗂️ Project Structure

```text
ford-price-intelligence/
│
├── ford_price_predictor.pkl
├── model_columns.pkl
│
├── ford_price_predictor_pkl.ipynb
│
├── main.py
├── index.html
├── style.css
├── script.js
│
├── requirements.txt
├── runtime.txt
│
└── README.md
```

### Key Files

**`ford_price_predictor_pkl.ipynb`**
Contains the machine learning workflow, including EDA, preprocessing, model training, hyperparameter tuning, evaluation, and model serialization.

**`ford_price_predictor.pkl`**
Serialized trained Random Forest model used for inference.

**`model_columns.pkl`**
Stores the feature-column structure required during prediction.

**`main.py`**
FastAPI application responsible for loading the trained model, validating input data, preprocessing requests, and returning predictions.

**`index.html`**
Frontend interface for entering vehicle information.

**`style.css`**
Frontend styling and responsive layout.

**`script.js`**
Handles frontend interaction and communication with the prediction API.

---

## ⚡ API

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Prediction Endpoint

```http
POST /api/predict
```

Example request:

```json
{
  "model": "Focus",
  "year": 2018,
  "transmission": "Manual",
  "mileage": 20000,
  "fuelType": "Petrol",
  "tax": 145,
  "mpg": 55,
  "engineSize": 1.2
}
```

Example response:

```json
{
  "predicted_price": 12500.00
}
```

*The response value above is an example format, not a claim about the model's actual prediction.*

---

## 🛠️ Tech Stack

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Random Forest Regression
* RandomizedSearchCV
* Joblib

### Backend

* FastAPI
* Pydantic
* Uvicorn

### Frontend

* HTML5
* CSS3
* JavaScript

### Model Persistence

* Joblib
* Pickle

---

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/AbhishekGrover1/ford-price-intelligence.git
cd ford-price-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI application

```bash
uvicorn main:app --reload
```

The application will start locally.

Open the frontend through the application root:

```text
/
```

The API documentation is also available through FastAPI's automatically generated documentation.

---

## 🔐 API Input Validation

The API validates incoming vehicle information before making predictions.

Validation includes:

* Valid Ford model
* Valid transmission type
* Valid fuel type
* Non-negative mileage
* Valid year range
* Valid tax value
* Positive MPG
* Valid engine-size range

This prevents unsupported categorical values and invalid numerical inputs from reaching the prediction pipeline.

---

## 📈 Feature Importance

The training workflow also extracts feature importance from the Random Forest model.

This provides interpretability into which vehicle attributes contribute most strongly to the model's predictions.

```python
model.feature_importances_
```

The project visualizes the top contributing features to help understand the model beyond its raw predictions.

---

## 🎯 Project Goals

The primary goals of this project are to:

* Build a practical regression model for vehicle price estimation
* Apply a complete machine learning workflow
* Preserve training-time feature structure during inference
* Expose the trained model through a REST API
* Create a usable prediction interface
* Move from experimentation toward a deployable ML application

---

## 🔮 Future Improvements

Potential improvements for the next version include:

* [ ] Compare Random Forest with XGBoost, LightGBM, and Gradient Boosting
* [ ] Add automated model benchmarking
* [ ] Introduce an explicit preprocessing pipeline
* [ ] Add model versioning
* [ ] Add experiment tracking with MLflow
* [ ] Add automated API tests
* [ ] Add prediction confidence / uncertainty estimates
* [ ] Add SHAP-based model explainability
* [ ] Add CI/CD
* [ ] Add monitoring for prediction drift
* [ ] Improve categorical feature handling
* [ ] Add automated retraining workflow
* [ ] Containerize the application with Docker

---

## 💡 Engineering Perspective

This project demonstrates the transition from a traditional machine learning notebook to a complete inference application.

Instead of stopping at model training, the project packages the trained model and exposes it through an API that performs:

```text
Request
   ↓
Validation
   ↓
Feature Transformation
   ↓
Model Inference
   ↓
Prediction
   ↓
JSON Response
```

This architecture provides a foundation for integrating the prediction model into web applications, automotive marketplaces, analytics platforms, or other vehicle-pricing workflows.

---

## 👨‍💻 Author

**Abhishek Grover**

AI/ML Engineer

* GitHub: **AbhishekGrover1**
* Portfolio: **abhishekgroverai.netlify.app**

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a star.

**Ford Price Intelligence — Machine Learning for Smarter Vehicle Price Estimation.**
