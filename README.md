# 基于金融知识图谱的实体检索系统设计与实现

本系统将Yago和Dbpedia公开数据集进行整合，根据Nasdaq的五百家公司对数据进行抽取并构建金融知识图谱。系统采用Vue-Django-MySQL框架实现可交互式可视化，为用户提供了实体检索，实体信息查看，相关实体推荐，实体相关新闻等功能，使用户更直观的对知识图谱进行探究，从中快速找到有用的信息。

![home-page](https://raw.githubusercontent.com/ww-1009/KGRS/master/img/sys_home_page.png)

## 源码文件

* fin_data_parse 数据处理
* IE2_BE 后端
* IE2_FE 前端

## 系统设计
**系统架构**

![sys-framework](https://raw.githubusercontent.com/ww-1009/KGRS/master/img/sys_framework.png)

**功能设计**

![function-module](https://raw.githubusercontent.com/ww-1009/KGRS/master/img/function_module.png)

## 模型训练
### 三元组数据
本系统基于Yago和Dbpedia数据集，抽取金融相关实体数据，采用三元组对其进行结构化存储。

以纳斯达克500家企业为中心，通过层次遍历获取四层的三元组信息作为本系统的金融相关数据。

由于首次删选数据中会存在大量非重要信息，因此本系统计算了每个实体的入度（in）和出度（out），将 in<3 或 out<3 的节点作为边缘节点进行清洗。

最后从wiki爬取各实体的简介以及图片，进一步丰富数据。

### 特征向量

数据集中包含了个实体的类型数据，其各类型存在继承关系，其形式如下图：

![type-tree](https://raw.githubusercontent.com/ww-1009/KGRS/master/img/type_tree.png)

采用Node2vec算法对类型数据进行词向量构建，能够很好的保留各类型数据之间的层次性。

### 图神经网络

推荐系统主体采用以链接预测为任务的图神经网络框架，模型框架图如下：

![model-structure](https://raw.githubusercontent.com/ww-1009/KGRS/master/img/model_structure.png)

**输入层**接收实体的32维类型词向量作为特征向量和图结构信息。

**隐含层**由两个图卷积层 (GCN) 组成，使用了 ReLU 激活函数。

**输出层**采用一个全连接层，将隐含层的输出映射到最终的一维预测值，即实体与实体之间的相关性指数。

对于图中已存在的链接，本模型将其作为正样本。并生成图中并不存在的链接作为负样本。损失函数采用交叉熵损失函数来衡量模型的预测误差。

## 服务部署
**前端**

1. 确保以安装完毕npm
2. 进入IE2_FE目录
3. 执行`npm install`安装依赖
4. 执行`npm run serve`部署服务

**后端**

1. 修改setting.py数据库配置
2. 确保数据库数据完整
3. 执行`python manage.py makemigrations`生成新的迁移文件
4. 执行`python manage.py migrate`将生成的py文件映射应用到数据库
5. `python manage.py runserver` 默认后端端口8000
