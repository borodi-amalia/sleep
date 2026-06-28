from cryptography.fernet import Fernet
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import hashlib
import secrets
import random
import smtplib
import os
from email.mime.text import MIMEText

load_dotenv(override=True)


def project_root():
    return Path(__file__).parent.parent


def generate_key():
    key_path = project_root() / "secret.key"
    key = Fernet.generate_key()

    with open(key_path, "wb") as key_file:
        key_file.write(key)

    print(f"Cheia a fost generată și salvată în '{key_path}'")


def load_key():
    key_path = project_root() / "secret.key"

    if not key_path.exists():
        raise FileNotFoundError(f"Nu există cheia de decriptare: {key_path}")

    return key_path.read_bytes()


def encrypt_file(file_path):
    file_path = Path(file_path)

    if not file_path.is_absolute():
        file_path = project_root() / file_path

    if not file_path.exists():
        print(f"Eroare: Fișierul {file_path} nu a fost găsit!")
        return

    key = load_key()
    f = Fernet(key)

    file_data = file_path.read_bytes()
    encrypted_data = f.encrypt(file_data)

    encrypted_path = file_path.with_name(file_path.name + ".encrypted")
    encrypted_path.write_bytes(encrypted_data)

    print(f"SUCCES: Fișierul {file_path} a fost criptat sub numele {encrypted_path}")


def decrypt_file_to_bytes(encrypted_file_path):
    encrypted_file_path = Path(encrypted_file_path)

    if not encrypted_file_path.is_absolute():
        encrypted_file_path = project_root() / encrypted_file_path

    if not encrypted_file_path.exists():
        raise FileNotFoundError(f"Fișierul criptat nu există: {encrypted_file_path}")

    key = load_key()
    f = Fernet(key)

    encrypted_data = encrypted_file_path.read_bytes()
    decrypted_data = f.decrypt(encrypted_data)

    return decrypted_data


def hash_password(password, salt=None):
    
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return salt, password_hash


def verify_password(password, salt, expected_hash):
    
    _, password_hash = hash_password(password, salt)
    return secrets.compare_digest(password_hash, expected_hash)


def audit_log(action, username="unknown", status="INFO"):
   
    logs_dir = project_root() / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_path = logs_dir / "security_audit.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"{timestamp} | {status} | user={username} | action={action}\n"

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(message)


def anonymize_dataframe(df):
    """
    Elimină coloanele care pot conține date personale sau identificatori
    """
    if df is None:
        return None

    sensitive_keywords = [
        "name", "nume",
        "email", "mail",
        "phone", "telefon",
        "address", "adresa",
        "cnp",
        "id",
        "unit", "unitate",
        "rank", "grad"
    ]

    columns_to_drop = []

    for column in df.columns:
        col_lower = column.lower()
        if any(keyword in col_lower for keyword in sensitive_keywords):
            columns_to_drop.append(column)

    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    return df
def generate_verification_code():
    """
    Generate a 6-digit verification code for email-based 2FA.
    """
    return str(random.randint(100000, 999999))


def send_verification_email(to_email, code):
    """
    Send a verification code to the user's email address.
    SMTP credentials are loaded from environment variables.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    print("SMTP_SERVER used:", smtp_server)
    print("SMTP_EMAIL used:", smtp_email)

    if not smtp_server or not smtp_email or not smtp_password:
        raise ValueError("SMTP configuration missing. Check the .env file.")

    subject = "Your dashboard verification code"
    body = f"""
Hello,

Your verification code for the Military Sleep Quality Dashboard is:

{code}

If you did not request this code, please ignore this email.
"""

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = smtp_email
    message["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(message)


if __name__ == "__main__":
    key_path = project_root() / "secret.key"

    if not key_path.exists():
        generate_key()

    encrypt_file("data/P2.4_Military_Responses.csv")
    encrypt_file("data/processed_sleep_data.csv")