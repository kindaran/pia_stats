import logging

from datetime import datetime
import csv

###############################################################################
###                                 FUNCTIONS                               ###
###############################################################################

def readFile(p_filename):

    try:
        logging.info(f"*****READING FILE {p_filename}")
        with open(p_filename, 'r') as read_file:
            data = read_file.read()
        # END WITH
        return data
    except Exception as e:
        msg = str(e)
        logging.error(f"*****Error in readFile(). Error: {msg}")
        return None
#END DEF

def parseText(p_text,p_wordlist):

    try:
        logging.info("*****PARSING TEXT")
        data = []
        lines = p_text.split("\n")
        for row in lines:
            if any(word in row for word in p_wordlist):
                data.append(row)
        #END FOR
        return data
    except Exception as e:
        msg = str(e)
        logging.error(f"*****Error in parseText(). Error: {msg}")
        return None
#END DEF

def generateOutputFilename(p_filename,p_extension):
    """
        * get current datetime
        * parse the filename param to extract only the filename without pathing and without extension
        * recreate filename as: <base filename> + "_" + <datetime as format YYYYMMDDHHMISS> + ".csv"    

    Args:
        p_filename (string): a filename, possibly including pathing and extension, to start with as a base
        p_extension (string): an extension string value for the target filename. This makes this proc a bit more generic
            to use across different apps. 

    Returns:
        string: the input filename modified
        None: on handled error
    """

    try:
        logging.info("*****GENERATE FILE NAME")
        # strips the raw filename out of file string
        filename = p_filename.split(".")[0].split("/")[-1]
        current_datetime = datetime.strftime(
        datetime.now(), "%Y%m%d%H%M%S")
        output_filename = filename + "_" + current_datetime + "." + p_extension
        logging.debug("Output filename: %s" % (output_filename))
        return output_filename
    except Exception as e:
        msg = str(e)
        logging.error("*****Error in generateOutputFilename. Error: {}".format(msg))
        return None
# END DEF

def writeCSVFile(p_filename, p_rows):

    try:
        logging.info("*****WRITING TO OUTPUT FILE")
        if len(p_rows) > 0:
            output_file = p_filename
            logging.debug('Writing to file: %s' % (output_file))
            with open(output_file, 'w') as hFile:
                writer = csv.writer(hFile,quoting=csv.QUOTE_ALL)
                writer.writerows(p_rows)
            #END WITH
            logging.info('Done writing')
        else:
            logging.warning("WARNING: No data to write***")
        #END IF
        return True
    except Exception as e:
        msg = str(e)
        logging.error(f"*****Error in writeCSVFile. Error:{msg}")
        return False

#END DEF


###############################################################################
###                                 MAIN                                    ###
###############################################################################
    
def main():

    try:
        logging.info("*****PROCESSING LOG FILE")
        ##read log file as text
        file = readFile(f"/home/kindaran/Logs/speedtest.log")
        # file = readFile(f"./speedtest.log")
        assert file != None, "Error retrieving log file"
        
        ##parse text for keywords and pull data
        keyRows = parseText(file,["Date","Download","Upload"])
        assert keyRows != None, "Error parsing log text"
        
        logging.info(f"Found {len(keyRows)} rows with keywords")
        logging.debug(keyRows)

        ##manipulate data for storage
        logging.info("*****GETTING KEY VALUES FROM TEXT")
        header = ["date","download_speed","upload_speed"]   
        output = [header]     
        
        keyValues = []
        for idx,row in enumerate(keyRows):
            splitRow = row.split(":")
            if splitRow[0].strip() != "Date":
                keyValues.append(float(splitRow[1].split()[0].strip()))
            else:
                keyValues.append(splitRow[1].strip())
            #END IF
            if (idx + 1) % 3 == 0:
                output.append(keyValues)
                keyValues = []
        #END FOR
        logging.debug(output)
        logging.info(f"Total rows to write to CSV: {len(output)}")
        
        ##write data to CSV
        outputFilename = generateOutputFilename("speedtest.log","csv")
        assert outputFilename != None, "Error generating target filename"
        
        assert writeCSVFile("/home/kindaran/Logs/" + outputFilename,output), "Error writing CSV file"
        
    except Exception as e:
        msg = str(e)
        logging.error(f"*****Error in main(). Error: {msg}")
        return 
    finally:
	    pass
	
###############################################################################
###                                 CALL MAIN                               ###
###############################################################################

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

if __name__ == '__main__':

    logging.info('*****PROGRAM START')

    main()

    logging.info('*****PROGRAM END')

#END IF