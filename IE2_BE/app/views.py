import json

from django.http import JsonResponse
from django.shortcuts import render

from app.models import FdEntity


# Create your views here.


def get_fd_group(request):
	data = json.loads(request.body.decode('utf-8'))
	print(data['inputstr'])
	try:

		inputstr = data['inputstr']
		fd_entity = FdEntity.objects.get(entity=inputstr)  # 查询指定ID的用户
		fd_entity_data = {'id': fd_entity.id, 'entity': fd_entity.entity,
						  'img_url': fd_entity.imgurl, 'relatedType': fd_entity.relatedtype,
						  'abstract': fd_entity.abstract}
		print(fd_entity_data)
	except Exception as e:
		return JsonResponse({'code': 0, 'msg': "查询inputstr出现异常，具体错误：" + str(e)})

	return JsonResponse({'code': 200, 'data': fd_entity_data})
