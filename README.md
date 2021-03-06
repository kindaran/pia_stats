# Extracting Speedtest Stats From a Log File
Both trying out a new VPN provider and then testing my own VPN server, I setup a bash script which calls a command line executable called "speedtest" to log hourly upload/download tests. In order to easily run analysis on those stats, I created a Python script to parse the log file and create a CSV file with date, upload speed, download speed. This can then be charted and/or used to generate averages, etc.

**NOTE: this code represents a specific point in time in my ongoing learning of Python. Certain code usage or patterns don't necessarily represent how I might code today.**

# Components
* bash shell script (actually contained in a separate GIT repository) that creates a start header and a date/time plus runs the speedtest executable all of which are redirected to a log file
* Python script: pia_stats.py to parse the log file and output a CSV file (called "pia" because I originally trialled a VPN provider named Private Internet Access)
* Python script: test_pia_stats.py which does some very basic testing on functions in the main script
* log file: named speedtest.log. For each execution of the bash shell, several lines are generated: 1) a header indicating the start of a run plus a date/time and 2) the output from the speedtest executable
* csv file: named speedtest_YYYYMMDDHHMISS.csv with the date/time component generated by a function in the Python script. Contains a header and data rows. Three columns: date (format YYYY-MM-DD HHMI), download_speed, upload_speed

## bash Shell
The bash shell does two things:
1) creates a header that indicates the start of an execution, including a date/time
2) runs the speedtest executable. 

In cron, the script output is redirected to a log file. Since the shell script is not in this repository (I have a separate repository for unix scripts), here it is:

```bash
#!/bin/sh

echo "********************"
echo "*****START TEST*****"
echo "********************"
CURRDATE=$(date +"%Y-%m-%d %H%M")
echo "Date: ${CURRDATE}"
echo
speedtest
```

The format of output in the log, for the data of interest, is "keyword: value" contained on distinct rows. 

## Python Script - Unit Test
Even before creating full code in the main Python script, I created tests in a unit test script. Then, as a test function is created, I filled out a function in the main Python script and then ran the unit test script. So, almost all of the main script functions were tested (to a small degree) prior to putting any code in the main() function.

The way I have evolved my unit testing is to create individual tests that are fully contained - ideally one test does not rely on another and each test creates objects and cleans them up when done. In this instance, I also added some logging to the script and also added try/except (which I havent done in the past).

## Python Script - Main
The main script contains the following major processing steps:
1) read in the complete log file (for now, the reference to the file is hard coded)
2) parse log file looking for specific words to pull out specific rows
3) further transform above rows to pull out the "value" component from the keyword:value rows
4) pivot data from individual rows into rows for the CSV with 3 elements per row
5) dump data, with a header, to a CSV file (having generated a unique file name)

Below, I'll focus a bit more on some of the code in the script.
### Parsing the Log File
* I recognized that all of the data I was interested in was in the format "keyword: string" and isolated on its own line. So it was obvious that I could fairly easily access the data I wanted - it's a matter of scanning through the log file and pulling out specific rows
* I didnt have to create a function that only deals with one keyword at a time, I can pass a list of words as a parameter and the function can compare the word list to a row in the log file

Here is the specific code:

```python
        for row in lines:
            if any(word in row for word in p_wordlist):
                data.append(row)
        #END FOR
 ```
1) loop through each row in the file
2) use some list comprehension to detect if a word in the list of keywords exists in the current row
3) if so, push that row on to a new list object
### Pivoting From Rows to Columns
The above function essentially generates a 1 dimensional array with sets of 3 rows belonging to an individual speedtest. So, I had to find a way to parse through the single dimension list and convert a set of 3 rows into 1 row with 3 elements. That is done as follows:
```python
        keyValues = []
        for idx,row in enumerate(keyRows):
            splitRow = row.split(":")       ##rows are in the format <keyword>: <value>
            if splitRow[0].strip() != "Date":
                ##these rows are either "Upload" or "Download"
                keyValues.append(float(splitRow[1].split()[0].strip()))
            else:
                #this row is "Date"
                keyValues.append(splitRow[1].strip())
            #END IF
            ##every 3 rows from the log file make 1 row of data: date, upload, download
            ##so the above code builds a data row and then it is added to a final csv output row
            if (idx + 1) % 3 == 0:      ##cant use raw idx because 0 mod anything is zero and that causes a problem
                output.append(keyValues)
                keyValues = []
            #END IF
        #END FOR
```
1) one key piece of code is the construction of the for loop: "for idx,row in enumerate(keyRows):". By using enumerate(), a means of counting rows is gained
2) parsing the row: remember that a row is in the format keyword, colon, value. So the first parse is to use .split(":"). In the case of the Date row, the string value at index 1 can be referenced as is. In the case of the download and upload rows, the value component is in the format number, space, unit of measure so those rows need one more split() and then retrieve the value at index 0. Each value is appended to a list object.
3) the final trick is to detect when 3 rows have been processed. That is done with "if (idx + 1) % 3 == 0:". Why "idx + 1"? The enumerate function generates a zero based series. If the code were "idx % 2" the idx at value zero would result in zero and falsely create a true condition. So, it is necessary to add 1 to the idx value. When idx+1 % 3 is true, push the current 3 element list onto a separate list and then reset that first list to empty to start building another set of 3 elements
### Writing Data to CSV
The final processing is fairly simple. I have a well used function to generate a unique file name in the format name_currentdatetime.extension where name and extension are parameters and currentdatetime comes from a datetime function in the format YYYYMMDDHH24MISS. Then a relatively simple function to write data in a list object to a CSV file using csv.writer().
