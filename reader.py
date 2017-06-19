import  csv
import ConfigParser


def get_haeader( conf = '.conf'):
    cf = ConfigParser.ConfigParser()
    cf.read(conf)
    return [ item.strip() for item in  cf.get('logfile','header').split(',') ]


    cf = ConfigParser.ConfigParser()
    cf.read(conf)
    return cf.get('logfile','delimiter')[1:-1]


def parse_file(datafile,header):
    with open(datafile,'r') as f:
        reader = csv.reader( f)
        return [ dict(zip(header,row))  for row in reader]

