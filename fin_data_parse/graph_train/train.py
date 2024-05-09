from pathlib import Path

import torch
from torch.nn import BCEWithLogitsLoss
from torch_geometric.data import Data
from torch.optim import Adam
from gensim.models import KeyedVectors
import numpy as np
import random

from lib.Db_sql import Db
from lib.GetTrainDate import get_train_data
from graph_train.train_tool import get_x, get_node_pairs, save_model

# 检查CUDA是否可用
from graph_train.module import ModifiedGCN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


def train(data, node_pairs_tensor, labels_tensor):
    model.train()
    optimizer.zero_grad()
    predictions = model(data.x, data.edge_index, node_pairs_tensor)
    loss = criterion(predictions.squeeze(), labels_tensor)
    loss.backward()
    optimizer.step()
    return loss.item()


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

    # 训练模型
    for epoch in range(100):
        loss = train(data, node_pairs_tensor, labels_tensor)
        print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')

    # 保存模型
    model_path = "model32.ckpt"
    save_model(model, model_path)
