# FreeWithBTC - Existing Code Reference

This document outlines the key functions, patterns, and data structures to port from the existing Bitcoin Budget app into the new FreeWithBTC application.

## Critical Functions to Port

### Bitcoin Price Modeling Functions
```python
# From streamlit_app.py - Core calculation functions
def calculate_bitcoin_price_conservative(current_price, years):
    """Conservative 4-year cycle model with realistic growth rates"""
    cycle_length = 4
    growth_rates = [0.5, 1.5, 2.0, 0.8]  # 50%, 150%, 200%, 80% per year
    floor_multiplier = 0.15  # 15% of peak becomes next cycle floor
    
    price = current_price
    for year in range(years):
        cycle_position = year % cycle_length
        annual_growth = growth_rates[cycle_position]
        price *= (1 + annual_growth)
    
    return price

def calculate_bitcoin_price_optimistic(current_price, years):
    """Optimistic model with higher growth trajectory"""
    cycle_length = 4
    growth_rates = [1.0, 2.0, 3.0, 1.0]  # 100%, 200%, 300%, 100% per year
    floor_multiplier = 0.2  # 20% of peak becomes next cycle floor
    
    price = current_price
    for year in range(years):
        cycle_position = year % cycle_length
        annual_growth = growth_rates[cycle_position]
        price *= (1 + annual_growth)
    
    return price

def calculate_net_worth_projection(profile, years, model='conservative'):
    """Calculate user's net worth over time"""
    # This is the core function powering all three pillars
    current_btc_sats = profile['current_btc_sats']
    monthly_dca_sats = profile['monthly_dca_sats']
    
    # Calculate Bitcoin price appreciation
    current_btc_price = 100000  # $100k assumption
    if model == 'conservative':
        future_btc_price = calculate_bitcoin_price_conservative(current_btc_price, years)
    else:
        future_btc_price = calculate_bitcoin_price_optimistic(current_btc_price, years)
    
    # Calculate total Bitcoin accumulated through DCA
    total_dca_sats = monthly_dca_sats * 12 * years
    total_btc_sats = current_btc_sats + total_dca_sats
    
    # Calculate net worth in future dollars
    btc_multiplier = future_btc_price / current_btc_price
    future_net_worth_sats = total_btc_sats * btc_multiplier
    
    return future_net_worth_sats
```

### Purchasing Power Calculations
```python
def calculate_purchasing_power_improvement(monthly_expenses_sats, years, model='conservative'):
    """Calculate how expenses reduce on Bitcoin standard"""
    current_btc_price = 100000
    if model == 'conservative':
        future_btc_price = calculate_bitcoin_price_conservative(current_btc_price, years)
    else:
        future_btc_price = calculate_bitcoin_price_optimistic(current_btc_price, years)
    
    # Your expenses in Bitcoin terms become cheaper as Bitcoin appreciates
    purchasing_power_multiplier = future_btc_price / current_btc_price
    future_expense_cost_reduction = 1 - (1 / purchasing_power_multiplier)
    
    return future_expense_cost_reduction

# Example: 86.4% reduction means expenses cost 13.6% of current amount
```

### Financial Freedom Timeline
```python
def calculate_financial_freedom_timeline(profile, model='conservative'):
    """Calculate when Bitcoin holdings cover annual expenses"""
    monthly_expenses_sats = profile['monthly_expenses_sats']
    annual_expenses_sats = monthly_expenses_sats * 12
    
    # Find the year when net worth covers 25 years of expenses
    for year in range(1, 31):  # Check up to 30 years
        net_worth = calculate_net_worth_projection(profile, year, model)
        
        # If net worth covers 25 years of expenses, you're financially free
        if net_worth >= annual_expenses_sats * 25:
            return year
    
    return 30  # Cap at 30 years if not achieved
```

## Mobile-Responsive UI Functions

### Layout Helpers (Keep Exactly As-Is)
```python
def is_mobile_layout():
    """Check if mobile layout is enabled"""
    return st.session_state.get('mobile_mode', False)

def get_responsive_columns(desktop_cols):
    """Get responsive column count for desktop vs mobile"""
    if is_mobile_layout():
        return min(2, desktop_cols)  # Max 2 columns on mobile
    return desktop_cols

def mobile_friendly_metrics(metrics_data):
    """Display metrics in mobile-friendly layout"""
    if is_mobile_layout():
        # Stack in pairs for mobile
        for i in range(0, len(metrics_data), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(metrics_data):
                    with col:
                        metric = metrics_data[i + j]
                        st.metric(metric['label'], metric['value'])
    else:
        # Single row for desktop
        cols = st.columns(len(metrics_data))
        for i, (col, metric) in enumerate(zip(cols, metrics_data)):
            with col:
                st.metric(metric['label'], metric['value'])

def mobile_responsive_header(text, level=3):
    """Show smaller headers on mobile"""
    if is_mobile_layout():
        level = min(6, level + 1)  # One level smaller on mobile
    st.markdown('#' * level + ' ' + text)
```

## UX Enhancement Functions (Keep All)

### Toast Notification System
```python
def show_success_toast(message):
    """Show Bitcoin-themed success toast"""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #f7931a 0%, #ffb84d 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            margin: 8px 0;
            box-shadow: 0 2px 8px rgba(247, 147, 26, 0.3);
        ">
            ✅ {message}
        </div>
        """, 
        unsafe_allow_html=True
    )

def show_bitcoin_toast(message, toast_type='success'):
    """Show styled toast notification with Bitcoin theming"""
    colors = {
        'success': ('#f7931a', '#ffb84d', '✅'),
        'warning': ('#ff9800', '#ffb74d', '⚠️'),
        'error': ('#f44336', '#e57373', '❌'),
        'info': ('#2196f3', '#64b5f6', 'ℹ️')
    }
    
    color1, color2, icon = colors.get(toast_type, colors['success'])
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, {color1} 0%, {color2} 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            margin: 8px 0;
            box-shadow: 0 2px 8px rgba(247, 147, 26, 0.3);
        ">
            {icon} {message}
        </div>
        """, 
        unsafe_allow_html=True
    )

def show_loading_spinner(message="Loading..."):
    """Show loading spinner with message"""
    return st.spinner(message)

def with_loading_state(func, loading_message="Processing..."):
    """Execute function with loading state"""
    with st.spinner(loading_message):
        return func()
```

## Bitcoin Amount Formatting (Critical)

### Satoshi Handling Functions
```python
def format_sats(satoshis):
    """Format satoshis for display"""
    if satoshis == 0:
        return "0 sats"
    return f"{satoshis:,} sats"

def format_btc(satoshis):
    """Format as BTC for display"""
    btc = satoshis / 100_000_000
    return f"{btc:.8f} BTC"

def parse_amount_input(text):
    """Parse user input to satoshis (integers only)"""
    try:
        # Remove commas and whitespace
        clean_text = text.replace(',', '').strip()
        
        # Handle BTC input (convert to satoshis)
        if 'btc' in clean_text.lower():
            btc_amount = float(clean_text.lower().replace('btc', '').strip())
            return int(btc_amount * 100_000_000)
        
        # Handle satoshi input
        return int(float(clean_text))
        
    except (ValueError, TypeError):
        raise ValueError(f"Invalid amount format: {text}")

def validate_bitcoin_amount(sats):
    """Validate Bitcoin amount is positive integer"""
    return isinstance(sats, int) and sats >= 0
```

## Session State Management

### Current Session State Structure (Adapt)
```python
# From existing app - simplify for FreeWithBTC
def initialize_session_state():
    """Initialize session state for FreeWithBTC"""
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'profile_type': 'new_stacker',
            'current_btc_sats': 10_000_000,  # 0.1 BTC
            'monthly_dca_sats': 50_000_000,  # $500 equivalent
            'monthly_expenses_sats': 400_000_000,  # $4000 equivalent
            'age': 32,
            'target_retirement_age': 65,
            'customized': False
        }
    
    if 'ui_state' not in st.session_state:
        st.session_state.ui_state = {
            'mobile_mode': False,
            'current_pillar': 'dashboard',
            'show_advanced_features': False
        }
    
    if 'current_month' not in st.session_state:
        st.session_state.current_month = datetime.now().strftime('%Y-%m')
    
    if 'calculations_cache' not in st.session_state:
        st.session_state.calculations_cache = {}
```

## Export/Import Functionality

### Data Management Functions (Port Directly)
```python
import json
from datetime import datetime

def export_budget_data():
    """Export user data as JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"freewithbtc_profile_{timestamp}.json"
    
    export_data = {
        'version': '1.0',
        'timestamp': timestamp,
        'app': 'FreeWithBTC',
        'user_data': st.session_state.user_data,
        'ui_state': st.session_state.ui_state
    }
    
    return json.dumps(export_data, indent=2), filename

def import_budget_data(json_data):
    """Import and validate user data from JSON"""
    try:
        data = json.loads(json_data)
        
        # Validate data structure
        if 'user_data' not in data:
            raise ValueError("Invalid file format: missing user_data")
        
        # Update session state
        st.session_state.user_data = data['user_data']
        if 'ui_state' in data:
            st.session_state.ui_state.update(data['ui_state'])
        
        # Clear calculations cache
        st.session_state.calculations_cache = {}
        
        return True, "Profile imported successfully!"
        
    except Exception as e:
        return False, f"Import failed: {str(e)}"
```

## Plotly Chart Configuration

### Chart Styling (Keep Bitcoin Orange Theme)
```python
import plotly.express as px
import plotly.graph_objects as go

def create_bitcoin_price_chart(years_data, prices_data, title):
    """Create Bitcoin price projection chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years_data,
        y=prices_data,
        mode='lines+markers',
        line=dict(color='#f7931a', width=3),
        marker=dict(color='#f7931a', size=6),
        name='Bitcoin Price'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Years",
        yaxis_title="Bitcoin Price (USD)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#333333'),
        height=400 if not is_mobile_layout() else 300
    )
    
    return fig

def create_net_worth_chart(years_data, net_worth_data, title):
    """Create net worth projection chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years_data,
        y=net_worth_data,
        mode='lines+markers',
        fill='tonexty',
        line=dict(color='#f7931a', width=3),
        fillcolor='rgba(247, 147, 26, 0.1)',
        name='Net Worth'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Years",
        yaxis_title="Net Worth (USD)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#333333'),
        height=400 if not is_mobile_layout() else 300
    )
    
    return fig
```

## Envelope Budgeting Functions (Optional Advanced Feature)

### Core Budgeting Functions (Port for Advanced Users)
```python
# These functions power the advanced budgeting feature
def add_account(name, initial_balance, is_tracked=True):
    """Add Bitcoin account (tracked/untracked)"""
    # Implementation from existing app

def add_income(amount_sats, description, date, account_id):
    """Add income transaction with account tracking"""
    # Implementation from existing app

def add_expense(amount_sats, description, category_id, date, account_id):
    """Add expense transaction with account tracking"""
    # Implementation from existing app

def get_account_balance(account_id):
    """Get current account balance"""
    # Implementation from existing app

def get_category_balance(category_id):
    """Get category balance (allocated - spent)"""
    # Implementation from existing app
```

## Constants and Configuration

### Key Constants (Update for FreeWithBTC)
```python
# Bitcoin constants
SATOSHIS_PER_BITCOIN = 100_000_000
CURRENT_BITCOIN_PRICE = 100_000  # Update as needed

# App constants
APP_NAME = "FreeWithBTC"
APP_VERSION = "1.0"
BITCOIN_ORANGE = "#f7931a"

# Default profiles
NEW_STACKER_DEFAULTS = {
    'current_btc_sats': 10_000_000,      # 0.1 BTC
    'monthly_dca_sats': 50_000_000,      # $500
    'monthly_expenses_sats': 400_000_000, # $4000
    'age': 32
}

OLD_STACKER_DEFAULTS = {
    'current_btc_sats': 100_000_000,     # 1.0 BTC
    'monthly_dca_sats': 100_000_000,     # $1000
    'monthly_expenses_sats': 600_000_000, # $6000
    'age': 38
}
```

## Data Structures to Adapt

### Session State Data Structure (Simplified)
```python
# Original has complex budgeting data - simplify for FreeWithBTC
st.session_state = {
    'user_data': {
        # Core profile data only
        'profile_type': 'new_stacker',
        'current_btc_sats': 10_000_000,
        'monthly_dca_sats': 50_000_000,
        'monthly_expenses_sats': 400_000_000,
        'age': 32,
        'target_retirement_age': 65,
        'customized': False,
        # Advanced budgeting data (only if user enables)
        'accounts': [],
        'transactions': [],
        'categories': [],
        'allocations': []
    },
    'ui_state': {
        'mobile_mode': False,
        'current_pillar': 'dashboard',
        'show_advanced_features': False
    },
    'calculations_cache': {}
}
```

## Error Handling Patterns (Keep)

### Validation and Error Recovery
```python
def safe_calculate(calculation_func, *args, fallback_value=None, error_message=None):
    """Safely execute calculation with error handling"""
    try:
        return calculation_func(*args)
    except Exception as e:
        if error_message:
            st.error(error_message)
        else:
            st.error(f"Calculation error: {str(e)}")
        return fallback_value

def validate_inputs(profile):
    """Validate profile inputs before calculations"""
    # Implementation from existing app
    pass
```

## Migration Priority

### Phase 1: Core Functions (Must Port)
1. ✅ **Bitcoin price modeling** (conservative/optimistic)
2. ✅ **Net worth calculations** (core of all three pillars)
3. ✅ **Mobile responsive helpers** (critical for UX)
4. ✅ **UX enhancement functions** (toasts, loading states)
5. ✅ **Bitcoin amount formatting** (satoshis-only standard)

### Phase 2: Enhanced Features (Should Port)
1. ✅ **Export/import functionality** (user data control)
2. ✅ **Session state management** (privacy-first approach)
3. ✅ **Plotly chart configurations** (Bitcoin orange theming)
4. ✅ **Error handling patterns** (graceful degradation)

### Phase 3: Advanced Features (Optional Port)
1. 🔄 **Envelope budgeting system** (for power users)
2. 🔄 **Advanced reports** (from reports.py module)
3. 🔄 **Complex data structures** (accounts, transactions, categories)

## Key Differences for FreeWithBTC

### Simplifications:
- **Remove complex budgeting** by default (make it optional)
- **Two user profiles** instead of infinite customization
- **Three pillars focus** instead of many features
- **Immediate value** instead of setup requirements

### Enhancements:
- **Profile-based defaults** for quick starts
- **Educational content** about Bitcoin superiority
- **Freedom timeline focus** instead of budgeting focus
- **Bitcoin-only narrative** throughout

Remember: **Port the calculation engine and UX infrastructure, but simplify the user experience dramatically for FreeWithBTC's focused mission.** 