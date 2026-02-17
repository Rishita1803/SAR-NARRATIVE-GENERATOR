import uuid
import random
from datetime import datetime, timedelta
from database import get_db_connection

def seed_suspicious_case():
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    try:
        # 1. Create the Customer
        customer_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO Customers (customer_id, full_name, risk_score, kyc_status, occupation, country_of_residence)
            VALUES (%s, 'Rajesh Kumar', 75, 'Verified', 'Consultant', 'IN')
        """, (customer_id,))

        # 2. Generate 47 Incoming Transactions (Structuring)
        total_inbound = 5000000.00 # ₹50 Lakhs
        for i in range(47):
            amt = round(random.uniform(95000, 105000), 2)
            cur.execute("""
                INSERT INTO Transactions (customer_id, source_account, destination_account, amount, transaction_type, is_alert, alert_type)
                VALUES (%s, %s, 'ACC-8899', %s, 'UPI_IN', TRUE, 'Potential Structuring')
            """, (customer_id, f"SRC-ACT-{i}", amt))

        # 3. Generate 1 Massive Outgoing Wire (Integration)
        cur.execute("""
            INSERT INTO Transactions (customer_id, source_account, destination_account, amount, transaction_type, is_alert, alert_type)
            VALUES (%s, 'ACC-8899', 'OFFSHORE-UAE-123', %s, 'WIRE_OUT', TRUE, 'Rapid Movement of Funds')
        """, (customer_id, total_inbound))

        conn.commit()
        print("✅ Success! 47 incoming transactions and 1 wire-out seeded for Rajesh Kumar.")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_suspicious_case()