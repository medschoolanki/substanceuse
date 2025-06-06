import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Alcohol & Nicotine Calculator",
    page_icon="🧮",
    layout="wide"
)

# Title and description
st.title("Alcohol & Nicotine Calculator")
st.write("""
This app helps you calculate standard drinks from alcoholic beverages and nicotine consumption from vapes.
""")

# Create tabs for different calculators
tab1, tab2 = st.tabs(["🍷 Alcohol Calculator", "💨 Nicotine Calculator"])

# ALCOHOL CALCULATOR TAB
with tab1:
    st.header("Standard Drinks Calculator")
    st.write("A standard drink calculation using the formula: Volume (mL) × %ABV ÷ 17.05")
    
    # Create two columns for alcohol calculator
    alc_col1, alc_col2 = st.columns([3, 2])
    
    with alc_col1:
        # Beverage selection
        beverage_type = st.selectbox(
            "Select beverage type:",
            ["Beer", "Wine", "Spirits", "Cocktail", "Custom"],
            key="beverage_type"
        )

        # Set default ABV based on beverage type (as decimal, not percentage)
        if beverage_type == "Beer":
            default_abv = 0.05  # 5%
        elif beverage_type == "Wine":
            default_abv = 0.12  # 12%
        elif beverage_type == "Spirits":
            default_abv = 0.40  # 40%
        elif beverage_type == "Cocktail":
            default_abv = 0.15  # 15%
        else:  # Custom
            default_abv = 0.05

        # Volume input with unit selection
        st.subheader("Volume")
        volume_unit = st.selectbox(
            "Volume unit:",
            ["mL", "Liters", "oz (fluid ounces)"],
            key="volume_unit"
        )

        if volume_unit == "mL":
            volume = st.number_input(
                "Enter volume (mL):",
                min_value=0.0,
                step=10.0,
                value=330.0,
                key="volume_ml"
            )
            volume_ml = volume
        elif volume_unit == "Liters":
            volume = st.number_input(
                "Enter volume (Liters):",
                min_value=0.0,
                step=0.1,
                value=0.33,
                key="volume_l"
            )
            volume_ml = volume * 1000
        else:  # oz
            volume = st.number_input(
                "Enter volume (fl oz):",
                min_value=0.0,
                step=0.5,
                value=12.0,
                key="volume_oz"
            )
            volume_ml = volume * 29.5735

        # ABV input (as decimal)
        abv_decimal = st.number_input(
            "Alcohol content (as decimal, e.g., 0.05 for 5%):",
            min_value=0.0,
            max_value=1.0,
            step=0.005,
            value=default_abv,
            format="%.3f",
            key="abv_decimal"
        )

        # Show percentage equivalent
        st.write(f"*Equivalent to {abv_decimal * 100:.1f}% ABV*")

        # Number of drinks input
        st.subheader("Quantity")
        num_drinks = st.number_input(
            "Number of drinks of this amount:",
            min_value=1,
            step=1,
            value=1,
            key="num_drinks"
        )

        # Calculate button for alcohol
        alc_calculate = st.button("Calculate Standard Drinks", type="primary", key="alc_calc")

    # Function to calculate standard drinks using supervisor's formula
    def calculate_standard_drinks_new(volume_ml, abv_decimal):
        # Formula: Volume in mL × %ABV ÷ 17.05
        standard_drinks = (volume_ml * abv_decimal) / 17.05
        return standard_drinks

    # Results section for alcohol
    with alc_col2:
        st.subheader("Results")
        if alc_calculate:
            single_drink_standard = calculate_standard_drinks_new(volume_ml, abv_decimal)
            total_standard_drinks = single_drink_standard * num_drinks
            
            st.markdown(f"""
            ### 🥃 {total_standard_drinks:.2f} total standard drinks
            
            **Details:**
            - Beverage: {beverage_type}
            - Volume per drink: {volume} {volume_unit} ({volume_ml:.0f} mL)
            - ABV: {abv_decimal:.3f} ({abv_decimal * 100:.1f}%)
            - Number of drinks: {num_drinks}
            - Standard drinks per unit: {single_drink_standard:.2f}
            
            **Calculation:**
            ({volume_ml:.0f} mL × {abv_decimal:.3f} ÷ 17.05) × {num_drinks} = {total_standard_drinks:.2f}
            """)
            
            # Visual representation
            if total_standard_drinks > 0:
                full_drinks = int(total_standard_drinks)
                partial = total_standard_drinks - full_drinks
                
                # Limit visual icons to prevent overwhelming display
                if full_drinks <= 20:
                    drink_icons = "🥃 " * full_drinks
                    if partial >= 0.5:
                        drink_icons += "🥄 "
                    st.markdown(f"**Visual:** {drink_icons}")
                else:
                    st.markdown(f"**Visual:** 🥃 × {full_drinks} drinks" + (" + 🥄" if partial >= 0.5 else ""))
                    
            # Show breakdown if multiple drinks
            if num_drinks > 1:
                st.markdown(f"""
                **Breakdown:**
                - Per drink: {single_drink_standard:.2f} standard drinks
                - Total ({num_drinks} drinks): {total_standard_drinks:.2f} standard drinks
                """)
        else:
            st.info("Enter your beverage details and click Calculate")

    # Reference table for alcohol
    st.markdown("---")
    st.subheader("Standard Drink Reference")
    reference_data = {
        "Beverage": ["Beer (5%)", "Wine (12%)", "Spirits (40%)", "Shot (40%)"],
        "Typical Volume": ["330 mL", "150 mL", "45 mL", "30 mL"],
        "ABV (decimal)": ["0.05", "0.12", "0.40", "0.40"],
        "Standard Drinks": ["~0.97", "~1.06", "~1.06", "~0.70"]
    }
    reference_df = pd.DataFrame(reference_data)
    st.table(reference_df)

# NICOTINE CALCULATOR TAB
with tab2:
    st.header("Nicotine Calculator")
    st.write("Calculate daily nicotine consumption and pack-per-day equivalence from vape usage.")
    
    # Create two columns for nicotine calculator
    nic_col1, nic_col2 = st.columns([3, 2])
    
    with nic_col1:
        st.subheader("Vape Details")
        
        # Nicotine percentage input
        nicotine_percent = st.number_input(
            "Nicotine content (%, e.g., 5 for 5%):",
            min_value=0.0,
            max_value=50.0,
            step=0.1,
            value=5.0,
            key="nic_percent"
        )
        
        # Convert to mg/mL
        nicotine_mg_ml = nicotine_percent * 10  # 5% = 50mg/mL
        st.write(f"*Equivalent to {nicotine_mg_ml:.0f} mg/mL*")
        
        # Vape capacity
        vape_capacity = st.number_input(
            "Vape capacity (mL):",
            min_value=0.0,
            step=0.5,
            value=18.0,
            key="vape_capacity"
        )
        
        # Days to finish
        days_to_finish = st.number_input(
            "Days to finish this amount:",
            min_value=0.1,
            step=0.5,
            value=7.0,
            key="days_finish"
        )
        
        # Calculate button for nicotine
        nic_calculate = st.button("Calculate Nicotine Consumption", type="primary", key="nic_calc")

    # Function to calculate nicotine consumption
    def calculate_nicotine_consumption(nicotine_percent, capacity_ml, days):
        # Calculate mg/mL (5% = 50mg/mL)
        mg_per_ml = nicotine_percent * 10
        
        # Total nicotine in the vape
        total_nicotine_mg = mg_per_ml * capacity_ml
        
        # Daily nicotine consumption
        daily_nicotine_mg = total_nicotine_mg / days
        
        # Pack per day equivalent (21mg = 1 pack per day)
        ppd_equivalent = daily_nicotine_mg / 21
        
        return mg_per_ml, total_nicotine_mg, daily_nicotine_mg, ppd_equivalent

    # Results section for nicotine
    with nic_col2:
        st.subheader("Results")
        if nic_calculate:
            mg_per_ml, total_nic, daily_nic, ppd = calculate_nicotine_consumption(
                nicotine_percent, vape_capacity, days_to_finish
            )
            
            st.markdown(f"""
            ### 💨 {daily_nic:.0f} mg nicotine per day
            ### 🚬 {ppd:.1f} pack-per-day equivalent
            
            **Details:**
            - Nicotine concentration: {nicotine_percent}% ({mg_per_ml:.0f} mg/mL)
            - Vape capacity: {vape_capacity} mL
            - Usage period: {days_to_finish} days
            - Total nicotine: {total_nic:.0f} mg
            
            **Calculation:**
            {mg_per_ml:.0f} mg/mL × {vape_capacity} mL ÷ {days_to_finish} days = {daily_nic:.0f} mg/day
            {daily_nic:.0f} mg ÷ 21 mg/pack = {ppd:.1f} ppd
            """)
            
            # Visual representation
            if ppd >= 1:
                pack_icons = "📦 " * int(ppd)
                if ppd % 1 >= 0.5:
                    pack_icons += "📋 "
                st.markdown(f"**Visual:** {pack_icons}")
            else:
                st.markdown("**Visual:** 📋 (less than 1 pack equivalent)")
                
        else:
            st.info("Enter your vape details and click Calculate")

    # Reference table for nicotine
    st.markdown("---")
    st.subheader("Nicotine Reference")
    nic_reference_data = {
        "Nicotine %": ["3%", "5%", "6%"],
        "mg/mL": ["30", "50", "60"],
        "Example: 2mL/day consumption": ["60 mg/day (2.9 ppd)", "100 mg/day (4.8 ppd)", "120 mg/day (5.7 ppd)"]
    }
    nic_reference_df = pd.DataFrame(nic_reference_data)
    st.table(nic_reference_df)

# General health information
st.markdown("---")
st.markdown("""
### Important Information
* **Alcohol**: This calculator uses the formula provided: Volume (mL) × %ABV ÷ 17.05
* **Nicotine**: 21mg of nicotine equals 1 pack-per-day equivalence
* These calculators are for educational purposes only
* Always use substances responsibly
* If you're concerned about your consumption, please consult a healthcare professional
""")
