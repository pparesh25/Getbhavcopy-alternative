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
    url = "https://archives.nseindia.com/content/fo"
    date_str = date.strftime("%Y%m%d").upper()
    filename = "BhavCopy_NSE_FO_0_0_0_{}_F_0000.csv.zip".format(date_str)
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
    if file.endswith("0000.csv"):
        # Extract the date from the file name
        date = file[22:30]  # Assuming the date is always at the same position

        # Generate the new file name
        new_name = date + ".csv"

        # Remove 'cm' and 'bhav' from the file name
        new_name = new_name.replace("BhavCopy_NSE_FO_0_0_0_", "").replace("_F_0000", "")

        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date, "%Y%m%d")

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
        
        # Filter rows based on SERIES column
        df = df[df['FinInstrmTp'].isin(['STF','IDF'])]  
                   
        # Remove the specified columns
        columns_to_remove = ['BizDt',
                             'Sgmt',
                            'Src',
                            'FinInstrmTp',
                            'FinInstrmId',
                            'ISIN',
                            'SctySrs',
                            'FininstrmActlXpryDt',
                            'StrkPric',
                            'OptnTp',
                            'FinInstrmNm',
                            'LastPric',
                            'PrvsClsgPric',
                            'UndrlygPric',
                            'SttlmPric',
                            'OpnIntrst',
                            'ChngInOpnIntrst',
                            'TtlTrfVal',
                            'TtlNbOfTxsExctd',
                            'SsnId',
                            'NewBrdLotQty',
                            'Rmks',
                            'Rsvd1',
                            'Rsvd2',
                            'Rsvd3',
                            'Rsvd4'
                            ]
        df = df.drop(columns=columns_to_remove)
        
        # Sort the DataFrame by the 'TckrSymb' column
        df = df.sort_values(by='TckrSymb')
        
        """
        # Group the data by SYMBOL
        grouped = df.groupby('TckrSymb')
        
        # Sort the data within each group by EXPIRY_DT in ascending order
        df['SYMBOL_NEW'] = grouped['XpryDt'].transform(lambda x: x.factorize()[0] + 1)

        # Apply the renaming
        df['SYMBOL_NEW'] = df.apply(lambda row: f"{row['TckrSymb']}-{row['SYMBOL_NEW']}", axis=1)
        """
        # Convert XpryDt to datetime format
        df['XpryDt'] = pd.to_datetime(df['XpryDt'])

        # Group by TckrSymb
        grouped = df.groupby('TckrSymb')
        # Sort the dataframe by TckrSymb and XpryDt
        df = df.sort_values(by=['TckrSymb', 'XpryDt']).reset_index(drop=True)
        
        # Group by TckrSymb and create a new column with incremental numbering
        df['SYMBOL_NEW'] = df.groupby('TckrSymb').cumcount() + 1
        
        # Apply the renaming to get the desired SYMBOL_NEW format
        df['SYMBOL_NEW'] = df.apply(lambda row: f"{row['TckrSymb']}-{row['SYMBOL_NEW']}", axis=1)
        
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
        cols.remove('SYMBOL_NEW')
        cols.insert(cols.index('TradDt'), 'SYMBOL_NEW')
        df = df[cols]
     
        # Remove the specified columns
        columns_to_remove = ['TckrSymb', 'XpryDt']
        df = df.drop(columns=columns_to_remove)
               
               
        
                            
        # Save the modified dataframe back to CSV
        df.to_csv(file_path, index=False,header=False)
        
#___________________________________________________________________________


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