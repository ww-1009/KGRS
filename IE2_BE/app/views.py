import json

from django.core.serializers import serialize
from django.db.models import Q, Max
from django.http import JsonResponse
from django.shortcuts import render

from app.models import FdEntity, FdRelation, SelfGraphInfo, SelfRelation, SelfEntity


# Create your views here.


def get_fd_group(request):
	data = json.loads(request.body.decode('utf-8'))
	print(data['inputstr'])
	entity_relation = []
	entity_node = []
	node_map = {}
	try:
		inputstr = data['inputstr']
		fd_entity = FdEntity.objects.get(entity=inputstr)
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
			node_map[fd_relation_data["id_s"]] = {"name": fd_relation_data["s"], "category": 1,
												  "id": fd_relation_data["id_s"]}
			node_map[fd_relation_data["id_o"]] = {"name": fd_relation_data["o"], "category": 1,
												  "id": fd_relation_data["id_o"]}
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


def new_self_graph(request):
	data = json.loads(request.body.decode('utf-8'))
	user_id = data['user_id']
	graph_name = data['graph_name']
	try:
		# 获取number_field字段的最大值
		graph_id_max = SelfGraphInfo.objects.aggregate(Max('graph_id'))['number_field__max']

		if graph_id_max is None:
			graph_id_max = -1  # 如果表为空，可以设置一个默认值
		graph_id = graph_id_max + 1
		new_self_graph_info = SelfGraphInfo(user_id=user_id, graph_name=graph_name, graph_id=graph_id, deleted=0)
		new_self_graph_info.save()
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "查询inputstr出现异常，具体错误：" + str(e)})

	return JsonResponse({'code': 200, 'graph_id': graph_id})


def get_self_group_info(request):
	data = json.loads(request.body.decode('utf-8'))
	user_id = data["user_id"]
	try:
		self_group_info_data = SelfGraphInfo.objects.filter(user_id=user_id, deleted=0)
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "获取自有图谱信息出现异常，具体错误：" + str(e)})
def get_self_group(request):
	data = json.loads(request.body.decode('utf-8'))
	user_id = data["user_id"]
	graph_id = data["graph_id"]
	try:
		self_entity_data = SelfEntity.objects.filter(user_id=user_id, graph_id=graph_id)
		for item in self_entity_data:
			print(item.entity, item.relatedtype, item.abstract)

		self_relation_data = SelfRelation.objects.filter(user_id=user_id, graph_id=graph_id)

	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "获取自有图谱出现异常，具体错误：" + str(e)})
