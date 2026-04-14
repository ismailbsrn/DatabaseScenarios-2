from fastapi import FastAPI
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
app = FastAPI(title="SQL Injection Demo API")

DB_CONFIG = {
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/api/vulnerable/customer")
def get_customer_vulnerable(first_name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = f"SELECT first_name, last_name FROM customer WHERE first_name = '{first_name}';"
    
    try:
        cur.execute(query)
        results = cur.fetchall()
        return {"calisan_sorgu": query, "sonuclar": results}
    except Exception as e:
        return {"hata": str(e)}
    finally:
        conn.close()

@app.get("/api/secure/customer")
def get_customer_secure(first_name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # ÇÖZÜM: Parametrik sorgu (Parameterized Query) kullanmak.
    # %s işareti bir yer tutucudur. psycopg2 kütüphanesi gelen veriyi güvenli bir şekilde escape eder.
    query = "SELECT first_name, last_name FROM customer WHERE first_name = %s;"
    
    try:
        cur.execute(query, (first_name,)) # Parametre tuple olarak gönderiliyor
        results = cur.fetchall()
        return {"calisan_sorgu": query, "sonuclar": results}
    except Exception as e:
        return {"hata": str(e)}
    finally:
        conn.close()