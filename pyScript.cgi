#!/usr/bin/python
import cgi
import cgitb
from requests import request, codes
import mysql.connector
from RankStructures import orderStructures;
from PageBuilder import PageBuilder;

cgitb.enable()


def main():
    # First line, *first character*, must have header
    # "Content-Type: text/html" followed by blank line
    print "Content-Type: text/html"
    print

    # You can copy and paste html code from Dreamweaver
    #print '''
    #    <TITLE>CGI script output</TITLE>
    #    <H1>This tries to connect to glycomeDB</H1>
    #'''
    # All data in html form can be obtained with a class called FieldStorage
    # The object you construct can be indexed like a dictionary
    form = cgi.FieldStorage()
    if "search" not in form:
        print '''
            <h1><span style="color: red;">Nothing in search cgi
         var!</span></h1>
            Please fill in the name field.
        '''
    else:
        queryStructure = form["search"].value.replace(' ', '\n')
        #print "<H3>Here is the Query:</H3><p> %s </p>" % repr(
         #   queryStructure)

    try:
        # Query the Swiss search tool for the matching ids
        swissResults = Requester(queryStructure)
        ids = swissResults.getIDs()
        #print "<H2>Here are the IDs:</H2><p> %s </p>" % str(ids)

        # Then get the structure data from AndyBaay's database
        # Connecting to the database
        #print '<h3>Trying to connect to AndyBaay\'s Glycome DB cache...</h3>'
        try:
            cnx = mysql.connector.connect(user='andybaay_general',
                                          password='ineedglycans',
                                          database='andybaay_glycomeDB',
                                          host='206.221.178.138')
            cnx.connect()
            #print('<h3>Connected!</h3>')
            #print "<h3>Sending this to GlycomeDB for structure data:</h3><p> " \
            #      "%s </p>" % formatedIDList(ids)
            cursor = cnx.cursor()
            query = ("SELECT * FROM structure WHERE structure_id in %s" % \
                     formatedIDList(ids))
            cursor.execute(query)
            glycoCTDictionary = {}
            for (id, glycoCT) in cursor:
                glycoCTDictionary[id] = glycoCT
            #print "<h3>Response:</h3><p> " \
            #      "%s </p>" % repr(glycoCTDictionary)
            orderedIds, scores = orderStructures(queryStructure,
                                               glycoCTDictionary)
            #print "<h3>Ordered IDs:</h3><p> " \
            #      "%s </p>" % repr(orderedIds)
            #print "<h3>Score Dictionary: </h3><p> " \
            #      "%s </p>" % repr(scores)
            #print "<h3>Image: </h3><img src= \"" \
            #      "%s\">" % swissResults.getImg()
            #print "<h3>Building the page now</h3>"
            webpage = PageBuilder(orderedIds)
            resultPage = webpage.getHTML()
            for line in resultPage:
                print line
            print  # to end the CGI response headers.
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

        print "<p> That is all </p>"
    except Exception,e:
        print "<p> Recieved an error with your search: %s </p>" %e

'''Takes the list of IDs and returns a string representation but with
parenthesis instead of brakcets
'''
def formatedIDList(listOfIds):
    return '(' + str(listOfIds)[1:-1] + ')'

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

        # Ask the server for structures that are similar to the searchStructure
        response = request('POST', self.__baseUrl + 'substructureSearch',\
                                 json={"glycoCtCode": self.__searchStruct})

        # If we get a good request, proceed to parse the response for the
        # Glycome_DB id numbers
        #print '<H2>Here is the response from GLYS3:</H2>'
        if response.status_code == codes.ok:
            #print(response.content)
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
