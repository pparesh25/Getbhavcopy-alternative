If you are using this script after 16-06-2023 to download data, this guide is not for you, just use and enjoy 

However, if you downloaded data using this script before 16-06-2023 and have a data gap between 04-05-2023 and 16-06-2023 for symbols listed in the "BZ" series, Because i filtered rows in the "SERIES" column based on the values 'EQ' and 'BE' and added 'BZ' on 16/06/2023.

To fill this data gap, I retrieved historical End-of-Day (EOD) data for the companies listed in the 'BZ' series from the BZ folder, up until 16/06/2023, and updated it. use this data to fill that gape 

From that date onwards, a Python script will download the data from the bhavcopy.

