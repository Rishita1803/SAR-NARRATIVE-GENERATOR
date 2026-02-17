from database import get_db_connection
import uuid
from datetime import datetime

def seed_clean_records():
    conn = get_db_connection()
    if not conn: return
    cur = conn.cursor()
    
    try:
        # --- CASE: NORMAL USER (Ishaan Verma) ---
        ishaan_id = str(uuid.uuid4())
        
        # 1. Add Customer (Low Risk)
        cur.execute("""
            INSERT INTO Customers (customer_id, full_name, risk_score, occupation, country_of_residence) 
            VALUES (%s, %s, %s, %s, %s)""",
            (ishaan_id, 'Ishaan Verma', 10, 'Software Engineer', 'IN'))
        
        # 2. Add Normal Transactions (Salary & Rent)
        # Transaction 1: Salary Credit
        cur.execute("""
            INSERT INTO Transactions (customer_id, amount, transaction_type, is_alert, alert_type) 
            VALUES (%s, %s, %s, %s, %s)""",
            (ishaan_id, 80000.00, 'SALARY_CREDIT', False, None))
        
        # Transaction 2: Rent Payment
        cur.execute("""
            INSERT INTO Transactions (customer_id, amount, transaction_type, is_alert, alert_type) 
            VALUES (%s, %s, %s, %s, %s)""",
            (ishaan_id, 25000.00, 'RENT_PAYMENT', False, None))

        conn.commit()
        print("✅ Success: Clean data added for Ishaan Verma.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_clean_records()