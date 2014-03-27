#!/usr/bin/python3

##################################################
#
# RateMovie - a command line tool for sorting movies.
# written by Mohsin Tariq (mohsin.tariq10@gmail.com)
#
##################################################

import os
import argparse
import urllib
import urllib2
import xml.etree.ElementTree as ET

DESCRIPTION = ""
SEARCH_URL = "http://www.omdbapi.com/?s={}&r=XML"

def argparsing(parser):
    parser.add_argument("--verbose","-v",action="store_true",help="increase output verbosity", default="false")
    parser.add_argument("moviesdir",help = "directory of movies",type = str)
    return parser

def getresult(url):
    print url
    result = urllib.urlopen(url)
    return result.read()

def dirlist(arg):
    os.chdir(arg.moviesdir)
    allfiles = os.listdir(os.getcwd())
    return filter(lambda file:os.path.isdir(file),allfiles)



def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser = argparsing(parser)
    arg = parser.parse_args()

    directories = dirlist(arg)
    for d in directories:
        webpage = getresult(SEARCH_URL.format(urllib.quote(d)))
        xmlfile = os.getcwd()+"/" + d +"/.xml"
        file = open(xmlfile, 'w+')
        file.write(webpage)
        file.close()
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        if root.attrib["response"]== "True":
            try:
                name = root[0].attrib["imdbRating"] or ""
                os.rename(os.getcwd()+"/" + d ,os.getcwd()+"/" +name+ d)
            except:
                pass
if __name__ == "__main__":
    main()
