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
    #print("Zip file extracted:", zip_file)


def rename_files(directory):
    # Rename files in the specified directory to the desired format
    files = os.listdir(directory)
    renamed_files = []

    for file in files:
        if file.endswith("bhav.csv"):
            # Extract the date from the file name
            date = file[2:11]
            new_name = date + ".csv"
            new_name = new_name.replace("cm", "").replace("bhav", "")
            date_obj = datetime.strptime(date, "%d%b%Y")
            new_name = date_obj.strftime("%Y-%m-%d") + "-NSE-EQ.csv"

            # Rename the file
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            renamed_files.append((file, new_name))
        else:
            print(f"File '{file}' does not end with 'bhav.csv' and was not renamed.")

    #if renamed_files:
        #for old_name, new_name in renamed_files:
           #print(f"File '{old_name}' renamed to: '{new_name}'")
    #else:
        #print("No files found or no files meet the desired condition.")


# Download and extract files

output_folder = "C:/data"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#start_date = input("Enter the start date (YYYY-MM-DD): ")
#end_date = input("Enter the end date (YYYY-MM-DD): ")

#start = datetime.strptime(start_date, "%Y-%m-%d")
#end = datetime.strptime(end_date, "%Y-%m-%d")

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
    url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}".format(
        date.strftime("%Y"), date.strftime("%b").upper())
    date_str = date.strftime("%d%b%Y").upper()
    filename = "cm{}bhav.csv.zip".format(date_str)
    url = "{}/{}".format(url, filename)

    try:
        # Download the file and add it to the list of downloaded files
        downloaded_file = download_file(url, output_folder)
        downloaded_files.append(downloaded_file)
    except Exception as e:
        print("Error downloading file, Probable holiday:", filename)
        print(e)

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
    #print("Removed:", file)


# Rename and modify files

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
                columns_to_remove = ['LAST', 'PREVCLOSE', 'TOTTRDVAL', 'TOTALTRADES', 'ISIN']
                df = df.drop(columns=columns_to_remove)

                # Filter rows based on SERIES column
                df = df[df['SERIES'].isin(['EQ', 'BE'])]

                # Convert the TIMESTAMP column to the desired format
                df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%d-%b-%Y').dt.strftime('%Y%m%d')

                # Reorder the columns
                cols = df.columns.tolist()
                cols.remove('TIMESTAMP')
                cols.insert(cols.index('OPEN'), 'TIMESTAMP')
                df = df[cols]

                # Remove the SERIES column
                df = df.drop(columns=['SERIES'])

                # Save the modified dataframe back to CSV
                df.to_csv(file_path, index=False, header=False)

                #print(f"{file} : Data Structure converted to getbhavcopy")
            except FileNotFoundError:
                print(f"File not found: {file}")


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

# Define the valid index names
valid_index_names = [
    'Nifty 50', 'Nifty Next 50', 'Nifty Midcap Liquid 15', 'Nifty 100', 'Nifty 200', 'Nifty 500',
    'Nifty Midcap 150', 'Nifty Midcap 50', 'NIFTY Midcap 100', 'NIFTY Smallcap 100', 'NIFTY LargeMidcap 250',
    'Nifty Auto', 'Nifty Bank', 'Nifty Financial Services', 'Nifty FMCG', 'Nifty IT', 'Nifty Media',
    'Nifty Metal', 'Nifty Pharma', 'Nifty Private Bank', 'Nifty PSU Bank', 'Nifty Realty', 'Nifty Commodities',
    'Nifty India Consumption', 'Nifty CPSE', 'Nifty Energy', 'NIFTY100 ESG', 'NIFTY100 Enhanced ESG',
    'Nifty Infrastructure', 'Nifty MNC', 'Nifty PSE', 'NIFTY SME EMERGE', 'Nifty Services Sector',
    'Nifty Shariah 25', 'Nifty50 Shariah', 'Nifty500 Shariah', 'Nifty Aditya Birla Group',
    'Nifty Mahindra Group', 'Nifty Tata Group', 'Nifty Tata Group 25% Cap', 'Nifty100 Liquid 15',
    'NIFTY500 Value 50', 'NIFTY Quality Low-Volatility 30', 'NIFTY Alpha Quality Low-Volatility 30',
    'NIFTY Alpha Quality Value Low-Volatility 30', 'NIFTY50 Equal Weight', 'Nifty100 Equal Weight',
    'Nifty100 Low Volatility 30', 'Nifty50 USD', 'Nifty50 Dividend Points', 'Nifty Dividend Opportunities 50',
    'Nifty Alpha 50', 'Nifty 50 Arbitrage', 'Nifty 50 Futures Index', 'Nifty 50 Futures TR Index',
    'Nifty High Beta 50', 'Nifty Low Volatility 50', 'Nifty50 Value 20', 'Nifty Growth Sectors 15',
    'Nifty50 TR 2x Leverage', 'Nifty50 PR 2x Leverage', 'Nifty50 TR 1x Inverse', 'Nifty50 PR 1x Inverse',
    'Nifty Composite G-sec Index', 'Nifty 4-8 yr G-Sec Index', 'Nifty 8-13 yr G-Sec',
    'Nifty 10 yr Benchmark G-Sec', 'Nifty 10 yr Benchmark G-Sec (Clean Price)', 'Nifty 11-15 yr G-Sec Index',
    'Nifty 15 yr and above G-Sec Index', 'India VIX'
]

# Define the mapping between index names and their corresponding symbols
index_name_mapping = {
    'Nifty 50': 'NSENIFTY',
    'Nifty Next 50': 'NIFTYJUNIOR',
    'Nifty Midcap Liquid 15': 'NIFTYMIDCAPLIQ15',
    'Nifty 100': 'NSE100',
    'Nifty 200': 'NIFTY200',
    'Nifty 500': 'NSE500',
    'Nifty Midcap 150': 'NSEMIDCAP150',
    'Nifty Midcap 50': 'MIDCAP50',
    'NIFTY Midcap 100': 'NSEMIDCAP',
    'NIFTY Smallcap 100': 'NSESMLCAP100',
    'NIFTY LargeMidcap 250': 'NIFTYLARGEMIDCAP250',
    'Nifty Auto': 'NIFTYAUTO',
    'Nifty Bank': 'BANKNIFTY',
    'Nifty Financial Services': 'NIFTYFINSERVICE',
    'Nifty FMCG': 'NIFTYFMGC',
    'Nifty IT': 'NSEIT',
    'Nifty Media': 'NIFTYMEDIA',
    'Nifty Metal': 'NIFTYMETAL',
    'Nifty Pharma': 'NIFTYPHARMA',
    'Nifty Private Bank': 'NIFTYPVTBANK',
    'Nifty PSU Bank': 'NIFTYPSUBANK',
    'Nifty Realty': 'NIFTYREALTY',
    'Nifty Commodities': 'NIFTYCOMMODITIES',
    'Nifty India Consumption': 'NIFTYCONSUMPTION',
    'Nifty CPSE': 'NIFTYCPSE',
    'Nifty Energy': 'NIFTYENERGY',
    'NIFTY100 ESG': 'NIFTY100ESG',
    'NIFTY100 Enhanced ESG': 'NIFTY100ENHESG',
    'Nifty Infrastructure': 'NIFTYINFRA',
    'Nifty MNC': 'NIFTYMNC',
    'Nifty PSE': 'NIFTYPSE',
    'NIFTY SME EMERGE': 'NIFTYSMEEMERGE',
    'Nifty Services Sector': 'NIFTYSERVSECTOR',
    'Nifty Shariah 25': 'NIFTYSHARIAH25',
    'Nifty50 Shariah': 'NIFTY50SHARIAH',
    'Nifty500 Shariah': 'NIFTY500SHARIAH',
    'Nifty Aditya Birla Group': 'NIFTYABGROUP',
    'Nifty Mahindra Group': 'NIFTYMAHINDRA',
    'Nifty Tata Group': 'NIFTYTATA',
    'Nifty Tata Group 25% Cap': 'NIFTYTATA25CAP',
    'Nifty100 Liquid 15': 'NIFTYLIQ15',
    'NIFTY500 Value 50': 'NIFTY500VALUE50',
    'NIFTY Quality Low-Volatility 30': 'NIFTYQUALLOWVOL30',
    'NIFTY Alpha Quality Low-Volatility 30': 'NIFTYALPHAQUALLOWVOL30',
    'NIFTY Alpha Quality Value Low-Volatility 30': 'NIFTYALPHAQUALVALLOWVOL30',
    'NIFTY50 Equal Weight': 'NIFTY50EQUALWEIGHT',
    'Nifty100 Equal Weight': 'NIFTY100EQUALWEIGHT',
    'Nifty100 Low Volatility 30': 'NIFTY100LOWVOL30',
    'Nifty50 USD': 'NSEDEFTY',
    'Nifty50 Dividend Points': 'NIFTY50DIVPOINT',
    'Nifty Dividend Opportunities 50': 'NIFTYDIVOPPS50',
    'Nifty Alpha 50': 'NIFTYALPHA50',
    'Nifty 50 Arbitrage': 'NIFTY50ARBITRAGE',
    'Nifty 50 Futures Index': 'NIFTY50FUTINDEX',
    'Nifty 50 Futures TR Index': 'NIFTY50FUTTRINDEX',
    'Nifty High Beta 50': 'NIFTYHIGHBETA50',
    'Nifty Low Volatility 50': 'NIFTYLOWVOL50',
    'Nifty50 Value 20': 'NIFTY50VALUE20',
    'Nifty Growth Sectors 15': 'NIFTYGROWSECT15',
    'Nifty50 TR 2x Leverage': 'NIFTY50TR2XLEV',
    'Nifty50 PR 2x Leverage': 'NIFTY50PR2XLEV',
    'Nifty50 TR 1x Inverse': 'NIFTY50TR1XINV',
    'Nifty50 PR 1x Inverse': 'NIFTY50PR1XINV',
    'Nifty Composite G-sec Index': 'NIFTY-GS-COMPSITE',
    'Nifty 4-8 yr G-Sec Index': 'NIFTY-GS-4-8YR',
    'Nifty 8-13 yr G-Sec': 'NIFTY-GS-8-13YR',
    'Nifty 10 yr Benchmark G-Sec': 'NIFTY-GS-10YR',
    'Nifty 10 yr Benchmark G-Sec (Clean Price)': 'NIFTY-GS-10YR-CLN',
    'Nifty 11-15 yr G-Sec Index': 'NIFTY-GS-11-15YR',
    'Nifty 15 yr and above G-Sec Index': 'NIFTY-GS-15YRPLUS',
    'India VIX': 'VIX'
}

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

        # Filter the DataFrame to include only valid index names
        df = df[df['Index Name'].isin(valid_index_names)]

        # Replace the index names with their corresponding symbols
        df['Index Name'] = df['Index Name'].replace(index_name_mapping)

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
        #print(f"Downloaded file: {filename} renamed to {new_filename}")

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
        #print(f"Changed extension: {filename} -> {new_filename}")

# Copy files to destination folder
destination_folder = "C:/Get_bhav_copy NSE"
for filename in os.listdir(source_folder):
    if filename.endswith("-NSE-EQ.txt"):
        source_filepath = os.path.join(source_folder, filename)
        destination_filepath = os.path.join(destination_folder, filename)
        shutil.copy2(source_filepath, destination_filepath)
        #print(f"Copied file: {filename} -> {destination_folder}")

# Remove source folders
shutil.rmtree("C:/data")
shutil.rmtree("C:/dataind")
#print("Removed folders: C:/data, C:/dataind")
print()
print("All Eq-bhavcopy with indexes data are saved to 'C:/Get_bhav_copy NSE'.")
print()
print("If you find my work valuable, please consider donating.")
print("💲 Donate via UPI: p.paresh25@oksbi")
