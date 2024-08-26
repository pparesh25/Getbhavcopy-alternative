# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 14:43:37 2024

@author: ppare
"""

import os
import sys
import socket
import zipfile
import pandas as pd
import urllib.request
from datetime import datetime, timedelta


def Download_NSE_Bhavcopy_File(NSE_Bhavcopy_URL, Bhavcopy_Download_Folder):
    # Download a file from the given URL to the specified output folder
    filename = os.path.basename(NSE_Bhavcopy_URL)
    output_path = os.path.join(Bhavcopy_Download_Folder, filename)
    urllib.request.urlretrieve(NSE_Bhavcopy_URL, output_path)
    print(f'Eq-bhavcopy {filename} downloaded.')
    return output_path

def Extract_NSE_Bhavcopy_Zip_Files(zip_file, output_folder):
    # Extract files from the given ZIP file to the specified output folder
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    print("Zip file extracted:", zip_file)

def Rename_NSE_Bhavcopy_Files(directory):
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
        
def Modify_NSE_Bhavcopy_Files(directory):
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

                print(f"{file} :Eq_Bhavcopy Data Structure converted to getbhavcopy")
            except FileNotFoundError:
                print(f"File not found: {file}")
                
                
def download_NSE_Index_file(NSE_Index_URL, index_file_download_folder):
    # Download a file from the given URL to the specified output folder
    filename = os.path.basename(NSE_Index_URL)
    output_path = os.path.join(index_file_download_folder, filename)
    urllib.request.urlretrieve(NSE_Index_URL, output_path)
    print(f'NSE_Index_file {filename} downloaded.')
    return output_path

def process_index_files(index_file_download_folder):
    
    # Define the columns to remove from the downloaded index files
    columns_to_remove = ['Points Change', 'Change(%)', 'Turnover (Rs. Cr.)', 'P/E', 'P/B', 'Div Yield']

    # Loop through each file in the destination directory
    for filename in os.listdir(index_file_download_folder):
        # Check if the file is a CSV file starting with "ind_close_all_" and ending with ".csv"
        if filename.startswith("ind_close_all_") and filename.endswith(".csv"):
            # Construct the file path
            file_path = os.path.join(index_file_download_folder, filename)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Remove the unwanted columns from the DataFrame
            df.drop(columns=columns_to_remove, inplace=True)

            # Convert the 'Index Date' column to the desired date format
            df['Index Date'] = pd.to_datetime(df['Index Date'], format='%d-%m-%Y').dt.strftime('%Y%m%d')
            
            # Save the modified DataFrame back to the original file
            df.to_csv(file_path, index=False)
            
            print(f"Index file: {filename} Data Structure converted to getbhavcopy" )

def rename_index_files(index_file_download_folder):
    
    files_renamed = False

    # Loop through each file in the destination directory
    for filename in os.listdir(index_file_download_folder):
        # Check if the file is a CSV file starting with "ind_close_all_" and ending with ".csv"
        if filename.startswith("ind_close_all_") and filename.endswith(".csv"):
            # Extract the date from the file name
            date_str = filename.split("_")[-1].split(".")[0]
            date = datetime.strptime(date_str, "%d%m%Y").date()

            # Create the new file name with the desired format
            new_filename = date.strftime("%Y-%m-%d-NSE-IND.csv")
            new_file_path = os.path.join(index_file_download_folder, new_filename)

            # Rename the file to the new file name
            os.rename(os.path.join(index_file_download_folder, filename), new_file_path)

            # Print a message indicating the file processing and renaming
            print(f"Index file: {filename} renamed to {new_filename}")

            # Set the flag to indicate that files have been renamed
            files_renamed = True

    # If no files were renamed, print a message indicating no matching files were found
    if not files_renamed:
        print("No files matching the criteria were found.")

    return files_renamed

def correct_index_date(index_file_download_folder):
    
    # Get the list of CSV files in the folder ending with "-NSE-IND.csv"
    csv_files = [file for file in os.listdir(index_file_download_folder) if file.endswith('-NSE-IND.csv')]

    # Loop through each CSV file
    for file_name in csv_files:
        # Construct the file path
        file_path = os.path.join(index_file_download_folder, file_name)

        # Extract the date from the file name
        date_parts = file_name.split('-')
        date = '-'.join(date_parts[0:3])
        extracted_date = date.replace('-', '')

        # Read the CSV file into a pandas DataFrame
        data_frame = pd.read_csv(file_path)

        # Get the value in the first row of the 'Index Date' column
        data_frame_date = data_frame['Index Date'].astype(str).iloc[0]

        # Compare the extracted date with the value in the DataFrame
        if extracted_date != data_frame_date:
            # If the dates are different, correct the date format in the DataFrame
            print("Date format corrected to Index_Date :", file_name)
            data_frame['Index Date'] = extracted_date

            # Save the modified DataFrame back to the original file
            data_frame.to_csv(file_path, index=False)
            
# Define the function to append index data to EQ-bhavcopy files
def append_index_data_to_eq_bhavcopy(index_file_download_folder, Bhavcopy_Download_Folder):
    
    # Get the list of CSV files in the index file download folder
    source_csv_files = [file for file in os.listdir(index_file_download_folder) if file.endswith('.csv')]
    #print("Found the following CSV files in the index file download folder:")
    #print(source_csv_files)

    # Process each CSV file
    for source_file_name in source_csv_files:
        # Construct the source file path
        source_file_path = os.path.join(index_file_download_folder, source_file_name)
        #print(f"Processing file: {source_file_name}")

        # Extract date from the source file name
        source_date_parts = source_file_name.split('-')
        source_date = '-'.join(source_date_parts[0:3])
        #source_extracted_date = source_date.replace('-', '')
        #print(f"Extracted date: {source_extracted_date}")

        # Create the destination file name
        destination_file_name = source_date + '-NSE-EQ.csv'
        destination_file_path = os.path.join(Bhavcopy_Download_Folder, destination_file_name)
        #print(f"Destination file: {destination_file_name}")

        # Check if the destination file already exists
        if os.path.exists(destination_file_path):
            #print(f"Destination file exists: {destination_file_path}")

            # Read the source CSV file into a pandas DataFrame
            source_data_frame = pd.read_csv(source_file_path)
            #print("Read source CSV file into DataFrame")

            # Append the source DataFrame to the destination CSV file
            source_data_frame.to_csv(destination_file_path, mode='a', header=False, index=False)
            #print("Appended source DataFrame to destination CSV file")

            # Check if data copy was successful
            if os.path.exists(destination_file_path):
                print(f"Index data save to Eq-bhavcopy {destination_file_path} successful. ")
            else:
                print(f"Data copy failed: {destination_file_path}")
        else:
            print(f"Eq-bhavcopy {destination_file_path} not available to save index data.")
            
            
def change_file_extension(Bhavcopy_Download_Folder, old_extension, new_extension):
    
    # Iterate through all files in the folder
    for filename in os.listdir(Bhavcopy_Download_Folder):
        # Check if the file ends with the old extension
        if filename.endswith("-NSE-EQ.csv"):
            # Split the filename into name and extension, and replace the extension with the new extension
            new_filename = os.path.splitext(filename)[0] + ".txt"
            
            # Construct the full path of the old file
            old_filepath = os.path.join(Bhavcopy_Download_Folder, filename)
            
            # Construct the full path of the new file
            new_filepath = os.path.join(Bhavcopy_Download_Folder, new_filename)
            
            # Rename the old file to the new file
            os.rename(old_filepath, new_filepath)
            
            # Print a message to confirm the file extension change
            #print(f"Changed Bhavcopy extension: {filename} to {new_filename}")
            
            
def copy_and_remove_files(Bhavcopy_Download_Folder, Final_Bhavcopy_Folder, remove_folders):
    
    # Copy files to destination folder
    for filename in os.listdir(Bhavcopy_Download_Folder):
        if filename.endswith("-NSE-EQ.txt"):
            source_filepath = os.path.join(Bhavcopy_Download_Folder, filename)
            destination_filepath = os.path.join(Final_Bhavcopy_Folder, filename)
            with open(source_filepath, 'rb') as source_file:
                with open(destination_filepath, 'wb') as destination_file:
                    destination_file.write(source_file.read())
            print(f"Bhavcopy file: {filename} copied to {Final_Bhavcopy_Folder}")

    # Remove source folders
    for folder in remove_folders:
        for root, dirs, files in os.walk(folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(folder)


# Download and extract files
Bhavcopy_Download_Folder = "C:/Data_NSE_temporary"
if os.path.exists(Bhavcopy_Download_Folder):
    # Remove the folder and its contents
    for root, dirs, files in os.walk(Bhavcopy_Download_Folder, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(Bhavcopy_Download_Folder)

# Create the folder again
os.makedirs(Bhavcopy_Download_Folder)

# Download index files
index_file_download_folder = "C:/Data_NSE_Ind_temporary"
if os.path.exists(index_file_download_folder):
    # Remove the folder and its contents
    for root, dirs, files in os.walk(index_file_download_folder, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(index_file_download_folder)

# Create the folder again
os.makedirs(index_file_download_folder)
    
# Final Bhavcopy folder 
Final_Bhavcopy_Folder = "C:/Getbhavcopy_NSE"
if not os.path.exists(Final_Bhavcopy_Folder):
    os.makedirs(Final_Bhavcopy_Folder)
    #print(f"Created folder: {Final_Bhavcopy_Folder}")


# Check if the folder exists and contains files
folder_path = "C:\\Getbhavcopy_NSE"
if os.path.isdir(folder_path) and os.listdir(folder_path):
    # Get the list of files in the folder
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Extract the last date from the file names
    last_date_str = max(f[:10] for f in file_list)
    last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    today = datetime.now().date()   
    if last_date.date() == today:
        print()
        print()
        print("The Bhavcopy database is up to date today",last_date.date(),"and no need to download any files.")
        print()
        print()
        print("If you find my work valuable, please consider donating.")
        print()
        print()
        print("💲 Donate via UPI: p.paresh25@oksbi")
        print()
        print()
        sys.exit()
    next_date = last_date + timedelta(days=1)

    # Set the start date to the next day of the last date
    start_date_str = next_date.strftime('%Y-%m-%d')

    # Set the end date to the current date
    end_date_str = datetime.today().strftime('%Y-%m-%d')
    
    # Print the start and end dates
    print(f"Start date: {start_date_str}")
    print(f"End date: {end_date_str}")
    print()

else:
    # If the folder does not exist or is empty, get user input for the dates
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

socket.setdefaulttimeout(2)

downloaded_files = []

for date in date_range:
    # Construct the URL for downloading the file
    NSE_Bhavcopy_URL = "https://archives.nseindia.com/content/cm"
    date_str = date.strftime("%Y%m%d")
    filename = "BhavCopy_NSE_CM_0_0_0_{}_F_0000.csv.zip".format(date_str)
    NSE_Bhavcopy_URL = "{}/{}".format(NSE_Bhavcopy_URL, filename)
    date = date.strftime('%d-%m-%Y')
    #print("URL:", NSE_Bhavcopy_URL)
    try:
        # Download the file and add it to the list of downloaded files
        Downloaded_Bhavcopy_file = Download_NSE_Bhavcopy_File(NSE_Bhavcopy_URL, Bhavcopy_Download_Folder)
        downloaded_files.append(Downloaded_Bhavcopy_file)
    except Exception as e:
        print(date,"Bhavcopy Zip file not availabel to Download on NSE Server")
        #print(e)
        

for file in downloaded_files:
    try:
        # Extract the downloaded ZIP files
        Extract_NSE_Bhavcopy_Zip_Files(file, Bhavcopy_Download_Folder)
    except Exception as e:
        print("Error extracting file:", file)
        print(e)

for file in downloaded_files:
    # Remove the downloaded ZIP files
    os.remove(file)
    print("Removed:", file)
    
for date in date_range:
    # Construct the URL for downloading the file
    NSE_Index_URL = 'https://archives.nseindia.com/content/indices'
    date_str = date.strftime('%d%m%Y')
    filename = f'ind_close_all_{date_str}.csv'.format(date_str)
    NSE_Index_URL = "{}/{}".format(NSE_Index_URL, filename)
    date = date.strftime('%d-%m-%Y')
    #print("URL:", NSE_Index_URL)

    try:
        # Download the file and add it to the list of downloaded files
        Downloaded_index_file = download_NSE_Index_file(NSE_Index_URL, index_file_download_folder)
        downloaded_files.append(Downloaded_index_file)
    except Exception as e:
        print(date,"Index file not availabel to Download on NSE Server")
        #print(e)
   
Rename_NSE_Bhavcopy_Files(Bhavcopy_Download_Folder)
Modify_NSE_Bhavcopy_Files(Bhavcopy_Download_Folder)

process_index_files(index_file_download_folder)
rename_index_files(index_file_download_folder)
correct_index_date(index_file_download_folder)

append_index_data_to_eq_bhavcopy(index_file_download_folder, Bhavcopy_Download_Folder)
change_file_extension(Bhavcopy_Download_Folder, ".csv", ".txt")

remove_folders = [Bhavcopy_Download_Folder, index_file_download_folder]
copy_and_remove_files(Bhavcopy_Download_Folder, Final_Bhavcopy_Folder, remove_folders)
print()
print()
print("All Eq-bhavcopy with indexes data are saved to 'C:/Getbhavcopy_NSE'.")
print()
print()
print("If you find my work valuable, please consider donating.")
print()
print()
print("💲 Donate via UPI: p.paresh25@oksbi")
print()
print()



