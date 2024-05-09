import torch
from torch_geometric.nn import GCNConv
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 链接预测模型
class ModifiedGCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(ModifiedGCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.fc = torch.nn.Linear(2 * hidden_channels, out_channels)  # 假设链接预测为二分类问题

    def forward(self, x, edge_index, node_pairs):
        # 通过GCN层处理图
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.conv2(x, edge_index))
        # 提取节点对的特征
        node_pairs_features = torch.cat([x[node_pairs[:, 0]], x[node_pairs[:, 1]]], dim=-1)
        # 使用全连接层预测节点对之间的链接概率
        out = self.fc(node_pairs_features)
        return out
