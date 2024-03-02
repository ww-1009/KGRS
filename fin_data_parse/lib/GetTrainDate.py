import re
from lib.Db_sql import Db


def contains_wikicat(input_string):
    pattern = r'Wikicat'
    if re.search(pattern, input_string):
        return True
    else:
        return False


def remove_prefix(input_str):
    # 使用一个正则表达式同时匹配三种情况
    result = re.sub(r'^Yago', '', input_str)
    result = re.sub(r'\d+$', '', result)
    return result


def get_train_data():
    db = Db("FinancialDate")
    entity_data = []
    entitys = db.select("SELECT id,entity,relatedType FROM entity_parsed")
    for entity in entitys:
        labels = entity[2].split(';')
        if labels and labels[-1] == '':
            labels.pop()
        label_list = []
        for label in labels:
            if contains_wikicat(label):
                continue
            label_list.append(remove_prefix(label))
        entity_data.append({"id": entity[0], "label": label_list})

    relation_data = db.select("SELECT id_S,P,id_O FROM relation_parsed")

    return entity_data, relation_data
#
#
# if __name__ == '__main__':
#     entity_data, relation_data = get_train_data()
#     print(entity_data[5],entity_data[1],entity_data[2])
#     print(relation_data[0],relation_data[1],relation_data[2])
#     print(len(entity_data))
#     print(len(relation_data))