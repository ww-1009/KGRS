#!/usr/bin/env python
# -*- coding:utf-8 -*-

import elasticsearch
from Graph import Graph
from lib.Db_sql import Db
def getESDate_all():
    # 创建Elasticsearch客户端
    client = elasticsearch.Elasticsearch(["localhost:9200"])
    # 搜索所有文档
    res = client.search(index="reindex", size=4000,scroll="1m")
    total=res["hits"]['total'] # 数据项数
    G = Graph()
    node_help = {}  # id:entity

    NoType=0
    Nolink = 0
    count=0
    # 遍历搜索结果
    while count<total:
        relations_temp=[]
        nodes_temp = []
        for hit in res["hits"]["hits"]:
            data = hit["_source"]
            count = count + 1
            '''设置relation表数据'''
            try:
                node = data['node']  # 读取查询数据中的node项
                link = data['link']  # 读取查询数据中的link项
                # 映射id和entity
                for value in node.values():
                    for i in value:
                        node_help[int(i[0])] = i[1]
                '''设置relation'''
                for value in link.values():
                    for i in value:
                        i.insert(2, node_help[int(i[2])])
                        i.insert(1, node_help[int(i[0])])
                        relations_temp.append(tuple(i))
            except KeyError:
                Nolink=Nolink+1
                # print(data["id"], data["name"], "无node或link")

            '''设置entity表数据'''
            try:
                relatedType = data['relatedType']
            except KeyError:
                NoType=NoType+1
                # print(data["id"], data["name"], "无type")
                relatedType = None
            G.nodes[int(data["id"])] = dict(entity=data["name"],
                                            imgUrl=data["imgUrl"],
                                            relatedType=relatedType,
                                            abstract=data["abstract"])

            '''将type设置为"type1;type2;type3;"'''
            typeString = ""
            if relatedType != None:
                for type in relatedType:
                    typeString = typeString + type + ";"
            '''将nodes数据格式化为SQl插入格式;格式为[(id, entity, imgUrl, relatedType, abstract),]'''
            temp = tuple([data["id"], data["name"], data["imgUrl"], typeString, data["abstract"]])
            nodes_temp.append(temp)

        relations_temp = list(set(relations_temp))  # 阶段性去重
        G.relations.extend(relations_temp)

        '''分批写入数据库'''
        writeToSql(nodes_temp, relations_temp)

        '''统计个数'''
        print("当前count个数为：", count)
        print("当前Nolink个数为：", Nolink,"当前NoType个数为：", NoType)

        # 获取下一次搜索请求的游标
        scroll_id = res["_scroll_id"]
        # 发送新的搜索请求
        res = client.scroll(scroll_id=scroll_id, scroll="1m")

    G.relations = list(set(G.relations))  # 去重
    G.relations_num = len(G.relations)
    G.nodes_num = len(G.nodes)
    print("G.nodes的个数：", G.nodes_num,"node_help中的个数：", len(node_help))
    print("G.relations的个数：", G.relations_num)
    return G


def writeToSql(entity_data,relations_data):
    db = Db("FinancialDate")
    sql1 = 'insert ignore into relation (id_S,S, P, O,id_O) values (%s, %s, %s, %s, %s);'
    db.insert_ignore(sql1, relations_data)

    sql2 = 'insert ignore into entity (id, entity, imgUrl, relatedType, abstract) values (%s, %s, %s, %s, %s);'
    db.insert_ignore(sql2, entity_data)

    db.connect_close()

if __name__ == '__main__':
    G=getESDate_all()


