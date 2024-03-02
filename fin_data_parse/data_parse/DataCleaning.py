from pymysql.converters import escape_string
from lib.Db_sql import Db


'''获取可能需要清理的entity和relation'''
def clean1():
    db = Db("FinancialDate")
    results = db.select("SELECT id,entity FROM entity WHERE imgUrl='' and relatedType='' and abstract = ''")
    print(len(results))
    res = {}
    insert_datas = []
    # results=[(id,entity),]
    for entity in results:
        id_S = db.select("SELECT count(*) FROM relation WHERE id_S='%s'", escape_string(str(entity[0])))
        id_O = db.select("SELECT count(*) FROM relation WHERE id_O='%s'", escape_string(str(entity[0])))
        # res[entity[0]]=[entity[1],id_S[0][0],id_O[0][0]]
        insert_datas.append((str(entity[0]), escape_string(str(entity[1])), str(id_S[0][0]), str(id_O[0][0])))

    db = Db("FinancialDate")
    db.insert_ignore('insert ignore into NeedClean (id,entity, idS_num, idO_num) values (%s, %s, %s, %s);',insert_datas)

'''获取需要清理的entity'''
def clean2():
    db = Db("FinancialDate")
    results = db.select("SELECT id FROM NeedClean WHERE idS_num<4 and idO_num<9;")
    # print(results)
    entity_del=[]
    relation_del=[]
    for id in results:
        entity_del.append((str(id[0])))
        # relation_del.append((str(id[0]),str(id[0])))
    # print(relation_del)
    # db.insert_ignore("SELECT * FROM entity WHERE id = '%s';",entity_del)
    # print("entity删选成功")

    db.insert_ignore("DELETE FROM relation WHERE id_S = %s ;", entity_del)
    db.insert_ignore("DELETE FROM relation WHERE id_O = %s ;", entity_del)
    print("relation删选成功")


if __name__ == '__main__':
    # clean1()
    clean2()
