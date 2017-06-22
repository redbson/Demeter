#coding: utf-8
import  csv
import ConfigParser


def get_haeader( conf = '.cfg'):
    '''
    该函数用于从配置文件中读取日志文件配置头。
    :param conf: 配置文件
    :return: .cfg 文件中的解析

    '''

    cf = ConfigParser.ConfigParser()
    cf.read(conf)
    return [ item.strip() for item in  cf.get('logfile','header').split(',') ]

    # cf = ConfigParser.ConfigParser()
    # cf.read(conf)
    # return cf.get('logfile','delimiter')[1:-1]




def parse_file(datafile,header):
    '''
    :param datafile: 日志文件
    :param header: 日志的头信息
    :return: 将日志文件解析程字典
    '''
    with open(datafile,'r') as f:
        reader = csv.reader( f)
        return [ dict(zip(header,row))  for row in reader]



