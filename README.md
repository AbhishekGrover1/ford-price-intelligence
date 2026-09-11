
<div align="center">

[![Live Demo](https://img.shields.io/badge/Live%20Demo-view%20app-46E3B7?style=flat-square&logo=render&logoColor=white)](https://ford-price-intelligence-1.onrender.com)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-c6a15b?style=flat-square)

**A full-stack machine learning system that predicts Ford vehicle market valuations with high fidelity — powered by an optimized regression model, served through a high-performance FastAPI backend and a custom dark-themed interface.**

</div> 

---

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Engineering Notes](#engineering-notes)
- [License](#license)
- [Connect](#connect)

---

## Overview

**Ford Price Intelligence** bridges raw automotive data and real-time predictive analytics. By serializing a production-grade machine learning model (`ford_price_predictor.pkl`) via `joblib` and integrating it into an asynchronous `FastAPI` application, the system delivers instant, reliable price estimations directly to a responsive user interface.

No mock data or static placeholders—the application handles live user requests through an optimized REST API pipeline.

## Live Demo

**[ford-price-intelligence-1.onrender.com](https://ford-price-intelligence-1.onrender.com)**

Experience the live application directly in your browser. Test out vehicle pricing inputs or run the codebase locally in under two minutes ([Getting Started](#getting-started)).

> *Hosted on Render's efficient cloud infrastructure. If the service has been idle, please allow 30–50 seconds for the initial cold start.*

## Key Features

- 🔮 **Live ML-Powered Predictions** served over a fully documented REST API
- 📊 **Robust Regression Model** optimized for high-precision automotive valuation
- 🎨 **Sleek, Hand-Crafted Dark UI** built with custom CSS and modern typography (Fraunces & IBM Plex)
- 🐳 **Containerization-Ready** via a clean Docker configuration for seamless orchestration
- ⚡ **High-Performance Backend** built on FastAPI with strict Pydantic payload validation

## Architecture

The system follows a production-oriented machine learning pipeline, organized into logical layers that transform raw inputs into real-time price intelligence:

```mermaid
flowchart TD
    subgraph L1["Data Layer"]
        A[Ford Vehicle Dataset] --> B[Exploratory Data Analysis]
        B --> C[Feature Engineering]
        C --> D[Data Preprocessing]
    end

    subgraph L2["Model Layer"]
        D --> E["Random Forest / Ensemble Regressor"]
        E --> F["Hyperparameter Optimization"]
        F --> G["Model Serialization • Joblib"]
    end

    subgraph L3["Service Layer"]
        G --> H["FastAPI Backend"]
        H --> I["REST API • /api/predict"]
    end

    subgraph L4["Presentation Layer"]
        I --> J["HTML • CSS • JavaScript UI"]
        J --> K["Vehicle Price Prediction"]
    end

    subgraph L5["Deployment Layer"]
        K --> L["Render Cloud Deployment"]
        L --> M["🚀 Live Ford Price Intelligence"]
    end

