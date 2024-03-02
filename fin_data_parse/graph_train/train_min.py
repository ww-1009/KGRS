from pathlib import Path

import torch
from torch.nn import BCEWithLogitsLoss
from torch_geometric.data import Data
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
from gensim.models import KeyedVectors
import numpy as np
import random
from lib.GetTrainDate import get_train_data

# 检查CUDA是否可用
from graph_train.module import ModifiedGCN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


class NodePairDataset(Dataset):
    def __init__(self, node_pairs_tensor, labels_tensor):
        self.node_pairs_tensor = node_pairs_tensor
        self.labels_tensor = labels_tensor

    def __len__(self):
        return self.node_pairs_tensor.size(0)

    def __getitem__(self, idx):
        return self.node_pairs_tensor[idx], self.labels_tensor[idx]

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
        return np.zeros(model.vector_size)  # 如果没有有效的标签，则返回零向量


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
    print("node_pairs_tensor:",node_pairs_tensor.shape)
    print("labels_tensor:", labels_tensor.shape)
    return node_pairs_tensor, labels_tensor


def get_x(entity_datas, relation_datas):
    # 加载node2vec模型
    node2vec_model_path = Path(__file__).parent.parent.joinpath('label_embedding/node2vec_model16.bin')
    node2vec_model = KeyedVectors.load_word2vec_format(node2vec_model_path, binary=True)
    node_features = []
    for data in entity_datas:
        label_embeddings = get_label_embedding(data['label'], node2vec_model)
        node_features.append(label_embeddings)

    # 将列表转换为张量
    x = torch.tensor(node_features, dtype=torch.float)
    print("x:",x.shape)

    edges = [[data[0], data[2]] for data in relation_datas]  # 根据spo构建边
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    print("edge_index:", edge_index.shape)
    # 创建图数据对象
    data = Data(x=x, edge_index=edge_index).to(device)

    return data


def train(data, batch_node_pairs, batch_labels):
    model.train()
    optimizer.zero_grad()

    # 需要从data.x中索引节点对的特征
    batch_src_node_features = data.x[batch_node_pairs[:, 0]]  # 源节点特征
    batch_dst_node_features = data.x[batch_node_pairs[:, 1]]  # 目标节点特征

    # 将节点特征合并为模型输入
    batch_node_features = torch.cat([batch_src_node_features, batch_dst_node_features], dim=1)

    predictions = model(batch_node_features)
    loss = criterion(predictions.squeeze(), batch_labels)
    loss.backward()
    optimizer.step()
    return loss.item()


if __name__ == '__main__':
    entity_datas, relation_datas = get_train_data()
    # 假设数据
    # entity_datas = [
    #     {'id': 0, 'spo': [0, 'worksAt', 1], 'text': 'Alice is a software engineer at CompanyA.',
    #      'label': ['Abstraction', 'ArtificialLanguage', 'Attribute', 'Code']},
    #     {'id': 1, 'spo': [1, 'worksAt', 2], 'text': 'Bob is a data scientist at CompanyB.',
    #      'label': ['Abstraction', 'ArtificialLanguage', 'Attribute', 'Code']},
    #     {'id': 2, 'spo': [0, 'worksAt', 2], 'text': 'Alice is a software engineer at CompanyA.',
    #      'label': ['Code', 'CodingSystem', 'Communication']},
    #     {'id': 3, 'spo': [3, 'worksAt', 1], 'text': 'Alice is a software engineer at CompanyA.',
    #      'label': ['Code', 'CodingSystem', 'Communication']}
    # ]
    #
    # relation_datas = [(0, 'worksAt', 1), (1, 'worksAt', 2), (0, 'worksAt', 2), (3, 'worksAt', 1)]

    data = get_x(entity_datas, relation_datas)
    node_pairs_tensor, labels_tensor = get_node_pairs(relation_datas, len(entity_datas))
    dataset = NodePairDataset(node_pairs_tensor, labels_tensor)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # 模型和优化器
    model = ModifiedGCN(in_channels=16, hidden_channels=32, out_channels=1).to(device)
    optimizer = Adam(model.parameters(), lr=0.01)
    criterion = BCEWithLogitsLoss()

    # 训练模型
    for epoch in range(100):
        total_loss = 0
        for batch_node_pairs, batch_labels in dataloader:
            batch_loss = train(data,batch_node_pairs.to(device), batch_labels.to(device))
            total_loss += batch_loss
        print(f'Epoch {epoch + 1}, Loss: {total_loss / len(dataloader)}')

    # 保存模型
    torch.save(model.state_dict(), 'gcn_model.pth')
