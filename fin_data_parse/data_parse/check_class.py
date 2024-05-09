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
    # result = re.sub(r'^Wikicat', '', input_str)
    result = re.sub(r'^Yago', '', input_str)
    result = re.sub(r'\d+$', '', result)
    return result


if __name__ == '__main__':
    class_list = []
    db = Db("FinancialDate")
    results = db.select("SELECT class_name FROM class_forest_re2;")
    for result in results:
        class_list.append(result[0])

    results = db.select("SELECT relatedType FROM entity;")
    db.connect_close()

    no_class = []
    for result in results:
        temp_list = result[0].split(";")
        for relationType in temp_list:
            if contains_wikicat(relationType):
                continue
            relationType = remove_prefix(relationType)
            if relationType not in class_list:
                no_class.append(relationType)
    no_class = list(set(no_class))
    print(len(no_class))
