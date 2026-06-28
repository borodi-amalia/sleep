import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
import joblib
import warnings

warnings.filterwarnings('ignore')


class OptimizedSleepModel:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_path = self.project_root / "data" / "P2.4_Military_Responses.csv"
        self.models_dir = self.project_root / "models"
        self.results_dir = self.project_root / "results"
        self.models_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        self.feature_names = []

    def load_data(self):
        df = pd.read_csv(self.data_path)
        print(f"Date încărcate: {df.shape}")
        return df

    def prepare_target(self, df):
        quality_col = None
        for col in df.columns:
            if 'sleep quality' in col.lower():
                quality_col = col
                break

        quality_mapping = {
            'Very Bad': 1,
            'Pretty Bad': 2,
            'Quite Good': 3,
            'Very Good': 4
        }

        df['sleep_quality_numeric'] = df[quality_col].map(quality_mapping)

        print("Distribuția calității somnului:")
        print(df['sleep_quality_numeric'].value_counts().sort_index())

        return df, 'sleep_quality_numeric'

    def preprocess_features(self, df, target_col):
        quality_col = None
        for col in df.columns:
            if 'sleep quality' in col.lower():
                quality_col = col
                break

        exclude_cols = [target_col, quality_col]
        for col in df.columns:
            if 'timestamp' in col.lower() or 'id' in col.lower():
                exclude_cols.append(col)

        features_df = df.drop(exclude_cols, axis=1, errors='ignore').copy()

        for col in features_df.columns:
            if features_df[col].dtype == 'object':
                if any(kw in col.lower() for kw in ['frequency', 'often', 'times']):
                    mapping = {
                        'Never': 0,
                        'Less than 1': 0.5,
                        '1-2 times': 1.5,
                        'More than 3': 4,
                        'Less than once a week': 0.5,
                        'Once or twice a week': 1.5,
                        'Three or more times a week': 4
                    }
                    features_df[col] = features_df[col].map(mapping)
                else:
                    try:
                        le = LabelEncoder()
                        features_df[col] = le.fit_transform(features_df[col].fillna('Missing').astype(str))
                    except:
                        print(f"  Nu pot face encoding pentru coloana: {col}")
                        features_df[col] = features_df[col].astype('category').cat.codes

        for col in features_df.columns:
            if features_df[col].dtype == 'object':
                features_df[col] = pd.to_numeric(features_df[col], errors='coerce')

        features_df = features_df.fillna(features_df.mean()) #inlocuieste NaN cu media coloanei

        engineered_features = features_df.copy()

        time_cols = [col for col in features_df.columns if any(kw in col.lower() for kw in ['time', 'hour'])]

        for col in time_cols:
            try:
                minutes_vals = []
                for val in features_df[col]:
                    try:
                        if pd.isna(val):
                            minutes_vals.append(0)
                        else:
                            time_str = str(val).strip()
                            if ':' in time_str:
                                parts = time_str.split(':')
                                hours = int(parts[0])
                                minutes = int(parts[1]) if len(parts) > 1 else 0
                            else:
                                hours = int(float(time_str))
                                minutes = 0

                            total_minutes = hours * 60 + minutes
                            if total_minutes < 720:
                                total_minutes += 1440
                                #calculat pt a vedea la cat s a culcat lumea
                            minutes_vals.append(total_minutes)
                    except:
                        minutes_vals.append(0)

                engineered_features[f"{col}_minutes"] = minutes_vals
            except Exception as e:
                print(f"Eroare la procesarea coloanei {col}: {e}")

        features_df = engineered_features

        if features_df.isna().sum().sum() > 0:
            features_df = features_df.fillna(0)

        self.feature_names = features_df.columns.tolist()

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(features_df)

        X = pd.DataFrame(X_scaled, columns=features_df.columns)
        y = df[target_col]

        if X.isna().sum().sum() > 0:
            print(f"EROARE: Încă avem {X.isna().sum().sum()} valori NaN după standardizare.")
            X = X.fillna(0)

        return X, y

    def balance_classes(self, X, y):

        print(f"Distribuția claselor înainte de echilibrare:")
        print(pd.Series(y).value_counts().sort_index())

        if X.isna().sum().sum() > 0:
            print(f"EROARE: Încă avem {X.isna().sum().sum()} valori NaN înainte de SMOTE.")
            X = X.fillna(0)

        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        #face ca fiecare clasa sa aiba un numar egal de instante
        print(f"Distribuția claselor după echilibrare(SMOTE):")
        print(pd.Series(y_resampled).value_counts().sort_index())

        return X_resampled, y_resampled

    def optimize_random_forest(self, X, y):
        print("\nOptimizăm hiperparametrii pentru Random Forest...")

        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'class_weight': ['balanced', 'balanced_subsample', None]
        }

        base_model = RandomForestClassifier(random_state=42)

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        #80% antrenare 20% validare

        random_search = RandomizedSearchCV(
            base_model,
            param_distributions=param_grid,
            n_iter=10,
            cv=5,
            scoring='f1_macro',
            n_jobs=-1,
            random_state=42,
            verbose=1
        )

        random_search.fit(X_train, y_train)

        print(f"\nCei mai buni parametri: {random_search.best_params_}")
        print(f"Cel mai bun scor (F1 macro): {random_search.best_score_:.3f}")
        #Se antrenează mai multe modele și se păstrează cel cu scorul F1 macro cel mai bun.
        best_model = random_search.best_estimator_
        y_pred = best_model.predict(X_val)

        print("\nEvaluare pe setul de validare:")
        print(f"Acuratețe: {accuracy_score(y_val, y_pred):.3f}")
        print(f"F1 Score (macro): {f1_score(y_val, y_pred, average='macro'):.3f}")

        return best_model

    def evaluate_model(self, model, X, y):
        print("\nEvaluare finală a modelului optimizat:")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        model.fit(X_train, y_train) #antrenare model

        y_pred = model.predict(X_test) #prezicere

        accuracy = accuracy_score(y_test, y_pred) #procentul total de predictii corecte
        f1 = f1_score(y_test, y_pred, average='macro')

        print(f"Acuratețe: {accuracy:.3f}")
        print(f"F1 Score (macro): {f1:.3f}")

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)

        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['', 'Very Bad', 'Pretty Bad', 'Quite Good', 'Very Good'],
                    yticklabels=['', 'Very Bad', 'Pretty Bad', 'Quite Good', 'Very Good'])
        plt.title('Confusion Matrix - Optimized Model')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.savefig(self.results_dir / 'optimized_confusion_matrix.png')
        plt.close()

        self.analyze_feature_importance(model, X)

        return accuracy, f1

    def analyze_feature_importance(self, model, X):
        """Analizăm importanța tuturor features"""
        importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        print(f"\nTop 10 cele mai importante features:")
        print(importance_df.head(10))

        plt.figure(figsize=(12, 10))
        sns.barplot(data=importance_df.head(30), x='importance', y='feature')
        plt.title(f'Top 30 Cele Mai Importante Features')
        plt.xlabel('Importanță')
        plt.tight_layout()
        plt.savefig(self.results_dir / 'optimized_feature_importance.png')
        plt.close()

        return importance_df

    def save_model(self, model):
        model_path = self.models_dir / 'optimized_sleep_model.pkl'

        metadata = {
            'model': model,
            'feature_names': self.feature_names,
            'scaler': self.scaler
        }

        joblib.dump(metadata, model_path)
        print(f"\nModel salvat la: {model_path}")

    def run_pipeline(self):
        df = self.load_data()

        df, target_col = self.prepare_target(df)

        X, y = self.preprocess_features(df, target_col)

        X_balanced, y_balanced = self.balance_classes(X, y)

        optimized_model = self.optimize_random_forest(X_balanced, y_balanced)

        accuracy, f1 = self.evaluate_model(optimized_model, X_balanced, y_balanced)

        self.save_model(optimized_model)

        print("\n=== PERFORMANȚĂ MODEL ===")
        print(f"Acuratețe: {accuracy * 100:.1f}%")
        print(f"F1 Score (macro): {f1:.3f}")

        return optimized_model, accuracy, f1


if __name__ == "__main__":
    np.random.seed(42)

    optimized_model = OptimizedSleepModel()
    model, accuracy, f1 = optimized_model.run_pipeline()