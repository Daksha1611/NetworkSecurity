# 🛡️ Network Security — Phishing Detection MLOps Pipeline

A production-grade Machine Learning system to detect **phishing websites** in real time. Built with a focus on **MLOps best practices** — modular pipelines, experiment tracking, containerization, and CI/CD automation — mirroring how ML systems are architected and maintained in real engineering teams.

---

## Problem Statement

Phishing attacks are one of the most common cybersecurity threats, tricking users into visiting fraudulent websites designed to steal credentials and sensitive data. This project builds an end-to-end ML pipeline that classifies whether a given website is **phishing** or **legitimate** based on a set of extracted URL and webpage features.

---

## System Architecture

```
MongoDB Atlas (Raw Data)
        ↓
Data Ingestion Pipeline
        ↓
Data Validation Pipeline
        ↓
Data Transformation Pipeline
        ↓
Model Trainer (MLflow + DagsHub Tracking)
        ↓
FastAPI Application (/train + /predict endpoints)
        ↓
Docker Container
        ↓
GitHub Actions CI/CD → AWS ECR → AWS EC2
```

---

## Key Features

- **Automated ETL Pipeline** — Raw phishing data ingested from MongoDB Atlas, validated against a defined schema, and transformed into model-ready features automatically
- **Modular Project Structure** — Each pipeline stage (ingestion, validation, transformation, training) is an independently testable, config-driven Python module
- **Experiment Tracking** — Every training run is logged with MLflow, with remote tracking hosted on DagsHub for full reproducibility
- **FastAPI REST API** — Two endpoints: `/train` to trigger the full training pipeline and `/predict` to run inference on uploaded CSV data
- **Containerized with Docker** — Self-contained image that runs identically in any environment
- **CI/CD Pipeline** — GitHub Actions workflow automatically builds and pushes the Docker image on every push to `main`

---

## Tech Stack

| Category | Tools |
|---|---|
| **ML & Data** | Scikit-learn, Pandas, NumPy |
| **MLOps** | MLflow, DagsHub |
| **Database** | MongoDB Atlas |
| **Backend** | FastAPI, Uvicorn |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Cloud** | AWS ECR (container registry) |
| **Language** | Python 3.9 |

---

## Project Structure

```
NetworkSecurity/
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py       # Pulls data from MongoDB Atlas
│   │   ├── data_validation.py      # Schema validation & drift detection
│   │   ├── data_transformation.py  # Feature engineering & preprocessing
│   │   └── model_trainer.py        # Model training & MLflow logging
│   ├── Pipeline/
│   │   └── training_pipeline.py    # Orchestrates all pipeline stages
│   ├── Entity/
│   │   └── config_entity.py        # Config dataclasses for each component
│   ├── Constant/
│   │   └── training_pipeline.py    # Pipeline constants & hyperparameters
│   ├── Exception/
│   │   └── Exception.py            # Custom exception handler
│   ├── logging/
│   │   └── logger.py               # Centralized logging setup
│   └── Utils/
│       └── main_utils/utils.py     # Shared utility functions
├── Network_Data/
│   └── phisingData.csv             # Raw phishing dataset
├── data_schema/                    # Schema definition for validation
├── final_model/                    # Trained model + preprocessor artifacts
├── prediction_output/              # Prediction results output
├── templates/
│   └── table.html                  # HTML template for prediction display
├── .github/workflows/              # GitHub Actions CI/CD workflow
├── app.py                          # FastAPI application entry point
├── main.py                         # Standalone pipeline runner
├── push_data.py                    # Script to push CSV data to MongoDB
├── Dockerfile                      # Docker container definition
├── requirements.txt                # Python dependencies
└── setup.py                        # Package setup
```

---

## Pipeline Stages

### 1. Data Ingestion
Connects to MongoDB Atlas, fetches the phishing dataset, and splits it into train/test sets. Outputs are stored as artifacts for the next stage.

### 2. Data Validation
Validates the ingested data against a predefined schema — checks for missing columns, correct data types, and data drift between train and test sets. Generates a validation report.

### 3. Data Transformation
Applies preprocessing — handles missing values using KNN imputation, scales features, and builds a scikit-learn preprocessing pipeline saved as a `.pkl` artifact.

### 4. Model Training
Trains a classification model on the transformed data. Every experiment — parameters, metrics (F1, precision, recall), and artifacts — is tracked with **MLflow** on **DagsHub**. The best model is saved to `final_model/`.

---

## Getting Started

### Prerequisites
- Python 3.9+
- MongoDB Atlas account with connection URI
- DagsHub account (for MLflow tracking)

### 1. Clone the Repository
```bash
git clone https://github.com/Daksha1611/NetworkSecurity.git
cd NetworkSecurity
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
MONGO_URI=your_mongodb_atlas_connection_string
MLFLOW_TRACKING_URI=your_dagshub_mlflow_uri
MLFLOW_TRACKING_USERNAME=your_dagshub_username
MLFLOW_TRACKING_PASSWORD=your_dagshub_token
```

### 4. Push Data to MongoDB
```bash
python push_data.py
```

### 5. Run the Training Pipeline
```bash
python main.py
```

### 6. Start the FastAPI Server
```bash
python app.py
```
The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Redirects to Swagger docs |
| `/train` | GET | Triggers the full ML training pipeline |
| `/predict` | POST | Accepts a CSV file, returns phishing predictions |

### Example — Predict via curl
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@your_data.csv;type=text/csv"
```

---

## Running with Docker

```bash
# Build the image
docker build -t networksecurity:latest .

# Run the container
docker run -p 8000:8000 --env-file .env networksecurity:latest
```

---

## CI/CD Pipeline

The `.github/workflows/` directory contains a GitHub Actions workflow that triggers on every push to `main`:

1. Checks out the repository
2. Builds the Docker image
3. Authenticates with AWS
4. Pushes the image to **AWS ECR**

This ensures the latest version of the application is always packaged and ready for deployment without any manual steps.

---

## Experiment Tracking

All training runs are tracked on DagsHub via MLflow. Each run logs:
- Model parameters (hyperparameters)
- Evaluation metrics (F1 score, precision, recall, accuracy)
- Model artifacts (trained model + preprocessor)

This enables full reproducibility — any past experiment can be re-run or compared from the DagsHub dashboard.

---

## Dataset

The project uses a **phishing website detection dataset** containing URL and webpage-based features that distinguish phishing sites from legitimate ones. The raw data is stored in MongoDB Atlas and pulled programmatically at the start of each pipeline run.

---


## Author

**Daksha Mehta**
- GitHub: [@Daksha1611](https://github.com/Daksha1611)