# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 12:55:52 2024

@author: ppare
"""

import os
import socket
import shutil
import zipfile
import requests
import pandas as pd
import urllib.request
from datetime import datetime, timedelta



def download_file(url, output_folder):
    # Download a file from the given URL to the specified output folder
    filename = os.path.basename(url)
    output_path = os.path.join(output_folder, filename)
    urllib.request.urlretrieve(url, output_path)
    print(f'Eq-bhavcopy {filename} downloaded.')
    return output_path


def extract_files(zip_file, output_folder):
    # Extract files from the given ZIP file to the specified output folder
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    print("Zip file extracted:", zip_file)


def rename_files(directory):
    # Rename files in the specified directory to the desired format
    files = os.listdir(directory)
    renamed_files = []

    for file in files:
        if file.endswith("0000.csv"):
            # Extract the date from the file name
            date = file[22:30]
            new_name = date + ".csv"
            new_name = new_name.replace("BhavCopy_NSE_CM_0_0_0_", "").replace("_F_0000", "")
            date_obj = datetime.strptime(date, "%Y%m%d")
            new_name = date_obj.strftime("%Y-%m-%d") + "-NSE-EQ.csv"

            # Rename the file
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            renamed_files.append((file, new_name))
        else:
            print(f"File '{file}' does not end with 'bhav.csv' and was not renamed.")

    if renamed_files:
        for old_name, new_name in renamed_files:
           print(f"File '{old_name}' renamed to: '{new_name}'")
    else:
        print("No files found or no files meet the desired condition.")
        
def modify_files(directory):
    # Modify the renamed files in the specified directory
    files = os.listdir(directory)

    for file in files:
        if file.endswith("-NSE-EQ.csv"):
            file_path = os.path.join(directory, file)

            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Remove the specified columns
                columns_to_remove = ['BizDt','Sgmt','Src','FinInstrmTp','FinInstrmId','ISIN','XpryDt','FininstrmActlXpryDt',	
                                     'StrkPric','OptnTp','FinInstrmNm','LastPric','PrvsClsgPric','UndrlygPric','SttlmPric',
                                     'OpnIntrst','ChngInOpnIntrst','TtlTrfVal','TtlNbOfTxsExctd','SsnId','NewBrdLotQty','Rmks','Rsvd1','Rsvd2','Rsvd3','Rsvd4']
                
                df = df.drop(columns=columns_to_remove)

                # Filter rows based on SERIES column
                df = df[df['SctySrs'].isin(['EQ', 'BE', 'BZ'])]

                # Convert the TradDt column to the desired format
                #df['TradDt'] = pd.to_datetime(df['TradDt'], format='%m/%d/%Y').dt.strftime('%Y%m%d')
                
                # Convert the 'TradDt' column to datetime by inferring the format
                df['TradDt'] = pd.to_datetime(df['TradDt'], errors='coerce')

                # Check if there are any NaT (Not a Time) values which indicate conversion issues
                if df['TradDt'].isna().any():
                    print("There are some dates that couldn't be converted:")
                    print(df[df['TradDt'].isna()])

                # Convert the datetime object to the desired string format
                df['TradDt'] = df['TradDt'].dt.strftime('%Y%m%d')
                
                                
                # Reorder the columns
                cols = df.columns.tolist()
                cols.remove('TradDt')
                cols.insert(cols.index('OpnPric'), 'TradDt')
                df = df[cols]

                # Remove the SctySrs column
                df = df.drop(columns=['SctySrs'])
                
                # Sort the DataFrame by the 'TckrSymb' column
                df = df.sort_values(by='TckrSymb')

                # Save the modified dataframe back to CSV
                df.to_csv(file_path, index=False, header=False)

                print(f"{file} : Data Structure converted to getbhavcopy")
            except FileNotFoundError:
                print(f"File not found: {file}")        


# Download and extract files

output_folder = "C:/data"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Collect start and end dates as input
start_date_str = input('Enter the start date (YYYY-MM-DD): ')
end_date_str = input('Enter the end date (YYYY-MM-DD): ')

# Convert input dates to datetime objects
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

delta = end_date - start_date
date_range = []
for i in range(delta.days + 1):
    date = start_date + timedelta(days=i)
    if date.weekday() < 5:
        date_range.append(date)

socket.setdefaulttimeout(1)

downloaded_files = []

for date in date_range:
    # Construct the URL for downloading the file
    url = "https://archives.nseindia.com/content/cm"
    date_str = date.strftime("%Y%m%d")
    filename = "BhavCopy_NSE_CM_0_0_0_{}_F_0000.csv.zip".format(date_str)
    url = "{}/{}".format(url, filename)
    #print("URL:", url)

    try:
        # Download the file and add it to the list of downloaded files
        downloaded_file = download_file(url, output_folder)
        downloaded_files.append(downloaded_file)
    except Exception as e:
        print("Error downloading file, Probable holiday:", filename)
        #print(e)

for file in downloaded_files:
    try:
        # Extract the downloaded ZIP files
        extract_files(file, output_folder)
    except Exception as e:
        print("Error extracting file:", file)
        print(e)

for file in downloaded_files:
    # Remove the downloaded ZIP files
    os.remove(file)
    print("Removed:", file)
    

rename_files(output_folder)
modify_files(output_folder)

# Define the destination directory and source folder paths
destination_dir = 'C:/dataind'
source_folder = 'C:/dataind'
destination_folder = 'C:/data'

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
                    print(f'Indexes data file download for {current_date.date()} successful.')
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
folder_path = 'C:/dataind'

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
        print("Date format corrected to Index_Date :", file_name)
        data_frame['Index Date'] = A

        # Save the modified DataFrame back to the original file
        data_frame.to_csv(file_path, index=False)

# Get the list of CSV files in the source folder
source_csv_files = [file for file in os.listdir(source_folder) if file.endswith('.csv')]

# Process each CSV file
for source_file_name in source_csv_files:
    # Construct the source file path
    source_file_path = os.path.join(source_folder, source_file_name)

    # Extract date from the source file name
    source_date_parts = source_file_name.split('-')
    source_date = '-'.join(source_date_parts[0:3])
    source_extracted_date = source_date.replace('-', '')

    # Create the destination file name
    destination_file_name = source_date + '-NSE-EQ.csv'
    destination_file_path = os.path.join(destination_folder, destination_file_name)

    # Check if the destination file already exists
    if os.path.exists(destination_file_path):
        # Read the source CSV file into a pandas DataFrame
        source_data_frame = pd.read_csv(source_file_path)

        # Append the source DataFrame to the destination CSV file
        source_data_frame.to_csv(destination_file_path, mode='a', header=False, index=False)

        # Check if data copy was successful
        if os.path.exists(destination_file_path):
            print(f"Index data save to Eq-bhavcopy {destination_file_path} successful. ")
        else:
            print(f"Data copy failed: {destination_file_path}")
    else:
        print(f"Eq-bhavcopy {destination_file_path} not available to save index data.")
        



# Create folder if not present
folder_path = "C:/Get_bhav_copy NSE"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Created folder: {folder_path}")

# Change extension from .csv to .txt
source_folder = "C:/data"
for filename in os.listdir(source_folder):
    if filename.endswith("-NSE-EQ.csv"):
        new_filename = os.path.splitext(filename)[0] + ".txt"
        old_filepath = os.path.join(source_folder, filename)
        new_filepath = os.path.join(source_folder, new_filename)
        os.rename(old_filepath, new_filepath)
        print(f"Changed extension: {filename} -> {new_filename}")

# Copy files to destination folder
destination_folder = "C:/Get_bhav_copy NSE"
for filename in os.listdir(source_folder):
    if filename.endswith("-NSE-EQ.txt"):
        source_filepath = os.path.join(source_folder, filename)
        destination_filepath = os.path.join(destination_folder, filename)
        shutil.copy2(source_filepath, destination_filepath)
        print(f"Copied file: {filename} -> {destination_folder}")

# Remove source folders
shutil.rmtree("C:/data")
shutil.rmtree("C:/dataind")
print("Removed folders: C:/data, C:/dataind")
print()
print("All Eq-bhavcopy with indexes data are saved to 'C:/Get_bhav_copy NSE'.")
print()
print("If you find my work valuable, please consider donating.")
print("💲 Donate via UPI: p.paresh25@oksbi")