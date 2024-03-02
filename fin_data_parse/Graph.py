#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Graph:
    def __init__(self):
        # nodes={id:{entity:,imgUrl:,relatedType:,abstract:}}
        # relations=[(id_s,s,p,o,id_o),]
        self.nodes={}
        self.relations=[]

        self.nodes_num=0
        self.relations_num=0
