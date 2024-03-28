from django.utils import timezone
from app.models import SelfGraphInfo, SelfEntity, SelfRelation


def save_group_info(user_id, graph_id, graph_name, description):
    if graph_id == -1:
        graph_id = SelfGraphInfo.objects.count() + 1
    now_time = timezone.now()
    # 尝试获取现有对象或创建新对象
    save_object, created = SelfGraphInfo.objects.get_or_create(graph_id=graph_id,
                                                               defaults={'user_id': user_id, 'graph_name': graph_name,
                                                                         'description': description, 'deleted': 0,
                                                                         'update_time': now_time,
                                                                         'create_time': now_time})
    # 如果对象存在，则更新字段值
    if not created:
        save_object.graph_name = graph_name
        save_object.description = description
        save_object.update_time = now_time
        save_object.save()


def save_self_entity(user_id, graph_id, entity, imgurl, relatedtype, abstract, entity_id):
    if entity_id == -1:
        entity_id = SelfEntity.objects.filter(user_id=user_id, graph_id=graph_id).count()
    print(entity_id)
    relatedtype_string = ";".join(relatedtype)
    now_time = timezone.now()
    # 尝试获取现有对象或创建新对象
    save_object, created = SelfEntity.objects.get_or_create(graph_id=graph_id, entity_id=entity_id,
                                                            defaults={'user_id': user_id, 'entity': entity,
                                                                      'imgurl': imgurl,
                                                                      'relatedtype': relatedtype_string,
                                                                      'abstract': abstract, 'deleted': 0,
                                                                      'update_time': now_time, 'create_time': now_time})
    # 如果对象存在，则更新字段值
    if not created:
        save_object.entity = entity
        save_object.relatedType = relatedtype_string
        save_object.imgurl = imgurl
        save_object.abstract = abstract
        save_object.update_time = now_time
        save_object.save()
