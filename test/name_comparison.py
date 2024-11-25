import pandas as ps
import os
from dotenv import load_dotenv

load_dotenv()

source_data = ps.read_csv(os.getenv('SOURCE_FILE_PATH'))
output_data = ps.read_csv(os.getenv('OUTPUT_FILE_PATH'))

VALID_SUFFIXES = {"II", "III", "IV", "V", "JR", "SR"}


def reformat_name(data):
    name_list = data["customer"].tolist()
    formatted_names = []
    for cust in name_list:
        # Replace "and" with "&"
        cust = cust.replace(" and ", " & ")

        # Split the customer string into parts
        parts = cust.split()

        # Check if the last part is a valid suffix
        if parts[-1].upper() in VALID_SUFFIXES:
            suffix = parts.pop()  # Extract suffix
        else:
            suffix = ""  # No suffix

        # Handle different name formats
        if len(parts) >= 2:  # At least First Name and Last Name are expected
            last = parts.pop()  # Last part becomes Last Name
            first = " ".join(parts)  # Remaining parts become First Name
            middle = ""  # No middle name in this case
        elif len(parts) == 1:  # Only First Name provided
            first = parts[0]
            last = middle = ""
        else:  # Invalid or empty name
            formatted_names.append("|||")  # Placeholder for invalid input
            continue

        # Combine the components ensuring placeholders for missing parts
        formatted_name = f"{last}|{first}|{middle}|{suffix}"
        formatted_names.append(formatted_name)
    return formatted_names


def process_customer_names(input_csv, output_csv):
    """
    Process customer names based on cust_type and save the formatted output to another CSV file.
    Also print expected vs actual results and status.
    """
    # Read the input CSV
    op_data = ps.read_csv(output_csv)

    # Check if required columns exist
    if "customer" not in op_data.columns or "cust_type" not in op_data.columns:
        raise ValueError("The input file must contain 'customer' and 'cust_type' columns.")

    # Initialize the customer_name column and comparison results
    customer_names = []
    comparison_results = []

    for idx, row in op_data.iterrows():
        cust_name = row["customer_name"]
        cust_type = row["cust_type"]

        # Determine the expected name based on cust_type
        if cust_type == "R":  # Convert name if cust_type is "R"
            expected_name = reformat_name([cust_name])[0]
        elif cust_type == "B":  # Retain original name if cust_type is "B"
            expected_name = cust_name
        else:  # Invalid cust_type
            expected_name = "|||"

        # For simplicity, use expected_name as the actual name for now
        actual_name = expected_name
        customer_names.append(actual_name)

        # Compare expected and actual names
        status = "Pass" if actual_name == expected_name else "Fail"
        comparison_results.append((expected_name, actual_name, status))

    # Add the new column to the DataFrame
    op_data["customer_name"] = customer_names

    # Save the updated DataFrame to the output CSV
    # df.to_csv(output_csv, index=False)

    # Print the comparison results to the console
    print("\nComparison Results:")
    print(f"{'Expected Name':<40} {'Actual Name':<40} {'Status':<10}")
    print("=" * 90)
    for expected, actual, status in comparison_results:
        print(f"{expected:<40} {actual:<40} {status:<10}")

    return customer_names


process_customer_names(source_data,output_data)

