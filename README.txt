# DSCI510_project (Tao Yang)

To simply run this program (python3 and related packages required):
sqlite3, datetime, bs4, requests, webbrowser, urllib, xlrd, pandas, http.client, sqlalchemy, matplotlib, scipy,
csv, sys
You may want to use pip or conda to install packages that are mentioned above:
(for example, in command line or terminal, type: 'pip install sqlite3')

==========================================================================

Create the data base:
(!!!This step is needed only if you do not have 'TaoProject.db' downloaded.!!!)
If you did not download  'TaoProject.db' file, please run 'createDB.py' in your command-line or terminal:

'python createDB.py'

This will ask you if you downloaded 'F005006_3m.csv' file, and if you did, input 'y' for yes. If you did not 
download the csv file, input 'n' for no, and please move the csv to the directory that is same as the py file. 
Then the data base will be created.

===========================================================================

Printing out the datasets and analysis:
In your command line or terminal, please run:

'python script.py' 
or 
'python script.py --static'

Both of them will ask you if you downloaded 'F005006_3m.csv' file, and if you did, input 'y' for yes. If you 
did not download the csv file, input 'n' for no, and please move the csv to the directory that is same as the py file. 
'python script.py' will print out the whole datasets and analyze from the datasets.
'python script.py --static' will read the data base and analyze from the data base.
Both of them will generate graphs and Pearson correlation coefficient and ask you if you want to do a predict.
While you are doing predicion, simply follow the command line and enter your input.

===========================================================================

Maintainability/extensibility: 
Since my data is time series data, as time goes by, we can collect more data in the future. And we can always
 update the datasets so that the accuracy of our analysis will be higher and higher.

 