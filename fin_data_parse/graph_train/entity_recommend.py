import torch
import torch.nn.functional as F

# 简单推荐逻辑
from graph_train.module import ModifiedGCN


def get_related_entities(model, entity_id, related_id_list):
    # 将实体id转换为张量
    node_pairs_tensor = torch.tensor([[entity_id, neighbor_id] for neighbor_id in range(len(entity_datas))],
                                     dtype=torch.long).to(device)
    # print("entity_id_tensor:", node_pairs_tensor.shape)

    # 使用模型预测相关实体id
    prediction = model(data.x, data.edge_index, node_pairs_tensor)
    # print("prediction:",prediction.shape)
    related_prediction_dic = {}
    for related_id in related_id_list:
        # 找到与指定实体ID相关的预测值
        related_prediction_dic[related_id] = prediction[related_id].item()
    # 返回预测结果
    return related_prediction_dic


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

    model_path = "model32.ckpt"
    # 加载模型
    load_model(model, model_path)

    sql_datas = []
    db = Db('FD_dg')
    for entity_id in range(47065):
        relation_id_list = []
        results = db.select("select id_S, id_O from fd_relation where id_S = '%s' or id_O = '%s'", entity_id, entity_id)
        sql_data = [entity_id]
        for item in results:
            relation_id_list.append(item[0])
            relation_id_list.append(item[1])
        relation_id_list = list(set(relation_id_list))
        relation_id_list.remove(entity_id)
        # 获取相关实体id
        related_prediction_dic = get_related_entities(model, entity_id, relation_id_list)
        # 获取前五大
        sorted_items = sorted(related_prediction_dic.items(), key=lambda x: x[1], reverse=True)[:5]
        for key, value in sorted_items:
            sql_data.append(key)
            sql_data.append(value)
        while len(sql_data) < 11:
            sql_data.extend([-1])
        print(sql_data)
        sql_datas.append(tuple(sql_data))

    sql_string = 'insert into fd_top5 (id, top1_id, value1, top2_id, value2,top3_id, value3,top4_id, value4,top5_id, value5) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    db.insert_ignore(sql_string, sql_datas)
