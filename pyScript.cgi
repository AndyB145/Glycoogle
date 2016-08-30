#!/usr/bin/python
import cgi
import cgitb
from requests import request, codes
import mysql.connector

cgitb.enable()


def main():
    # First line, *first character*, must have header
    # "Content-Type: text/html" followed by blank line
    print "Content-Type: text/html"
    print

    # You can copy and paste html code from Dreamweaver
    print '''
        <TITLE>CGI script output</TITLE>
        <H1>This tries to connect to glycomeDB</H1>
    '''
    # All data in html form can be obtained with a class called FieldStorage
    # The object you construct can be indexed like a dictionary
    form = cgi.FieldStorage()
    if "search" not in form:
        print '''
            <h1><span style="color: red;">Nothing in search cgi var!</span></h1>
            Please fill in the name field.
        '''
    else:
        queryStructure = form["search"].value.replace(' ', '\n')
        print "<H3>Here is the Query:</H3><p> %s </p>" % repr(
            queryStructure)

    try:
        # Query the Swiss search tool for the matching ids
        swissResults = Requester(queryStructure)
        print "<H2>Here are the IDs:</H2><p> %s </p>" % swissResults.getIDs()

        # Then get the structure data from AndyBaay's database
        # Connecting to the database
        print '<h3>Trying to connect to AndyBaay\'s Glycome DB cache...</h3>'
        try:
            cnx = mysql.connector.connect(user='andybaay_general',
                                          password='ineedglycans',
                                          database='andybaay_glycomeDB',
                                          host='206.221.178.138')
            cnx.connect()
            print('<h3>Success!</h3>')
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print(
                "<h1>Something is wrong with your user name or password</h1>")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("<h1>Database does not exist</h1>")
            else:
                print(err)
        else:

            cnx.close()

        #print "<p> %s </p>" % swissResults.getIDs()
        print "<p> That is all </p>"
    except Exception,e:
        print "<p> Recieved an error with your search: %s </p>" %e


class BadStructure(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)



class Requester:

    DEFAULT_SEARCH_STRUCT = "RES\n1b:x-dgal-HEX-1:5\n2b:b-dglc-HEX-1:5\n3s:n" \
                       "-acetyl\n4b" \
                  ":b-dgal-HEX-1:5\n5b:a-lgal-HEX-1:5|6:d\nLIN\n1:1o(" \
                  "3+1)2d\n2:2d(2+1)3n\n3:2o(3+1)4d\n4:4o(2+1)5d"
    DEFAULT_BASE_URL = "http://glycoproteome.expasy.org/substructuresearch" \
                    "/service/"

    # Temporary test variables to avoid over-query of the database
    RETURNED_IMAGE = '''data:image/jpg;base64,/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a
HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIy
MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCACGAO4DASIA
AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA
AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3
ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm
p6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA
AwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx
BhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK
U1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3
uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iii
gAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKA
CiiigAooooAKKzdV8QaVopjXUL6OGST/AFcXLSSf7qLlm/AVRt/GugTzpC93LaySEKgvrSa1Dk9A
plRQT7CodSClyt6hY6CiiirAKKKKACiuR1n4neEPD+rz6VqerNBe2+3zYxaTPt3KGHKoR0YHr3qj
/wALm8A/9Bx//AC4/wDjdbRw9aSvGLa9GK6O8org/wDhc3gH/oOP/wCAFx/8brtLC+t9T062v7OT
zLW6iSaF9pG5GAKnB5GQR1qJ0p0/ji16gmmWKKKKgYUUVm6r4g0rRTGuoX0cMkn+ri5aST/dRcs3
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
O5goxyWwF5xgMT2wdeiigAooooAKKKKACiiigAooooAK5vwpPDa+G724uJY4YItT1N5JJGCqii8n
JJJ4AA5zXSVwdlbXc2hWlxbWsl7HZ+I9QuJ7ONkDTqLm6CgByqErI0cnzEY8vI+YAEA7S2v7O82/
ZbuCfdEk48qQNmN87H4/hba2D0ODjpViuX8NaTcadq2oXc2m/Z11HMy4nDm3HmO/kuM8sXmll3Lu
AMjpnbHGX6igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiig
AooooApaxqltomj3mqXjbbe1iaVyOpAHQepPQD1NcF8IvFb61Yajp16kcV/FdS3gROhjnkaQ49dr
s6/Tb61j/GfxF51xaeGLd/lXbd3uPr+6Q/iCx/3V9a8+8P67J4Y8RWWtR7ikDbbhF53wNw49yB8w
91FclTEqFZQ6dT6DB5JPEZdUxX2l8Pmlv/wPNH1HRTIZo7iCOaF1eKRQ6OpyGBGQRT66z58KKKKA
CiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKpavqltomj3mqXjFb
e1iaVyOpAHQepPQD1NXar31hZ6naPaahaQXds+N8NxGJEbByMqQQeQDQB8sXd9darqF1qd8f9LvJ
TNKB0Unoo9lACj2FRV9Kf8IJ4P8A+hU0P/wXQ/8AxNH/AAgng/8A6FTQ/wDwXQ//ABNedLAOTcnL
8P8Agn2VDiyFCnGlCholb4v/ALU5P4N+IvtmhzeH7h83GmYMGerW7H5f++TlfoF9a9MrL07wzoOj
3JudM0TTbGdlKGW2tI4mKkgkZUA44HHtWpXfBNRSbufJ4ipCpVlOEeVN3tvb8goooqjEKKKKACii
igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA
KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/Z'''

    RETURNED_IDS = [16711, 7972, 10769, 32671, 2216, 6169, 3288, 7988, 1346,\
    9363, 3696, 7986, 7987, 32675, 32666, 9090, 12205, 20489, 9089, 18125,\
    19904, 18117, 10829, 32673, 32674, 7899, 20452, 1954, 20775, 3822, 2764,\
    20566, 20567, 2043, 10303, 20625, 14429, 20936, 502, 21391, 5849, 32670,\
    4858, 15649, 9997, 19345, 28531, 10496, 18971, 13514, 21733, 20766, 14070,\
    14452, 19134, 10299, 17827, 21632, 32621, 5689, 7976, 10362, 19052, 12955,\
    3823, 16732, 18675, 1378, 19955, 2044, 32622, 19036, 19038, 20305, 2767,\
    7900, 20468, 8189, 12056, 1273, 1274, 3600, 7896, 7897, 7901, 10492, 2024,
    10300, 14730, 19875, 10307, 32669, 32650, 7980, 13077, 19715, 20120, 22064,\
    8134, 8191, 14727, 13078, 20756, 9112, 8190, 21442, \
    20945, 16475, 1343, 19823, 10382, 10365, 9361, 32667, 32668, 5433, 5434,\
    17781, 10302, 969, 9111, 9103, 9104, 14453, 14454, 19714, 21025, 7983,\
    19100, 20287, 32672, 1010, 9102, 2820, 1389, 21815, 20732, 10828, 32570,\
    32571, 32678, 32572, 32573, 9221, 10144, 7979, 2031, 33, 545, 7890, 9055,\
    21270, 7894, 10384, 14449, 32676, 32677, 9222, 20370, 18392, 21876, 32644,\
    547, 1964, 2018, 9557, 13072, 9097, 14430, 14431, 32665, 32615, 968, 26292,\
    12054, 13516, 33362, 24775, 9362, 1387, 10761, 2119, 19217, 20954, 34,\
    3964, 8582, 19054, 6050, 1297, 20525, 14208, 20467, 10142, 1952, 20208,\
    10304, 10305, 9559, 10306, 2157, 12154, 10493, 20063, 9556, 24766, 3662,\
    9056, 7556, 24800, 10363, 10360, 1009, 982, 19053, 4309, 10367, 20807,\
    14726, 12206, 10301, 9558, 13071, 14426, 20191, 18406, 21047, 4860, 14427,\
    14424, 19807, 19812, 1275, 20363, 32620, 10039, 21389, 1001, 24791, 10768,\
    10364, 2385, 12055, 10143, 10366, 7971, 21261, 10361, 10031, 2204, 1949]


    # Can't have two optional parameters. Probably OK to leave DEFAULT_BASE_URL
    # as a class constant since this shouldn't change from run to run
    def __init__(self, searchStructureInGlycoCt = DEFAULT_SEARCH_STRUCT):
        self.__searchStruct = searchStructureInGlycoCt
        self.__baseUrl = self.DEFAULT_BASE_URL
        self.__img = self.__getSearchedImage__()
        self.__ids = self.__getSimilarStructures__()

    # Getters
    def getIDs(self):
        return self.__ids

    def getImg(self):
        return self.__img


    ''' Takes the local structure stored in glycoCt condensed format and
    generates a POST request to the Expasy server to retreive an image
    version of the search structure'''
    def __getSearchedImage__(self):

        #TEMPORARY FOR TESTING ****************************
        return self.RETURNED_IMAGE

        # Generate the request for an Image of the search structure
        response = request('POST', self.__baseUrl + 'imageGenerator', \
                            json={"glycoCtCode" : self.__searchStruct})
        # Check if we got a good repsponse
        if response.status_code == codes.ok:
            imgURL = 'data:image/jpg;base64,'
            for item in response:
                imgURL += str(item)
            return imgURL
        else:
            raise(BadStructure("Couldn't generate an image from your search "
                               "structure"))

    ''' Takes the local structure stored in glycoCt condensed format and
    generates a POST request to the Expasy server to retrieve all similar
    structures in the database'''
    def __getSimilarStructures__(self):

        # Temporary return- REMOVE LATER**************************
        #return self.RETURNED_IDS

        # Ask the server for structures that are similar to the searchStructure
        response = request('POST', self.__baseUrl + 'substructureSearch',\
                                 json={"glycoCtCode": self.__searchStruct})

        # If we get a good request, proceed to parse the response for the
        # Glycome_DB id numbers
        print '<H2>Here is the response from GLYS3:</H2>'
        if response.status_code == codes.ok:
            print(response.content)
            # Split on the beginning of each url that includes the glycan id num
            # Discard the first item to remove header info from the list
            splitResults = str(response.content).split(
                            '"value" : "http://mzjava.expasy.org/glycan/')[1:]
            ids = []
            for i in range(0,len(splitResults)):
                # Isolate the glycan id and truncate the line based on a
                # closing quotation mark that ends the glycan id number
                splitResults[i] = splitResults[i][:splitResults[i].find('\"')]

                # 'GC' corresponds to results from the Glycome_DB database,
                # which are the only results we are interested in
                if splitResults[i].find("GC") > -1:
                    ids.append(int(splitResults[i][3:])) #chop 'GC_' from id
            return ids
        else:
            raise(BadStructure("Unable to find any mathces or there was an "
                               "error with the query"))

if __name__ == "__main__":
    main()
