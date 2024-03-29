from pathlib import Path

import torch
from torch.nn import BCEWithLogitsLoss
from torch_geometric.data import Data
from torch.optim import Adam
from gensim.models import KeyedVectors
import numpy as np
import random
from lib.GetTrainDate import get_train_data

# 检查CUDA是否可用
from graph_train.module import ModifiedGCN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# 函数：获取标签的平均词向量
def get_label_embedding(labels, model):
    embeddings = []
    for label in labels:
        try:
            embedding = model[label]
            embeddings.append(embedding)
        except KeyError:
            continue  # 如果模型中不存在标签，则跳过
    if embeddings:
        return np.mean(embeddings, axis=0)
    else:
        return np.zeros(16)  # 确保这里是16，与node2vec模型的向量维度一致


# 生成节点对和标签张量
def get_node_pairs(relation_datas, num_entities):
    # 创建一个空的字典来存储节点对是否存在关系
    edges_dict = {(item[0], item[2]): 1 for item in relation_datas}
    # 生成负样本，确保它们不在edges_dict中
    while len(edges_dict) < num_entities * 2:  # 假设负样本数量为实体数量的两倍
        u = random.randint(0, num_entities - 1)
        v = random.randint(0, num_entities - 1)
        if u != v and (u, v) not in edges_dict:
            edges_dict[(u, v)] = 0
    # 将edges_dict的键（节点对）和值（存在/不存在关系）分别转换为列表
    node_pairs = list(edges_dict.keys())
    labels = list(edges_dict.values())

    # 转换为张量
    node_pairs_tensor = torch.tensor(node_pairs, dtype=torch.long)  # 节点对
    labels_tensor = torch.tensor(labels, dtype=torch.float)  # 标签
    print("node_pairs_tensor:", node_pairs_tensor.shape)
    print("labels_tensor:", labels_tensor.shape)
    return node_pairs_tensor, labels_tensor


def get_x(entity_datas, relation_datas):
    # 加载node2vec模型
    node2vec_model_path = Path(__file__).parent.parent.joinpath('label_embedding/node2vec_model32.bin')
    node2vec_model = KeyedVectors.load_word2vec_format(node2vec_model_path, binary=True)
    node_features = []
    for data in entity_datas:
        label_embeddings = get_label_embedding(data['label'], node2vec_model)
        node_features.append(label_embeddings)

    # 将列表转换为张量
    x = torch.tensor(node_features, dtype=torch.float)
    print("x:", x.shape)

    edges = [[data[0], data[2]] for data in relation_datas]  # 根据spo构建边
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    print("edge_index:", edge_index.shape)
    # 创建图数据对象
    data = Data(x=x, edge_index=edge_index)

    return data


def train(data, node_pairs_tensor, labels_tensor):
    model.train()
    optimizer.zero_grad()
    predictions = model(data.x, data.edge_index, node_pairs_tensor)
    loss = criterion(predictions.squeeze(), labels_tensor)
    loss.backward()
    optimizer.step()
    return loss.item()


def save_model(model, path):
    torch.save(model.state_dict(), path)


def load_model(model, path):
    model.load_state_dict(torch.load(path))


def get_related_entities(model, entity_id):
    # 将实体id转换为张量
    node_pairs_tensor = torch.tensor([[entity_id, neighbor_id] for neighbor_id in range(len(entity_datas))], dtype=torch.long).to(device)
    # print("entity_id_tensor:", node_pairs_tensor.shape)

    # 使用模型预测相关实体id
    prediction = model(data.x, data.edge_index, node_pairs_tensor)
    # print("prediction:",prediction.shape)

    # 使用循环找到张量中数值最大的5个元素及其值
    values = []
    indices = []
    for i in range(len(prediction)):
        if len(values) < 5:
            values.append(prediction[i])
            indices.append(i)
        else:
            min_value = min(values)
            min_index = values.index(min_value)
            if prediction[i] > min_value:
                values[min_index] = prediction[i]
                indices[min_index] = i

    # 打印值和索引
    for value, index in zip(values, indices):
        print(f"Value: {value}, Index: {index}")

    # 返回预测结果
    return prediction


if __name__ == '__main__':
    entity_datas, relation_datas = get_train_data()

    data = get_x(entity_datas, relation_datas)
    data = data.to(device)

    node_pairs_tensor, labels_tensor = get_node_pairs(relation_datas, len(entity_datas))
    node_pairs_tensor = node_pairs_tensor.to(device)
    labels_tensor = labels_tensor.to(device)

    # 模型和优化器
    model = ModifiedGCN(in_channels=32, hidden_channels=64, out_channels=1).to(device)
    optimizer = Adam(model.parameters(), lr=0.01)
    criterion = BCEWithLogitsLoss()

    # # 训练模型
    # for epoch in range(100):
    #     loss = train(data, node_pairs_tensor, labels_tensor)
    #     print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')
    #
    # # 保存模型
    model_path = "model32.ckpt"
    # save_model(model, model_path)

    # 加载模型
    load_model(model, model_path)

    # 输入实体id
    entity_id = 12578
    # 获取相关实体id
    related_entities = get_related_entities(model, entity_id)

    # # 打印相关实体id
    # print(related_entities)

