"""
Utility functions for the dashboard
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from io import BytesIO
import joblib
from dashboard_config import COLOR_MAP, SLEEP_CLASSES, QUESTION_TYPES
from security_tool import decrypt_file_to_bytes, anonymize_dataframe, audit_log


def load_data(username="unknown"):
    """Load data securely from encrypted CSV if available, otherwise from plain CSV"""
    try:
        project_root = Path(__file__).parent.parent

        csv_path = project_root / "data" / "P2.4_Military_Responses.csv"
        encrypted_path = project_root / "data" / "P2.4_Military_Responses.csv.encrypted"

        if encrypted_path.exists():
            decrypted_bytes = decrypt_file_to_bytes(encrypted_path)
            df = pd.read_csv(BytesIO(decrypted_bytes))

            # Security step: remove sensitive columns before using data in dashboard
            df = anonymize_dataframe(df)

            audit_log("Encrypted dataset loaded and anonymized", username=username, status="SUCCESS")
            return df

        if csv_path.exists():
            df = pd.read_csv(csv_path)

            # Security step: remove sensitive columns before using data in dashboard
            df = anonymize_dataframe(df)

            audit_log("Plain CSV dataset loaded and anonymized", username=username, status="WARNING")
            st.warning("Plain CSV file was used. For better security, use the encrypted dataset.")
            return df

        st.error(
            f"Data file not found. Expected either:\n\n"
            f"- {encrypted_path}\n"
            f"- {csv_path}"
        )
        audit_log("Dataset loading failed: file not found", username=username, status="ERROR")
        return None

    except Exception as e:
        st.error(f"Error loading data: {e}")
        audit_log(f"Dataset loading failed: {e}", username=username, status="ERROR")
        return None

def load_model():
    """Load the optimized model"""
    try:
        project_root = Path(__file__).parent.parent
        model_path = project_root / "models" / "optimized_sleep_model.pkl"
        metadata = joblib.load(model_path)
        return metadata
    except Exception as e:
        st.error(f"Could not load the optimized model: {e}")
        return None


def find_sleep_quality_column(df):
    """Identify the sleep quality column"""
    if df is None:
        return None

    for col in df.columns:
        if 'sleep quality' in col.lower():
            return col

    return None


def categorize_features(feature_names, categories):
    """Group features by categories"""
    categorized = {}

    # Initialize categories
    for cat in categories:
        categorized[cat['name']] = []

    # Place each feature in the appropriate category
    for feature in feature_names:
        assigned = False
        for cat in categories:
            if any(kw in feature.lower() for kw in cat['keywords']):
                categorized[cat['name']].append(feature)
                assigned = True
                break

        # If it doesn't fit any category, put it in Other
        if not assigned:
            if "Other" not in categorized:
                categorized["Other"] = []
            categorized["Other"].append(feature)

    return categorized


def create_question_input(question_info, key_prefix="q"):
    """
    Create the appropriate widget for a question based on its type

    Args:
        question_info (dict): Information about the question
        key_prefix (str): Prefix for the widget key

    Returns:
        tuple: (display_value, numeric_value)
    """
    # Extract question information
    q_id = question_info["id"]
    q_text = question_info["question"]
    q_type = question_info["type"]

    # Generate a unique key for the widget
    widget_key = f"{key_prefix}_{q_id}"

    # Get the definitions for this question type
    type_def = QUESTION_TYPES.get(q_type)
    if not type_def:
        st.warning(f"Unknown question type: {q_type}")
        return None, None

    # Create the appropriate widget
    widget_type = type_def["widget"]

    if widget_type == "number_input":
        defaults = type_def.get("defaults", {})
        # Pull defaults out
        min_val = defaults.get("min_value", 0)
        max_val = defaults.get("max_value", 100)
        step_val = defaults.get("step", 1)
        # Determine initial value
        initial_val = defaults.get("value", min_val)

        # If any of min, max, or step is a float, cast them all to float
        if any(isinstance(x, float) for x in (min_val, max_val, step_val)):
            min_val = float(min_val)
            max_val = float(max_val)
            step_val = float(step_val)
            initial_val = float(initial_val)

        # Ensure initial is within bounds
        if initial_val < min_val:
            initial_val = min_val
        elif initial_val > max_val:
            initial_val = max_val

        # Finally call Streamlit
        value = st.number_input(
            q_text,
            min_value=min_val,
            max_value=max_val,
            value=initial_val,
            step=step_val,
            key=widget_key
        )
        return value, value


    elif widget_type == "selectbox":
        options = type_def.get("options", [])
        values = type_def.get("values", {})

        value = st.selectbox(
            q_text,
            options=options,
            key=widget_key
        )

        numeric_value = values.get(value, 0)
        return value, numeric_value

    elif widget_type == "radio":
        options = type_def.get("options", [])
        values = type_def.get("values", {})

        value = st.radio(
            q_text,
            options=options,
            key=widget_key,
            horizontal=True
        )

        numeric_value = values.get(value, 0)
        return value, numeric_value

    elif widget_type == "slider":
        options = type_def.get("options", [1, 2, 3, 4, 5])
        labels = type_def.get("labels", {})
        values = type_def.get("values", {})

        # Get min, max, and default values
        min_val = min(options)
        max_val = max(options)
        default_val = options[len(options) // 2]  # middle value

        value = st.slider(
            q_text,
            min_value=min_val,
            max_value=max_val,
            value=default_val,
            step=1,
            key=widget_key
        )

        # Display the label if available
        if value in labels:
            st.caption(f"Selected: {labels[value]}")

        numeric_value = values.get(value, value)
        return value, numeric_value

    # Default, return None if type is not supported
    return None, None


def prepare_prediction_data(user_inputs, feature_names, scaler=None):
    """
    Prepare data for prediction based on user inputs

    Args:
        user_inputs (dict): Dictionary with numeric values entered
        feature_names (list): List of feature names for the model
        scaler (object, optional): Scaler for standardization

    Returns:
        numpy.ndarray: Feature vector for prediction
    """
    # Create feature vector for prediction
    features_vector = np.zeros(len(feature_names))

    # Fill the vector with user entered values
    for i, feature in enumerate(feature_names):
        # Try to find the column in user_inputs
        for col, val in user_inputs.items():
            if col in feature or feature in col:
                features_vector[i] = val
                break

    # Scale the vector if we have a scaler
    if scaler is not None:
        try:
            features_vector = scaler.transform([features_vector])[0]
        except Exception as e:
            st.warning(f"Could not scale the feature vector: {e}")

    return features_vector


def show_prediction_results(model, features_vector):
    """
    Display prediction results

    Args:
        model: Trained model
        features_vector: Feature vector for prediction
    """
    # Make the prediction
    prediction = model.predict([features_vector])[0]
    probabilities = model.predict_proba([features_vector])[0]

    # Display the result
    st.success(f"Estimated sleep quality: **{SLEEP_CLASSES[prediction]}**")

    # Display probabilities
    prob_df = pd.DataFrame({
        'Sleep Quality': [SLEEP_CLASSES[i + 1] for i in range(len(probabilities))],
        'Probability': probabilities
    })

    fig = px.bar(
        prob_df,
        x='Sleep Quality',
        y='Probability',
        title='Prediction Probabilities',
        color='Sleep Quality',
        color_discrete_map=COLOR_MAP
    )

    st.plotly_chart(fig, use_container_width=True)

    # If the model has feature_importances_, show contributions
    if hasattr(model, 'feature_importances_'):
        st.subheader("Top factors that influenced the prediction")
        st.info("These factors had the greatest influence on the prediction.")


def create_sleep_quality_chart(df, quality_col):
    """Create chart for sleep quality distribution"""
    # Map values to numbers for sorting
    mapping = {
        'Very Bad': 1,
        'Pretty Bad': 2,
        'Quite Good': 3,
        'Very Good': 4
    }

    # Create a DataFrame with chart data
    quality_counts = df[quality_col].value_counts().reset_index()
    quality_counts.columns = ['Sleep Quality', 'Count']

    # Add sorting column
    quality_counts['Sort'] = quality_counts['Sleep Quality'].map(mapping)
    quality_counts = quality_counts.sort_values('Sort')

    # Create chart
    fig = px.bar(
        quality_counts,
        x='Sleep Quality',
        y='Count',
        title='Sleep Quality Distribution',
        color='Sleep Quality',
        color_discrete_map=COLOR_MAP
    )

    return fig


def create_feature_importance_chart(model, feature_names, top_n=15):
    """Create chart for feature importance"""
    if not hasattr(model, 'feature_importances_'):
        return None

    # Create DataFrame for importance
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    # Limit to top N
    importance_df = importance_df.head(top_n)

    # Simplify names
    importance_df['Feature'] = importance_df['Feature'].apply(
        lambda x: x.split('. ', 1)[1] if '. ' in x else x
    )

    # Create chart
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title=f'Top {top_n} Factors by Importance'
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    return fig