# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:37:55 2024

@author: ppare
"""


import os
import socket
import zipfile
import requests
import pandas as pd
from datetime import datetime, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def Download_BSE_Bhavcopy_File(BSE_Bhavcopy_URL, Bhavcopy_Download_Folder):
    # Download a file from the given URL to the specified output folder
    filename = os.path.basename(BSE_Bhavcopy_URL)
    output_path = os.path.join(Bhavcopy_Download_Folder, filename)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        with requests.get(BSE_Bhavcopy_URL, stream=True, headers=headers, verify=False) as response:
            response.raise_for_status()  # Check if the request was successful
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        
        print(f'Eq-bhavcopy {filename} downloaded.')
        return output_path
    
    except requests.exceptions.RequestException as e:
        print(formatted_date, "Bhavcopy file not available to download on BSE Server"  )
        return None
    
def Extract_BSE_Bhavcopy_Zip_Files(zip_file, Bhavcopy_Download_Folder):
    # Extract files from the given ZIP file to the specified output folder
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(Bhavcopy_Download_Folder)
    print("Zip file extracted:", zip_file)
    
def Rename_BSE_Bhavcopy_Files(directory):
    # Rename files in the specified directory to the desired format
    files = os.listdir(directory)
    renamed_files = []
    for file in files:
        if file.endswith(".CSV"):
            # Extract the date from the file name
            date = file[12:18]
            new_name = date + ".csv"
            new_name = new_name.replace("EQ_ISINCODE_", "")
            date_obj = datetime.strptime(date, "%d%m%y")
            new_name = date_obj.strftime("%Y-%m-%d") + "-BSE-EQ.csv"

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
        
def Modify_BSE_Bhavcopy_Files(directory):
    # Modify the renamed files in the specified directory
    files = os.listdir(directory)
    for file in files:
        if file.endswith("-BSE-EQ.csv"):
            file_path = os.path.join(directory, file)
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Remove the specified columns
                columns_to_remove = [
                                    
                                         #"SC_CODE",
                                         "SC_NAME",
                                         #"SC_GROUP", 
                                         "SC_TYPE", 
                                         #"OPEN",
                                         #"HIGH",
                                         #"LOW", 
                                         #"CLOSE",
                                         "LAST",
                                         "PREVCLOSE",
                                         "NO_TRADES",
                                         #"NO_OF_SHRS",
                                         "NET_TURNOV",
                                         "TDCLOINDI",
                                         "ISIN_CODE",
                                         #"TRADING_DATE"
                                                         ]
	

                                                  
                
                df = df.drop(columns=columns_to_remove)
                """                
                Mutual_Fund_symbol_to_remove = [
                    'SENSEX1', 'SBISENSEX', 'CPSEETF', 'SENSEXBEES', 'SETFBSE100', 'UTISENSETF', 
                    'HDFCSENSEX', 'BSLSENETFG', 'IDFSENSEXE', 'ICICIB22', 'BSE500IETF', 'SETFSN50', 
                    'UTISXN50', 'SNXT50BEES', 'SENSEXADD', 'SENSEXETF', 'SENSEXIETF', 'MOM100', 
                    'NIFTYIETF', 'NIF100IETF', 'NIF100BEES', 'NIFTY1', 'UTINIFTETF', 'LICNETFN50', 
                    'HDFCNIFTY', 'LICNFNHGP', 'NV20IETF', 'MIDSELIETF', 'LOWVOLIETF', 'UTINEXT50', 
                    'NEXT50IETF', 'NIFTYETF', 'ABSLNN50ET', 'BANKIETF', 'PVTBANIETF', 'NIESSPJ', 
                    'NIESSPC', 'NIEHSPI', 'NIESSPE', 'NIEHSPD', 'NIEHSPE', 'NIESSPK', 'NIEHSPG', 
                    'NIEHSPH', 'NIEHSPL', 'NIESSPL', 'NIESSPM', 'ABSLBANETF', 'MIDCAPIETF', 'NEXT50', 
                    '08MPD', '08GPG', '11DPR', '11GPG', '11MPD', '11MPR', '11QPD', '11AGG', '11AMD', 
                    '11DPD', 'ALPL30IETF', 'ITIETF', 'HDFCNIFBAN', 'UTIBANKETF', 'ESG', 'INFRABEES', 
                    'MAFANG', 'HEALTHIETF', 'BFSI', 'FMCGIETF', 'AXISTECETF', 'AXISHCETF', 'AXISCETF', 
                    'MASPTOP50', 'CONSUMIETF', 'EQUAL50ADD', 'MAHKTECH', 'MONQ50', 'MIDQ50ADD', 
                    'NIFTY50ADD', 'AUTOIETF', 'MAKEINDIA', 'MOMOMENTUM', 'TECH', 'HEALTHY', 'BSLNIFTY', 
                    'MIDCAPETF', 'MOLOWVOL', 'MOHEALTH', 'MOM30IETF', 'HDFCNIF100', 'HDFCNEXT50', 
                    'INFRAIETF', 'NIFTYQLITY', 'MOMENTUM', 'MOVALUE', 'MOQUALITY', 'HDFCQUAL', 
                    'HDFCGROWTH', 'HDFCVALUE', 'HDFCLOWVOL', 'HDFCMOMENT', 'HDFCNIFIT', 'HDFCPVTBAN', 
                    'FINIETF', 'COMMOIETF', 'BANKETFADD', 'HDFCBSE500', 'HDFCSML250', 'HDFCMID150', 
                    'PSUBNKIETF', 'AXSENSEX', 'LOWVOL', 'ITETFADD', 'BANKETF', 'PSUBANKADD', 
                    'PVTBANKADD', 'QUAL30IETF', 'NIFMID150', 'NAVINIFTY', 'ITETF', 'ALPHAETF', 
                    'NIFTYBETF', 'BANKBETF', 'NIFITETF', 'HDFCPSUBK', 'LICNMID100', 'SMALLCAP', 
                    'MIDSMALL', 'MID150CASE', 'TOP100CASE', 'BBNPNBETF', 'EVINDIA', 'SBINEQWETF', 
                    'OILIETF', 'ABSLPSE', 'NIFTYBEES', 'JUNIORBEES', 'BANKBEES', 'PSUBANK', 
                    'PSUBNKBEES', 'SHARIABEES', 'QNIFTY', 'MOM50', 'BANKNIFTY1', 'SETFNIFBK', 
                    'SETFNIF50'
                                    ]

                # Filter out rows where 'TckrSymb' is in the list of values to remove
                df = df[~df['SC_CODE'].isin(Mutual_Fund_symbol_to_remove)]
                
                
                # Filter rows based on SERIES column
                df = df[df['SC_GROUP'].isin(['A', 'B', 'M',"MS","MT","P","R","T","W","X","XT","Z","ZP"])]  
                """                
                # Convert the 'TradDt' column to datetime by inferring the format
                df['TRADING_DATE'] = pd.to_datetime(df['TRADING_DATE'], errors='coerce')

                # Check if there are any NaT (Not a Time) values which indicate conversion issues
                if df['TRADING_DATE'].isna().any():
                    print("There are some dates that couldn't be converted:")
                    print(df[df['TRADING_DATE'].isna()])

                # Convert the datetime object to the desired string format
                df['TRADING_DATE'] = df['TRADING_DATE'].dt.strftime('%Y%m%d')              
                               
                # Reorder the columns
                cols = df.columns.tolist()
                cols.remove('TRADING_DATE')
                cols.insert(cols.index('OPEN'), 'TRADING_DATE')
                df = df[cols]
                
                # Remove the SC_GROUP column
                df = df.drop(columns=['SC_GROUP'])
                
            
                # Save the modified dataframe back to CSV
                df.to_csv(file_path, index=False, header=False)

                print(f"{file} :Eq_Bhavcopy Data Structure converted to getbhavcopy")
            except FileNotFoundError:
                print(f"File not found: {file}")
    
def change_file_extension(Bhavcopy_Download_Folder, old_extension, new_extension):
    
    # Iterate through all files in the folder
    for filename in os.listdir(Bhavcopy_Download_Folder):
        # Check if the file ends with the old extension
        if filename.endswith("-BSE-EQ.csv"):
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
        if filename.endswith("-BSE-EQ.txt"):
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
        
 
# Download files
Bhavcopy_Download_Folder = "C:/data_BSE"
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
    
# Final Bhavcopy folder 
Final_Bhavcopy_Folder = "C:/Getbhavcopy_BSE"
if not os.path.exists(Final_Bhavcopy_Folder):
    os.makedirs(Final_Bhavcopy_Folder)
    #print(f"Created folder: {Final_Bhavcopy_Folder}")
    
"""
# Check if the folder exists and contains files
folder_path = "C:\\Getbhavcopy_BSE"
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
        print("The Getbhavcopy_BSE database is up to date today",last_date.date(),"and no need to download any files.")
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
"""    

start_date_str = input('Enter the start date (YYYY-MM-DD): ')
end_date_str = input('Enter the end date (YYYY-MM-DD): ')    

# Convert input dates to datetime objects
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

delta = end_date - start_date
date_range = []
for i in range(delta.days + 1):
    date = start_date + timedelta(days=i)
    if date.weekday() < 5:  # Only include weekdays (Monday-Friday)
        date_range.append(date)

socket.setdefaulttimeout(3)

downloaded_files = []

for date in date_range:
    # Construct the URL for downloading the file
    #https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_140820.zip
    BSE_Bhavcopy_URL = "https://www.bseindia.com/download/BhavCopy/Equity"
    date_str = date.strftime("%d%m%y")
    filename = f"EQ_ISINCODE_{date_str}.zip"
    BSE_Bhavcopy_URL = f"{BSE_Bhavcopy_URL}/{filename}"
    formatted_date = date.strftime('%Y-%m-%d')
    #print("URL:", BSE_Bhavcopy_URL)
    
    try:
        # Download the file and add it to the list of downloaded files
        Downloaded_Bhavcopy_file = Download_BSE_Bhavcopy_File(BSE_Bhavcopy_URL, Bhavcopy_Download_Folder)
        if Downloaded_Bhavcopy_file:
            downloaded_files.append(Downloaded_Bhavcopy_file)
    except Exception as e:
        print(formatted_date, "Bhavcopy file not available to download on BSE Server")
        print(e)
        
        
for file in downloaded_files:
    try:
        # Extract the downloaded ZIP files
        Extract_BSE_Bhavcopy_Zip_Files(file, Bhavcopy_Download_Folder)
    except Exception as e:
        print("Error extracting file:", file)
        print(e)
        
for file in downloaded_files:
    # Remove the downloaded ZIP files
    os.remove(file)
    print("Removed:", file)
    
      
Rename_BSE_Bhavcopy_Files(Bhavcopy_Download_Folder)

Modify_BSE_Bhavcopy_Files(Bhavcopy_Download_Folder)
change_file_extension(Bhavcopy_Download_Folder, ".csv", ".txt")
remove_folders = ["C:/data_BSE"]
copy_and_remove_files(Bhavcopy_Download_Folder, Final_Bhavcopy_Folder, remove_folders)

print()
print()
print("All Eq-bhavcopy are saved to 'C:/Getbhavcopy_BSE'.")
print()
print()
print("If you find my work valuable, please consider donating.")
print()
print()
print("💲 Donate via UPI: p.paresh25@oksbi")
print()
print()