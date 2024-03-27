import json
import os
import sys

from django.core.serializers import serialize
from django.db.models import Q, Max
from django.http import JsonResponse
from django.shortcuts import render

from app.models import SelfGraphInfo, SelfRelation, SelfEntity
from .fd_graph.get_graph import get_fd_graph
from .self_graph.get_graph import get_group_info, get_self_entity, get_self_relation, get_self_graph

CURRENT_DIR = os.path.dirname(__file__)


# Create your views here.


def get_fd_group(request):
	data = json.loads(request.body.decode('utf-8'))
	print(data['inputstr'])
	try:
		entity_node, entity_relation, entity_info_all, entity_top = get_fd_graph(data)
	except Exception as e:
		print(f'出错了{e}')
		return JsonResponse({'code': 0, 'msg': "查询inputstr出现异常，具体错误：" + str(e)})

	return JsonResponse({'code': 200, 'entity_node': entity_node, 'entity_relation': entity_relation,
						 'entity_info_all': entity_info_all, 'entity_top': entity_top})


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
		graph_info_list = get_group_info(user_id)
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "获取自有图谱信息出现异常，具体错误：" + str(e)})
	return JsonResponse({'code': 200, 'graph_info_list': graph_info_list, 'total': len(graph_info_list)})


def get_self_entity_info(request):
	data = json.loads(request.body.decode('utf-8'))
	graph_id = data["graph_id"]
	print(graph_id)
	try:
		entity_info_list, entity_id_map = get_self_entity(graph_id)
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "获取图谱节点出现异常，具体错误：" + str(e)})
	return JsonResponse({'code': 200, 'entity_info_list': entity_info_list, 'total': len(entity_info_list)})


def get_self_relation_info(request):
	data = json.loads(request.body.decode('utf-8'))
	graph_id = data["graph_id"]
	print(graph_id)
	try:
		relation_info_list = get_self_relation(graph_id)
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "获取图谱节点出现异常，具体错误：" + str(e)})
	return JsonResponse({'code': 200, 'relation_info_list': relation_info_list, 'total': len(relation_info_list)})


def get_self_group(request):
	data = json.loads(request.body.decode('utf-8'))
	graph_id = data["graph_id"]
	print(graph_id)
	try:
		entity_info_list, entity_id_map = get_self_entity(graph_id)
		relation_info_list = get_self_relation(graph_id)
		entity_node, entity_relation, entity_info_all = get_self_graph(entity_info_list, relation_info_list, entity_id_map)
	except Exception as e:
		print(f"出错了{e}")
		return JsonResponse({'code': 0, 'msg': "获取自有图谱出现异常，具体错误：" + str(e)})
	return JsonResponse({'code': 200, 'entity_node': entity_node, 'entity_relation': entity_relation, 'entity_info_all': entity_info_all})


def getnewstop(request):
	try:
		datas = []
		tops = []
		img = []
		file_path = os.path.join(CURRENT_DIR, r'news_top.txt')
		f = open(file_path, "r", encoding="utf-8")
		for i in range(12):
			new = f.readline()
			new = new.split(";")
			tops.append(new)
		for i in range(3):
			img.append(f.readline())
		f.close()
		datas.append(tops)
		# print(tops)
		datas.append(img)
		return JsonResponse({'code': 1, 'data': datas})
	except Exception as e:
		# 如果出现异常，返回
		print(str(e))
		return JsonResponse({'code': 0, 'msg': "top出现异常，具体错误：" + str(e)})
