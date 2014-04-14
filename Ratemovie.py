#!/usr/bin/python

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
import cmd
import os.path

DESCRIPTION = ""
SEARCH_URL = "http://www.omdbapi.com/?s={}&r=XML"
PATH = ""

class RateMovie(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">>"

    def do_list(self,args):
        """lists all the directories"""
        os.system("ls")

    def do_movies(self,args):
        """lists all the movies"""
        allfiles = os.listdir(PATH)
        movies = filter(lambda file:os.path.isdir(file) and ".xml" in os.listdir(file),allfiles)
        if movies == "":
            print ("Either You Don't have movies or you have not rated the movies. See help")
        else:
            for d in movies:
                print ( d)

    def do_ratings(self,args):
        """lists all the ratings"""
        print("all the ratings here")

    def do_rate(self,args):
        """rates the movies according to imdb ratings"""
        allfiles = os.listdir(PATH)
        directories = filter(lambda file:os.path.isdir(file),allfiles)
        for d in directories:
            webpage = getresult(SEARCH_URL.format(urllib.quote(d)))
            xmlfile = os.curdir + os.sep + d + os.sep + os.extsep +"xml"
            file = open(xmlfile, 'w+')
            file.write(webpage)
            file.close()
            tree = ET.parse(xmlfile)
            root = tree.getroot()
            if root.attrib["response"]== "True":
                try:
                    name = root[0].attrib["imdbRating"] or ""
                    os.rename(os.curdir + os.sep + d ,os.getcwd()+ os.sep +name+ d)
                except:
                    pass

    def do_quit(self,args):
        """quits the program"""
        print("Good Bye !!!")
        return True


def argparsing(parser):
    parser.add_argument("--verbose","-v",action="store_true",help="increase output verbosity", default="false")
    parser.add_argument("moviesdir",help = "directory of movies",type = str)
    return parser

def getresult(url):
    print (url)
    result = urllib.urlopen(url)
    return result.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser = argparsing(parser)
    arg = parser.parse_args()
    PATH = arg.moviesdir
    os.chdir(PATH)
    rm = RateMovie()
    rm.cmdloop()
