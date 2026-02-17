-- Enable UUID extension for unique tracking across distributed systems
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Customers Table (KYC Data)
CREATE TABLE Customers (
    customer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    risk_score INT CHECK (risk_score BETWEEN 0 AND 100),
    kyc_status VARCHAR(50),
    occupation VARCHAR(100),
    onboarding_date DATE,
    country_of_residence VARCHAR(2) -- ISO code
);

-- 2. Transactions Table (Alerts & Activity)
CREATE TABLE Transactions (
    transaction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES Customers(customer_id),
    source_account VARCHAR(50),
    destination_account VARCHAR(50),
    amount DECIMAL(15, 2),
    currency VARCHAR(3) DEFAULT 'INR',
    transaction_type VARCHAR(50), -- e.g., 'UPI_IN', 'WIRE_OUT'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_alert BOOLEAN DEFAULT FALSE,
    alert_type VARCHAR(100) -- e.g., 'Structuring', 'Rapid Movement of Funds'
);

-- 3. AuditLogs Table (Transparency & Traceability)
CREATE TABLE AuditLogs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID, -- Links to the specific investigation
    action_taken VARCHAR(100), -- e.g., 'DATA_RETRIEVAL', 'DRAFT_GENERATED'
    performed_by VARCHAR(100), -- 'SYSTEM_AI' or 'ANALYST_NAME'
    rationale TEXT, -- The "Why" behind the action
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB -- Stores the specific data points used by the LLM
);