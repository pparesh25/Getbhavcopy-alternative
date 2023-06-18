# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 20:30:41 2023

@author: ppare
"""

# Download all NSE index data with original index name

# Import necessary libraries
import os
import requests
from datetime import datetime, timedelta
import pandas as pd

# Prompt the user to enter the start and end dates
start_date_str = input('Enter the start date (YYYY-MM-DD): ')
end_date_str = input('Enter the end date (YYYY-MM-DD): ')

# Convert the input dates to datetime objects
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

# Define the destination directory and source folder paths
destination_dir = 'C:/Data_NSE_indexes'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Set the base URL for downloading index files
base_url = 'https://archives.nseindia.com/content/indices'

# Define the columns to remove from the downloaded index files
columns_to_remove = ['Points Change', 'Change(%)', 'Turnover (Rs. Cr.)', 'P/E', 'P/B', 'Div Yield']


# Initialize the current date as the start date
current_date = start_date

# Loop through each date from the start date to the end date
while current_date <= end_date:
    # Check if the current date is a weekday (Monday to Friday)
    if current_date.weekday() < 5:
        # Format the date as 'ddmmyyyy' string
        date_str = current_date.strftime('%d%m%Y')

        # Construct the file name for the index file of the current date
        file_name = f'ind_close_all_{date_str}.csv'

        # Construct the URL to download the index file
        url = f'{base_url}/{file_name}'

        try:
            # Send a GET request to download the index file
            response = requests.get(url, timeout=1)

            if response.status_code == 200:
                # If the request is successful, save the file to the destination directory
                file_path = os.path.join(destination_dir, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)

                if os.path.getsize(file_path) > 0:
                    # If the file is downloaded successfully and not empty, print a success message
                    print(f'Index data file download for {current_date.date()} successful.')
                else:
                    # If the file is empty, print a failure message
                    print(f'Failed to download the index data file for {current_date.date()}.')
            else:
                # If the request fails, print the error message
                print(f'Failed to download the index data file for {current_date.date()}. Error: {response.status_code}')

        except requests.exceptions.RequestException:
            # If a timeout or other exception occurs, print a timeout message
            print(f'Timeout occurred Probable holiday {current_date.date()}.')

    # Move to the next date
    current_date += timedelta(days=1)

# Initialize a flag to track if any files are renamed
files_renamed = False

# Loop through each file in the destination directory
for filename in os.listdir(destination_dir):
    # Check if the file is a CSV file starting with "ind_close_all_" and ending with ".csv"
    if filename.startswith("ind_close_all_") and filename.endswith(".csv"):
        # Construct the file path
        file_path = os.path.join(destination_dir, filename)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Remove the unwanted columns from the DataFrame
        df.drop(columns=columns_to_remove, inplace=True)

        # Convert the 'Index Date' column to the desired date format
        df['Index Date'] = pd.to_datetime(df['Index Date'], format='%d-%m-%Y').dt.strftime('%Y%m%d')

        
        # Save the modified DataFrame back to the original file
        df.to_csv(file_path, index=False)

        # Extract the date from the file name
        date_str = filename.split("_")[-1].split(".")[0]
        date = datetime.strptime(date_str, "%d%m%Y").date()

        # Create the new file name with the desired format
        new_filename = date.strftime("%Y-%m-%d-NSE-IND.csv")
        new_file_path = os.path.join(destination_dir, new_filename)

        # Rename the file to the new file name
        os.rename(file_path, new_file_path)

        # Print a message indicating the file processing and renaming
        print(f"Downloaded file: {filename} renamed to {new_filename}")

        # Set the flag to indicate that files have been renamed
        files_renamed = True

# If no files were renamed, print a message indicating no matching files were found
if not files_renamed:
    print("No files matching the criteria were found.")

# Specify the folder path containing the CSV files
folder_path = 'C:/Data_NSE_indexes'

# Get the list of CSV files in the folder ending with "-NSE-IND.csv"
csv_files = [file for file in os.listdir(folder_path) if file.endswith('-NSE-IND.csv')]

# Loop through each CSV file
for file_name in csv_files:
    # Construct the file path
    file_path = os.path.join(folder_path, file_name)

    # Extract the date from the file name
    date_parts = file_name.split('-')
    date = '-'.join(date_parts[0:3])
    extracted_date = date.replace('-', '')
    A = str(extracted_date)

    # Read the CSV file into a pandas DataFrame
    data_frame = pd.read_csv(file_path)

    # Get the value in the first row of the 'Index Date' column
    B = data_frame['Index Date'].astype(str).iloc[0]

    # Compare the extracted date with the value in the DataFrame
    if A != B:
        # If the dates are different, correct the date format in the DataFrame
        data_frame['Index Date'] = A
        print("Date format corrected to Index_Date :", file_name)

        # Save the modified DataFrame back to the original file
        data_frame.to_csv(file_path, index=False)



