from cryptography.fernet import Fernet
import io
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler


class DataPreparation:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_path = self.project_root / "data" / "P2.4_Military_Responses.csv.encrypted"
        self.encoders = {}
        self.scalers = {}

    def load_data(self):
        try:
            key_path = "secret.key"
            # Forțăm calea către fișierul criptat
            encrypted_path = "data/P2.4_Military_Responses.csv.encrypted"
            
            with open(key_path, "rb") as k:
                key = k.read()
            f = Fernet(key)
            
            with open(encrypted_path, "rb") as file:
                encrypted_content = file.read()
            
            decrypted_content = f.decrypt(encrypted_content)
            self.df = pd.read_csv(io.BytesIO(decrypted_content))
            
            print("Succes: Datele au fost decriptate în memorie!")
            return self.df
            
        except Exception as e:
            print(f"Eroare la decriptare: {e}")
            # Dacă nu găsește fișierul criptat, încercăm să returnăm originalul 
            # (doar ca să nu crape dashboard-ul în timpul testelor)
            return pd.read_csv(self.data_path)

    def find_column_by_partial_name(self, partial_name):
        for col in self.df.columns:
            if partial_name.lower() in col.lower():
                return col
        return None

    def prepare_sleep_quality_target(self):
        quality_col = self.find_column_by_partial_name("How would you rate your sleep quality")

        if quality_col is None:
            print("EROARE: Nu am găsit coloana pentru calitatea somnului!")
            return


        quality_mapping = {
            'Very Bad': 1,
            'Pretty Bad': 2,
            'Quite Good': 3,
            'Very Good': 4
        }

        self.df['sleep_quality_numeric'] = self.df[quality_col].map(quality_mapping)
        print(
            f"Calitatea somnului convertită la valori numerice: {self.df['sleep_quality_numeric'].value_counts().sort_index()}")

    def prepare_environmental_features(self):
        frequency_mapping = {
            'Never': 0,
            'Less than 1': 0.5,
            '1-2 times': 1.5,
            'More than 3': 4
        }

        cold_col = self.find_column_by_partial_name("extremely cold at night")
        hot_col = self.find_column_by_partial_name("extremely hot at night")
        noise_col = self.find_column_by_partial_name("hearing a noise")
        cough_col = self.find_column_by_partial_name("coughing at night")

        freq_columns = {
            'cold_at_night_freq': cold_col,
            'hot_at_night_freq': hot_col,
            'noise_at_night_freq': noise_col,
            'cough_snoring_freq': cough_col
        }

        for new_name, col in freq_columns.items():
            if col:
                self.df[new_name] = self.df[col].map(frequency_mapping)
                print(f"Creat feature: {new_name}")


    def prepare_sleep_features(self):
        sleep_duration_col = self.find_column_by_partial_name("How many hours did you sleep")
        sleep_latency_col = self.find_column_by_partial_name("How long (minutes) did it usually take")
        bedtime_col = self.find_column_by_partial_name("What time did you usually go to bed")
        waketime_col = self.find_column_by_partial_name("What time did you usually get up")

        if sleep_duration_col:
            self.df['sleep_duration'] = pd.to_numeric(self.df[sleep_duration_col], errors='coerce')
            print(f"Creat feature: sleep_duration din '{sleep_duration_col}'")

        if sleep_latency_col:
            self.df['sleep_latency'] = pd.to_numeric(self.df[sleep_latency_col], errors='coerce')
            print(f"Creat feature: sleep_latency din '{sleep_latency_col}'")

        if bedtime_col:
            self.df['bedtime_numeric'] = self.convert_time_to_minutes(self.df[bedtime_col])
            print(f"Creat feature: bedtime_numeric din '{bedtime_col}'")

        if waketime_col:
            self.df['waketime_numeric'] = self.convert_time_to_minutes(self.df[waketime_col])
            print(f"Creat feature: waketime_numeric din '{waketime_col}'")


    def convert_time_to_minutes(self, time_series):

        def time_to_minutes(time_str):
            try:
                time_str = str(time_str).strip()

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

                return total_minutes
            except:
                return np.nan

        return time_series.apply(time_to_minutes)

    def create_feature_dataset(self):
        features = []

        potential_features = [
            'sleep_duration',
            'sleep_latency',
            'bedtime_numeric',
            'waketime_numeric',
            'cold_at_night_freq',
            'hot_at_night_freq',
            'noise_at_night_freq',
            'cough_snoring_freq'
        ]

        for feature in potential_features:
            if feature in self.df.columns:
                features.append(feature)

        sports_col = self.find_column_by_partial_name("practical sports lessons")
        martial_arts_col = self.find_column_by_partial_name("martial arts")
        military_col = self.find_column_by_partial_name("military training")

        if sports_col:
            self.df['sports_hours'] = pd.to_numeric(self.df[sports_col], errors='coerce')
            features.append('sports_hours')

        if martial_arts_col:
            self.df['martial_arts_hours'] = pd.to_numeric(self.df[martial_arts_col], errors='coerce')
            features.append('martial_arts_hours')

        if military_col:
            self.df['military_hours'] = pd.to_numeric(self.df[military_col], errors='coerce')
            features.append('military_hours')

        print(f"\nFeatures finale: {features}")

        X = self.df[features].copy()
        y = self.df['sleep_quality_numeric'].copy()

        X = X.fillna(X.mean())

        processed_data_path = self.project_root / "data" / "processed_sleep_data.csv"
        final_df = pd.concat([X, y], axis=1)
        final_df.to_csv(processed_data_path, index=False)

        print(f"\nDataset-ul final salvat la: {processed_data_path}")
        print(f"Features: {X.shape[1]}")
        print(f"Observații: {X.shape[0]}")

        return X, y


if __name__ == "__main__":
    prep = DataPreparation()
    df = prep.load_data()
    prep.prepare_sleep_quality_target()
    prep.prepare_environmental_features()
    prep.prepare_sleep_features()
    X, y = prep.create_feature_dataset()

    print("\nSucces")
