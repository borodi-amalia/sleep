# Military Sleep Quality Analysis

This project analyzes sleep quality in military personnel using machine learning and presents the results through a secure Streamlit dashboard. The workflow includes data preparation, model training, report generation, and interactive prediction.

## Project overview

The repository contains a complete end-to-end pipeline for:

- loading and preprocessing survey data related to sleep quality,
- training an optimized machine learning model for sleep quality prediction,
- generating visual and textual reports,
- running a protected dashboard for exploratory analysis and prediction.

The analysis focuses on factors such as sleep duration, sleep latency, environmental disturbances (temperature, noise, coughing/snoring), and other lifestyle or training-related variables.

## Main features

- Secure data loading from encrypted files
- Privacy-preserving preprocessing and anonymization
- Machine learning model training with Random Forest and SMOTE balancing
- Feature importance analysis
- Interactive dashboard with authentication and 2-factor verification
- Automated report generation in Markdown and HTML

## Repository structure

```text
.
├── data/                      # Raw and encrypted datasets
├── logs/                      # Security and audit logs
├── models/                    # Trained model artifacts
├── reports/                   # Generated Markdown/HTML reports
├── results/                   # Model evaluation charts and metrics
├── src/                       # Source code
│   ├── data_preparation.py    # Data loading and feature engineering
│   ├── optimized_sleep_model.py  # Model training pipeline
│   ├── generate_report.py     # Report generation
│   ├── sleep_dashboard.py     # Streamlit dashboard
│   ├── dashboard_config.py    # Dashboard configuration and question definitions
│   ├── dashboard_utils.py     # Dashboard helper functions
│   └── security_tool.py       # Encryption, auth, and logging utilities
├── requirements.txt           # Python dependencies
├── secret.key                 # Fernet key used for encryption
└── .env                       # Environment variables for dashboard security
```

## Requirements

Python 3.10+ is recommended.

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Environment configuration

Before running the dashboard, create or update the project environment variables in the `.env` file.

Required variables include:

```env
DASHBOARD_USERNAME=your_username
DASHBOARD_PASSWORD_SALT=your_salt
DASHBOARD_PASSWORD_HASH=your_password_hash
DASHBOARD_USER_EMAIL=your_email
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_EMAIL=your_smtp_email
SMTP_PASSWORD=your_smtp_password
```

The password hash should be generated using the hashing utilities in the project, or you can use a known secure hash value that matches the verification logic.

## Data and security notes

The project uses encrypted CSV files in the `data/` folder. The encryption key is stored in `secret.key`.

The dashboard also:

- anonymizes sensitive columns before using the data,
- writes audit events to `logs/security_audit.log`,
- requires authentication before access.

If the encrypted data is missing or the key is unavailable, the application may fall back to a plain data file during development, but this is not recommended for production use.

## Usage

### 1. Train the machine learning model

Run:

```bash
python src/optimized_sleep_model.py
```

This script will:

- load the survey dataset,
- prepare the target label and features,
- balance the classes with SMOTE,
- train a Random Forest classifier,
- save the model in `models/optimized_sleep_model.pkl`,
- generate charts in `results/`.

### 2. Generate reports

Run:

```bash
python src/generate_report.py
```

This creates Markdown and HTML reports in the `reports/` folder.

### 3. Start the dashboard

Run:

```bash
streamlit run src/sleep_dashboard.py
```

Then open the local URL shown by Streamlit in your browser.

## Data preparation workflow

The preprocessing pipeline is implemented in `src/data_preparation.py` and includes:

- decrypting the encrypted input file,
- mapping sleep quality to numeric values,
- engineering features such as sleep duration, latency, bedtime, wake time,
- creating a processed dataset for model training.

## Model details

The training pipeline uses:

- Random Forest Classifier,
- RandomizedSearchCV for hyperparameter tuning,
- SMOTE to balance minority classes,
- standard scaling for numerical features.

## Report outputs

The project generates:

- `reports/military_sleep_analysis_report_*.md`
- `reports/military_sleep_analysis_report_*.html`
- `reports/military_sleep_executive_summary.md`

## Notes for development

- The dashboard is designed for research and demonstration purposes.
- Model accuracy and feature importance are based on the current dataset and training setup.
- If you modify the data schema, the feature engineering and dashboard question mappings may need to be updated.

## License

This project is intended for academic and internal analysis purposes.
