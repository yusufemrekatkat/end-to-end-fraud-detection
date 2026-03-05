#  Fraud Sentinel AI: End-to-End Fraud Detection Pipeline

Fraud Sentinel is a production-ready, end-to-end machine learning pipeline designed to detect fraudulent transactions. Moving beyond isolated model training, this project is built with industrial-grade data ingestion, high-speed vectorized batch processing, and a fully containerized microservices architecture.

*Note: An AI-assisted workflow was utilized during rapid prototyping, architectural design, and debugging to embrace modern human-AI collaborative engineering.*

---

##  Key Architectural Features

*  **High-Performance Vectorized Processing:** Eliminates traditional `for`-loops by leveraging Pandas and NumPy vectorization. Capable of processing massive datasets (555K+ rows) in mere seconds without API bottlenecks.
*  **Dynamic Percentile Thresholding:** Emulates real-world banking "Alert Rates". Instead of static probability thresholds, the system dynamically flags the top 1% of the riskiest transactions as `BLOCK` and the next 2% as `REVIEW`, elegantly handling highly imbalanced data.
*  **Defensive Data Ingestion:** A sanitization layer that intercepts missing (NaN), malformed, or unexpected inputs before they reach the model, preventing system crashes and ensuring 100% API uptime.
*  **Containerized Backend:** The FastAPI-based inference engine, ML models, and dependencies are fully isolated and served via Docker.
*  **Executive Analyst Dashboard:** A robust Streamlit frontend featuring Dark Mode protection. It provides financial risk summaries (e.g., "Total Amount at Risk"), interactive metrics, and the ability to export only suspicious transactions to optimize file sizes.

---

##  Tech Stack

* **Machine Learning:** Scikit-learn (Random Forest), NumPy, Pandas, Joblib
* **Backend API:** FastAPI, Uvicorn, Python 3.11
* **Frontend UI:** Streamlit, Requests
* **DevOps & MLOps:** Docker, Docker Compose, Git

---

##  Getting Started

### Prerequisites
Make sure you have [Docker](https://www.docker.com/) and [Python 3.11+](https://www.python.org/) installed on your machine.

### 1. Fire up the Backend (Docker)
Initialize the containerized machine learning serving API:
```bash
docker compose -f docker/docker-compose.yml up --build serve

The API will be available at http://localhost:8000.

2. Launch the Frontend (Executive UI)
Open a new terminal, activate your virtual environment, and start the dashboard:

Bash
streamlit run app_ui.py
The UI will open in your default browser at http://localhost:8501.

💡 Usage
Single Transaction Check: Navigate to the " Single Query" tab in the UI to manually test individual transactions.

Batch Analytics (Dashboard): Upload massive .csv files in the " Batch Dashboard" tab. The system will process hundreds of thousands of rows in seconds, providing an executive summary of blocked transactions and allowing you to download the filtered suspicious data.
