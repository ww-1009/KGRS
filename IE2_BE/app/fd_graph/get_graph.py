import re

from app.models import FdEntity, FdRelation, FdTop5
from django.db.models import Q


def get_entity_info(entity_name):
	fd_entity = FdEntity.objects.get(entity=entity_name)
	fd_entity_data = {'id': fd_entity.id, 'entity': fd_entity.entity,
					  'img_url': fd_entity.imgurl, 'relatedType': fd_entity.relatedtype,
					  'abstract': fd_entity.abstract}
	return fd_entity_data


def get_relation_top(entity_id):
	fd_entity_top = FdTop5.objects.get(id=entity_id)
	top_dic = {fd_entity_top.top1_id: fd_entity_top.value1,
			   fd_entity_top.top2_id: fd_entity_top.value2,
			   fd_entity_top.top3_id: fd_entity_top.value3,
			   fd_entity_top.top4_id: fd_entity_top.value4,
			   fd_entity_top.top5_id: fd_entity_top.value5}
	entity_top = {}
	for key, value in top_dic.items():
		if key == -1:
			break
		fd_entity = FdEntity.objects.get(id=key)
		entity_top[fd_entity.entity] = value
	return entity_top


def get_fd_graph(data):
	entity_relation = []
	entity_node = []
	node_map = {}
	node_id_map = {}  # 映射节点id
	inputstr = data['inputstr']

	fd_entity_data = get_entity_info(inputstr)
	key_entity_name = fd_entity_data['entity']
	key_entity_id = fd_entity_data['id']

	entity_top = get_relation_top(key_entity_id)

	node_id_map[key_entity_id] = 0  # 将首节点id映射为0
	node_map[key_entity_id] = {"name": key_entity_name, "category": 0, "id": 0}  # 添加首节点
	fd_ralation = FdRelation.objects.filter(Q(id_s=key_entity_id) | Q(id_o=key_entity_id))
	fd_relation_datas = fd_ralation.values("id_s", "s", "p", "o", "id_o")
	for fd_relation_data in fd_relation_datas:
		if fd_relation_data["id_s"] not in node_id_map:
			node_id_map[fd_relation_data["id_s"]] = len(node_id_map)
		if fd_relation_data["id_o"] not in node_id_map:
			node_id_map[fd_relation_data["id_o"]] = len(node_id_map)
		# relation_temp = {"source": fd_relation_data["id_s"], "target": fd_relation_data["id_o"], "category": 0, "value": fd_relation_data["p"], "symbolSize": 10}
		entity_relation.append({"source": node_id_map[fd_relation_data["id_s"]],
								"target": node_id_map[fd_relation_data["id_o"]],
								"category": 0, "value": fd_relation_data["p"], "symbolSize": 10})
		node_map[fd_relation_data["id_s"]] = {"name": fd_relation_data["s"], "category": 1,
											  "id": node_id_map[fd_relation_data["id_s"]]}
		node_map[fd_relation_data["id_o"]] = {"name": fd_relation_data["o"], "category": 1,
											  "id": node_id_map[fd_relation_data["id_o"]]}
	node_map[key_entity_id] = {"name": key_entity_name, "category": 0, "id": 0}  # 添加首节点
	for value in node_map.values():
		entity_node.append(value)

	entity_info_all = {}
	for entity_id, fake_id in node_id_map.items():
		fd_entity = FdEntity.objects.get(id=entity_id)
		relatedtype_list = fd_entity.relatedtype.split(';')
		relatedtype_list.pop()
		relatedtype_list_parsed = []
		for relatedtype in relatedtype_list:
			if len(relatedtype_list_parsed) > 10:
				break
			if re.search(r'^Yago', relatedtype) or re.search(r'^^Wikicat', relatedtype):
				continue
			relatedtype_list_parsed.append(re.sub(r'\d+$', '', relatedtype))

		fd_entity_data = {'id': fake_id, 'entity': fd_entity.entity,
						  'img_url': fd_entity.imgurl, 'relatedType': relatedtype_list_parsed,
						  'abstract': fd_entity.abstract}
		entity_info_all[fake_id] = fd_entity_data

	return entity_node, entity_relation, entity_info_all, entity_top
