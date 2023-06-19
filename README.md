# Getbhavcopy-alternative

This Python program is a perfect alternative to the Getbhavcopy software.
It generates the same text file as the one obtained by Getbhavcopy software.
The generated file includes symbol, date, open, high, low, close and volume data arranged in columns and date format matches that of Getbhavcopy software.
Additionally, all NSE index names have been changed to match the names used in Getbhavcopy's old files.
This ensures compatibility with the old database of Amibroker or data import format without requiring any modifications.


Files names
2023-05-19-NSE-EQ.txt<br>
2023-05-18-NSE-EQ.txt<br>
2023-05-17-NSE-EQ.txt<br>


Eq-data

20MICRONS,20230519,83.5,84.9,82.35,83.55,100156<br>
21STCENMGM,20230519,18.0,18.6,18.0,18.5,3918<br>
360ONE,20230519,402.2,407.95,399.15,403.3,349082<br>
3IINFOLTD,20230519,32.05,32.2,31.8,32.05,242770<br>
3MINDIA,20230519,23398.05,24004.0,23340.0,23911.9,2607<br>


Indexes-data
NSENIFTY,20230519,18186.15,18218.1,18060.4,18203.4,260898407<br>
NIFTYJUNIOR,20230519,40453.4,40630.5,40090.25,40546.15,237559580<br>
NSE100,20230519,18034.5,18074.5,17911.7,18060.35,498457987<br>
NIFTY200,20230519,9495.8,9512.1,9425.05,9505.0,957979355<br>
NSE500,20230519,15399.5,15418.8,15278.7,15407.55,1395757427<br>
MIDCAP50,20230519,9199.15,9200.3,9095.05,9176.1,229862132<br>

# For original indexes name

If you want to download bhavcopy with NSE original indexes name use this py script 

>> Getbhavcopy-Eq-with original Indexes name .py 

Use historical eod data from folder

>> NSE index with original name up to 2023-06-19 

If you want to download only indexes with NSE original indexes name use this py script 

>> NSE Index only with orignal index name.py

If you want to download only indexes with old Getbhavcopy indexes name use this py script 

>> NSE index only with old getbhavcopy name .py

# My recommendation

The Getbhavcopy software did not download all indexes.
Use the Index Eod data from the folder "NSE index with the original name up to 2023-06-19" and update the database until 2023-06-19.
Then, execute the Python script named "NSE Index only with original index name.py" to update the data for your required date.
Finally, Use the Python script "Getbhavcopy-Eq-with original Indexes name.py" to regularly update your database.

The benefit of downloading data using the "Getbhavcopy-Eq-with original Indexes name.py" script is that it will automatically add any new indexes introduced by NSE.


