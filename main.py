# -*- coding:utf-8 -*-

import reader as  rd
import analyst  as aly
import pprint
from pymongo import MongoClient


############################### Read Log ###############################
log = rd.parse_file('access.log', rd.get_haeader())


############################### Analyic Log ###############################
for i,item in enumerate(log):
    url_parser = aly.url_parser(item['http_referer'])
    request_parser = aly.request_parser(item['request'])
    url_parser[1].update(request_parser[2])

    log[i]['parese'] = {
        'data': aly.stand_time(item['time_local'][1:-1]),
        'local': aly.ip(item['remote_addr']),
        'requset_type': request_parser[0],
        'requset_addr': url_parser[0]+request_parser[1],
        'requset_param': url_parser[1],
        'user_agent': aly.user_agent(item['http_user_agent'])[0]
    }


############################### WOrk on DB ###############################
client = MongoClient()
db = client.log
collection = db.log

# clean doc
collection.remove()

# insert doc
map(collection.insert, log)



# query doc
pipeline_requst_type = [{"$group": {"_id": '$parese.requset_type', "count": {"$sum": 1}}},
                        {'$match':{ 'count': {'$gt':1 }}},
                        {'$sort': {"count": -1}} ]
pipeline_user_agent = [{"$group": {"_id": '$parese.user_agent', "count": {"$sum": 1}}}, {'$sort': {"count": -1}} ]

#pipeline_form = [{"$group": {"_id": '$remote_addr', "count": {"$sum": 1}}}, {'$sort': {"count": -1}}]

pipeline_form = [{"$unwind" : "$parese.requset_type"}]

def data_sources(db, pipeline):
    return [doc for doc in db.aggregate(pipeline)]

result1 =  data_sources(collection, pipeline_form)
result2 =  data_sources(collection, pipeline_requst_type)
result3 =  data_sources(collection, pipeline_user_agent)


pprint.pprint(result1)
pprint.pprint(result2)
pprint.pprint(result3)

