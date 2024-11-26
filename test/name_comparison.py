import pandas as ps
import os
from dotenv import load_dotenv

load_dotenv()

source_data = ps.read_csv(os.getenv('SOURCE_FILE_PATH'))
output_data = ps.read_csv(os.getenv('OUTPUT_FILE_PATH'))

VALID_SUFFIXES = {"II", "III", "IV", "V", "JR", "SR"}


def reformat_name(source):
    name_list = source["customer"].tolist()
    formatted_names = []
    for cust in name_list:
        cust = cust.replace(" and ", " & ")

        parts = cust.split()

        if parts[-1].upper() in VALID_SUFFIXES:
            suffix = parts.pop()
        else:
            suffix = ""

        if len(parts) >= 2:
            last = parts.pop()
            first = " ".join(parts)
            middle = ""
        elif len(parts) == 1:
            first = parts[0]
            last = middle = ""
        else:
            formatted_names.append("|||")
            continue

        formatted_name = f"{last}|{first}|{middle}|{suffix}"
        formatted_names.append(formatted_name)
    print(formatted_names)
    return formatted_names


reformat_name(source_data)


'''
def process_customer_names(output_csv):

    customer_names = []
    comparison_results = []

    for idx, row in output_csv.iterrows():
        cust_type = row["cust_type"]

        
        if cust_type == "R":
            expected_name = reformat_name(source_data)
        elif cust_type == "B":  
            expected_name = source_csv["customer"]
        else: 
            expected_name = "|||"

        
        actual_name = expected_name
        customer_names.append(actual_name)

        
        status = "Pass" if actual_name == expected_name else "Fail"
        comparison_results.append((expected_name, actual_name, status))

   
    output_csv["customer_name"] = customer_names

    
    output_csv.to_csv(output_csv, index=False)

    print("\nComparison Results:")
    print(f"{'Expected Name':<40} {'Actual Name':<40} {'Status':<10}")
    print("=" * 90)
    for expected, actual, status in comparison_results:
        print(f"{expected:<40} {actual:<40} {status:<10}")

    return customer_names


process_customer_names(source_data, output_data)
'''

