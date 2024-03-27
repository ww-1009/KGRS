<template>
    <div>
        <div style="width: 100%; height: 690px; float: left" ref="graph">
            <!-- <el-empty description="暂无图谱" :image-size="200" style="margin-top:20px"></el-empty> -->
        </div>
        <!-- <el-empty description="暂无图谱" :image-size="200" style="margin-top:70px"></el-empty> -->
    </div>
</template>


<script>
export default {
    name: "GraphShow",
    props: {
        activeGraphId: 0,
    },
    data() {
        return {
            Mychart: null,
            loading: false,
            dialogVisible: false,
            entityNode: [],
            entityLinks: [],
            entityInfoAll: {}
        };
    },

    mounted() {
        this.initechart();
        this.getSelfGraph();
    },

    methods: {
        getSelfGraph() {
            let that = this;
            this.$http
                .post("nasdaq/selfgraph/", {
                    graph_id: 1,
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.entityNode = res.data['entity_node']
                        that.entityLinks = res.data['entity_relation']
                        that.entityInfoAll = res.data['entity_info_all']
                        that.upDatecharts(that.entityNode, that.entityLinks, that.entityInfoAll);
                    } else {
                        //失败的提示！
                        that.$message("暂无数据");
                    }
                })
                .catch(function (err) {
                    console.log(err);
                    that.$message.error("获取后端查询结果出现异常!");
                });
        },

        initechart() {
            this.Mychart = this.$echarts.init(this.$refs.graph);
        },
        //更新图谱
        upDatecharts(node, links, entityInfoAll) {
            let that = this;
            // this.entityInfo = entityInfoAll;
            var option = {
                tooltip: {},
                animationDurationUpdate: 200,
                label: {
                    normal: {
                        show: true,
                        textStyle: {
                            fontSize: 12,
                        },
                    },
                },
                legend: {
                    x: "center",
                    show: false,
                },
                series: [
                    {
                        type: "graph",
                        layout: "force",
                        symbolSize: 42,
                        focusNodeAdjacency: true,
                        legendHoverLink: true,
                        roam: true,
                        draggable: true,
                        edgeSymbol: ["none", "arrow"],
                        categories: [
                            {
                                name: "查询实体",
                                itemStyle: {
                                    normal: {
                                        color: "#009800",
                                    },
                                },
                            },
                            {
                                name: "一级实体",
                                itemStyle: {
                                    normal: {
                                        color: "#4592FF",
                                    },
                                },
                            },
                            {
                                name: "二级实体",
                                itemStyle: {
                                    normal: {
                                        color: "#C71585",
                                    },
                                },
                            },
                            {
                                name: "class",
                                itemStyle: {
                                    normal: {
                                        color: "#C72585",
                                    },
                                },
                            },
                        ],
                        label: {
                            normal: {
                                show: true,
                                textStyle: {
                                    fontSize: 10,
                                },
                            },
                        },
                        force: {
                            repulsion: 800,
                            gravity: 0.03,
                            edgeLength: [10, 50],
                            layoutAnimation: true
                        },
                        // edgeSymbolSize: [40, 50],
                        edgeLabel: {
                            normal: {
                                show: true,
                                textStyle: {
                                    fontSize: 10,
                                },
                                formatter: "{c}",
                            },
                        },
                        data: node,
                        links: links,
                        lineStyle: {
                            normal: {
                                opacity: 0.9,
                                width: 1.3,
                                curveness: 0.2,
                                color: "#262626",
                            },
                        },
                    },
                ],
            };
            this.Mychart.setOption(option);
            // this.Mychart.off('click')
            this.Mychart.on('mouseover', function (params) {
                if (params.dataType == "node") {
                    console.log(entityInfoAll[params.data["id"]])
                    that.$emit('entity-info', { entityInfo: entityInfoAll[params.data["id"]]});
                    // that.entityInfo = that.entityInfoAll[params.data["id"]];
                    // console.log(that.entityInfo)
                }
            });

        },
    }
}
</script>
