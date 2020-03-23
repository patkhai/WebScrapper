import unittest 
from webcrawler import checkURL, searchURL, listURL

class WebCrawlerTestCase(unittest.TestCase): 
    """ Test Case for webcrawler.py """

    def test_validLink(self): 
        self.assertTrue(checkURL("https://www.rescale.com"))
   
    def test_getLinks(self):  
        content = searchURL("https://www.rescale.com")
        self.assertTrue(content)

    def test_listURL(self): 
        self.assertIsNone(listURL("https://www.rescale.com"))
        
if __name__ == '__main__': 
    unittest.main()