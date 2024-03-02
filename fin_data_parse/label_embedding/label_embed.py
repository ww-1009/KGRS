import os

# 设置PYTORCH_CUDA_ALLOC_CONF环境变量
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'

import torch
from torch_geometric.data import Data,NeighborSampler
from torch_geometric.nn import GCNConv
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from lib.Db_sql import Db
from sklearn.decomposition import PCA

# 检查CUDA是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

db = Db("FinancialDate")
class_tree = db.select("SELECT class_name,sup FROM class_forest_re2;")
db.connect_close()
print(len(class_tree))

# 创建节点列表和边列表
nodes = set()
edges = []
for child, parent in class_tree:
    nodes.add(child)
    nodes.add(parent)
    edges.append((child, parent))

# 创建节点到索引的映射，以便将节点名称转换为整数索引
node_to_idx = {node: idx for idx, node in enumerate(nodes)}

# 转换边关系为整数索引形式
edges_idx = [(node_to_idx[child], node_to_idx[parent]) for child, parent in edges]

# 创建图数据对象
edge_index = torch.tensor(edges_idx, dtype=torch.long).t().contiguous()
x_original = torch.eye(len(nodes))  # 使用one-hot编码作为节点特征
print(f"x_original:{x_original.size()}")
# 使用PCA减少特征维度
pca = PCA(n_components=0.95)  # 保留95%的方差
x_reduced = pca.fit_transform(x_original)
print(f"x_reduced:{x_reduced.size()}")

data = Data(x=x_reduced, edge_index=edge_index)

# 定义GNN模型
class GNN(torch.nn.Module):
    def __init__(self, num_nodes, hidden_dim, output_dim):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(num_nodes, hidden_dim // 2)
        self.conv2 = GCNConv(hidden_dim // 2, output_dim)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

# 因为这是一个无监督任务，我们可以使用节点重建作为目标，或者使用其他无监督学习方法
# 定义模型、优化器和损失函数
model = GNN(num_nodes=len(nodes), hidden_dim=4, output_dim=data.x.size(1))
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.MSELoss()

model=model.to(device)
data=data.to(device)

# 定义NeighborSampler
train_loader = NeighborSampler(data.edge_index, sizes=[10, 10], batch_size=16, shuffle=True, node_idx=None)
# 定义NeighborSampler
# train_loader = NeighborSampler(data.edge_index, sizes=[-1], batch_size=32, shuffle=True, node_idx=None)
# 训练模型
# def train(data):
#     model.train()
#     optimizer.zero_grad()
#     output = model(data.x, data.edge_index)
#     loss = criterion(output, data.x)  # 尝试重建输入特征
#     loss.backward()
#     optimizer.step()
#     return loss.item()

def train():
    model.train()

    total_loss = 0
    for batch_size, n_id, adjs in train_loader:
        adjs = [adj.to(device) for adj in adjs]
        optimizer.zero_grad()
        batch_x = data.x[n_id].to(device)
        batch_edge_index, _, size = adjs[0]
        output = model(batch_x, batch_edge_index)
        loss = criterion(output[:batch_size], batch_x[:batch_size])  # 只考虑batch内的节点
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(train_loader)

# 执行训练
epochs = 100
for epoch in range(epochs):
    loss = train(data)
    print(f'Epoch {epoch+1}/{epochs}, Loss: {loss:.4f}')


# def save_embeddings(model, data, filename):
#     model.eval()
#     with torch.no_grad():
#         # 确保数据在正确的设备上
#         data = data.to('cpu')
#         embeddings = model(data.x, data.edge_index).detach().cpu().numpy()
#     # 保存嵌入向量到文件
#     print(embeddings)
#     np.save(filename, embeddings)
#
# # 保存嵌入向量
# save_embeddings(model, data, 'embeddings.npy')


def save_embeddings_and_labels(model, data, filename_embeddings, filename_labels):
    model.eval()
    with torch.no_grad():
        embeddings = model(data.x.to(device), data.edge_index.to(device)).detach().cpu().numpy()

    # 将节点索引到类型名称的映射保存为一个列表，确保顺序与嵌入向量一致
    idx_to_label = {v: k for k, v in node_to_idx.items()}
    labels = [idx_to_label[idx] for idx in range(len(nodes))]

    # 保存嵌入向量到文件
    np.save(filename_embeddings, embeddings)
    # 同时保存标签到另一个文件
    np.save(filename_labels, labels)

    print("Embeddings and labels saved.")


# 保存嵌入向量和对应的标签
save_embeddings_and_labels(model, data, 'embeddings.npy', 'labels.npy')