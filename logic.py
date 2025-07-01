import pandas as pd
import mysql.connector
from mysql.connector import Error
import joblib

# Load model
try:
    model = joblib.load('logistic_regression_model (1).pkl')
except FileNotFoundError:
    raise FileNotFoundError("❌ Model file tidak ditemukan.")

# Koneksi ke database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='outlier_data'  # Nama database kamu
        )
        return conn
    except Error as e:
        raise ConnectionError(f"❌ Koneksi ke database gagal: {e}")
    
    
def predict_purchase(data: dict):
    # Encode country dan productname jika diperlukan
    input_df = pd.DataFrame([{
        'Country': data['country_encoded'],         # hasil encoding
        'ProductName': data['product_encoded'],     # hasil encoding
        'Quantity': data['quantity'],
        'Price': data['price']                      
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    return prediction, probability, input_df

def save_to_database(data: dict):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (
            country, productname, quantity
        ) VALUES (%s, %s, %s)
    """, (
        data['country'],
        data['productname'],
        data['quantity']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_predictions():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM predictions ORDER BY customerid DESC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    cursor.close()
    conn.close()
    return df