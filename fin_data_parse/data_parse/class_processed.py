import re
import json
from collections import deque
from lib.Db_sql import Db


class TreeNode:
    def __init__(self):
        self.sup = []
        self.sub = []
        self.info = {}  # {root:{"high":1,"deep":0}}


class ClassProcessed:
    def __init__(self, class_sup_map):
        self.class_sup_map = class_sup_map  # [(class,superclass),] 查表得
        self.class_forest = {}  # {class:TreeNode}
        self.root_sub = {}  # {root:subs}root下的所有子类

    def contains_wikicat(self,input_string):
        pattern = r'Wikicat'
        if re.search(pattern, input_string):
            return True
        else:
            return False

    def remove_prefix(self, input_str):
        # 使用一个正则表达式同时匹配三种情况
        # result = re.sub(r'^Wikicat', '', input_str)
        result = re.sub(r'^Yago', '', input_str)
        result = re.sub(r'\d+$', '', result)
        return result

    def getforest(self,re_set=0):
        for i in self.class_sup_map:
            if re_set:
                class_now = self.remove_prefix(i[0])  # 当前类型
                superclass = self.remove_prefix(i[1])  # 父类型
            else:
                class_now = i[0]  # 当前类型
                superclass = i[1]  # 父类型
            if class_now not in self.class_forest.keys():
                self.class_forest[class_now] = TreeNode()
            if superclass not in self.class_forest[class_now].sup:
                self.class_forest[class_now].sup.append(superclass)

            if superclass not in self.class_forest.keys():
                self.class_forest[superclass] = TreeNode()
            if class_now not in self.class_forest[superclass].sub:
                self.class_forest[superclass].sub.append(class_now)

        print(f"类型数为：{len(self.class_forest)}")
        return self.class_forest

    def get_root(self):
        roots = []
        sup_num = 0
        for class_node, node_value in self.class_forest.items():
            if not node_value.sup:
                roots.append(class_node)
                self.root_sub[class_node] = []
            if len(node_value.sup) > 1:
                sup_num += 1
        print(sup_num)
        return roots

    def BFS(self, root):
        queue = []
        queue.append((root, 0))
        while queue:
            # 出队一个节点
            class_node, current_level = queue.pop(0)
            node_value = self.class_forest[class_node]

            # 访问该节点
            self.root_sub[root].append(class_node)
            node_value.info[root] = {"high": 1,
                                     "deep": current_level}

            # 将该节点的子节点入队
            for child_class in node_value.sub:
                queue.append((child_class, current_level + 1))

        return current_level + 1

    def BFS_GRAPH(self, root):
        visited = set()
        queue = deque([(root, 0)])  # 使用元组记录节点和层数
        next_level = 0
        while queue:
            class_node, current_level = queue.popleft()
            if class_node not in self.class_forest:
                continue
            node_value = self.class_forest[class_node]

            if class_node not in visited:
                visited.add(class_node)
                # 判断wikicat
                if self.contains_wikicat(class_node):
                    pres = node_value.sup
                    successors = node_value.sub
                    for pre in pres:
                        self.class_forest[pre].sub.remove(class_node)
                        self.class_forest[pre].sub = list(set(self.class_forest[pre].sub+successors))
                    for suc in successors:
                        self.class_forest[suc].sup.remove(class_node)
                        self.class_forest[suc].sup = list(set(self.class_forest[suc].sup+pres))

                    del self.class_forest[class_node]
                else:
                    self.root_sub[root].append(class_node)
                    node_value.info[root] = {"high": 1,
                                            "deep": current_level}

                    # 将当前顶点的未访问邻居加入队列，并记录层数
                    next_level = current_level + 1
                queue.extend((neighbor, next_level) for neighbor in node_value.sub if
                             neighbor not in visited)

        return current_level + 1

    def set_High(self, root, high):
        for sub in self.root_sub[root]:
            self.class_forest[sub].info[root]["high"] = high

    def save_dump(self, sql, db_name="FinancialDate"):
        print(sql)
        db = Db(db_name)
        datas = []
        for class_name, class_value in self.class_forest.items():
            info = json.dumps(class_value.info)
            sup = ';'.join(class_value.sup)
            sub = ';'.join(class_value.sub)
            datas.append((class_name, sup, sub, info))
        db.insert_ignore(sql, datas)
        print(f"插入表{db_name}成功！")
        db.connect_close()


#  处理类型
if __name__ == '__main__':
    db = Db("dbpedia&&yago")
    results = db.select("SELECT *FROM class_hierarchy_yago_new;")
    db.connect_close()
    cp = ClassProcessed(results)
    # 无正则
    # result = cp.getforest(re_set=0)
    # roots = cp.get_root()
    # for root in roots:
    #     high = cp.BFS(root)
    #     print(f"{root}树高为：{high}")
    #     cp.set_High(root, high)

    # 有正则
    result = cp.getforest(re_set=1)
    roots = cp.get_root()
    # ['PhysicalEntity', 'Literal', 'PermanentlyLocatedEntity', 'Dryad', 'LegalActorGeo']
    for root in roots:
        high = cp.BFS_GRAPH(root)
        print(f"{root}树高为：{high}")
        cp.set_High(root, high)
    print(len(cp.class_forest))
    # 保存入数据库
    cp.save_dump('insert ignore into class_forest_re2 (class_name, sup, sub, info) values (%s, %s, %s, %s);',
                 "FinancialDate")