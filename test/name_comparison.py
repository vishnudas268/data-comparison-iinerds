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
    return formatted_names


def checking_output_data(source, output):
    formatted_names_list = reformat_name(source)
    list_names = [s.upper() for s in formatted_names_list]
    source["customer_upper"] = source["customer"].str.upper()
    for _, row in output.iterrows():
        cust_type = row["cust_type"]
        customer_name = row["customer_name"]
        if cust_type == "R":
            if customer_name in list_names:
                print(f"{customer_name} is converted correctly")
            else:
                print(f"{customer_name} is not converted correctly")
        else:
            if customer_name in source["customer_upper"].values:
                print(f"{customer_name} is converted correctly")
            else:
                print(f"{customer_name} is not converted correctly")


checking_output_data(source_data, output_data)
