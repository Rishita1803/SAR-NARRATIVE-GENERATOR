import json
from fetch_case import fetch_case_as_json  # This imports your Step 5 code
from database import get_db_connection, log_audit_step

def generate_sar_narrative(customer_name):
    # 1. Fetch the data we prepared in Step 5
    case_data = fetch_case_as_json(customer_name)
    
    if "error" in case_data:
        print(f"Error: {case_data['error']}")
        return

    # 2. Extract pieces of information for the report
    profile = case_data['customer_profile']
    alerts = case_data['alerts']
    summary = case_data['summary']

    # 3. Create the Narrative Template
    # This is the "Voice" of the AI.
    narrative = f"""
    === SUSPICIOUS ACTIVITY REPORT (DRAFT) ===
    
    PART I: SUBJECT INFORMATION
    Name: {profile['name']}
    Occupation: {profile['job']}
    Risk Score: {profile['risk_score']}
    Location: {profile['location']}

    PART II: SUMMARY OF SUSPICIOUS ACTIVITY
    A total of {summary['total_alerts']} transaction alerts were identified 
    totaling ₹{summary['total_value']:,}. 
    
    PART III: DETAILED CHRONOLOGY
    The activity began on {alerts[0]['time']}. The pattern shows:
    """

    # Add a line for every alert found in the JSON
    for alert in alerts:
        narrative += f"\n- {alert['time']}: {alert['type']} of ₹{alert['amount']:,} (Reason: {alert['reason']})"

    narrative += f"""
    
    PART IV: CONCLUSION & TYPOLOGY
    The observed behavior of high-frequency incoming transfers followed 
    by rapid depletion is consistent with money laundering typologies. 
    The mismatch between the subject's occupation ({profile['job']}) 
    and the transaction volume warrants further investigation.
    """

    # 4. THE AUDIT TRAIL (The most important part)
    # We record that the AI generated this specific report.
    conn = get_db_connection()
    log_audit_step(
        conn, 
        profile['id'], 
        "NARRATIVE_GENERATED", 
        f"AI drafted report based on {summary['total_alerts']} alerts totaling {summary['total_value']}."
    )
    conn.close()

    return narrative

if __name__ == "__main__":
    # Test with the data we seeded
    result = generate_sar_narrative("Rajesh Kumar")
    print(result)