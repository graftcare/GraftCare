// Indian States (28 only - no union territories)
const STATES = [
  { code: 'AP', name: 'Andhra Pradesh' },
  { code: 'AR', name: 'Arunachal Pradesh' },
  { code: 'AS', name: 'Assam' },
  { code: 'BR', name: 'Bihar' },
  { code: 'CG', name: 'Chhattisgarh' },
  { code: 'GA', name: 'Goa' },
  { code: 'GJ', name: 'Gujarat' },
  { code: 'HR', name: 'Haryana' },
  { code: 'HP', name: 'Himachal Pradesh' },
  { code: 'JK', name: 'Jammu and Kashmir' },
  { code: 'JH', name: 'Jharkhand' },
  { code: 'KA', name: 'Karnataka' },
  { code: 'KL', name: 'Kerala' },
  { code: 'MP', name: 'Madhya Pradesh' },
  { code: 'MH', name: 'Maharashtra' },
  { code: 'MN', name: 'Manipur' },
  { code: 'ML', name: 'Meghalaya' },
  { code: 'MZ', name: 'Mizoram' },
  { code: 'NL', name: 'Nagaland' },
  { code: 'OR', name: 'Odisha' },
  { code: 'PB', name: 'Punjab' },
  { code: 'RJ', name: 'Rajasthan' },
  { code: 'SK', name: 'Sikkim' },
  { code: 'TN', name: 'Tamil Nadu' },
  { code: 'TG', name: 'Telangana' },
  { code: 'TR', name: 'Tripura' },
  { code: 'UP', name: 'Uttar Pradesh' },
  { code: 'UT', name: 'Uttarakhand' },
  { code: 'WB', name: 'West Bengal' }
];

/**
 * Populate state dropdown in HTML element
 * @param {string} elementId - The ID of the select element
 * @param {string} defaultText - Default option text (optional)
 */
function populateStates(elementId, defaultText = '-- Select State --') {
  const element = document.getElementById(elementId);
  if (!element) {
    console.warn(`Element with ID "${elementId}" not found`);
    return;
  }

  // Clear existing options
  element.innerHTML = '';

  // Add default option
  const defaultOption = document.createElement('option');
  defaultOption.value = '';
  defaultOption.textContent = defaultText;
  element.appendChild(defaultOption);

  // Add all states
  STATES.forEach(state => {
    const option = document.createElement('option');
    option.value = state.code;
    option.textContent = state.name;
    option.dataset.code = state.code;
    element.appendChild(option);
  });
}

/**
 * Get state name by code
 * @param {string} code - State code (e.g., 'MH')
 * @returns {string} State name or empty string
 */
function getStateName(code) {
  const state = STATES.find(s => s.code === code);
  return state ? state.name : '';
}

/**
 * Get state code by name
 * @param {string} name - State name
 * @returns {string} State code or empty string
 */
function getStateCode(name) {
  const state = STATES.find(s => s.name === name);
  return state ? state.code : '';
}

/**
 * Initialize all state dropdowns on page
 */
function initializeAllStateDropdowns() {
  // Purchase Invoice state dropdowns - always populate these
  populateStates('pu-vstate', '-- Select Vendor State --');
  populateStates('pu-mystate', '-- Select Your State --');

  // Other state dropdowns - only populate if empty
  const stateDropdownIds = [
    'vendor-state',   // Generic vendor state
    'customer-state', // Generic customer state
    'buyer-state'     // Generic buyer state
  ];

  stateDropdownIds.forEach(id => {
    const element = document.getElementById(id);
    if (element && element.children.length <= 1) {
      populateStates(id);
    }
  });

  // Also find and populate any elements with data-type="state-select"
  const dataTypeSelects = document.querySelectorAll('[data-type="state-select"]');
  dataTypeSelects.forEach(select => {
    if (select.id && select.id !== 'pu-vstate' && select.id !== 'pu-mystate' && select.children.length <= 1) {
      populateStates(select.id);
    }
  });
}

/**
 * Debug function to check state initialization
 */
window.debugStates = function() {
  console.log('=== STATE DEBUG ===');
  console.log('Total States:', STATES.length);
  console.log('Dropdown IDs:', ['pu-vstate', 'pu-mystate', 'r-state', 'p-state']);
  console.log('Checking dropdowns...');

  ['pu-vstate', 'pu-mystate', 'r-state', 'p-state'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      console.log(`✓ ${id}: exists, options=${el.options.length}`);
    } else {
      console.log(`✗ ${id}: NOT FOUND`);
    }
  });
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    console.log('States.js: Initializing dropdowns...');
    initializeAllStateDropdowns();
    console.log('States.js: Initialization complete');
  });
} else {
  // DOM already loaded
  console.log('States.js: DOM already loaded, initializing...');
  setTimeout(function() {
    initializeAllStateDropdowns();
    console.log('States.js: Initialization complete');
  }, 500);
}
