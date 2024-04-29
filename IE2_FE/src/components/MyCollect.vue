<template>
    <div>
        <el-table :data="collectInfoList.filter(data => !search || data.entity.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">
            <el-table-column label="graph_name" prop="graph_name" width="180">
            </el-table-column>
            <el-table-column label="entity" prop="entity" width="120">
            </el-table-column>
            <el-table-column label="abstract" prop="abstract">
            </el-table-column>
            <el-table-column align="right">
                <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                </template>
                <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                    <el-button size="mini" type="danger"
                        @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="page"
            :page-sizes="[5, 10, 20]" :page-size="size" style="float:right"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
    </div>
</template>

<script>
export default {
    name: "InfoTable",
    data() {
        return {
            dialogVisible: false,
            dialog2Visible: false,
            addFlag: true,
            page: 1,
            total: 0,
            size: 10,
            collectInfoList: [],
            collectInfo: {},
            search: '',
            curId: ""
        }
    },
    computed: {
        userId: {
            get() {
                return this.$store.state.userId;
            },
            set(val) {
                this.$store.commit("changeUserId", val);
            },
        },
    },
    watch: {
        //假如现在是第三页，只有一条数据了。将其删除，就没有第三页了。应该跳到第二页展示出5条数据。
        //可是数据没有展示。原因是获取list的时候page参数没有改变。依然是3
        total() {
            if (this.total == (this.page - 1) * this.size && this.total != 0) {
                this.page -= 1;
                this.getGraphInfoList()
            }
        }
    },
    methods: {
        handleClose(done) {
            done();
        },
        handleSizeChange(val) {
            this.size = val
            this.getCollectList()
        },
        handleCurrentChange(val) {
            this.page = val;
            this.getCollectInfoList();
        },
        // editGraphInfo(index, row) {
        //     console.log(index, row);
        //     this.graphInfo = row;
        //     this.dialogVisible = true;
        //     this.addFlag = false;
        // },

        delCollect(row) {
            console.log(row)
            this.addFlag = false;
            this.dialog2Visible = true;
            this.curId = row.id;
        },
        async handleDel() {
            try {
                // let res = await axios.post(
                //     "http://127.0.0.1:8848/api/v1/book/del",
                //     qs.stringify({
                //         id: this.curId
                //     })
                // );
                this.curId = "";
                this.dialog2Visible = false;
                // this.$message({
                //     message: res.data.Msg,
                //     type: "success"
                // });
                this.getCollectInfoList();
            } catch (e) {
                console.log(e);
            }
        },

        saveCollectInfo() {
            let that = this;
            this.$http
                .post("nasdaq/savegraphinfo/", {
                    user_id: that.userId,
                    graph_id: that.graphInfo.id,
                    name: that.graphInfo.name,
                    description: that.graphInfo.description,
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.dialogVisible = false;
                        that.collectInfo = {};
                        that.getCollectInfoList();
                        that.$message({
                            message: "数据更新成功!",
                            type: 'success'
                        });
                    } else {
                        //失败的提示！
                        that.$message("数据更新失败");
                    }
                })
                .catch(function (err) {
                    console.log(err);
                    that.$message.error("后端更新数据出现异常!");
                });
        },

        getCollectInfoList() {
            let that = this;
            this.$http
                .post("nasdaq/collectinfolist/", {
                    user_id: that.userId,
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.collectInfoList = res.data['collect_info_list']
                        //         page: this.page,
                        //         size: this.size
                        that.dialogVisible = false;

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

        // enterGraph(index, row) {
        //     console.log(row.id)
        //     this.$emit('enter-graph', { activeName: "activeentiey", graph_id: row.id });
        // },

        // handleDelete(index, row) {
        //     console.log(index, row);
        // }
    },
    mounted() {
        this.getCollectInfoList();
    },
}
</script>