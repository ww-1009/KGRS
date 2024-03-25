from app.models import FdEntity, FdRelation
from django.db.models import Q


def get_entity_info(entity_name):
	fd_entity = FdEntity.objects.get(entity=entity_name)
	fd_entity_data = {'id': fd_entity.id, 'entity': fd_entity.entity,
					  'img_url': fd_entity.imgurl, 'relatedType': fd_entity.relatedtype,
					  'abstract': fd_entity.abstract}
	return fd_entity_data



def get_fd_graph(data):
	entity_relation = []
	entity_node = []
	node_map = {}
	node_id_map = {}  # 映射节点id
	inputstr = data['inputstr']

	fd_entity_data = get_entity_info(inputstr)
	key_entity_name = fd_entity_data['entity']
	key_entity_id = fd_entity_data['id']
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
	# entity_node.append({"name": fd_relation_data["s"], "category": 1, "id": fd_relation_data["id_s"]})
	# entity_node.append({"name": fd_relation_data["o"], "category": 1, "id": fd_relation_data["id_o"]})
	# fd_reelation_json = serialize("json", fd_relation) # 转化为json对象
	node_map[key_entity_id] = {"name": key_entity_name, "category": 0, "id": 0}  # 添加首节点
	for value in node_map.values():
		entity_node.append(value)

	return entity_node, entity_relation
