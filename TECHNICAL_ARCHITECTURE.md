# FreeWithBTC - Technical Architecture

## Technology Stack

### Core Technologies
- **Language**: Python 3.8+
- **Web Framework**: Streamlit (modern web UI)
- **Charts**: Plotly (interactive visualizations)
- **Data Processing**: Pandas + NumPy
- **Storage**: Session State only (privacy-focused, no database)
- **Deployment**: Streamlit Cloud with auto-deploy from GitHub

### Design Principles
- **Privacy-First**: Each user gets isolated data in st.session_state
- **Bitcoin-Only**: Satoshis everywhere, no other assets
- **Mobile-Responsive**: Single codebase with responsive layouts
- **Simplicity**: Built-in Streamlit components only

## File Structure

```
freewithbtc/
├── streamlit_app.py                 # Main application shell (~300 lines)
├── modules/
│   ├── __init__.py                  # Package initialization
│   ├── bitcoin_education.py         # Pillar 1: No Second Best (~600 lines)
│   ├── purchasing_power.py          # Pillar 2: Life Gets Cheaper (~500 lines)
│   ├── freedom_timeline.py          # Pillar 3: Escape Rat Race (~700 lines)
│   ├── three_pillars_dashboard.py   # Unified experience (~400 lines)
│   ├── user_profiles.py             # New/Old Stacker defaults (~200 lines)
│   ├── envelope_budgeting.py        # Advanced feature (~1500 lines)
│   ├── data_management.py           # Session state, import/export (~400 lines)
│   └── ui_components.py             # Shared UI helpers (~300 lines)
├── requirements.txt                 # Dependencies
├── README.md                        # Documentation
└── PROJECT_VISION.md               # Strategic reference
```

## Module Responsibilities

### `streamlit_app.py` (Main Application Shell)
**Purpose**: Application entry point and routing
**Key Functions**:
- `main()` - Application entry point
- `initialize_session_state()` - Setup user data
- `sidebar_navigation()` - Main navigation
- Page routing to three pillars dashboard
- Profile selection interface

### `bitcoin_education.py` (Pillar 1: No Second Best)
**Purpose**: Educational content proving Bitcoin superiority
**Key Functions**:
- `show_bitcoin_vs_assets()` - Comparison charts
- `show_monetary_properties()` - Education content
- `show_self_custody_benefits()` - Risk analysis
- `show_why_bitcoin_only()` - Philosophical content
- Asset performance comparisons (Bitcoin vs. stocks/gold/fiat)

### `purchasing_power.py` (Pillar 2: Life Gets Cheaper)
**Purpose**: Purchasing power calculator and projections
**Key Functions**:
- `calculate_future_purchasing_power()` - Core calculation
- `show_expense_reduction_timeline()` - Visual projections
- `calculate_lifestyle_improvements()` - Quality of life metrics
- `show_deflationary_benefits()` - Bitcoin standard living
- Real purchasing power growth over time

### `freedom_timeline.py` (Pillar 3: Escape Rat Race)
**Purpose**: Financial freedom timeline calculator
**Key Functions**:
- `calculate_freedom_timeline()` - Years until work optional
- `show_escape_velocity()` - Stacking rate scenarios
- `calculate_post_freedom_sustainability()` - Lifestyle analysis
- `show_traditional_retirement_comparison()` - vs. fiat approach
- Work-optional lifestyle projections

### `three_pillars_dashboard.py` (Unified Experience)
**Purpose**: Integration layer showing all three pillars
**Key Functions**:
- `show_three_pillars_dashboard()` - Main dashboard
- `integrate_pillar_calculations()` - Data coordination
- `show_profile_based_results()` - New/Old Stacker results
- `provide_customization_gateway()` - Path to advanced features
- Smooth transitions between concepts

### `user_profiles.py` (Profile Management)
**Purpose**: Default user profiles and customization
**Key Functions**:
- `get_new_stacker_profile()` - 0.1 BTC defaults
- `get_old_stacker_profile()` - 1 BTC defaults
- `show_profile_selection()` - Profile chooser UI
- `customize_profile()` - User customization interface
- Profile switching and persistence

### `envelope_budgeting.py` (Advanced Feature)
**Purpose**: Full budgeting functionality for power users
**Key Functions**:
- Account-based budgeting system
- Income/expense tracking
- Category management
- Budget allocation tools
- **Note**: This is ported from existing Bitcoin Budget app

### `data_management.py` (Data Operations)
**Purpose**: Session state management and data persistence
**Key Functions**:
- `initialize_user_data()` - Setup data structures
- `export_data_to_json()` - Export functionality
- `import_data_from_json()` - Import functionality
- `validate_imported_data()` - Data validation
- Session state utilities

### `ui_components.py` (Shared UI Helpers)
**Purpose**: Reusable UI components and styling
**Key Functions**:
- `is_mobile_layout()` - Mobile detection
- `get_responsive_columns()` - Column adjustment
- `mobile_friendly_metrics()` - Responsive metrics
- `show_bitcoin_toast()` - Styled notifications
- `format_sats()` - Bitcoin amount formatting
- Loading states and UI enhancements

## Data Architecture

### Session State Structure
```python
st.session_state = {
    'user_data': {
        'profile_type': 'new_stacker',  # or 'old_stacker'
        'current_btc_sats': 10_000_000,  # 0.1 BTC
        'monthly_dca_sats': 50_000_000,  # $500 equivalent
        'monthly_expenses_sats': 400_000_000,  # $4000 equivalent
        'age': 32,
        'target_retirement_age': 65,
        'customized': False,
        # Advanced budgeting data (if used)
        'accounts': [],
        'transactions': [],
        'categories': [],
        'allocations': []
    },
    'ui_state': {
        'mobile_mode': False,
        'current_pillar': 'dashboard',
        'show_advanced_features': False
    }
}
```

### Bitcoin Models Integration
```python
# From existing Bitcoin Budget app
BITCOIN_MODELS = {
    'conservative': {
        'cycle_years': 4,
        'growth_rates': [0.5, 1.5, 2.0, 0.8],  # Per year in cycle
        'floor_multiplier': 0.15
    },
    'optimistic': {
        'cycle_years': 4,
        'growth_rates': [1.0, 2.0, 3.0, 1.0],
        'floor_multiplier': 0.2
    }
}
```

## Core Calculation Functions

### Bitcoin Price Projections
```python
def calculate_bitcoin_future_value(current_price, years, model='conservative'):
    """Calculate Bitcoin price at future date using cycle models"""
    
def calculate_net_worth_projection(profile, years, model='conservative'):
    """Calculate user's net worth over time"""
    
def calculate_purchasing_power_improvement(expenses_sats, years, model='conservative'):
    """Calculate how expenses reduce on Bitcoin standard"""
```

### Freedom Timeline Calculations
```python
def calculate_financial_freedom_date(profile, model='conservative'):
    """Calculate when Bitcoin holdings cover annual expenses"""
    
def calculate_escape_velocity(profile, model='conservative'):
    """Determine minimum stacking rate for freedom"""
```

## Mobile Responsiveness Architecture

### Detection System
```python
def is_mobile_layout():
    """Check if mobile layout is enabled"""
    return st.session_state.get('mobile_mode', False)

def get_responsive_columns(desktop_cols):
    """Get responsive column count for desktop vs mobile"""
    if is_mobile_layout():
        return min(2, desktop_cols)  # Max 2 columns on mobile
    return desktop_cols
```

### Layout Patterns
- **Desktop**: Multi-column layouts, side-by-side charts
- **Mobile**: Stacked layouts, full-width buttons
- **Responsive**: Single codebase with conditional rendering
- **User Control**: Toggle in sidebar for layout preference

## Styling and Theming

### Bitcoin Orange Theme
- **Primary Color**: #f7931a (Bitcoin orange)
- **Gradients**: Orange to gold transitions
- **Success States**: Bitcoin-themed success messages
- **Visual Hierarchy**: Tree-style indicators for organization

### Component Styling
```python
def show_bitcoin_toast(message, toast_type='success'):
    """Show styled toast notification with Bitcoin theming"""
    
def apply_bitcoin_gradient():
    """Apply Bitcoin orange gradient styling"""
```

## Performance Considerations

### Optimization Strategy
- **Session State**: Fast in-memory operations
- **Caching**: Use @st.cache_data for expensive calculations
- **Minimal Dependencies**: Keep package requirements light
- **Simple Operations**: Basic list/dict operations only

### Scalability Approach
- **Personal Use**: Optimized for individual users
- **No Database**: Session state handles all data
- **Stateless**: Each session is independent
- **Privacy-First**: No server-side storage

## Deployment Architecture

### Streamlit Cloud Deployment
- **Repository**: GitHub integration
- **Auto-Deploy**: Push to main branch triggers deployment
- **Environment**: Streamlit Community Cloud
- **Domain**: Custom domain support available

### Local Development
```bash
# Run locally for development
streamlit run streamlit_app.py

# Install dependencies
pip install -r requirements.txt
```

## Security and Privacy

### Privacy-First Design
- **No User Accounts**: No authentication required
- **Session Isolation**: Each user gets private session state
- **No Data Collection**: No analytics or tracking
- **Local Processing**: All calculations happen client-side
- **Export/Import**: User controls their own data

### Data Validation
- **Input Validation**: Sanitize all user inputs
- **Type Checking**: Ensure data integrity
- **Error Handling**: Graceful degradation on bad input
- **Session Recovery**: Handle corrupted session state

## Integration Points

### From Existing Bitcoin Budget App
**Functions to Port**:
- Bitcoin price modeling (conservative/optimistic)
- Net worth calculation algorithms
- Mobile responsive UI helpers
- UX enhancement functions (toasts, loading states)
- Export/import functionality
- Plotly chart configurations

**Data Structures to Adapt**:
- Session state management patterns
- Profile-based data organization
- Bitcoin amount formatting
- Error handling patterns

## Development Workflow

### Phase 1: Core Structure
1. Create main app shell and navigation
2. Implement user profile system
3. Build basic three pillars dashboard
4. Add mobile responsiveness

### Phase 2: Pillar Implementation
1. Bitcoin education content (Pillar 1)
2. Purchasing power calculator (Pillar 2)
3. Freedom timeline calculator (Pillar 3)
4. Integration and testing

### Phase 3: Advanced Features
1. Profile customization
2. Envelope budgeting (optional)
3. Export/import functionality
4. Polish and optimization

Remember: **Keep it simple, keep it Bitcoin-only, keep it privacy-first.** 