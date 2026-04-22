-- ============================================================================
-- COMPLETE STATES TABLE SETUP
-- Copy this entire script and run it in Supabase SQL Editor
-- ============================================================================

-- Step 1: Create the states table
CREATE TABLE IF NOT EXISTS states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code VARCHAR(2) NOT NULL UNIQUE,
    state_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_states_code ON states(state_code);
CREATE INDEX IF NOT EXISTS idx_states_name ON states(state_name);

-- Step 3: Insert all Indian states and union territories
INSERT INTO states (state_code, state_name) VALUES
-- STATES (28)
('AP', 'Andhra Pradesh'),
('AR', 'Arunachal Pradesh'),
('AS', 'Assam'),
('BR', 'Bihar'),
('CG', 'Chhattisgarh'),
('GA', 'Goa'),
('GJ', 'Gujarat'),
('HR', 'Haryana'),
('HP', 'Himachal Pradesh'),
('JK', 'Jammu and Kashmir'),
('JH', 'Jharkhand'),
('KA', 'Karnataka'),
('KL', 'Kerala'),
('MP', 'Madhya Pradesh'),
('MH', 'Maharashtra'),
('MN', 'Manipur'),
('ML', 'Meghalaya'),
('MZ', 'Mizoram'),
('NL', 'Nagaland'),
('OR', 'Odisha'),
('PB', 'Punjab'),
('RJ', 'Rajasthan'),
('SK', 'Sikkim'),
('TN', 'Tamil Nadu'),
('TG', 'Telangana'),
('TR', 'Tripura'),
('UP', 'Uttar Pradesh'),
('UT', 'Uttarakhand'),
('WB', 'West Bengal'),

-- UNION TERRITORIES (8)
('AN', 'Andaman and Nicobar Islands'),
('CH', 'Chandigarh'),
('DD', 'Dadra and Nagar Haveli and Daman and Diu'),
('LA', 'Ladakh'),
('LL', 'Lakshadweep'),
('DL', 'Delhi'),
('PY', 'Puducherry'),
('LD', 'Lakshadweep (Alt)');

-- Step 4: Verify all states are inserted
SELECT COUNT(*) as total_states, COUNT(DISTINCT state_code) as unique_codes
FROM states;

-- Step 5: Display all states
SELECT state_code, state_name FROM states ORDER BY state_name;
