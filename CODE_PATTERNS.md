# FreeWithBTC - Code Patterns & Style Guide

## Python Style Guidelines

### Naming Conventions
```python
# Functions and variables: snake_case
def calculate_freedom_timeline():
    user_profile = get_current_profile()
    monthly_dca = user_profile['monthly_dca_sats']

# Classes: PascalCase  
class BitcoinCalculator:
    def __init__(self):
        pass

# Constants: UPPER_CASE
BITCOIN_GENESIS_DATE = "2009-01-03"
SATOSHIS_PER_BITCOIN = 100_000_000

# Private functions: _leading_underscore
def _validate_bitcoin_amount(sats):
    return isinstance(sats, int) and sats >= 0
```

### Docstring Style
```python
def calculate_purchasing_power_improvement(expenses_sats, years, model='conservative'):
    """Calculate how expenses reduce on Bitcoin standard over time"""
    # Implementation here
    
def format_sats(satoshis):
    """Format satoshis for display as '1,000,000 sats'"""
    return f"{satoshis:,} sats"
```

### Line Length and Formatting
- **Max line length**: 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Function spacing**: 2 blank lines between functions
- **Import organization**: Standard library, third-party, local imports

## Streamlit Patterns

### Session State Initialization
```python
def initialize_session_state():
    """Initialize all required session state variables"""
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
    
    if 'calculations_cache' not in st.session_state:
        st.session_state.calculations_cache = {}
```

### Mobile-Responsive Layout Helpers
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

### Form Patterns with Mobile Support
```python
def show_profile_customization_form():
    """Show profile customization with mobile responsiveness"""
    form_key = "mobile_customize_form" if is_mobile_layout() else "customize_form"
    
    with st.form(form_key):
        st.subheader("Customize Your Profile")
        
        if is_mobile_layout():
            # Stack vertically on mobile
            current_btc = st.number_input("Current Bitcoin (BTC)", 
                                         value=0.1, min_value=0.0, step=0.01)
            monthly_dca = st.number_input("Monthly DCA ($)", 
                                         value=500, min_value=0, step=50)
            monthly_expenses = st.number_input("Monthly Expenses ($)", 
                                              value=4000, min_value=0, step=100)
            age = st.number_input("Current Age", 
                                 value=32, min_value=18, max_value=80)
        else:
            # Side-by-side on desktop
            col1, col2 = st.columns(2)
            with col1:
                current_btc = st.number_input("Current Bitcoin (BTC)", 
                                             value=0.1, min_value=0.0, step=0.01)
                monthly_dca = st.number_input("Monthly DCA ($)", 
                                             value=500, min_value=0, step=50)
            with col2:
                monthly_expenses = st.number_input("Monthly Expenses ($)", 
                                                  value=4000, min_value=0, step=100)
                age = st.number_input("Current Age", 
                                     value=32, min_value=18, max_value=80)
        
        submitted = st.form_submit_button("Update My Projections", 
                                         use_container_width=True)
        
        if submitted:
            with_loading_state(update_profile_and_recalculate, 
                             "Updating your projections...")
```

## Bitcoin-Specific Patterns

### Amount Handling (Satoshis Only)
```python
def format_sats(satoshis):
    """Format satoshis for display"""
    if satoshis == 0:
        return "0 sats"
    return f"{satoshis:,} sats"

def format_btc(satoshis):
    """Format as BTC for display"""
    btc = satoshis / SATOSHIS_PER_BITCOIN
    return f"{btc:.8f} BTC"

def parse_amount_input(text):
    """Parse user input to satoshis (integers only)"""
    try:
        # Remove commas and whitespace
        clean_text = text.replace(',', '').strip()
        
        # Handle BTC input (convert to satoshis)
        if 'btc' in clean_text.lower():
            btc_amount = float(clean_text.lower().replace('btc', '').strip())
            return int(btc_amount * SATOSHIS_PER_BITCOIN)
        
        # Handle satoshi input
        return int(float(clean_text))
        
    except (ValueError, TypeError):
        raise ValueError(f"Invalid amount format: {text}")

def validate_bitcoin_amount(sats):
    """Validate Bitcoin amount is positive integer"""
    return isinstance(sats, int) and sats >= 0
```

### Bitcoin Price Models
```python
BITCOIN_MODELS = {
    'conservative': {
        'cycle_years': 4,
        'growth_rates': [0.5, 1.5, 2.0, 0.8],  # Per year in cycle
        'floor_multiplier': 0.15,
        'description': 'Realistic 4-year cycle model'
    },
    'optimistic': {
        'cycle_years': 4,
        'growth_rates': [1.0, 2.0, 3.0, 1.0],
        'floor_multiplier': 0.2,
        'description': 'Higher growth trajectory'
    }
}

def calculate_bitcoin_price_projection(current_price, years, model='conservative'):
    """Calculate Bitcoin price at future date using cycle models"""
    model_config = BITCOIN_MODELS[model]
    cycle_years = model_config['cycle_years']
    growth_rates = model_config['growth_rates']
    
    price = current_price
    for year in range(years):
        cycle_position = year % cycle_years
        annual_growth = growth_rates[cycle_position]
        price *= (1 + annual_growth)
    
    return price

@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_net_worth_projection(profile, years, model='conservative'):
    """Calculate user's net worth over time with caching"""
    # Implementation here
    pass
```

## UX Enhancement Functions

### Toast Notifications
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

### Error Handling Patterns
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

def validate_profile_data(profile):
    """Validate profile data before calculations"""
    required_fields = ['current_btc_sats', 'monthly_dca_sats', 'monthly_expenses_sats', 'age']
    
    for field in required_fields:
        if field not in profile:
            raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(profile[field], (int, float)) or profile[field] < 0:
            raise ValueError(f"Invalid value for {field}: {profile[field]}")
    
    return True
```

## Data Management Patterns

### Session State Operations
```python
def get_user_profile():
    """Get current user profile from session state"""
    return st.session_state.user_data

def update_user_profile(updates):
    """Update user profile in session state"""
    if validate_profile_data(updates):
        st.session_state.user_data.update(updates)
        st.session_state.user_data['customized'] = True
        # Clear calculations cache when profile changes
        st.session_state.calculations_cache = {}

def reset_to_default_profile(profile_type='new_stacker'):
    """Reset to default profile"""
    if profile_type == 'new_stacker':
        default_profile = {
            'profile_type': 'new_stacker',
            'current_btc_sats': 10_000_000,  # 0.1 BTC
            'monthly_dca_sats': 50_000_000,  # $500 equivalent
            'monthly_expenses_sats': 400_000_000,  # $4000 equivalent
            'age': 32,
            'target_retirement_age': 65,
            'customized': False
        }
    else:  # old_stacker
        default_profile = {
            'profile_type': 'old_stacker',
            'current_btc_sats': 100_000_000,  # 1 BTC
            'monthly_dca_sats': 100_000_000,  # $1000 equivalent
            'monthly_expenses_sats': 600_000_000,  # $6000 equivalent
            'age': 38,
            'target_retirement_age': 55,
            'customized': False
        }
    
    st.session_state.user_data = default_profile
    st.session_state.calculations_cache = {}
```

### Export/Import Patterns
```python
import json
from datetime import datetime

def export_user_data():
    """Export user data as JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"freewithbtc_profile_{timestamp}.json"
    
    export_data = {
        'version': '1.0',
        'timestamp': timestamp,
        'user_data': st.session_state.user_data,
        'ui_state': st.session_state.ui_state
    }
    
    return json.dumps(export_data, indent=2), filename

def import_user_data(uploaded_file):
    """Import user data from JSON file"""
    try:
        data = json.loads(uploaded_file.getvalue())
        
        # Validate data structure
        if 'user_data' not in data:
            raise ValueError("Invalid file format: missing user_data")
        
        # Validate profile data
        validate_profile_data(data['user_data'])
        
        # Update session state
        st.session_state.user_data = data['user_data']
        if 'ui_state' in data:
            st.session_state.ui_state.update(data['ui_state'])
        
        # Clear cache
        st.session_state.calculations_cache = {}
        
        return True, "Profile imported successfully!"
        
    except Exception as e:
        return False, f"Import failed: {str(e)}"
```

## Chart and Visualization Patterns

### Plotly Chart Configuration
```python
import plotly.express as px
import plotly.graph_objects as go

def create_bitcoin_chart(data, title, mobile_friendly=True):
    """Create Bitcoin-themed chart with responsive design"""
    
    fig = px.line(data, x='year', y='value', title=title)
    
    # Bitcoin orange theme
    fig.update_traces(line_color='#f7931a', line_width=3)
    
    # Responsive layout
    if is_mobile_layout() and mobile_friendly:
        fig.update_layout(
            height=300,  # Shorter on mobile
            font=dict(size=10),
            title=dict(font=dict(size=14)),
            margin=dict(l=20, r=20, t=40, b=20)
        )
    else:
        fig.update_layout(
            height=400,
            font=dict(size=12),
            title=dict(font=dict(size=16))
        )
    
    # Bitcoin-themed styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
    )
    
    return fig

def show_responsive_charts(chart1, chart2, titles):
    """Show charts responsively (side-by-side on desktop, stacked on mobile)"""
    if is_mobile_layout():
        # Stack vertically on mobile
        st.plotly_chart(chart1, use_container_width=True)
        st.plotly_chart(chart2, use_container_width=True)
    else:
        # Side-by-side on desktop
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(chart1, use_container_width=True)
        with col2:
            st.plotly_chart(chart2, use_container_width=True)
```

## Performance Patterns

### Caching Strategies
```python
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def expensive_calculation(profile, years, model):
    """Cache expensive calculations"""
    # Expensive computation here
    return results

def get_cached_calculation(cache_key, calculation_func, *args):
    """Get cached calculation or compute if not cached"""
    if cache_key in st.session_state.calculations_cache:
        return st.session_state.calculations_cache[cache_key]
    
    result = calculation_func(*args)
    st.session_state.calculations_cache[cache_key] = result
    return result
```

### Memory Management
```python
def cleanup_old_cache():
    """Clean up old cached calculations"""
    max_cache_size = 10
    cache = st.session_state.calculations_cache
    
    if len(cache) > max_cache_size:
        # Keep only the most recent entries
        keys_to_keep = list(cache.keys())[-max_cache_size:]
        st.session_state.calculations_cache = {
            k: cache[k] for k in keys_to_keep
        }
```

## Testing Patterns

### Manual Testing Helpers
```python
def debug_session_state():
    """Show session state for debugging (only in development)"""
    if st.checkbox("Show Debug Info"):
        st.write("User Data:", st.session_state.user_data)
        st.write("UI State:", st.session_state.ui_state)
        st.write("Cache Keys:", list(st.session_state.calculations_cache.keys()))

def validate_calculations(profile):
    """Validate calculation results make sense"""
    try:
        # Test basic calculations
        freedom_timeline = calculate_freedom_timeline(profile)
        purchasing_power = calculate_purchasing_power_improvement(
            profile['monthly_expenses_sats'], 10
        )
        
        # Sanity checks
        assert freedom_timeline > 0, "Freedom timeline should be positive"
        assert purchasing_power > 0, "Purchasing power should improve"
        
        return True, "Calculations validated"
        
    except Exception as e:
        return False, f"Validation failed: {str(e)}"
```

Remember: **Keep it simple, keep it Bitcoin-only, and always validate user inputs before calculations.** 