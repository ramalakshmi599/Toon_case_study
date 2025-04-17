import pandas as pd
from utils import toon_customers_basedOnAge, toon_customers_basedOnProvince , toon_customers_basedOnYearRange,toon_customers_basedOnSurfaceArea, toon_electricity_usage_analysis, toon_compare_electricity_usage, toon_compare_toon_gas_usage,toon_app_payment_analysis,toon_mandate_status,toon_active_contracts,non_toon_compare_electricity_usage,non_toon_compare_toon_gas_usage


# Import the CSV file
data = pd.read_csv('../data_set.csv', delimiter=';')

# Handle cases where the column might have string values 'True'/'False' or NaN
data['bought_toon'] = data['bought_toon'].apply(lambda x: str(x).lower() == 'true' if pd.notna(x) else False)

# Count the rows where 'bought_toon' is True
count = data[data['bought_toon'] == True].shape[0]
print(f"Number of people who bought Toon is : {count}")

# Convert 'age' to numeric 
data['age'] = pd.to_numeric(data['age'], errors='coerce')
#data.dropna(subset=['age'], inplace=True)

# Convert 'BOUWJAAR_PAND' to numeric
data['BOUWJAAR_PAND'] = pd.to_numeric(data['BOUWJAAR_PAND'], errors='coerce')


def main(data):
 
   #Customer who bought toon based on age
    count_below_25, count_25_35, count_35_45, count_above_45 = toon_customers_basedOnAge(data)
    print(f"Number of customers below 25 years who bought Toon: {count_below_25}")
    print(f"Number of customers aged 25-35 years who bought Toon: {count_25_35}")
    print(f"Number of customers aged 35-45 years who bought Toon: {count_35_45}")
    print(f"Number of customers above 45 years who bought Toon: {count_above_45}")
    
    # Customer who bought toon based on province
    province_counts = toon_customers_basedOnProvince(data)
    print("Number of customers who bought Toon per province:")
    print(province_counts)

   # Customers who bought toon based on house construction year
    year_range_analysis = toon_customers_basedOnYearRange(data)
    print("\nNumber of Toon customers by house construction year ranges:")
    print(year_range_analysis)

    # Customer who bought toon based on surface area
    surface_area_counts = toon_customers_basedOnSurfaceArea(data)
    print("Toon customers based on house surface area:")
    print(surface_area_counts)

  # Analyze estimated peak and off-peak electricity usage
    summary = toon_electricity_usage_analysis(data)
    print("Electricity Usage Analysis Summary:")
    print(summary)

  # Compare electricity usage with last contract
    electricity_results = toon_compare_electricity_usage(data)
    print("Electricity consumption comparison for customers who bought Toon:")
    print("Total Electricity Usage This Year:", electricity_results["total_this_year"])
    print("Total Electricity Usage Last Contract:", electricity_results["total_last_contract"])
    print("Difference in Electricity Consumption:", electricity_results["usage_difference"])
    print("Percentage Change in Electricity Usage:", 
          f"{electricity_results['percentage_change']:.2f}%" if electricity_results['percentage_change'] is not None else "N/A")

 # Call the function to compare gas usage
    gas_comparison = toon_compare_toon_gas_usage(data)
    print("Gas consumption comparison for customers who bought Toon:")
    print(f"Total Gas Consumption This Year: {gas_comparison['total_this_year']}")
    print(f"Total Gas Consumption Last contract: {gas_comparison['total_last_year']}")
    print(f"Difference in gas Consumption: {gas_comparison['consumption_difference']}")
    print(f"Percentage Change in Gas Usage: {gas_comparison['percentage_change']:.2f}%")

# Customers who have used app for payment features
    true_counts = toon_app_payment_analysis(data)
    print("Customers who have used app for payment features:")
    for column, count in true_counts.items():
        print(f"Count of True for {column}: {count}")

# Customers who accepted or declined mandate
    true_counts = toon_mandate_status(data)
    print("Customers who have accepted or declined mandates:")
    for column, count in true_counts.items():
        print(f"Count of True for {column}: {count}")
    
# Customers with active contracts
    true_counts = toon_active_contracts(data)
    print("Customers who have active boiler and electricity contract:")
    for column, count in true_counts.items():
        print(f"Count of True for {column}: {count}")

 # Compare electricity usage for non toon users with last contract

    electricity_results = non_toon_compare_electricity_usage(data)
    print("Electricity consumption comparison for non Toon customers:")
    print("Total electricity usage this year:", electricity_results["total_this_year"])
    print("Total electricity usage last contract:", electricity_results["total_last_contract"])
    print("Difference in electricity consumption:", electricity_results["usage_difference"])
    print("Percentage change in electricity usage:", 
          f"{electricity_results['percentage_change']:.2f}%" if electricity_results['percentage_change'] is not None else "N/A")

 # Compare gas usage for non toon users with last contract
    gas_comparison = non_toon_compare_toon_gas_usage(data)
    print("Gas consumption comparison for non Toon customers:")
    print(f"Total gas consumption this year: {gas_comparison['total_this_year']}")
    print(f"Total gas consumption last contract: {gas_comparison['total_last_year']}")
    print(f"Difference in gas consumption: {gas_comparison['consumption_difference']}")
    print(f"Percentage change in gas usage: {gas_comparison['percentage_change']:.2f}%")

if __name__ == "__main__":
    main(data)



