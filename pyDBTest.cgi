#!/usr/bin/python
import cgitb
import json
import subprocess

cgitb.enable()

def main():
    print "Content-Type: text/html"
    print ""
    print '''
    <TITLE>PHP Tester</TITLE>
    <H1>This tries to connect to glycomeDB and show structure data</H1>
    '''

    proc = subprocess.Popen("php phpTest.php 2 2300 2301", shell=True,
                            stdout=subprocess.PIPE)
    script_response = proc.stdout.read()

    print '<H1> %s </H1>' % (script_response)

    print '<H2>I guess the response was empty</H2>'



if __name__ == "__main__":
    main()


