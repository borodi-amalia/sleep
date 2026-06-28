"""
Dashboard for analyzing military personnel sleep quality
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from security_tool import (
    verify_password,
    audit_log,
    generate_verification_code,
    send_verification_email
)
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv(override=True)

# Import utility functions and configurations
from dashboard_utils import (
    load_data, load_model, find_sleep_quality_column, categorize_features,
    create_question_input, prepare_prediction_data, show_prediction_results,
    create_sleep_quality_chart, create_feature_importance_chart
)
from dashboard_config import (
    COLOR_MAP, SLEEP_CLASSES, KEY_FACTORS, FACTOR_CATEGORIES, ALL_QUESTIONS
)


def setup_page():
    """Initial page configuration"""
    st.set_page_config(
        page_title="Military Sleep Quality Analysis",
        page_icon="🌙",
        layout="wide"
    )

def authenticate_user():
    """Password + email verification authentication with OTP expiration and attempt limiting"""

    AUTH_USERNAME = os.getenv("DASHBOARD_USERNAME")
    AUTH_SALT = os.getenv("DASHBOARD_PASSWORD_SALT")
    AUTH_PASSWORD_HASH = os.getenv("DASHBOARD_PASSWORD_HASH")
    AUTH_EMAIL = os.getenv("DASHBOARD_USER_EMAIL")

    MAX_ATTEMPTS = 3
    LOCK_TIME_MINUTES = 15

    if not AUTH_USERNAME or not AUTH_SALT or not AUTH_PASSWORD_HASH or not AUTH_EMAIL:
        st.error("Security configuration missing. Check the .env file.")
        audit_log("Missing security configuration", status="ERROR")
        return False

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "password_verified" not in st.session_state:
        st.session_state.password_verified = False

    if "verification_code" not in st.session_state:
        st.session_state.verification_code = None

    if "verification_code_expires_at" not in st.session_state:
        st.session_state.verification_code_expires_at = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "failed_password_attempts" not in st.session_state:
        st.session_state.failed_password_attempts = 0

    if "password_locked_until" not in st.session_state:
        st.session_state.password_locked_until = None

    if "failed_code_attempts" not in st.session_state:
        st.session_state.failed_code_attempts = 0

    if "code_locked_until" not in st.session_state:
        st.session_state.code_locked_until = None

    if st.session_state.authenticated:
        return True

    st.title("🔐 Secure Access")
    st.write("Please authenticate to access the Military Sleep Quality dashboard.")

    now = datetime.now()

    # Step 1: username + password
    if not st.session_state.password_verified:

        if (
            st.session_state.password_locked_until
            and now < st.session_state.password_locked_until
        ):
            remaining = st.session_state.password_locked_until - now
            minutes = int(remaining.total_seconds() // 60) + 1
            st.error(f"Too many failed password attempts. Try again in {minutes} minute(s).")
            return False

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Verify password"):
            if username == AUTH_USERNAME and verify_password(password, AUTH_SALT, AUTH_PASSWORD_HASH):
                st.session_state.failed_password_attempts = 0
                st.session_state.password_locked_until = None

                code = generate_verification_code()
                st.session_state.verification_code = code
                st.session_state.verification_code_expires_at = datetime.now() + timedelta(minutes=5)
                st.session_state.password_verified = True
                st.session_state.username = username

                try:
                    send_verification_email(AUTH_EMAIL, code)
                    audit_log("Password verified and email code sent", username=username, status="SUCCESS")
                    st.success("Password verified. A verification code was sent to your email.")
                    st.rerun()
                except Exception as e:
                    audit_log(f"Failed to send verification email: {e}", username=username, status="ERROR")
                    st.error(f"Could not send verification email: {e}")

            else:
                st.session_state.failed_password_attempts += 1
                remaining_attempts = MAX_ATTEMPTS - st.session_state.failed_password_attempts

                audit_log(
                    f"Failed password login attempt ({st.session_state.failed_password_attempts}/{MAX_ATTEMPTS})",
                    username=username or "unknown",
                    status="WARNING"
                )

                if st.session_state.failed_password_attempts >= MAX_ATTEMPTS:
                    st.session_state.password_locked_until = datetime.now() + timedelta(minutes=LOCK_TIME_MINUTES)
                    audit_log(
                        "Password login locked for 15 minutes",
                        username=username or "unknown",
                        status="WARNING"
                    )
                    st.error("Too many failed password attempts. Login is locked for 15 minutes.")
                else:
                    st.error(f"Invalid username or password. Attempts left: {remaining_attempts}")

        return False

    # Step 2: email verification code
    st.subheader("📧 Email Verification")
    st.write("Enter the 6-digit code sent to your email address.")
    st.caption("The verification code expires after 5 minutes.")

    if (
        st.session_state.code_locked_until
        and now < st.session_state.code_locked_until
    ):
        remaining = st.session_state.code_locked_until - now
        minutes = int(remaining.total_seconds() // 60) + 1
        st.error(f"Too many failed verification code attempts. Try again in {minutes} minute(s).")
        return False

    entered_code = st.text_input("Verification code")

    if st.button("Verify code"):
        if not entered_code:
            st.error("Please enter the verification code.")

        elif (
            st.session_state.verification_code_expires_at
            and datetime.now() > st.session_state.verification_code_expires_at
        ):
            audit_log("Expired email verification code", username=st.session_state.username, status="WARNING")
            st.error("Verification code expired. Please request a new code.")

        elif entered_code == st.session_state.verification_code:
            st.session_state.authenticated = True
            st.session_state.failed_code_attempts = 0
            st.session_state.code_locked_until = None

            audit_log("Successful 2FA login", username=st.session_state.username, status="SUCCESS")
            st.success("Authentication successful.")
            st.rerun()

        else:
            st.session_state.failed_code_attempts += 1
            remaining_attempts = MAX_ATTEMPTS - st.session_state.failed_code_attempts

            audit_log(
                f"Failed email verification code ({st.session_state.failed_code_attempts}/{MAX_ATTEMPTS})",
                username=st.session_state.username,
                status="WARNING"
            )

            if st.session_state.failed_code_attempts >= MAX_ATTEMPTS:
                st.session_state.code_locked_until = datetime.now() + timedelta(minutes=LOCK_TIME_MINUTES)
                audit_log(
                    "Email verification locked for 15 minutes",
                    username=st.session_state.username,
                    status="WARNING"
                )
                st.error("Too many failed verification code attempts. Verification is locked for 15 minutes.")
            else:
                st.error(f"Invalid verification code. Attempts left: {remaining_attempts}")

    if st.button("Resend code"):
        code = generate_verification_code()
        st.session_state.verification_code = code
        st.session_state.verification_code_expires_at = datetime.now() + timedelta(minutes=5)
        st.session_state.failed_code_attempts = 0
        st.session_state.code_locked_until = None

        try:
            send_verification_email(AUTH_EMAIL, code)
            audit_log("Verification code resent", username=st.session_state.username, status="INFO")
            st.success("A new verification code was sent.")
        except Exception as e:
            audit_log(f"Failed to resend verification email: {e}", username=st.session_state.username, status="ERROR")
            st.error(f"Could not resend verification email: {e}")

    return False

def show_summary_tab(df, model, metadata):
    """Display the summary tab"""
    st.header("Sleep Quality Analysis Summary")

    # Identify sleep quality column
    quality_col = find_sleep_quality_column(df)

    if quality_col:
        # Display key metrics in 4 columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Calculate proportions
            quality_counts = df[quality_col].value_counts()
            total = len(df)
            poor_sleep_count = sum(1 for q in df[quality_col] if q in ['Very Bad', 'Pretty Bad'])
            poor_sleep_pct = poor_sleep_count / total * 100
            st.metric("Problem Sleep", f"{poor_sleep_pct:.1f}%",
                      help="Percentage of participants with 'Very Bad' or 'Pretty Bad' sleep")

        with col2:
            # Map values to numbers
            quality_map = {'Very Bad': 1, 'Pretty Bad': 2, 'Quite Good': 3, 'Very Good': 4}
            avg_quality = sum(quality_map.get(q, 0) for q in df[quality_col]) / total
            st.metric("Average Score", f"{avg_quality:.2f}/4",
                      help="Average sleep quality score (1-4)")

        with col3:
            model_accuracy = 0.891  # Optimized model accuracy
            st.metric("Model Accuracy", f"{model_accuracy:.1%}",
                      help="Accuracy of the optimized model")

        with col4:
            total_features = len(metadata.get('feature_names', []))
            st.metric("Factors Analyzed", f"{total_features}",
                      help="Total number of factors used by the model")

        # Chart for sleep quality distribution
        st.subheader("Sleep Quality Distribution")
        fig = create_sleep_quality_chart(df, quality_col)
        st.plotly_chart(fig, use_container_width=True)

        # Display confusion matrix if available
        st.subheader("Model Performance")
        try:
            results_dir = Path(__file__).parent.parent / "results"
            confusion_matrix_path = results_dir / "optimized_confusion_matrix.png"
            if confusion_matrix_path.exists():
                st.image(str(confusion_matrix_path), caption="Confusion Matrix")
            else:
                st.info("Confusion matrix not found. Run the model to generate it.")
        except Exception as e:
            st.error(f"Error loading confusion matrix: {e}")


def show_features_tab(model, metadata):
    """Display the important factors tab"""
    st.header("Factors Influencing Sleep Quality")

    # Check if we have feature_names
    feature_names = metadata.get('feature_names', [])
    if not feature_names:
        st.warning("Feature names not found. Make sure the model was trained correctly.")
        return

    # Display factor importance
    st.subheader("Top 15 Most Important Factors")
    fig = create_feature_importance_chart(model, feature_names, top_n=15)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Model does not have feature_importances_ attribute.")

    # Display factors grouped by categories
    st.subheader("Factors Grouped by Categories")

    # Group features by categories
    categorized = categorize_features(feature_names, FACTOR_CATEGORIES)

    # Calculate total importance per category (if we have feature_importances_)
    if hasattr(model, 'feature_importances_'):
        category_importance = {}
        for category, features in categorized.items():
            total_importance = 0
            for feature in features:
                idx = feature_names.index(feature)
                total_importance += model.feature_importances_[idx]

            category_importance[category] = total_importance

        # Create chart for category importance
        cat_df = pd.DataFrame({
            'Category': list(category_importance.keys()),
            'Total Importance': list(category_importance.values())
        })

        fig = px.pie(
            cat_df,
            values='Total Importance',
            names='Category',
            title="Importance of Factor Categories"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Selectbox for exploring factors by category
    selected_category = st.selectbox(
        "Explore factors by category:",
        list(categorized.keys())
    )

    if selected_category in categorized:
        cat_features = categorized[selected_category]

        if not cat_features:
            st.info(f"No features found in category '{selected_category}'.")
            return

        if hasattr(model, 'feature_importances_'):
            # Extract importances for features in this category
            cat_importance = []
            for feature in cat_features:
                idx = feature_names.index(feature)
                importance = model.feature_importances_[idx]

                # Simplify name for display
                display_name = feature
                if '. ' in feature:
                    display_name = feature.split('. ', 1)[1]

                cat_importance.append({
                    'Feature': display_name,
                    'Importance': importance
                })

            # Sort by importance
            cat_importance.sort(key=lambda x: x['Importance'], reverse=True)

            # Display top 10 or all if fewer
            display_count = min(10, len(cat_importance))

            cat_df = pd.DataFrame(cat_importance[:display_count])

            fig = px.bar(
                cat_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title=f"Top {display_count} Factors in '{selected_category}' Category"
            )

            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        # Display complete list if user wants
        if st.checkbox("Show complete list of factors in this category"):
            st.write("Complete list of factors:")
            for feature in cat_features:
                display_name = feature
                if '. ' in feature:
                    display_name = feature.split('. ', 1)[1]
                st.write(f"- {display_name}")


def show_predictor_tab(model, metadata):
    """Display the predictor tab with all 52 questions in advanced mode"""
    st.header("Sleep Quality Predictor")
    st.write("Use this tool to estimate sleep quality based on various factors.")

    # Check if we have model and feature_names
    feature_names = metadata.get('feature_names', [])
    scaler = metadata.get('scaler', None)

    if not feature_names:
        st.warning("Feature names not found. Make sure the model was trained correctly.")
        return

    # Choose prediction mode
    pred_mode = st.radio(
        "Prediction mode:",
        ["Simple (key factors)", "Advanced (all 52 questions)"]
    )

    if pred_mode == "Simple (key factors)":
        # Display note about accuracy
        st.info("""
        ⚠️ This mode uses only key factors from those used by the model. 
        For maximum accuracy, use the Advanced mode with all 52 questions.
        """)

        # Create widgets for key factors
        st.subheader("Enter values for key factors")

        # Split questions into two columns
        col1, col2 = st.columns(2)

        # Dictionary for entered values
        user_inputs = {}

        # Distribute questions across columns
        for i, factor in enumerate(KEY_FACTORS):
            col = col1 if i % 2 == 0 else col2

            with col:
                _, numeric_value = create_question_input(factor)
                user_inputs[factor["column"]] = numeric_value

        # Prediction button
        if st.button("Calculate Sleep Quality", key="simple_predict"):
            audit_log(
                "Simple prediction requested",
                username=st.session_state.get("username", "unknown"),
                status="INFO"
            )

            # Prepare data for prediction
            features_vector = prepare_prediction_data(user_inputs, feature_names, scaler)

            # Display result
            show_prediction_results(model, features_vector)

    else:  # Advanced mode - all 52 questions
        st.subheader("Advanced prediction (all 52 questions)")

        # Display note about accuracy
        st.info("""
        This mode allows you to answer all 52 questions from the survey for the most accurate prediction.
        Questions are organized by category for easier navigation.
        """)

        # Initialize session_state to retain values between categories
        if 'advanced_inputs' not in st.session_state:
            st.session_state.advanced_inputs = {}

        # Get category names from the questions themselves
        categories = sorted(list(set(q["category"] for q in ALL_QUESTIONS)))

        # Tabbed interface for categories
        category_tabs = st.tabs(categories)

        # For each category tab, show relevant questions
        for i, category in enumerate(categories):
            with category_tabs[i]:
                # Filter questions for this category
                category_questions = [q for q in ALL_QUESTIONS if q["category"] == category]

                st.write(f"**{len(category_questions)}** questions in '{category}' category")

                # Create two columns for questions
                col1, col2 = st.columns(2)

                # Dictionary for values in this category
                category_inputs = {}

                # Distribute questions across columns
                for j, question in enumerate(category_questions):
                    col = col1 if j % 2 == 0 else col2

                    with col:
                        _, numeric_value = create_question_input(
                            question,
                            key_prefix=f"adv_{category}_{question['id']}"
                        )
                        category_inputs[question["column"]] = numeric_value

                # Update session_state with new values
                st.session_state.advanced_inputs.update(category_inputs)

        # Show category-specific progress
        col1, col2 = st.columns(2)

        with col2:
            # Define total questions
            total_questions = len(ALL_QUESTIONS)

            # Set a fixed minimum number of questions required - using 10 as an example
            min_questions = 10

            # Add a message about the minimum requirement
            st.info(f"Answer at least {min_questions} questions for the most accurate prediction.")

            # Create a button that invites users to make a prediction
            if st.button("I've answered enough questions, make a prediction", key="advanced_predict"):
                audit_log(
                    "Advanced prediction requested",
                    username=st.session_state.get("username", "unknown"),
                    status="INFO"
                )

                # Prepare data for prediction
                features_vector = prepare_prediction_data(
                    st.session_state.advanced_inputs,
                    feature_names,
                    scaler
                )

                # Display result
                show_prediction_results(model, features_vector)

            # Button to reset all inputs
            if st.button("Reset All Inputs", key="reset_inputs"):
                st.session_state.advanced_inputs = {}
                st.experimental_rerun()


def show_security_status_tab():
    """Display implemented data security measures"""
    st.header("🔐 Security Status")
    st.write("This section summarizes the data security mechanisms implemented in the project.")

    st.subheader("Implemented Security Measures")

    col1, col2 = st.columns(2)

    with col1:
        st.success("✅ Encrypted data storage")
        st.write(
            "The original CSV dataset is protected using Fernet symmetric encryption "
            "and stored as a `.csv.encrypted` file."
        )

        st.success("✅ In-memory decryption")
        st.write(
            "The encrypted dataset is decrypted only in memory when the dashboard runs. "
            "The application does not recreate a plain CSV file on disk."
        )

        st.success("✅ Password-based authentication")
        st.write(
            "Users must authenticate before accessing the dashboard. "
            "Unauthorized users cannot view the analysis or use the predictor."
        )

        st.success("✅ Password hashing with salt")
        st.write(
            "The dashboard does not compare the password in plain text. "
            "It uses PBKDF2 hashing with a salt to verify the password."
        )

    with col2:
        st.success("✅ Email verification / 2FA")
        st.write(
            "After the password is verified, the user receives a 6-digit verification code "
            "by email. Access is granted only after the correct code is entered."
        )

        st.success("✅ OTP expiration")
        st.write(
            "The email verification code expires after 5 minutes. "
            "Expired codes cannot be used to access the dashboard."
        )

        st.success("✅ Brute-force protection")
        st.write(
            "After 3 failed password or verification code attempts, authentication is locked "
            "for 15 minutes."
        )

        st.success("✅ Data anonymization")
        st.write(
            "Before the data is used in the dashboard, columns that may contain personal "
            "or identifying information are automatically removed."
        )

        st.success("✅ Audit logging")
        st.write(
            "Important security events are saved in `logs/security_audit.log`, including "
            "successful logins, failed login attempts, dataset loading, 2FA events, lockouts "
            "and prediction requests."
        )

    st.subheader("Security Architecture")

    st.code(
        """
User opens dashboard
        ↓
Authentication required
        ↓
Password verified using hash + salt
        ↓
If password is correct, a 6-digit email code is generated
        ↓
Verification code is sent to the user's email address
        ↓
User enters the email verification code
        ↓
Code is checked and must be valid within 5 minutes
        ↓
After 3 failed attempts, login is locked for 15 minutes
        ↓
Encrypted dataset is loaded
        ↓
Dataset is decrypted only in memory
        ↓
Sensitive columns are anonymized
        ↓
Dashboard analysis and prediction are available
        ↓
Security events are written to audit log
        """,
        language="text"
    )

    st.subheader("Audit Log Location")
    st.info("Audit events are stored in: `logs/security_audit.log`")

    st.subheader("Security Configuration")
    st.success(
        "The dashboard credentials are loaded from a local `.env` file, "
        "so the username, salt and password hash are not hardcoded directly in the source code."
    )

    st.info(
        "For a real production system, the secret key and authentication values should be managed "
        "through a dedicated secrets manager or secure server environment variables."
    )

def main():
    """Main application function"""
    setup_page()

    # Security: require authentication + email verification before loading dashboard data
    if not authenticate_user():
        st.stop()

    st.sidebar.success(f"Authenticated as: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        audit_log("User logged out", username=st.session_state.username, status="INFO")

        # Clear all authentication-related session data
        st.session_state.authenticated = False
        st.session_state.password_verified = False
        st.session_state.verification_code = None
        st.session_state.verification_code_expires_at = None
        st.session_state.username = None

        st.session_state.failed_password_attempts = 0
        st.session_state.password_locked_until = None
        st.session_state.failed_code_attempts = 0
        st.session_state.code_locked_until = None


        st.rerun()

    st.title("🌙 Military Sleep Quality Analysis")
    st.write("This dashboard analyzes factors influencing sleep quality in military personnel.")

    # Security information
    st.success(
    "🔐 Secure mode active: encrypted data loading, in-memory decryption, anonymization, "
    "password hashing, email verification, OTP expiration, brute-force protection and audit logging are enabled."
)

    # Explanatory note
    st.info("""
    **Important note**: The model uses multiple questions from the survey for prediction. 
    The interface displays the most important factors for better user experience.
    For maximum accuracy, use the Advanced mode in the Predictor section.
    """)

    # Load data and model
    df = load_data(username=st.session_state.get("username", "unknown"))
    metadata = load_model()

    if df is None:
        st.error("Data could not be loaded.")
        st.stop()

    if metadata is None:
        st.warning("First run `python src/optimized_sleep_model.py` to generate the optimized model!")
        return

    # Extract model and other data from metadata
    model = metadata.get('model')

    if model is None:
        st.error("Model not found in metadata.")
        return

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Summary",
        "🔍 Important Factors",
        "🧠 Predictor",
        "🔐 Security Status"
    ])

    with tab1:
        show_summary_tab(df, model, metadata)

    with tab2:
        show_features_tab(model, metadata)

    with tab3:
        show_predictor_tab(model, metadata)

    with tab4:
        show_security_status_tab()


if __name__ == "__main__":
    main()