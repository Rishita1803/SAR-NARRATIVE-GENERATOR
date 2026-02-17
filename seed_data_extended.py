from database import get_db_connection
import uuid

def seed_additional_cases():
    conn = get_db_connection()
    if not conn: return
    cur = conn.cursor()
    
    try:
        # --- CASE 1: THE "MONEY MULE" (Anita Sharma) ---
        # Pattern: Small deposits from many people, then one transfer to a crypto exchange.
        anita_id = str(uuid.uuid4())
        cur.execute("INSERT INTO Customers (customer_id, full_name, risk_score, occupation) VALUES (%s, %s, %s, %s)",
                    (anita_id, 'Anita Sharma', 40, 'Student'))
        
        for i in range(10):
            cur.execute("""INSERT INTO Transactions (customer_id, amount, transaction_type, is_alert, alert_type) 
                           VALUES (%s, %s, 'UPI_IN', TRUE, 'Mule Pattern')""", 
                        (anita_id, 5000.00))
        
        # --- CASE 2: THE "SHELL COMPANY" (Apex Global Solutions) ---
        # Pattern: Large, round-dollar transfers with no clear business purpose.
        apex_id = str(uuid.uuid4())
        cur.execute("INSERT INTO Customers (customer_id, full_name, risk_score, occupation) VALUES (%s, %s, %s, %s)",
                    (apex_id, 'Apex Global Solutions', 90, 'Import/Export'))
        
        cur.execute("""INSERT INTO Transactions (customer_id, amount, transaction_type, is_alert, alert_type) 
                       VALUES (%s, %s, 'WIRE_OUT', TRUE, 'High-Value Round Sum')""", 
                    (apex_id, 2500000.00))

        conn.commit()
        print("✅ Added Anita Sharma (Mule) and Apex Global (Shell Company) to the database.")
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_additional_cases()