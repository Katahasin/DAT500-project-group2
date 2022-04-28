# DAT500-project-group6


## To-do to run project as is

1. Run get-data.sh which will download and place warc files inside the crawl-data folder.

2. Move all files to the first directory level of crawl-data.

4. Run the script run-all.sh

### To make scripts run

1. run chmod r+x "script-name.sh"
2. run "./script-name.sh"

### run-all.sh explanation

./payload-packetization.sh;
./pre-processing.sh;
./labelling.sh;
./LSH.sh;

1. Breaks up large warc files into smaller distributable equal size packets

2. Cleans raw data into usable data objects

3. Parses and detects data to flag for negative content and updates data objects with calculated scores

4. Runs locality sensitive hashing on small batches to locate similarity accross sites

### To install modules on all nodes
1. run setup-folder-permissions.sh

## To-do to customize project

1. get-data.sh: Pick the warc file slices from the month/year you want and paste the file name inside the script. This will download all the data you want to your local main node (namenode). They will be placed inside the crawl-data folder. The files can be found here: https://commoncrawl.org/the-data/get-started/

2. Move all files to the first directory level of crawl-data.

3. This must be done for the LSH script. Add your files to the packetization queue in payload-packetization.sh

4. Run the script run-all.sh





