#!/usr/bin/python
import cgi
import mysql.connector

def main():
    # First line, *first character*, must have header
    # "Content-Type: text/html" followed by blank line
    print "Content-Type: text/html"
    print

    # You can copy and paste html code from Dreamweaver
    print '''
            <TITLE>DB Testing</TITLE>
            <H1>This is the new mysql script glycomeDB Added mysql import</H1>
    '''
    print '<h2>trying to connect - should close</h2>'
    try:
        cnx = mysql.connector.connect(user='andybaay_general',
                                      password='ineedglycans',
                                      database='andybaay_glycomeDB',
                                      host='206.221.178.138')
        cnx.connect()
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

if __name__ == "__main__":
    main()