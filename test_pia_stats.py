import unittest
import logging
import os

import pia_stats as pia


class TestPIA(unittest.TestCase):
    
    def setUp(self):
        try:
            logging.debug("*****RUNNING SETUP")
            self.test_filepath = f"./"
            self.test_filename = "testfile.txt"
            self.test_fq_filename = self.test_filepath + self.test_filename
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in setUp. Error: {msg}")
    #END DEF
    
    def tearDown(self):
        try:
            logging.debug("*****RUNNING TEARDOWN")
            if os.path.isfile(self.test_fq_filename):
                os.remove(self.test_fq_filename)
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in tearDown. Error: {msg}")
    #END DEF
    
    def createTestFile(self,p_data,p_path):

        try:
            logging.info("*****CREATING TEST FILE")
            with open(p_path, 'w') as text_file:
                text_file.write(p_data)
            # END WITH
            return True
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in createTestFile. Error: {msg}")
            return False

    #END DEF
    
    def test_readFile(self):
        try:
            logging.debug("*****TESTING readFile*****")
            self.createTestFile("this is a test",self.test_fq_filename)
            result = pia.readFile(self.test_fq_filename)
            self.assertEqual(len(result),14)
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in test_readFile. Error: {msg}")
    #END DEF
    
    def test_parseFile_singleKeyword(self):
        try:
            logging.debug("*****TESTING parseFile single*****")
            testString = \
                "This is a test string\ntest flag: test"
            self.createTestFile(testString,self.test_fq_filename)
            file = pia.readFile(self.test_fq_filename)
            result = pia.parseText(file,["flag"])
            self.assertEqual(result[0],"test flag: test")
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in test_parseFile_singleKeyword. Error: {msg}")
        
    #END DEF
    
    def test_parseFile_multiKeyword(self):
        try:
            logging.debug("*****TESTING parseFile multi*****")
            testString = \
                "This is a test string\ntest flag: test"
            self.createTestFile(testString,self.test_fq_filename)
            file = pia.readFile(self.test_fq_filename)
            result = pia.parseText(file,["flag","string"])
            self.assertEqual(len(result),2)
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in test_parseFile_singleKeyword. Error: {msg}")
        
    #END DEF    
    
    def test_writeCSV(self):
        try:
            logging.debug("*****TESTING writeCSV*****")
            testData = [["column1","column2"],["data1","data2"]]
            pia.writeCSVFile(self.test_fq_filename,testData)
            result = pia.readFile(self.test_fq_filename)
            self.assertEqual(len(result),36)
        except Exception as e:
            msg = str(e)
            logging.error(f"*****Error in test_writeCSV. Error: {msg}")
    #END DEF
    
#END CLASS

if __name__ == "__main__":
    unittest.main()