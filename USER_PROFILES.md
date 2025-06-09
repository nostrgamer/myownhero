# FreeWithBTC - User Profiles & Default Data

## User Profile System

### Profile Types Overview
The app targets two primary user personas with pre-configured defaults to eliminate setup friction while providing compelling projections.

## New Stacker Profile (Primary Target - 80% of users)

### Demographics & Psychographics
- **Age Range**: 30-35 years old
- **Bitcoin Journey**: Early adopter, just started stacking
- **Mindset**: Curious about Bitcoin's potential, seeking conviction
- **Financial Situation**: Stable income, beginning to save seriously
- **Pain Points**: Uncertain about Bitcoin-only strategy, needs proof of concept
- **Motivation**: Wants to escape traditional retirement planning

### Default Profile Configuration
```python
NEW_STACKER_PROFILE = {
    'profile_type': 'new_stacker',
    'current_btc_sats': 10_000_000,        # 0.1 BTC
    'monthly_dca_sats': 50_000_000,        # $500 worth in sats (assuming $100k BTC)
    'monthly_expenses_sats': 400_000_000,   # $4000 worth in sats
    'age': 32,
    'target_retirement_age': 65,
    'current_fiat_savings_sats': 1_000_000_000,  # $10k equivalent
    'annual_income_sats': 6_000_000_000,    # $60k equivalent
    'customized': False,
    'created_date': '2024-01-01',
    'last_updated': '2024-01-01'
}
```

### Three Pillars Messaging for New Stackers
1. **No Second Best**: "See how Bitcoin outperformed every other investment over the last decade"
2. **Life Gets Cheaper**: "Your $4,000 monthly expenses become $544 in 10 years (86.4% reduction)"
3. **Escape Rat Race**: "Work becomes optional in 15 years with simple DCA strategy"

### Expected Emotional Journey
1. **Skeptical Interest**: "Can Bitcoin really do this?"
2. **Mathematical Proof**: "The numbers don't lie"
3. **Conviction Building**: "This is actually possible"
4. **Action Oriented**: "I need to stack more Bitcoin"

## Old Stacker Profile (Secondary Target - 20% of users)

### Demographics & Psychographics
- **Age Range**: 35-45 years old
- **Bitcoin Journey**: Established Bitcoiner, 3+ years experience
- **Mindset**: High conviction, wants optimization and validation
- **Financial Situation**: Higher income, significant Bitcoin holdings
- **Pain Points**: Wants to optimize stacking strategy and timeline
- **Motivation**: Accelerate path to financial freedom

### Default Profile Configuration
```python
OLD_STACKER_PROFILE = {
    'profile_type': 'old_stacker',
    'current_btc_sats': 100_000_000,       # 1.0 BTC
    'monthly_dca_sats': 100_000_000,       # $1000 worth in sats
    'monthly_expenses_sats': 600_000_000,   # $6000 worth in sats
    'age': 38,
    'target_retirement_age': 55,
    'current_fiat_savings_sats': 5_000_000_000,  # $50k equivalent
    'annual_income_sats': 10_000_000_000,   # $100k equivalent
    'customized': False,
    'created_date': '2024-01-01',
    'last_updated': '2024-01-01'
}
```

### Three Pillars Messaging for Old Stackers
1. **No Second Best**: "Validate your Bitcoin-only strategy with comparative analysis"
2. **Life Gets Cheaper**: "Your $6,000 monthly expenses become $816 in 10 years"
3. **Escape Rat Race**: "Work becomes optional in 10-12 years with your current stack"

### Expected Emotional Journey
1. **Validation Seeking**: "Confirm I'm on the right path"
2. **Optimization Focus**: "How can I accelerate this?"
3. **Confidence Building**: "I'm ahead of most people"
4. **Strategic Planning**: "Should I increase my DCA?"

## Profile Selection UI

### Selection Interface
```python
def show_profile_selection():
    """Profile selection with clear value propositions"""
    st.title("🎯 Choose Your Bitcoin Journey")
    st.markdown("Select the profile that best matches your situation for personalized projections.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌱 New Stacker", use_container_width=True, type="primary"):
            st.session_state.user_data = NEW_STACKER_PROFILE.copy()
            st.session_state.profile_selected = True
            st.rerun()
        
        st.markdown("""
        **Perfect if you:**
        - Own 0.01 to 0.5 BTC
        - Started stacking recently
        - Want to see Bitcoin's potential
        - Need conviction for Bitcoin-only approach
        
        **Your Preview:**
        - Current Stack: 0.1 BTC
        - Monthly DCA: $500
        - Expenses: $4,000/month
        - Freedom Timeline: ~15 years
        """)
    
    with col2:
        if st.button("🦬 Old Stacker", use_container_width=True, type="secondary"):
            st.session_state.user_data = OLD_STACKER_PROFILE.copy()
            st.session_state.profile_selected = True
            st.rerun()
        
        st.markdown("""
        **Perfect if you:**
        - Own 0.5+ BTC
        - Been stacking for years
        - High Bitcoin conviction
        - Want to optimize your strategy
        
        **Your Preview:**
        - Current Stack: 1.0 BTC
        - Monthly DCA: $1,000
        - Expenses: $6,000/month
        - Freedom Timeline: ~10 years
        """)
```

## Bitcoin Models & Assumptions

### Conservative Model (Default)
```python
CONSERVATIVE_MODEL = {
    'cycle_years': 4,
    'growth_rates': [0.5, 1.5, 2.0, 0.8],  # 50%, 150%, 200%, 80% per year
    'floor_multiplier': 0.15,  # 15% of peak becomes next cycle floor
    'description': 'Realistic 4-year cycle model based on historical patterns',
    'average_annual_growth': 1.20  # ~120% annually over full cycle
}
```

### Optimistic Model (Alternative)
```python
OPTIMISTIC_MODEL = {
    'cycle_years': 4,
    'growth_rates': [1.0, 2.0, 3.0, 1.0],  # 100%, 200%, 300%, 100% per year
    'floor_multiplier': 0.2,   # 20% of peak becomes next cycle floor
    'description': 'Higher growth trajectory for bull case scenarios',
    'average_annual_growth': 1.75  # ~175% annually over full cycle
}
```

### Current Bitcoin Price Assumptions
```python
CURRENT_BITCOIN_PRICE = 100_000  # $100k USD (update as needed)
SATOSHIS_PER_BITCOIN = 100_000_000
USD_TO_SATS_RATE = SATOSHIS_PER_BITCOIN / CURRENT_BITCOIN_PRICE  # 1000 sats per dollar
```

## Customization Options

### Profile Customization Form
```python
def show_profile_customization():
    """Allow users to customize their profile"""
    current_profile = get_user_profile()
    
    with st.form("customize_profile"):
        st.subheader("🎛️ Customize Your Numbers")
        
        # Current Holdings
        st.markdown("### Current Bitcoin Holdings")
        current_btc = st.number_input(
            "Bitcoin Amount (BTC)", 
            value=current_profile['current_btc_sats'] / SATOSHIS_PER_BITCOIN,
            min_value=0.0, 
            max_value=100.0,
            step=0.01,
            format="%.3f"
        )
        
        # Monthly Contributions
        st.markdown("### Monthly Dollar Cost Averaging")
        monthly_dca_usd = st.number_input(
            "Monthly DCA Amount ($)", 
            value=int(current_profile['monthly_dca_sats'] / USD_TO_SATS_RATE),
            min_value=0, 
            max_value=10000,
            step=50
        )
        
        # Living Expenses
        st.markdown("### Monthly Living Expenses")
        monthly_expenses_usd = st.number_input(
            "Monthly Expenses ($)", 
            value=int(current_profile['monthly_expenses_sats'] / USD_TO_SATS_RATE),
            min_value=0, 
            max_value=20000,
            step=100
        )
        
        # Demographics
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input(
                "Current Age", 
                value=current_profile['age'],
                min_value=18, 
                max_value=80
            )
        
        with col2:
            retirement_age = st.number_input(
                "Target Retirement Age", 
                value=current_profile['target_retirement_age'],
                min_value=age + 1, 
                max_value=85
            )
        
        # Advanced Options
        with st.expander("🔧 Advanced Options"):
            current_savings_usd = st.number_input(
                "Current Fiat Savings ($)", 
                value=int(current_profile.get('current_fiat_savings_sats', 0) / USD_TO_SATS_RATE),
                min_value=0,
                step=1000
            )
            
            annual_income_usd = st.number_input(
                "Annual Income ($)", 
                value=int(current_profile.get('annual_income_sats', 0) / USD_TO_SATS_RATE),
                min_value=0,
                step=5000
            )
        
        submitted = st.form_submit_button("Update My Projections", use_container_width=True)
        
        if submitted:
            # Convert to satoshis and update profile
            updated_profile = {
                'current_btc_sats': int(current_btc * SATOSHIS_PER_BITCOIN),
                'monthly_dca_sats': int(monthly_dca_usd * USD_TO_SATS_RATE),
                'monthly_expenses_sats': int(monthly_expenses_usd * USD_TO_SATS_RATE),
                'age': age,
                'target_retirement_age': retirement_age,
                'current_fiat_savings_sats': int(current_savings_usd * USD_TO_SATS_RATE),
                'annual_income_sats': int(annual_income_usd * USD_TO_SATS_RATE),
                'customized': True,
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            }
            
            update_user_profile(updated_profile)
            show_success_toast("Profile updated! Check your new projections below.")
            st.rerun()
```

## Demo Data & Examples

### Sample Calculations for New Stacker
```python
NEW_STACKER_EXAMPLES = {
    'net_worth_10_years': {
        'conservative': 2_500_000_000,  # $2.5M worth in sats
        'optimistic': 5_000_000_000     # $5M worth in sats
    },
    'purchasing_power_reduction': {
        '5_years': 0.65,   # 65% reduction (expenses cost 35% of current)
        '10_years': 0.864, # 86.4% reduction (expenses cost 13.6% of current)
        '15_years': 0.95   # 95% reduction (expenses cost 5% of current)
    },
    'freedom_timeline': {
        'conservative': 15,  # Years until financially free
        'optimistic': 12
    }
}
```

### Sample Calculations for Old Stacker
```python
OLD_STACKER_EXAMPLES = {
    'net_worth_10_years': {
        'conservative': 15_000_000_000,  # $15M worth in sats
        'optimistic': 25_000_000_000     # $25M worth in sats
    },
    'purchasing_power_reduction': {
        '5_years': 0.65,   # 65% reduction
        '10_years': 0.864, # 86.4% reduction  
        '15_years': 0.95   # 95% reduction
    },
    'freedom_timeline': {
        'conservative': 10,  # Years until financially free
        'optimistic': 8
    }
}
```

## Profile Validation

### Input Validation Rules
```python
def validate_profile_inputs(profile):
    """Validate profile data makes sense"""
    validation_rules = [
        ('current_btc_sats', 'Bitcoin holdings', 0, 21_000_000 * SATOSHIS_PER_BITCOIN),
        ('monthly_dca_sats', 'Monthly DCA', 0, 1_000_000_000),  # Max $10k/month
        ('monthly_expenses_sats', 'Monthly expenses', 0, 2_000_000_000),  # Max $20k/month
        ('age', 'Age', 18, 80),
        ('target_retirement_age', 'Retirement age', profile['age'] + 1, 85)
    ]
    
    errors = []
    for field, name, min_val, max_val in validation_rules:
        value = profile.get(field, 0)
        if not isinstance(value, (int, float)) or value < min_val or value > max_val:
            errors.append(f"{name} must be between {min_val:,} and {max_val:,}")
    
    # Logical validations
    if profile['monthly_expenses_sats'] > profile['monthly_dca_sats'] * 10:
        errors.append("Monthly expenses seem very high compared to DCA amount")
    
    if profile['target_retirement_age'] <= profile['age']:
        errors.append("Retirement age must be greater than current age")
    
    return len(errors) == 0, errors
```

## Profile Comparison & Insights

### Profile Performance Comparison
```python
def compare_profiles():
    """Show how different profiles perform"""
    comparison_data = {
        'New Stacker': {
            'starting_btc': 0.1,
            'monthly_dca': 500,
            'freedom_years': 15,
            'net_worth_10yr': '$2.5M'
        },
        'Old Stacker': {
            'starting_btc': 1.0,
            'monthly_dca': 1000,
            'freedom_years': 10,
            'net_worth_10yr': '$15M'
        }
    }
    
    # Display comparison table
    df = pd.DataFrame(comparison_data).T
    st.dataframe(df, use_container_width=True)
```

### Profile Migration Paths
```python
def show_profile_progression():
    """Show how New Stacker can become Old Stacker"""
    st.markdown("""
    ### 📈 Your Bitcoin Journey Progression
    
    **New Stacker → Old Stacker**
    - Increase stack to 1+ BTC over 2-3 years
    - Maintain consistent $500+ monthly DCA
    - Build conviction through education
    - Optimize strategy based on results
    
    **Old Stacker → Bitcoin Whale**
    - Reach 10+ BTC through continued DCA
    - Accelerate freedom timeline to 5-7 years
    - Consider advanced strategies (within Bitcoin-only framework)
    - Mentor other stackers
    """)
```

Remember: **Profiles are starting points, not limitations. Users should see themselves progressing from New Stacker to Old Stacker to Bitcoin Whale over time.** 