import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from construction_year_bins import year_bins, year_labels
from surface_area_bins import surface_bins,surface_labels


#Customers who bought toon based on age

def toon_customers_basedOnAge(data):
    # Filter customers who bought Toon
    toon_buyers = data[data['bought_toon'] == True]

    # Segment customers into age categories
    below_25 = toon_buyers[toon_buyers['age'] < 25]
    age_25_35 = toon_buyers[(toon_buyers['age'] >= 25) & (toon_buyers['age'] <= 35)]
    age_35_45 = toon_buyers[(toon_buyers['age'] > 35) & (toon_buyers['age'] <= 45)]
    above_45 = toon_buyers[toon_buyers['age'] > 45]

    # Counts of each group
    count_below_25 = below_25.shape[0]
    count_25_35 = age_25_35.shape[0]
    count_35_45 = age_35_45.shape[0]
    count_above_45 = above_45.shape[0]

    # Visualization
    age_groups = ['<25', '25-35', '35-45', '>45']
    counts = [count_below_25, count_25_35, count_35_45, count_above_45]

    plt.figure(figsize=(10, 6))
    plt.bar(age_groups, counts, color=['green', 'teal', 'orange', 'blue'], alpha=0.7, width=0.5)
    plt.title("Customers who bought Toon by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Customers")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return count_below_25, count_25_35, count_35_45, count_above_45

#Customers who bought toon based on Province

def toon_customers_basedOnProvince(data):
    # Filter customers who bought Toon
    toon_buyers = data[data['bought_toon'] == True]

    # Group by province and count the number of customers
    province_counts = toon_buyers.groupby('province').size()
    province_counts = toon_buyers.groupby('province').size()
    
# Visualization
    plt.figure(figsize=(8, 6))
    plt.bar(province_counts.index, province_counts.values, color='blue', alpha=0.7)
    plt.title("Customers who bought Toon by province", fontsize=14)
    plt.xlabel("Province", fontsize=12)
    plt.ylabel("Number of Customers", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    return province_counts
 
 # Customers who bought toon based on house construction year ranges

def toon_customers_basedOnYearRange(data):
    
    # Filter customers who bought Toon
    toon_buyers = data[data['bought_toon'] == True].copy()

    # Categorize construction years into ranges
    toon_buyers['year_range'] = pd.cut(toon_buyers['BOUWJAAR_PAND'], bins=year_bins, labels=year_labels, right=False)

    # Group by year range and count customers
    year_range_counts = toon_buyers['year_range'].value_counts().sort_index()
    
   
   # Visualization
    plt.figure(figsize=(8, 6))
    plt.bar(year_range_counts.index, year_range_counts.values, color='blue', alpha=0.8)
    plt.title("Distribution of Toon customers by construction year range", fontsize=14)
    plt.xlabel("Construction year range", fontsize=12)
    plt.ylabel("Number of Customers", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    return year_range_counts

# Customers who bought toon based on surface area of the house
def toon_customers_basedOnSurfaceArea(data):
     
    toon_buyers = data[data['bought_toon']].copy()

    # Create a new column for surface area range
    toon_buyers['surface_area_range'] = pd.cut(toon_buyers['VLOEROPPERVLAK_VERBLIJFSOBJECT'], bins=surface_bins, labels=surface_labels, right=False)

    # Count customers in each range
    surface_area_counts = toon_buyers.groupby('surface_area_range', observed=False).size().reset_index(name='count')

    # Visualization
    plt.figure(figsize=(8, 6))
    plt.bar(surface_area_counts['surface_area_range'], surface_area_counts['count'], color='blue', alpha=0.8)
    plt.title("Distribution of Toon customers by surface area range", fontsize=14)
    plt.xlabel("Surface area range (m²)", fontsize=12)
    plt.ylabel("Number of customers", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    return surface_area_counts

# Analyze estimated peak and off peak electricity usage
def toon_electricity_usage_analysis(data):
    
    # Required columns
    required_columns = ['electricity_annual_consumption_estimated_offpeak', 'electricity_annual_consumption_estimated_peak','electricity_annual_consumption_estimated_total']
    
    toon_buyers = data[data['bought_toon'] == True].copy()
    # Check if required columns are present
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Dataset is missing required columns: {required_columns}")
    
    # Clean the data
    electricity_data = toon_buyers[required_columns].copy()
    electricity_data = electricity_data.dropna()
    electricity_data = electricity_data[(electricity_data >= 0).all(axis=1)]
    

  
    # Calculate proportions
    electricity_data['offpeak_proportion'] = electricity_data['electricity_annual_consumption_estimated_offpeak'] / electricity_data['electricity_annual_consumption_estimated_total']
    electricity_data['peak_proportion'] = electricity_data['electricity_annual_consumption_estimated_peak'] / electricity_data['electricity_annual_consumption_estimated_total']
    
    # Summary statistics
    summary = electricity_data.describe()
    
    # Visualization
    plt.figure(figsize=(8, 6))
    sns.histplot(electricity_data['offpeak_proportion'], kde=True, color='blue', label='Off-Peak Proportion')
    sns.histplot(electricity_data['peak_proportion'], kde=True, color='orange', label='Peak Proportion')
    plt.legend()
    plt.title("Proportions of Off-Peak and Peak Electricity Usage")
    plt.xlabel("Proportion")
    plt.ylabel("Frequency")
    plt.show()
    
    return summary

   #Compare electricity usage with last contract for toon customers
   
def toon_compare_electricity_usage(data):

    toon_buyers = data[data['bought_toon'] == True].copy()

     # Calculate total electricity usage for this year
    total_electricity_this_year = toon_buyers['electricity_annual_consumption_estimated_total'].sum()
    
    # Calculate total electricity usage for last year
    total_electricity_last_contract = toon_buyers['electricity_last_contract_annual_consumption_estimated_total'].sum()
    
    # Calculate the difference
    electricity_difference = total_electricity_this_year - total_electricity_last_contract
    percentage_change = (electricity_difference / total_electricity_last_contract) * 100 if total_electricity_last_contract != 0 else None
    
    periods = ['This Year','Last Contract']
    values = [total_electricity_this_year, total_electricity_last_contract]
    plt.figure(figsize=(8, 6))
    plt.bar(periods, values, color=['orange', 'blue'], alpha=0.7,width=0.5)
    plt.xlabel('Period', fontsize=12)
    plt.ylabel('Electricity Usage (kWh)', fontsize=12)
    plt.title('Electricity Usage Comparison(Toon Customers)', fontsize=14)
    for i, value in enumerate(values):
        plt.text(i, value + 1000, f'{int(value)}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()

    # Return results
    return {
        "total_this_year": total_electricity_this_year,
        "total_last_contract": total_electricity_last_contract,
        "usage_difference": electricity_difference,
        "percentage_change": percentage_change,
    }

 #Compare gas usage with last contract for toon customers
def toon_compare_toon_gas_usage(data):
   
    # Filter customers who bought Toon
    toon_buyers = data[data['bought_toon'] == True]

    # Calculate total gas consumption for this year
    total_gas_this_year = toon_buyers['gas_annual_consumption_estimated'].sum()

    # Calculate total gas consumption for last year
    total_gas_last_contract = toon_buyers['gas_last_contract_annual_consumption_estimated'].sum()

    # Calculate the difference
    gas_difference = total_gas_this_year - total_gas_last_contract
    percentage_change = (gas_difference / total_gas_last_contract) * 100 if total_gas_last_contract != 0 else None

    # Ensure the values are numeric
    total_gas_this_year = float(total_gas_this_year)
    total_gas_last_contract= float(total_gas_last_contract)

     # Define data for the bar graph
    periods = [ 'This Year','Last Contract']
    values = [total_gas_this_year, total_gas_last_contract]
    plt.figure(figsize=(8, 6))
    plt.bar(periods, values, color=['orange', 'blue'], alpha=0.7,width=0.5)
    plt.xlabel('Period', fontsize=12)
    plt.ylabel('Gas Usage (m³)', fontsize=12)
    plt.title('Gas Usage Comparison(Toon Customers)', fontsize=14)
    for i, value in enumerate(values):
        plt.text(i, value + 1000, f'{int(value)}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()

    # Return results
    return {
        "total_this_year": total_gas_this_year,
        "total_last_year": total_gas_last_contract,
        "consumption_difference": gas_difference,
        "percentage_change": percentage_change,
    }

# Analyse app selections related to payment
def toon_app_payment_analysis(data):
    
    # Filter Toon customers
    toon_buyers = data[data['bought_toon'] == True]
    
    # Specify the columns to analyze
    columns = [
        'app_advance_payment_adjustment_last_year',
        'app_check_advance_payment_last_year',
        'app_transaction_request_last_year',
        'app_determine_day_of_payment_last_year'
    ]
    
    # Count True values for each column
    true_counts = {col: toon_buyers[col].sum() for col in columns}
    #Visualization
    labels = list(true_counts.keys())
    values = list(true_counts.values())

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['blue', 'orange', 'green', 'purple'], alpha=0.8,width=0.5)
    plt.title("App Payment Feature Usage by Toon Customers", fontsize=14)
    plt.xlabel("App Payment Features", fontsize=12)
    plt.ylabel("Count of Users", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    for i, value in enumerate(values):
        plt.text(i, value + 0.5, f'{value}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()
    return true_counts

#Customers who accepted or declined mandate

def toon_mandate_status(data):
 
    toon_buyers = data[data['bought_toon'] == True]
    columns = [
       'app_mandate_no_last_year',
       'app_mandate_yes_last_year'
    ]
    # Count True values for each column
    true_counts = {col: toon_buyers[col].sum() for col in columns}

   # Visualization
    labels = list(true_counts.keys())
    values = list(true_counts.values())
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['orange', 'blue'], alpha=0.8,width=0.5)
    plt.title("Mandate Status for Toon Customers", fontsize=14)
    plt.xlabel("Mandate Status", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    for i, value in enumerate(values):
        plt.text(i, value + 0.5, f'{value}', ha='center', va='bottom', fontsize=10)
    plt.show()
    return true_counts

# Customers with active contracts
def toon_active_contracts(data):

    toon_buyers = data[data['bought_toon'] == True]

    columns = [
       'has_active_boiler_rent_contract',
       'has_active_electricity_contract'
     ]

   # Count True values for each column
    true_counts = {col: toon_buyers[col].sum() for col in columns}

    contract_types = list(true_counts.keys())
    counts = list(true_counts.values())

    #Visualization
    plt.figure(figsize=(8, 6))
    plt.bar(contract_types, counts, color=['orange','blue'], alpha=0.7,width=0.5)
    plt.xlabel('Contract Type', fontsize=12)
    plt.ylabel('Number of Active Contracts', fontsize=12)
    plt.title('Active Contracts for Toon Customers', fontsize=14)
    for i, count in enumerate(counts):
        plt.text(i, count + 0.5, str(count), ha='center', va='bottom', fontsize=10)

    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

    return true_counts


 #Compare electricity usage with last contract for non-toon users

def non_toon_compare_electricity_usage(data):

    non_toon_buyers = data[data['bought_toon'] == False].copy()

     # Calculate total electricity usage for this year
    total_electricity_this_year = non_toon_buyers['electricity_annual_consumption_estimated_total'].sum()
    
    # Calculate total electricity usage for last year
    total_electricity_last_contract = non_toon_buyers['electricity_last_contract_annual_consumption_estimated_total'].sum()
    
    # Calculate the difference
    electricity_difference = total_electricity_this_year - total_electricity_last_contract
    percentage_change = (electricity_difference / total_electricity_last_contract) * 100 if total_electricity_last_contract != 0 else None

    periods = ['This Year','Last Contract']
    values = [total_electricity_this_year, total_electricity_last_contract]

    #Visualization
    plt.figure(figsize=(8, 6))
    plt.bar(periods, values, color=['orange', 'blue'], alpha=0.7,width=0.5)
    plt.xlabel('Period', fontsize=12)
    plt.ylabel('Electricity Usage (kWh)', fontsize=12)
    plt.title('Electricity Usage Comparison (Non-Toon Customers)', fontsize=14)
    for i, value in enumerate(values):
        plt.text(i, value + 1000, f'{int(value)}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()


    # Return results
    return {
        "total_this_year": total_electricity_this_year,
        "total_last_contract": total_electricity_last_contract,
        "usage_difference": electricity_difference,
        "percentage_change": percentage_change,
    }

#Compare gas usage with last contract for toon customers
def non_toon_compare_toon_gas_usage(data):
   
    # Filter customers who bought Toon
    non_toon_buyers = data[data['bought_toon'] == False]

    # Calculate total gas consumption for this year
    total_gas_this_year = non_toon_buyers['gas_annual_consumption_estimated'].sum()

    # Calculate total gas consumption for last year
    total_gas_last_contract = non_toon_buyers['gas_last_contract_annual_consumption_estimated'].sum()

    # Calculate the difference
    gas_difference = total_gas_this_year - total_gas_last_contract
    percentage_change = (gas_difference / total_gas_last_contract) * 100 if total_gas_last_contract != 0 else None

   
    periods = [ 'This Year','Last Contract',]
    values = [total_gas_this_year, total_gas_last_contract]

    #Visualization
    plt.figure(figsize=(8, 6))
    plt.bar(periods, values, color=['orange', 'blue'], alpha=0.7,width=0.5)
    plt.xlabel('Period', fontsize=12)
    plt.ylabel('Gas Usage (m³)', fontsize=12)
    plt.title('Gas Usage Comparison (Non-Toon Customers)', fontsize=14)
    for i, value in enumerate(values):
        plt.text(i, value + 1000, f'{int(value)}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()
    

    # Return results
    return {
        "total_this_year": total_gas_this_year,
        "total_last_year": total_gas_last_contract,
        "consumption_difference": gas_difference,
        "percentage_change": percentage_change,
    }
