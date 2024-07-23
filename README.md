# Getbhavcopy-alternative
This Python program is a perfect alternative to the Getbhavcopy software.
It generates the same text file as the one obtained by Getbhavcopy software.
The generated file includes symbol, date, open, high, low, close and volume data arranged in columns and date format matches that of Getbhavcopy software.
Additionally, all NSE index names have been changed to match the names used in Getbhavcopy's old files.
This ensures compatibility with the old database of Amibroker or data import format without requiring any modifications.

Files names<br>
2023-05-19-NSE-EQ.txt<br>
2023-05-18-NSE-EQ.txt<br>

Eq-data<br>
20MICRONS,20230519,83.5,84.9,82.35,83.55,100156<br>
21STCENMGM,20230519,18.0,18.6,18.0,18.5,3918<br>

Indexes-data<br>
NSENIFTY,20230519,18186.15,18218.1,18060.4,18203.4,260898407<br>
NIFTYJUNIOR,20230519,40453.4,40630.5,40090.25,40546.15,237559580<br>

# Watch this Video
if you dont know how to use py script<br>

https://youtu.be/DmF2Ke0qS-Q

# Getbhavcopy NSE-EQ and indexes

To implement a new format, NSE has discontinued the old link for data download starting from July 8, 2024, and introduced a new format on a new link. Consequently, necessary changes have been made in the code to accommodate this update. A new file named "New-Getbhavcopy-Eq-with original Indexes name.py" has been created to download data after July 8, 2024.

However, the "Getbhavcopy-Eq-with original Indexes name.py" file will continue to be used to download historical data, as data prior to July 8, 2024, remains available through the old link

However, changing the data format or link by NSE does not affect the final Bhavcopy file. Only the method of creating the file has changed, with no impact on the end user.

# Download NSE Futures EOD
Use NSE_EOD_FO.zip for update until 23jul2024<br>
After that use >>> New_nse_fo.py <<< to download data from NSE<br>
To download historical data before 06jul2024 use >>> nse_fo.py <<<  
If you want to retain the 'OPEN_INT' column for open interest data, please comment out line 156 in the nse_fo.py and line 153 in New_nse_fo.py file.

# My recommendation

The Getbhavcopy software did not download all indexes. if you want to download and update all NSE indexes.<br> 
Use the Indexes Eod data from the folder "NSE index with the original name up to 2023-06-19" and update the database until 2023-06-19.
Then use the Python script named "NSE Index only with original index name.py" to update the data for your required date.<br>
Finally Use the Python script "Getbhavcopy-Eq-with original Indexes name.py" to regularly update your database.

The benefit of downloading data using the "Getbhavcopy-Eq-with original Indexes name.py" script is that it will automatically add any new indexes introduced by NSE.

# For indexes 

If you want to download bhavcopy with NSE original indexes name use this py script 

>> Getbhavcopy-Eq-with original Indexes name .py 

If you want to download only indexes with NSE original indexes name use this py script 

>> NSE Index only with orignal index name.py

If you want to download only indexes with old Getbhavcopy indexes name use this py script 

>> NSE index only with old getbhavcopy name .py

# Historical indexes data 

Use historical eod data from folder

>> NSE index with original name up to 2023-06-19

# Weekend

Added Weekend_Getbhavcopy-Eq-with original Indexes name.py file to download data in weekend.<br> 
But my recommendation is to use this to download data only on weekends when the market is open.

# Your generous contribution will help and allow me to allocate more time

If you find my work valuable and want to contribute its growth.

please consider making a donation. 

My UPI ID: p.paresh25@oksbi


