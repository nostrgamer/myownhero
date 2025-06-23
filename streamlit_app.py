import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def main():
    """Main function to route to different pages"""
    
    # Configure page
    st.set_page_config(
        page_title="The Hero",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Remove sidebar and menu
    st.markdown("""
    <style>
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize navigation if needed
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'
    
    # Route to appropriate page
    if st.session_state.current_page == 'landing':
        render_landing_page()
    elif st.session_state.current_page == 'question_everything':
        render_question_everything()
    elif st.session_state.current_page == 'time_has_value':
        render_time_has_value()
    elif st.session_state.current_page == 'hero_seeks_understanding':
        render_hero_seeks_understanding()
    elif st.session_state.current_page == 'same_rules_for_everyone':
        render_same_rules_for_everyone()
    elif st.session_state.current_page == 'bitcoin_revelation':
        st.success("🚧 Coming soon: The solution that changes everything")
        # Will implement bitcoin_revelation next
    elif st.session_state.current_page == 'heros_triumph':
        render_heros_triumph()
    else:
        st.error("Invalid page")

def render_landing_page():
    """Render the simple landing page"""
    
    # Title
    st.title("Are You the Hero in Your Life?")
    
    st.markdown("---")
    
    # Definition of hero
    st.markdown("""
    
    *noun* | he·ro | \ˈhir-ō\
    
    **Definition**: A person who takes control of their own destiny. Someone who makes conscious choices, takes responsibility for their outcomes, and refuses to be a victim of circumstances. Heroes don't wait for rescue—they rescue themselves.
    """)
    
    st.markdown("---")
    
    # The central questions
    st.markdown("### If not, do you wish to be?")
    
    st.markdown("---")
    
    # Simple yes/no choice
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("Take the Hero's Journey", type="primary", use_container_width=True):
            st.session_state.current_page = 'question_everything'
            st.rerun()

def render_question_everything():
    """Render the Question Everything page - Pillar 1"""
    
    st.title("A Hero Doesn't Just Take things at Face Value")
    st.markdown("### What if everything you've been told about success is wrong?")
    
    st.markdown("---")
    
    # The broken promise
    st.markdown("""
    ## The Script You Were Given
    
    *"Study hard, go to college, get a job, save money, buy a house, have a family."*
    
    This step-by-step formula worked for previous generations. But something fundamental changed.
    
    **Three of these steps are now financially impossible for most people:**
    """)
    
    # Show all three broken promises
    render_broken_promises()
    
    st.markdown("---")
    
    st.markdown("""
    ## The Hero's Realization
    
    **1971**: High school graduate could support a family on one income.
    
    **Today**: Two Master's degrees struggle to achieve what Homer Simpson had.
    
    **The money itself broke in 1971.**
    """)
    
    st.markdown("---")
    
    # Bridge to next pillar
    st.markdown("""
    *"If the money is broken, how much of my life am I really trading away?"*
    """)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", type="secondary"):
            st.session_state.current_page = 'landing'
            st.rerun()
    
    with col2:
        if st.button("Your Time Has Value →", type="primary"):
            st.session_state.current_page = 'time_has_value'
            st.rerun()

def render_broken_promises():
    """Show the three broken promises of the life script"""
    
    # Create tabs for each broken promise
    tab1, tab2, tab3 = st.tabs(["💸 College", "🏠 Housing", "👶 Family"])
    
    with tab1:
        render_college_crisis()
    
    with tab2:
        render_housing_crisis()
    
    with tab3:
        render_family_crisis()

def render_college_crisis():
    """Show the college affordability crisis"""
    
    st.markdown("### Promise #1: Go to College")
    
    # College and minimum wage data
    college_1985 = 3800  # Average annual tuition 1985
    college_2022 = 38000  # Average annual tuition 2022
    min_wage_1985 = 3.35  # Federal minimum wage 1985
    min_wage_2022 = 7.25  # Federal minimum wage 2022
    
    # Calculate hours needed to work
    hours_1985 = college_1985 / min_wage_1985
    hours_2022 = college_2022 / min_wage_2022
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Hours at Minimum Wage (Annual)',
        x=['1985', '2022'],
        y=[hours_1985, hours_2022],
        marker_color=['lightblue', 'darkblue'],
        text=[f'{hours_1985:,.0f} hours', f'{hours_2022:,.0f} hours'],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Hours of Work Needed for One Year of College',
        yaxis_title='Hours of Work Required',
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show the devastating comparison
    col1, col2 = st.columns(2)
    with col1:
        hours_per_week_1985 = hours_1985 / 52
        st.metric("1985", f"{hours_per_week_1985:.0f} hrs/week", "Part-time job could pay for college")
    
    with col2:
        hours_per_week_2022 = hours_2022 / 52
        st.metric("2022", f"{hours_per_week_2022:.0f} hrs/week", "Literally impossible - more than 2 full-time jobs!")
    
    st.markdown(f"""
    **1985**: {hours_per_week_1985:.0f} hours/week could pay for college.  
    **Today**: {hours_per_week_2022:.0f} hours/week required - **{hours_per_week_2022/40:.1f} full-time jobs**.
    
    *There aren't enough hours in the week.*
    """)
    
def render_housing_crisis():
    """Show the housing affordability crisis"""
    
    st.markdown("### Promise #2: Buy a House")
    
    # Hours of work required to buy a house - the real story
    # Baby Boomers: Median household income with 1 earner (~2,080 hours/year)
    # Millennials: Median household income requires 2 earners (~4,160+ hours/year)
    
    baby_boomers_house_hours = 7280   # 3.5x income × 2,080 hours (1 earner) 
    millennials_house_hours = 26208   # 6.3x income × 4,160 hours (2 earners)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Hours of Work Required to Buy Median House',
        x=['Baby Boomers (1985)', 'Millennials (2022)'],
        y=[baby_boomers_house_hours, millennials_house_hours],
        marker_color=['lightcoral', 'darkred'],
        text=[f'{baby_boomers_house_hours:,} hours', f'{millennials_house_hours:,} hours'],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Millennials Must Work 3.6x More Hours for the Same House',
        yaxis_title='Hours of Human Labor Required',
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show the devastating time comparison
    col1, col2 = st.columns(2)
    
    with col1:
        boomer_years = baby_boomers_house_hours / 2080  # Full-time years
        st.metric("Baby Boomers", f"{boomer_years:.1f} years", "One person working full-time")
    
    with col2:
        millennial_years = millennials_house_hours / 2080  # Full-time years 
        st.metric("Millennials", f"{millennial_years:.1f} years", "Of full-time labor required")
    
    st.markdown("---")
    
    st.markdown("""
    **Millennials**: 12.6 years of labor for the same house **Baby Boomers** got with 3.5 years.
    
    **Houses didn't get better. Your work ethic didn't get worse. The money itself changed.**
    """)

def render_family_crisis():
    """Show the family affordability crisis"""
    
    st.markdown("### Promise #3: Have a Family")
    
    # The death of 9-to-5 and family life
    multiple_jobs_1994 = 7.5  # Million Americans working multiple jobs (historical baseline)
    multiple_jobs_2024 = 8.9  # Million Americans working multiple jobs (record high)
    
    living_with_parents_1980 = 29  # % of young adults living with parents
    living_with_parents_2020 = 52  # % of young adults living with parents
    
    fig = go.Figure()
    
    # Show young adults can't leave home
    fig.add_trace(go.Bar(
        name='Young Adults Living with Parents',
        x=['1980', '2020'],
        y=[living_with_parents_1980, living_with_parents_2020],
        marker_color=['lightblue', 'darkblue'],
        text=[f'{living_with_parents_1980}%', f'{living_with_parents_2020}%'],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Young Adults Can\'t Afford to Leave Home',
        yaxis_title='Percentage Living with Parents',
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show the devastating comparison
    col1, col2 = st.columns(2)
    with col1:
        st.metric("1980", f"{living_with_parents_1980}%", "Normal rate - kids could launch")
    
    with col2:
        st.metric("2020", f"{living_with_parents_2020}%", "Great Depression levels")
    
    # Add the death of 9-to-5
    st.markdown("### The Death of \"Working 9 to 5\"")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("1980s", "9-to-5 Standard", "One job, evenings free, weekends yours")
    
    with col2:
        st.metric("2024", f"{multiple_jobs_2024}M Multiple Jobs", "Record high - no time for family")
    
    st.markdown("""
    **1980s**: One job, leave at 5pm, weekends yours.
    
    **Today**: 8.9 million Americans work multiple jobs (record high).
    
    *Families can't afford to have families.*
    """)
    
    # Add birth rate collapse data
    st.markdown("### Families Can't Afford to Have Families")
    
    # Birth rate data showing the collapse
    birth_rate_1957 = 122.9  # Births per 1,000 women 15-44 (baby boom peak)
    birth_rate_2023 = 54.5   # Current rate - less than half of 1957
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("1957", f"{birth_rate_1957}", "Baby boom - families could afford families")
    
    with col2:
        st.metric("2023", f"{birth_rate_2023}", "Birth rate collapsed - less than half of 1957")
    
    st.markdown(f"""
    **Birth rate collapsed**: From {birth_rate_1957} to {birth_rate_2023} births per 1,000 women.
    
    **15% of women ages 40-44 are now childless** - many wanted children but couldn't afford them in time.
    """)
    


def render_time_has_value():
    """Render Pillar 2: Your Time Has Value"""
    
    st.title("Your Time Has Real Value")
    st.markdown("### A hero realizes their most precious resource is being stolen")
    
    st.markdown("---")
    
    # The hero's realization
    st.markdown("""
    **You can't make more time. You can't buy more time. You can't borrow time.**
    
    **But you can calculate exactly how much time everything costs.**
    """)
    
    st.markdown("---")
    
    # Personal time-value calculator
    render_personal_time_calculator()
    
    st.markdown("---")
    
    # Show purchasing power theft
    render_purchasing_power_theft()
    
    st.markdown("---")
    
    # Bridge to Pillar 3
    st.markdown("""
    **The rules changed. Your time is being stolen. The treadmill gets faster.**
    
    *"What if things weren't always this way? Who benefits from this system?"*
    """)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Question Everything", type="secondary"):
            st.session_state.current_page = 'question_everything'
            st.rerun()
    
    with col2:
        if st.button("Seek Understanding →", type="primary"):
            st.session_state.current_page = 'hero_seeks_understanding'
            st.rerun()

def render_personal_time_calculator():
    """Personal time-value calculator"""
    
    st.markdown("## Calculate Your Real Time-Cost")
    
    # Initialize user data if not exists
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    # Get user's wage information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Your Take-Home Pay")
        
        # Pay frequency selector
        pay_frequency = st.selectbox(
            "How often do you get paid?",
            options=["Bi-weekly (every 2 weeks)", "Weekly", "Monthly"],
            index=0,  # Default to bi-weekly
            help="Choose how often you receive your paycheck",
            key="pay_frequency_main"
        )
        
        # Paycheck amount input
        if pay_frequency == "Weekly":
            paycheck_amount = st.number_input(
                "What's your weekly take-home pay? (USD)", 
                min_value=100, 
                max_value=10000, 
                value=st.session_state.user_data.get('weekly_pay', 800),
                help="Enter your actual weekly paycheck amount after taxes in US dollars",
                key="weekly_paycheck_input"
            )
            st.session_state.user_data['weekly_pay'] = paycheck_amount
            weekly_pay = paycheck_amount
            
        elif pay_frequency == "Bi-weekly (every 2 weeks)":
            paycheck_amount = st.number_input(
                "What's your bi-weekly take-home pay? (USD)", 
                min_value=200, 
                max_value=20000, 
                value=st.session_state.user_data.get('biweekly_pay', 1600),
                help="Enter your actual bi-weekly paycheck amount after taxes in US dollars",
                key="biweekly_paycheck_input"
            )
            st.session_state.user_data['biweekly_pay'] = paycheck_amount
            weekly_pay = paycheck_amount / 2
            
        else:  # Monthly
            paycheck_amount = st.number_input(
                "What's your monthly take-home pay? (USD)", 
                min_value=800, 
                max_value=40000, 
                value=st.session_state.user_data.get('monthly_pay', 3200),
                help="Enter your actual monthly paycheck amount after taxes in US dollars",
                key="monthly_paycheck_input"
            )
            st.session_state.user_data['monthly_pay'] = paycheck_amount
            weekly_pay = paycheck_amount / 4.33  # Average weeks per month
        
        # Calculate hourly wage assuming 40 hours/week
        hourly_wage = weekly_pay / 40
        
        # Store calculated hourly wage
        st.session_state.user_data['hourly_wage'] = hourly_wage
        
        # Calculate annual values
        annual_hours = 40 * 52  # 40 hours/week * 52 weeks
        annual_income = hourly_wage * annual_hours
        
        st.metric("Your Effective Hourly Rate", f"${hourly_wage:.2f}/hour", "After taxes, 40 hours/week")
        st.metric("Annual Take-Home", f"${annual_income:,.0f}", f"Working {annual_hours:,} hours/year")
    
    with col2:
        st.markdown("### Major Purchase Time-Costs")
        
        # Major purchases and their time costs
        median_house = 400000
        new_car = 35000
        college_degree = 40000
        
        house_hours = median_house / hourly_wage
        car_hours = new_car / hourly_wage
        college_hours = college_degree / hourly_wage
        
        # Display as time costs
        st.metric("Median House", f"{house_hours/annual_hours:.1f} years", f"{house_hours:,.0f} hours of your life")
        st.metric("New Car", f"{car_hours/annual_hours:.1f} years", f"{car_hours:,.0f} hours of your life")
        st.metric("College Degree", f"{college_hours/annual_hours:.1f} years", f"{college_hours:,.0f} hours of your life")
  
  
def render_purchasing_power_theft():
    """Show how purchasing power is systematically stolen"""
    
    st.markdown("## Your Purchasing Power Is Being Stolen")
    
    # The REAL comparison: 1970 vs 2024 with all factors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💚 1970: The Good Deal")
        st.markdown("""
        **Education**: High school diploma sufficient
        **Income**: 1 earner (husband)
        **House**: 2.5x annual income
        **Children**: Wife stays home (no daycare costs)
        """)
        
        # 1970 calculation: median income $9,870, median house $23,400
        income_1970 = 9870
        house_1970 = 23400
        years_1970 = house_1970 / income_1970
        
        st.metric("Total Timeline", f"{years_1970:.1f} years", "High school → house → family")
        
    with col2:
        st.markdown("### 🔴 2024: The Raw Deal")
        st.markdown("""
        **Education**: College degree required (4 years + debt)
        **Income**: 2 earners required (both work)
        **House**: 7x annual household income  
        **Children**: $15,000/year daycare per child
        """)
        
        # 2024 calculation: median household income $70,000, median house $490,000
        household_income_2024 = 70000
        house_2024 = 490000
        daycare_annual = 15000  # Per child
        college_cost = 40000    # Average debt
        
        # Timeline: 4 years college + house cost + 5 years daycare for 2 kids
        house_years_2024 = house_2024 / household_income_2024
        daycare_years = (daycare_annual * 2 * 5) / household_income_2024  # 2 kids, 5 years each
        college_years = 4
        total_timeline_2024 = college_years + house_years_2024 + daycare_years
        
        st.metric("Total Timeline", f"{total_timeline_2024:.1f} years", "College → house → daycare costs")
    
    # The devastating comparison chart
    fig = go.Figure()
    
    categories = ['1970 (Sound Money)', '2024 (Unlimited Money)']
    timelines = [years_1970, total_timeline_2024]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=timelines,
        marker_color=['lightgreen', 'darkred'],
        text=[f'{t:.1f} years' for t in timelines],
        textposition='auto',
        width=0.6
    ))
    
    fig.update_layout(
        title='Same Middle-Class Lifestyle: The Time Theft',
        yaxis_title='Years of Household Income Required',
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **1970**: 2.5 years for middle-class life  
    **2024**: {total_timeline_2024:.1f} years for the same life
    
    **The system stole {total_timeline_2024 - years_1970:.1f} years** of your life.
    """)

def render_hero_seeks_understanding():
    """Render Pillar 3: A Hero Seeks Freedom"""
    
    st.title("A Hero Seeks to Understand")
    st.markdown("### Who benefits?")
    
    st.markdown("---")    
  
    # Show who benefits from the time theft
    render_cantillon_effect()
    
    st.markdown("---")
    
    # Bridge to the solution
    st.markdown("""
    ## The Hero's Realization
    
    **You now understand the complete picture:**
    
    1. **The rules were rigged** → Traditional success made impossible
    2. **Your time is being stolen** → Purchasing power systematically drained  
    3. **The theft is by design** → Your stolen time enriches the money printers
    
    **This isn't your fault. This isn't capitalism. This is organized theft.**
    
    **But heroes don't stay victims. Heroes find a way out.**
    
    *What if there was money that couldn't be printed or stolen?*
    """)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Your Time Has Value", type="secondary"):
            st.session_state.current_page = 'time_has_value'
            st.rerun()
    
    with col2:
        if st.button("Same Rules for Everyone →", type="primary"):
            st.session_state.current_page = 'same_rules_for_everyone'
            st.rerun()

def render_cantillon_effect():
    """Show who benefits from the time theft"""
    
    # Show wealth transfer visualization
    years = ['1971', '1980', '1990', '2000', '2010', '2020', '2024']
    
    # Wealth share percentages (more dramatic to show the theft)
    top_1_pct = [10, 15, 22, 28, 35, 40, 45]     # Growing share
    bottom_50_pct = [25, 22, 18, 15, 10, 7, 2]    # Shrinking share
    
    fig = go.Figure()
    
    # Top 1% line
    fig.add_trace(go.Scatter(
        name='Top 1% Wealth Share',
        x=years,
        y=top_1_pct,
        mode='lines+markers',
        line=dict(color='darkred', width=4),
        marker=dict(size=12),
        fill='tonexty',
        fillcolor='rgba(139, 0, 0, 0.1)'
    ))
    
    # Bottom 50% line
    fig.add_trace(go.Scatter(
        name='Bottom 50% Wealth Share',
        x=years,
        y=bottom_50_pct,
        mode='lines+markers',
        line=dict(color='darkblue', width=4),
        marker=dict(size=12),
    ))
    
    fig.update_layout(
        title='The Great Time Theft: Where Your Stolen Time Goes',
        xaxis_title='Year',
        yaxis_title='Share of Total Wealth (%)',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # The hard-hitting revelation
    col1, col2 = st.columns(2)
    with col1:
        st.metric("1971: Bottom 50%", "25%", "Quarter of all wealth")
    with col2:
        st.metric("2024: Bottom 50%", "2%", "⬇️ 92% DECLINE")
    
    st.markdown("""
    ### The Time Theft Machine
    
    **This isn't an accident. This isn't market forces. This is theft.**
    
    **The system works exactly as designed:**
    1. **Print unlimited money** → Give to banks first
    2. **Banks buy assets** → Prices rise for everyone else  
    3. **Your wages stay flat** → You can afford less each year
    4. **Repeat forever** → Transfer wealth from workers to owners
    
    **Your time is being systematically stolen and transferred to those who create money from nothing.**
    
    **A hero doesn't accept being robbed. A hero finds a way out.**
    """)

def render_same_rules_for_everyone():
    """Render Pillar 4: Same Rules for Everyone (the universal standard)"""
    st.title("Same Rules for Everyone")
    st.markdown("### A hero discovers hard money")
    st.markdown("---")

    st.markdown("### Savings Power of Hard Money")
    
    st.markdown("""
    What if your expenses got cheaper every year instead of more expensive?
    
    Enter your total monthly or annual expenses in USD below. We'll show you the difference between the fiat standard and the hard money standard.
    """)

    # User input
    expense = st.number_input(
        "Your Expenses (USD)",
        min_value=1,
        value=2000,
        step=1,
        help="Enter your total monthly or annual expenses in USD.",
        key="expense_input_1"
    )

    # Assumptions
    INFLATION_RATE = 0.10  # 10% per year (fiat debasement)
    BITCOIN_ANNUAL_APPRECIATION = 0.35  # 35% per year (historical power law average)
    NET_BITCOIN_ADVANTAGE = BITCOIN_ANNUAL_APPRECIATION - INFLATION_RATE  # 25% net advantage
    YEARS = 10

    # Calculations
    future_fiat_expense = expense * ((1 + INFLATION_RATE) ** YEARS)
    
    # Hard money purchasing power increases over time (expenses get cheaper in hard money terms)
    hard_money_purchasing_power_multiplier = (1 + NET_BITCOIN_ADVANTAGE) ** YEARS  # ~9.3x purchasing power
    hard_money_expense_future = expense / hard_money_purchasing_power_multiplier
    hard_money_savings = future_fiat_expense - hard_money_expense_future

    # Pie Chart 1: Future Cost in Fiat (change color to blue)
    fig1 = go.Figure(data=[go.Pie(
        labels=["Expenses (Fiat)"],
        values=[future_fiat_expense],
        marker_colors=["#2563eb"],  # blue
        textinfo='label+percent',
        hoverinfo='label+value',
        hole=0.3
    )])
    fig1.update_layout(
        title="Future Cost in Fiat<br>(10 Years, 10% Inflation)",
        showlegend=False,
        height=400,  # Increase height to match right chart with legend
        margin=dict(l=40, r=40, t=80, b=60)  # Adjust margins to account for legend space
    )

    # Pie Chart 2: Future Cost with Hard Money Savings (change savings to orange)
    fig2 = go.Figure(data=[go.Pie(
        labels=["Expenses (Hard Money)", "Hard Money Savings"],
        values=[hard_money_expense_future, hard_money_savings],
        marker_colors=["#10b981", "#f7931a"],  # green, orange
        textinfo='label+percent',
        hoverinfo='label+value',
        hole=0.3,
        textposition='inside'  # Force text inside the pie slices
    )])
    fig2.update_layout(
        title="Future Cost with Hard Money<br>(10 Years, Savings Shown)",
        showlegend=True,
        height=400,  # Match height with left chart
        margin=dict(l=40, r=120, t=80, b=60),  # Match margins and account for legend
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )

    # Show charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(f"**In 10 years, your expenses in fiat will be:**\n\n**${future_fiat_expense:,.2f}**")
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f"**With hard money, your expenses become:**\n\n**${hard_money_expense_future:,.2f}**\n\n**Hard Money Savings:** **${hard_money_savings:,.2f}**")
    
    # Calculate and emphasize the percentage improvement
    savings_percentage = (hard_money_savings / future_fiat_expense) * 100
    st.markdown(f"""
    ###Your Life Just Got {savings_percentage:.1f}% Better!
    
    **On a hard money standard, you save {savings_percentage:.1f}% of what you would have spent on the fiat standard.**
    
    This is the power of money that gets stronger instead of weaker over time.
    """)

    st.markdown("""
    ---
    > **With hard money, your expenses don't just stay the same—they get dramatically cheaper over time.**  
    > This is the power of saving in money that appreciates faster than fiat debases.
    
    **Hard money's 35% annual appreciation vs fiat's 10% debasement = 25% net advantage per year**
    
    *Ready to discover what this revolutionary money is?*
    """)

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Seek Understanding", type="secondary"):
            st.session_state.current_page = 'hero_seeks_understanding'
            st.rerun()
    with col2:
        if st.button("The Hero's Triumph →", type="primary"):
            st.session_state.current_page = 'heros_triumph'
            st.rerun()

def render_heros_triumph():
    """Render the final page: The Hero's Next Step – Call to Action"""
    st.title("The Hero's Next Step")
    st.markdown("### Your Journey Toward Monetary Sovereignty Begins")
    st.markdown("---")

    st.markdown("""
    **Congratulations, Hero!**
    
    You've discovered the truth. You've seen the 95.9% advantage of hard money.
    
    **A hero doesn't just understand the problem. A hero takes action.**
    """)

    st.markdown("---")
    
    # The revelation
    st.markdown("""
    ## The Hard Money Revolution
    
    Hard money has existed over the ages, first as silver, then gold, but in a modern era new hard money has emerged superior to all others.
    
    The hard money with the same rules for everyone that is the most scarce in history?
    """)
    
    # Make the Bitcoin reveal REALLY stand out
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f7931a 0%, #ff6b35 100%); border-radius: 15px; margin: 2rem 0; border: 3px solid #f7931a;'>
        <h2 style='color: white; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>It's Called Bitcoin.</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### The Answer
    
    You asked: *"Am I the hero of my own life?"*
    
    **The answer is yes.** And heroes take action.
    
    **Welcome to the Bitcoin revolution, Hero. Are you ready to Learn More?**
    """)
    
    st.markdown("---")   
  
    # Large prominent button - direct link to Bitcoin.org
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <a href='https://bitcoin.org/en/' target='_blank' style='text-decoration: none;'>
                <button style='
                    background: linear-gradient(135deg, #f7931a 0%, #ff6b35 100%);
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: bold;
                    border-radius: 8px;
                    cursor: pointer;
                    width: 100%;
                    transition: transform 0.2s ease;
                ' onmouseover='this.style.transform="scale(1.05)"' onmouseout='this.style.transform="scale(1)"'>
                    Start Your Bitcoin Education →
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation - moved to bottom
    st.markdown("---")
    if st.button("← Back to Same Rules", type="secondary"):
        st.session_state.current_page = 'same_rules_for_everyone'
        st.rerun()

if __name__ == "__main__":
    main()