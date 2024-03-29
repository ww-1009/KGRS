from app.models import SelfGraphInfo, SelfEntity, SelfRelation


def get_graph_info(user_id):
    graph_info_list = []
    self_group_info = SelfGraphInfo.objects.filter(user_id=user_id, deleted=0)
    self_group_info_datas = self_group_info.values("graph_id", "graph_name", "update_time", "description")
    # print(self_group_info_datas)
    for group_info in self_group_info_datas:
        update = group_info['update_time'].date()
        temp_dic = {'id': group_info['graph_id'], 'update': update,
                    'name': group_info['graph_name'], 'description': group_info['description']}
        graph_info_list.append(temp_dic)

    return graph_info_list


def get_self_entity(graph_id):
    entity_info_list = []
    entity_id_map = {}
    self_entity_info = SelfEntity.objects.filter(graph_id=graph_id, deleted=0)
    self_entity_info_datas = self_entity_info.values("entity_id", "entity", "imgurl", "relatedtype", "abstract")
    for entity_info in self_entity_info_datas:
        entity_id_map[entity_info["entity_id"]] = len(entity_id_map)
        relatedtype_list = entity_info['relatedtype'].split(";")
        temp_dic = {"entity_id": entity_info["entity_id"], "id": len(entity_id_map), "entity": entity_info["entity"],
                    "img_url": entity_info["imgurl"], 'relatedType': relatedtype_list,
                    'abstract': entity_info["abstract"]}
        entity_info_list.append(temp_dic)
    return entity_info_list, entity_id_map


def get_self_relation(graph_id):
    relation_info_list = []
    self_relation_info = SelfRelation.objects.filter(graph_id=graph_id, deleted=0)
    self_relation_info_datas = self_relation_info.values("relation_id", "id_s", "s", "p", "o", "id_o")
    for relation_info in self_relation_info_datas:
        temp_dic = {'id': relation_info['relation_id'], 'id_s': relation_info["id_s"], 's': relation_info['s'],
                    'p': relation_info['p'], 'o': relation_info['o'], 'id_o': relation_info['id_o']}
        relation_info_list.append(temp_dic)

    return relation_info_list


def build_self_graph(entity_info_list, relation_info_list, entity_id_map):
    entity_node = []
    entity_relation = []
    entity_info_all = {}
    for entity_info in entity_info_list:
        entity_info_all[entity_info["id"]] = entity_info
        entity_node.append({"name": entity_info["entity"], "category": 1, "id": entity_info["id"]})

    for relation_info in relation_info_list:
        entity_relation.append({"source": entity_id_map[relation_info["id_s"]],
                                "target": entity_id_map[relation_info["id_o"]],
                                "category": 0, "value": relation_info['p'],
                                "symbolSize": 10})
    return entity_node, entity_relation, entity_info_all
