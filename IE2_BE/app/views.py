import json

from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from app.models import FdEntity, FdRelation


# Create your views here.


def get_fd_group(request):
	data = json.loads(request.body.decode('utf-8'))
	print(data['inputstr'])
	entity_relation = []
	entity_node = []
	node_map = {}
	try:
		inputstr = data['inputstr']
		fd_entity = FdEntity.objects.get(entity=inputstr)  # 查询指定ID的用户
		fd_entity_data = {'id': fd_entity.id, 'entity': fd_entity.entity,
						  'img_url': fd_entity.imgurl, 'relatedType': fd_entity.relatedtype,
						  'abstract': fd_entity.abstract}
		# entity_node.append({"name": fd_entity.entity, "category": 0, "id": fd_entity.id})

		fd_ralation = FdRelation.objects.filter(Q(id_s=fd_entity.id) | Q(id_o=fd_entity.id))
		fd_relation_datas = fd_ralation.values("id_s", "s", "p", "o", "id_o")
		for fd_relation_data in fd_relation_datas:
			# relation_temp = {"source": fd_relation_data["id_s"], "target": fd_relation_data["id_o"], "category": 0, "value": fd_relation_data["p"], "symbolSize": 10}
			entity_relation.append({"source": fd_relation_data["id_s"], "target": fd_relation_data["id_o"],
									"category": 0, "value": fd_relation_data["p"], "symbolSize": 10})
			node_map[fd_relation_data["id_s"]] = {"name": fd_relation_data["s"], "category": 1, "id": fd_relation_data["id_s"]}
			node_map[fd_relation_data["id_o"]] = {"name": fd_relation_data["o"], "category": 1, "id": fd_relation_data["id_o"]}
			# entity_node.append({"name": fd_relation_data["s"], "category": 1, "id": fd_relation_data["id_s"]})
			# entity_node.append({"name": fd_relation_data["o"], "category": 1, "id": fd_relation_data["id_o"]})
		# fd_reelation_json = serialize("json", fd_relation) # 转化为json对象
		node_map[fd_entity.id] = {"name": fd_entity.entity, "category": 0, "id": fd_entity.id}
		for value in node_map.values():
			entity_node.append(value)
		print(entity_node)
		print(entity_relation)
		# entity_node=[{'name': 'Elon Musk', 'category': 0, 'id': 0}, {'name': 'Bel Air, Los Angeles', 'category': 1, 'id': 1}]
		# entity_relation=[{'source': 0, 'target': 1, 'category': 0, 'value': 'residence', 'symbolSize': 10}]
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "查询inputstr出现异常，具体错误：" + str(e)})

	return JsonResponse({'code': 200, 'entity_node': entity_node, 'entity_relation': entity_relation})
