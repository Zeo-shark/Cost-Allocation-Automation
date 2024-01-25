import csv
import json
import pandas as pd

# import csv
# import json

def extract_bcsla_tag_to_column(input_csv, output_csv):
    """
    Reads a CSV file, extracts the "BCSLA" tag value from the 'TAGS' column,
    adds it as a new column named "BCSLA", and retains the original 'TAGS' column.
    """

    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['BCSLA']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()  # Write header with new "BCSLA" column

        for row in reader:
            tags_str = row.get('tags', '')  # Use get() to handle empty values
            tags_dict = json.loads(tags_str) if tags_str else {}  # Replace empty values with empty dictionary
            bcsla_value = tags_dict.get('BCSLA', '')  # Extract "BCSLA" value or use empty string
            row['BCSLA'] = bcsla_value  # Add "BCSLA" value to row
            writer.writerow(row)




def lookup_and_update_csv(source_csv, reference_excel):

    df = pd.read_csv(source_csv)

    # Read the lookup file
    lookup_df = pd.read_excel(reference_excel)

    # Merge the two dataframes on the BCSLA column
    merged_df = pd.merge(df, lookup_df, on='BCSLA')

    # Create the new columns
    merged_df['processName'] = merged_df['processName'].fillna('')
    merged_df['Vertical'] = merged_df['Vertical'].fillna('')

    # Write the updated dataframe to a new CSV file
    merged_df.to_csv('cost_allocation_excel.csv', index=False)

    print('New CSV file created successfully!')


# Example usage:
input_csv = "Billing file path.csv"
output_csv = "cost_allocation_excel.csv"
extract_bcsla_tag_to_column(input_csv, output_csv)
reference_excel = "lookup_mapping.xlsx"
lookup_and_update_csv(output_csv, reference_excel)

