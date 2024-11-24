import re

import pandas as ps
import os
from dotenv import load_dotenv

load_dotenv()

source_data = ps.read_csv(os.getenv('SOURCE_FILE_PATH'))
output_data = ps.read_csv(os.getenv('OUTPUT_FILE_PATH'))

'''
source_customer = source_data["customer"]
output_customer = output_data["customer_name"]
cust_data = output_data["cust_type"]


def format_name(customer_name):
    # Split the name into parts
    name_parts = customer_name.split()

    # Initialize components
    last_name = first_name = middle_name = suffix = ""

    # Check for suffix (valid suffixes)
    valid_suffixes = ['II', 'III', 'IV', 'V', 'JR', 'SR']
    if name_parts[-1].upper() in valid_suffixes:
        suffix = name_parts[-1].upper()  # Extract suffix
        name_parts = name_parts[:-1]  # Remove suffix from name_parts

    # Handle "and" in the name and ensure the correct assignment
    if 'and' in name_parts:
        and_index = name_parts.index('and')
        first_name = " ".join(name_parts[:and_index]).replace("and", "&")  # Everything before "and"
        middle_name = " ".join(name_parts[and_index+1:])  # Everything after "and"
    else:
        first_name = " ".join(name_parts[:-1])  # First name (or full name if no "and")
        last_name = name_parts[-1]  # Last name is the last element

    # Ensure proper formatting of the names
    first_name = first_name.strip().replace("and", "&")  # Remove extra spaces and replace "and" with "&"
    last_name = last_name.strip().upper()  # Capitalize last name
    middle_name = middle_name.strip()  # Remove any extra spaces from middle name

    # Return formatted name: "LAST|FIRST|MIDDLE|SUFFIX"
    return f"{last_name}|{first_name}|{middle_name}|{suffix}".strip("|")


def verify_names(output, source, cust):
    # If cust_type is 'R', format the source name and compare
    if cust_type == 'R':
        expected_name = format_name(source_customer)
    else:
        # If cust_type is 'B', compare the original name
        expected_name = source_customer

    # Return True if names match, otherwise False
    return output_customer == expected_name


# Iterate over rows in output_data to verify the names
results = []
for idx, row in output_data.iterrows():
    output_customer = row['customer_name']
    cust_type = row['cust_type']

    # Find the corresponding source customer name (assuming matching rows based on index)
    source_customer = source_data.iloc[idx]['customer']

    # Verify the names
    is_correct = verify_names(output_customer, source_customer, cust_type)

    # Store the result (True or False) and the expected name
    results.append(
        {'customer_name': output_customer, 'is_correct': is_correct, 'expected_name': format_name(source_customer)})

# Convert results into a DataFrame for easy display
results_df = ps.DataFrame(results)

# Display the results
print("Verification Results:")
print(results_df[['customer_name', 'is_correct', 'expected_name']])
'''


def extract_address_parts(address):
    # Regular expressions for each part of the address
    street_pattern = (r'(?P<st_no>\d+)(?P<st_no_suffix>[\w/-]*)\s*(?P<st_dir_prefix>[NSEW]*)\s*(?P<st_name>[\w\s]+)\s*'
                      r'(?P<st_suffix>Rd|Ln|St|Ave|Blvd|Dr|Ct|Pl|Way|Terrace|Cir|Pkwy)\s*(?P<st_dir_suffix>[NSEW]*)')

    # Apply the regex pattern to the address
    match = re.match(street_pattern, address.strip())

    if match:
        return match.groupdict()  # Return the matched groups as a dictionary
    return None  # If no match, return None


# Function to process the address data
def checking_address(data_value):
    # Concatenate address1 and address2, filling missing address2 with address1
    concatenated_address = data['address1'] + ' ' + data['address2'].fillna(data['address1'])

    # Loop through each concatenated address
    for address in concatenated_address:
        print(f"Original Address: {address}")

        # Extract address parts using the extract_address_parts function
        address_parts = extract_address_parts(address)

        if address_parts:
            print(f"Street Number: {address_parts['st_no']}")
            print(f"Street Number Suffix: {address_parts['st_no_suffix']}")
            print(f"Street Direction Prefix: {address_parts['st_dir_prefix']}")
            print(f"Street Name: {address_parts['st_name']}")
            print(f"Street Suffix: {address_parts['st_suffix']}")
            print(f"Street Direction Suffix: {address_parts['st_dir_suffix']}")
        else:
            print("Address format is not recognized.")


# Sample DataFrame with address data
data = {'address1': ['1-4668 W Newline RD', '952A Rolling Rd', '12145 1/2 S Constitution Rte', '1 Acre Ln',
                     '5532 old courthouse rd'],
        'address2': ['APT C 4A', 'S Green House', 'Office', '1 Acre Ln', None]}

df = ps.DataFrame(source_data)

# Call the function with the sample data
checking_address(df)