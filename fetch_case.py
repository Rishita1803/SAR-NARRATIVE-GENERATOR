import json
from database import get_db_connection

def fetch_case_data(customer_name="Anita Sharma"):
    conn = get_db_connection()
    if not conn:
        return None
    
    cur = conn.cursor()
    try:
        # 1. Fetch Customer Profile
        cur.execute("""
            SELECT customer_id, full_name, risk_score, occupation, country_of_residence 
            FROM Customers WHERE full_name = %s
        """, (customer_name,))
        customer = cur.fetchone()
        
        if not customer:
            print("No customer found.")
            return None

        # 2. Fetch all Transaction Alerts for this customer
        cur.execute("""
            SELECT transaction_id, amount, transaction_type, timestamp, alert_type
            FROM Transactions 
            WHERE customer_id = %s AND is_alert = TRUE
            ORDER BY timestamp ASC
        """, (customer[0],))
        transactions = cur.fetchall()

        # 3. Format into a clean JSON structure
        case_package = {
            "subject": {
                "name": customer[1],
                "risk_level": customer[2],
                "occupation": customer[3],
                "country": customer[4]
            },
            "alerts": [
                {
                    "id": t[0],
                    "amount": float(t[1]),
                    "type": t[2],
                    "date": t[3].isoformat(),
                    "reason": t[4]
                } for t in transactions
            ],
            "summary": {
                "total_alerts": len(transactions),
                "total_value": sum(float(t[1]) for t in transactions)
            }
        }

        return case_package

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    case = fetch_case_data()
    if case:
        # This prints the clean JSON the AI will "read"
        print(json.dumps(case, indent=4))