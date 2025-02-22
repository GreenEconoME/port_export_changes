# Define dictionary to hold the primary keys of each report
unique_keys = {
    'About': ["ESPM ID"],
    'Portfolio YoY': ["Year"],  
    'Annual Consumption Electric': ["Year", "ESPM ID"],
    'Annual Consumption Gas': ["Year", "ESPM ID"],
    'Annual Consumption Water': ["Year", "ESPM ID"],
    'Annual Generation Solar': ["Year", "ESPM ID"],
    'Quarterly Electric': ["Year", "ESPM ID"],
    'Quarterly Gas': ["Year", "ESPM ID"],
    'Quarterly Water': ["Year", "ESPM ID"],
    'Meter Activity': ["ESPM ID", "Meter ID"],  
    'Year To Date Variance': ["Year", "ESPM ID"], 
    'Annual Waste': ["Year", "ESPM ID"],
}

# List of the sheets to compare
sheets_to_compare = [
    'About',
    'Portfolio YoY',
    'Annual Consumption Electric',
    'Annual Consumption Gas',
    'Annual Consumption Water',
    'Annual Generation Solar',
    'Quarterly Electric',
    'Quarterly Gas',
    'Quarterly Water',
    'Meter Activity',
    'Year To Date Variance',
    'Annual Waste',
]