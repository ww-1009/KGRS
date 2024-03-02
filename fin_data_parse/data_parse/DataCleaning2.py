from pymysql.converters import escape_string
from lib.Db_sql import Db

'''获取可能需要清理的entity和relation'''


def get_need_clean_entity(db):
    results = db.select("SELECT id FROM entity WHERE relatedType=''")
    need_clean = [item[0] for item in results]
    print("需要清理的实体数：", len(need_clean))
    return need_clean


def id_map(entity_new_datas, relation_new_datas, extra_entitys_list):
    id_map = {}
    id = 0
    entity_dump = []
    relation_dump = []
    for entity_item in entity_new_datas:
        if entity_item[0] in extra_entitys_list:
            continue
        id_map[entity_item[0]] = id
        entity_item = list(entity_item)
        entity_item[0] = id
        entity_dump.append(tuple(entity_item))
        id += 1

    for relation_item in relation_new_datas:
        relation_item = list(relation_item)
        relation_item[0] = id_map[relation_item[0]]
        relation_item[4] = id_map[relation_item[4]]
        relation_dump.append(tuple(relation_item))
    return entity_dump, relation_dump


if __name__ == '__main__':
    db = Db("FinancialDate")
    need_clean_entity = get_need_clean_entity(db)
    entity_old_datas = db.select("SELECT * FROM entity")
    relation_old_datas = db.select("SELECT * FROM relation")
    db.connect_close()

    entity_new_datas = []
    entity_id_list = []
    for entity_item in entity_old_datas:
        if entity_item[0] in need_clean_entity:
            continue
        entity_id_list.append(entity_item[0])
        entity_new_datas.append(entity_item)
    print("entity_new_datas", len(entity_new_datas))

    relation_new_datas = []
    relation_id_list = []
    for relation_item in relation_old_datas:
        if relation_item[0] in need_clean_entity or relation_item[4] in need_clean_entity:
            continue
        if relation_item[0] not in entity_id_list or relation_item[4] not in entity_id_list:
            continue
        relation_id_list.append(relation_item[0])
        relation_id_list.append(relation_item[4])
        relation_new_datas.append(relation_item)
    relation_id_list = list(set(relation_id_list))

    extra_entitys = set(entity_id_list) - set(relation_id_list)
    extra_entitys_list = list(extra_entitys)
    print("entity多出了:", len(extra_entitys_list))

    entity_dump, relation_dump = id_map(entity_new_datas, relation_new_datas, extra_entitys_list)

    db = Db("FinancialDate")
    db.insert_ignore(
        'insert ignore into entity_copy1 (id, entity, imgUrl, relatedType, abstract) values (%s, %s, %s, %s, %s);',
        entity_dump)
    db.insert_ignore('insert ignore into relation_copy1 (id_S, S, P, O, id_O) values (%s, %s, %s, %s, %s);',
                     relation_dump)
