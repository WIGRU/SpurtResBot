import unittest
import sys
sys.path.insert(1, 'D:\PROGRAMMERING\Python\SpurtResBot\spurtresbot')

class test(unittest.TestCase):


    def test_search(self):
        print("search")
        import SearchCompetition
        searchWords = ["Mila", "Granskog", "Barkarby", 123, "¤%&1"]

        self.assertTrue(SearchCompetition.search(searchWords[0])["status"])
        self.assertTrue(SearchCompetition.search(searchWords[1])["status"])
        self.assertFalse(SearchCompetition.search(searchWords[2])["status"])
        self.assertFalse(SearchCompetition.search(searchWords[3])["status"])
        self.assertFalse(SearchCompetition.search(searchWords[4])["status"])


    def test_parse(self):
        print("parse")
        import parseXML

        comps = [17220, 21666, 12345]

        self.assertTrue(parseXML.parse(comps[0])["name"] == "Tiomila i Nynäshamn")
        self.assertTrue(parseXML.parse(comps[1])["name"] == "Markdubbeln, medel")
        self.assertTrue(parseXML.parse(comps[2])["name"] == "Motions 5-Dagars")
    
    
    def test_download(self):
        print("download")
        from spurtresbot import downloadResults
        scode = downloadResults.download(17220)
        self.assertTrue(scode == 200)


if __name__ == '__main__':
    unittest.main()
