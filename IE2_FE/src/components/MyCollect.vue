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
                    <el-button size="mini" @click="editCollectInfo(scope.$index, scope.row)">Edit</el-button>
                    <el-button size="mini" type="danger"
                        @click="delCollect(scope.row)">Delete</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="page"
            :page-sizes="[5, 10, 20]" :page-size="size" style="float:right"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
        <el-dialog :title="addFlag ? '新增实体' : '修改实体'" style="text-align:left !important" :visible.sync="dialogVisible"
            :before-close="handleClose">
            <el-form ref="form" label-width="80px">
                <el-form-item label="实体名称" style="width:250px">
                    <el-input v-model="collectInfo.entity" placeholder="请输入实体名称"></el-input>
                </el-form-item>
                <el-form-item label="实体类型" style="width:500px">
                    <el-tag :key="tag" v-for="tag in collectInfo.relatedType" closable :disable-transitions="false"
                        @close="tarClose(tag)">
                        {{ tag }}
                    </el-tag>
                    <el-input class="input-new-tag" v-if="tarinputVisible" v-model="tarinputValue" ref="saveTagInput"
                        size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm">
                    </el-input>
                    <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
                </el-form-item>
                <el-form-item label="实体描述" style="width:500px">
                    <el-input v-model="collectInfo.abstract" type="textarea" :rows="3" placeholder="请输入实体描述"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="success" @click="saveCollectInfo()">提交</el-button>
                <el-button type="primary" @click="dialogVisible = false">取消</el-button>
            </span>
        </el-dialog>
        <el-dialog title="提示" style="text-align:left !important" :visible.sync="dialog2Visible"
            :before-close="handleClose">
            <span>你确定要取消收藏这个实体吗?</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleDel()">提交</el-button>
                <el-button type="primary" @click="dialog2Visible = false">取消</el-button>
            </span>
        </el-dialog>
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

            tarinputVisible: false,
            tarinputValue: '',
            collectInfoList: [],
            collectInfo: {},
            search: '',
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

        editCollectInfo(index, row) {
            this.collectInfo = row;
            this.dialogVisible = true;
            this.addFlag = false;

        },

        delCollect(row) {
            this.addFlag = false;
            this.dialog2Visible = true;
            this.collectInfo = row
        },

        handleDel() {
            let that = this;
            this.$http
                .post("nasdaq/changecollect/", {
                    graph_id: that.collectInfo.graph_id,
                    entity_id: that.collectInfo.entity_id,
                    iscollect: 1
                })
            .then(function (res) {
                if (res.data.code === 200) {
                    that.dialog2Visible = false;
                    that.getCollectInfoList();
                    that.$message({
                        message: "取消收藏成功",
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

        saveCollectInfo() {
            let that = this;
            this.$http
                .post("nasdaq/saveentityinfo/", {
                    user_id: that.userId,
                    graph_id: that.collectInfo.graph_id,
                    entity_id: that.collectInfo.entity_id,
                    entity: that.collectInfo.entity,
                    imgurl: that.collectInfo.img_url,
                    abstract: that.collectInfo.abstract,
                    relatedtype: that.collectInfo.relatedType,
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.dialogVisible = false;
                        that.entityInfo = { entity_id: -1, id: -1, entity: '', img_url: '', relatedType: [], abstract: '' };
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