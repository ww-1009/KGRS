import networkx as nx
from node2vec import Node2Vec
from lib.Db_sql import Db

db = Db("FinancialDate")
class_tree = db.select("SELECT sup,class_name FROM class_forest_re2;")
db.connect_close()
print(len(class_tree))

# 使用DiGraph创建有向图
G = nx.DiGraph()
G.add_edges_from(class_tree)

# 使用Node2Vec训练模型
node2vec = Node2Vec(G, dimensions=16, walk_length=8, num_walks=100, workers=6)
model = node2vec.fit(window=8, min_count=1, batch_words=4)
print("训练完成")

# 保存Node2Vec模型
model.wv.save_word2vec_format("node2vec_model16.bin", binary=True)
# model.save("node2vec.model")
#
# # 保存节点到索引的映射
# import json
#
# node_to_index = {node: idx for idx, node in enumerate(G.nodes())}
# with open("node_to_index.json", "w") as f:
#     json.dump(node_to_index, f)
# print("保存成功")