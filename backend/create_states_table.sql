-- ============================================================================
-- CREATE STATES TABLE FOR INDIA
-- ============================================================================

CREATE TABLE IF NOT EXISTS states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code VARCHAR(2) NOT NULL UNIQUE,
    state_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INSERT ALL INDIAN STATES AND UNION TERRITORIES
-- ============================================================================

INSERT INTO states (state_code, state_name) VALUES
-- States (28)
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

-- Union Territories (8)
('AN', 'Andaman and Nicobar Islands'),
('CH', 'Chandigarh'),
('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
('LD', 'Ladakh'),
('LL', 'Lakshadweep'),
('DL', 'Delhi'),
('PY', 'Puducherry'),
('LA', 'Ladakh');

-- ============================================================================
-- CREATE INDEX FOR FASTER LOOKUPS
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_states_code ON states(state_code);
CREATE INDEX IF NOT EXISTS idx_states_name ON states(state_name);

-- ============================================================================
-- VERIFY DATA
-- ============================================================================

SELECT COUNT(*) as total_states FROM states;
