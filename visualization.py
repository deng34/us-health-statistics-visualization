import pandas as pd
import os
import json

# Directory path
directory_path = 'path/to/your/file'

# List of file names to be processed
file_names = [
    # Add your Excel files here
    'health_statistics_2014.xlsx',
    'health_statistics_2015.xlsx'
    # ... add other files as needed
]

all_data = []

total_files = len(file_names)
processed_files = 0

# Iterate through each file
for file_name in file_names:
    try:
        processed_files += 1
        print(f"Processing file {processed_files}/{total_files}: {file_name}")

        file_path = os.path.join(directory_path, file_name)

        # Verify file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        # Extract year from filename
        try:
            year = int(file_name.split('_')[1])
        except (IndexError, ValueError):
            print(f"Could not extract year from filename: {file_name}")
            continue

        # Read Excel file
        excel_data = pd.ExcelFile(file_path)

        # Iterate through each sheet in the file
        for sheet_name in excel_data.sheet_names:
            print(f"  Processing sheet: {sheet_name}")

            # Read the sheet into a DataFrame
            df = excel_data.parse(sheet_name)

            # Convert the sheet to a dictionary
            sheet_data = df.to_dict(orient='records')

            for record in sheet_data:
                record['year'] = year
                record['source_file'] = file_name
                record['condition'] = sheet_name

            # Append the sheet's data to the main list
            all_data.extend(sheet_data)

    except Exception as e:
        print(f"Error processing file {file_name}: {str(e)}")
        continue

if not all_data:
    print("No data was processed successfully. Check your input files and try again.")
    exit(1)

# Save the combined data to a single JSON file
try:
    output_json_path = os.path.join(directory_path, 'combined_health_statistics_2014_2023.json')
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, indent=4, ensure_ascii=False)
    print(f'Successfully saved combined JSON file at: {output_json_path}')
    print(f'Total records processed: {len(all_data)}')
except Exception as e:
    print(f"Error saving JSON file: {str(e)}")
