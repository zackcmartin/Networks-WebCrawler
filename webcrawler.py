#!/usr/bin/env python3
import argparse
import socket
from html.parser import HTMLParser
import sys
from urllib.parse import urlparse

loginUrl = 'http://fring.ccs.neu.edu/accounts/login/?next=/fakebook/'

csrfValue = None

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        self.getCsrf(tag, attrs)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)
    
    def getCsrf(self, tag, attrs):
        if ('name', 'csrfmiddlewaretoken') in attrs:
            try:
                csrfValue = attrs[2]
                print("csrfValue :", csrfValue)
            except:
                print("Could not find CSRF value")
                sys.exit(1)

parser = MyHTMLParser()

# Function to login to fakebook
def loginToFakebook(args):
    #setup the two params given
    username = args.username
    password = args.password
    
    # get host and path
    loginUrlParts = urlparse(loginUrl)
    host = loginUrlParts.netloc
    path = loginUrlParts.path
    
    # connect to socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, 80))
    except socket.error:
        print("Something went wrong with connecting. Double check that your url is accurate")
        sys.exit(1)
    print(loginUrlParts)
    
    request = ("GET " + path + " HTTP/1.1\r\nHOST: " + host + "\r\n\r\n")
    s.sendall(request.encode(encoding='UTF-8'))
    serverResponse = getServerMessage(s)
    parser.feed(serverResponse)
    # responseLines = serverResponse.splitlines()
    
    # print(responseLines)
    
# Gets the response from the server
def getServerMessage(s):
    finalResponse = ''
    while True:
        partOfResponse = s.recv(8192).decode('ascii')
        if len(partOfResponse) == 0:
            break
        finalResponse += partOfResponse
        # looks for if the string contains the "\n" 
        
    return finalResponse
    
# parses the input recieved
def parseInput():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    # tries to parse the arguments
    try:
        args = parser.parse_args()
    except:
        print("Malformed input")
        sys.exit(1)
        
    loginToFakebook(args)

# main function
def main():
    parseInput()

if __name__ == "__main__":
    main()