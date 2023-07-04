#PPP
import urllib.request
import os
import socket
import zipfile
from datetime import datetime, timedelta
import pandas as pd
import shutil

def download_file(url, output_folder):
    filename = os.path.basename(url)
    output_path = os.path.join(output_folder, filename)
    urllib.request.urlretrieve(url, output_path)
    print("Downloaded:", filename)
    return output_path

def extract_files(zip_file, output_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    print("Extracted:", zip_file)

output_folder = "C:/data_fo"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

delta = end - start
date_range = []
for i in range(delta.days + 1):
    date = start + timedelta(days=i)
    if date.weekday() < 5: 
        date_range.append(date)

socket.setdefaulttimeout(1) 

downloaded_files = []

for date in date_range:
    url = "https://archives.nseindia.com/content/historical/DERIVATIVES/{}/{}".format(
        date.strftime("%Y"), date.strftime("%b").upper())
    date_str = date.strftime("%d%b%Y").upper()
    filename = "fo{}bhav.csv.zip".format(date_str)
    url = "{}/{}".format(url, filename)

    try:
        downloaded_file = download_file(url, output_folder)
        downloaded_files.append(downloaded_file)
    except Exception as e:
        print("Error downloading file, Probable holiday:", filename)
        print(e)

for file in downloaded_files:
    try:
        extract_files(file, output_folder)
    except Exception as e:
        print("Error extracting file:", file)
        print(e)

for file in downloaded_files:
    os.remove(file)
    print("Removed:", file)

#______________________________


# List all the files in the directory
files = os.listdir(output_folder)

# Create an empty list to store the renamed file names
renamed_files = []

# Iterate over each file
for file in files:
    # Check if the file name ends with 'bhav.csv'
    if file.endswith("bhav.csv"):
        # Extract the date from the file name
        date = file[2:11]  # Assuming the date is always at the same position

        # Generate the new file name
        new_name = date + ".csv"

        # Remove 'cm' and 'bhav' from the file name
        new_name = new_name.replace("fo", "").replace("bhav", "")

        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date, "%d%b%Y")

        # Generate the new file name with the desired format
        new_name = date_obj.strftime("%Y-%m-%d") + "-NSE-FO.csv"

        # Construct the full file paths
        old_path = os.path.join(output_folder, file)
        new_path = os.path.join(output_folder, new_name)

        # Rename the file
        os.rename(old_path, new_path)

        # Add the renamed file name to the list
        renamed_files.append(new_name)
    else:
        # Print a message for files that do not meet the desired condition
        print(f"File '{file}' does not end with 'bhav.csv' and was not renamed.")

# Check if any files were renamed
if renamed_files:
    # Print the list of renamed files
    for renamed_file in renamed_files:
        print("File rename to:",renamed_file)
else:
    # Print a message if no files were found or met the desired condition
    print("No files found or no files meet the desired condition.")

#___________________________________________________________________________



# List all the files in the directory
files = os.listdir(output_folder)

# Iterate over each file
for file in files:
    # Check if the file has the desired format
    if file.endswith("-NSE-FO.csv"):
        # Construct the file path
        file_path = os.path.join(output_folder, file)

        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Group the data by SYMBOL
        grouped = df.groupby('SYMBOL')

        # Sort the data within each group by EXPIRY_DT in ascending order
        df['SYMBOL_NEW'] = grouped['EXPIRY_DT'].transform(lambda x: x.factorize()[0] + 1)

        # Apply the renaming
        df['SYMBOL_NEW'] = df.apply(lambda row: f"{row['SYMBOL']}-{row['SYMBOL_NEW']}", axis=1)

    	# Filter rows based on SERIES column
        df = df[df['INSTRUMENT'].isin(['FUTIDX','FUTSTK'])]
        
        # Remove the specified columns
        columns_to_remove = ['EXPIRY_DT',
                             'SYMBOL',
                             'STRIKE_PR',
                             'OPTION_TYP',
                             'INSTRUMENT',
                             'SETTLE_PR',
                             'VAL_INLAKH',
                             'OPEN_INT',
                             'CHG_IN_OI'
                             ]
        df = df.drop(columns=columns_to_remove)

        df.rename(columns={'SYMBOL_NEW': 'SYMBOL', 'CONTRACTS': 'VOLUME'}, inplace=True)             
               
        # Convert the TIMESTAMP column to the desired format
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%d-%b-%Y').dt.strftime('%Y%m%d')             
        
        # Reorder the columns
        cols = df.columns.tolist()
        cols.remove('TIMESTAMP')
        cols.insert(cols.index('OPEN'), 'TIMESTAMP')
        cols.remove('SYMBOL')
        cols.insert(cols.index('TIMESTAMP'), 'SYMBOL')
        df = df[cols]
                            
        # Save the modified dataframe back to CSV
        df.to_csv(file_path, index=False,header=False)


#___________________________________________________________

# Create folder if not present
save_fo_eod = "C:/NSE_EOD_FO"
if not os.path.exists(save_fo_eod):
    os.makedirs(save_fo_eod)
    print(f"Created folder: {save_fo_eod}")

# Change extension from .csv to .txt
for filename in os.listdir(output_folder):
    if filename.endswith("-NSE-FO.csv"):
        new_filename = os.path.splitext(filename)[0] + ".txt"
        old_filepath = os.path.join(output_folder, filename)
        new_filepath = os.path.join(output_folder, new_filename)
        os.rename(old_filepath, new_filepath)
        #print(f"Changed extension: {filename} -> {new_filename}")

# Copy files to destination folder
for filename in os.listdir(output_folder):
    if filename.endswith("-NSE-FO.txt"):
        source_filepath = os.path.join(output_folder, filename)
        destination_filepath = os.path.join(save_fo_eod, filename)
        shutil.copy2(source_filepath, destination_filepath)
        print(f"Copied file: {filename} -> {save_fo_eod}")

# Remove source folders
shutil.rmtree("C:/data_fo")

#print("Removed folders: C:/data_fo")
print()
print("All NSE_fo-bhavcopy are saved to 'C:/NSE_EOD_FO'.")
print()
print("If you find my work valuable, please consider donating.")
print()
print("💲 Donate via UPI: p.paresh25@oksbi")
