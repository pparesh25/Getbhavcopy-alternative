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

To implement a new format, NSE has discontinued the old link for data download starting from July 8, 2024, and introduced a new format on a new link. Consequently, necessary changes have been made in the code to accommodate this update. A new file named "New-Getbhavcopy-Eq-with original Indexes name.py" has been created to download data after July 8, 2024.( >>> Final_Bhavcopy_index_2024.py <<< file is added 27/07/2024 and this is a latest version of "New-Getbhavcopy-Eq-with original Indexes name.py" use that file to download data after July 8, 2024."New-Getbhavcopy-Eq-with original Indexes name.py" file is removed. )<br>

However, the "Getbhavcopy-Eq-with original Indexes name.py" file will continue to be used to download historical data, as data prior to July 8, 2024, remains available through the old link

However, changing the data format or link by NSE does not affect the final Bhavcopy file. Only the method of creating the file has changed, with no impact on the end user.

# Rewritten the code from the ground up
 Added >>> Final_Bhavcopy_index_2024.py <<< I've rewritten the code from the ground up, prioritizing clarity, organization, and performance. The revamped solution offers enhanced readability, faster execution, and a more maintainable structure. Renamed the final data folder to 'Getbhavcopy_NSE' and introduced an auto-date selection feature. Now, once a file is downloaded in the "Getbhavcopy_Nse" folder, the script automatically sets the start date from the previously downloaded file name and uses the current date as the end date, simplifying the download process.

# Download NSE Futures EOD

After 06jul2024 use >>> New_nse_fo.py <<< to download data from NSE<br>
To download historical data before 06jul2024 use >>> nse_fo.py <<<  <br>
If you want to retain the 'OPEN_INT' column for open interest data, please comment out line 156 in the nse_fo.py and line 153 in New_nse_fo.py file.<br>

Added py file >>> New_Nse_fo_roman_suffixes.py <<< for symbol name with roman suffixes.<br>
Also added >>> NSE_EOD_FO.zip <<< file for historical fo_eod files with symbol name with roman suffixes to fill gap in database.<br>
Futures Symbols were suffixed by roman figures for Near Month, Next Month & Far Month Expiries. viz. NIFTY-I, NIFTY-II & NIFTY-III.<br>
If you want to retain the 'OPEN_INT' column for open interest data, please comment out line 238.<br>

# Download BSE-Eq EOD Bhavcopy 

Added file >>> Getbhavcopy_BSE_Eq_New.py <<< <br>
Use this file to Download BSE-Eq Eod Bhavcopy after date 01 JUN 2024 <br>
All ETF and mutual fund symbols have been removed. If you need them, you can retrieve them by removing lines 109 to 140 from the code.<br> 

# Download NSE SME EOD Bhavcopy
Added file >>> Getbhavcopy_NSE_SME.py <<<
Use this file to Download NSE SME Eod Bhavcopy

# Your generous contribution will help and allow me to allocate more time

If you find my work valuable and want to contribute its growth.

please consider making a donation. 

My UPI ID: p.paresh25@oksbi


