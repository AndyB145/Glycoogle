#!/usr/bin/python
import cgi
import cgitb

cgitb.enable()

'''
#Broken python mysql interactor
import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='andybaay_Andy',
                                  password='%~P_hZS#6+9m',
                                  host='206.221.178.138',
                                  database='andybaay_glycomeDB')
    print('<h2>Success Baby!</h2>')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("<h1>Something is wrong with your user name or password</h1>")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("<h1>Database does not exist</h1>")
    else:
        print(err)
else:

    cnx.close()
'''

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
        print "<p>Here is the Query: %s world</p>" % (form["search"].value)

if __name__ == "__main__":
    main()
