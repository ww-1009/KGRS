import torch
import torch.nn.functional as F

# 简单推荐逻辑
from graph_train.module import ModifiedGCN

def load_model(model, path):
    model.load_state_dict(torch.load(path))

def recommend(entity_id, model, data):
    with torch.no_grad():
        logits = model(data)
        probabilities = F.softmax(logits, dim=1)
        _, indices = torch.sort(probabilities, descending=True)
        recommended_id = indices[:, 1]  # 假设推荐概率第二高的类别
        return recommended_id[entity_id].item()

def get_related_nodes(model, entity_id):
    # 使用模型预测相关节点id
    prediction = model(entity_id)

    # 返回预测结果
    return prediction

if __name__ == '__main__':
    # # 加载模型
    # model_loaded = ModifiedGCN(input_dim=16, output_dim=1)
    # model_loaded.load_state_dict(torch.load('gcn_model.pth'))
    # model_loaded.eval()
    #
    # # 示例：推荐实体
    # entity_id = 2
    # recommended_id = recommend(entity_id, model_loaded, data)
    # print(f'Recommended entity ID for entity {entity_id}: {recommended_id}')
    model = ModifiedGCN(in_channels=16, hidden_channels=32, out_channels=1)
    # 加载模型
    model_path = "model.ckpt"
    load_model(model, model_path)
    # 输入实体id
    entity_id = 1

    # 获取相关节点id
    related_nodes = get_related_nodes(model, entity_id)

    # 打印相关节点id
    print(related_nodes)