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

## 数据
本系统基于Yago和Dbpedia数据集，抽取金融相关实体数据，使用三元组对其进行结构化存储。

## 服务部署
**前端**

1. 确保以安装完毕npm
2. 进入IE2_FE目录
3. 执行`npm install`安装依赖
4. 执行`npm run serve`部署服务

**后端**

