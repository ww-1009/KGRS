<template>
    <div>
        <el-table
            :data="relationInfoList.filter(data => !search || data.s.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">
            <el-table-column label="id" prop="relation_id" width="80">
            </el-table-column>
            <el-table-column label="主语" prop="s" width="100">
            </el-table-column>
            <el-table-column label="谓语" prop="p" width="100">
            </el-table-column>
            <el-table-column label="宾语" prop="o" width="100">
            </el-table-column>
            <el-table-column align="right">
                <template slot="header" slot-scope="scope">
                    <el-row :gutter="5">
                        <el-col :span="8">
                            <el-button size="mini" type="success" @click="addFlag = true; dialogVisible = true"
                                round>New</el-button>
                        </el-col>
                        <el-col :span="16">
                            <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                        </el-col>
                    </el-row>
                </template>
                <template slot-scope="scope">
                    <el-button size="mini" @click="editRelationInfo(scope.$index, scope.row)" round>Edit</el-button>
                    <el-button size="mini" type="danger" @click="delRelation(scope.$index, scope.row)"
                        round>Del</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="page"
            :page-sizes="[5, 10, 20]" :page-size="size" style="float:right"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
        <el-dialog :title="addFlag ? '新增关系' : '修改关系'" style="text-align:left !important" :visible.sync="dialogVisible"
            :before-close="handleClose">
            <el-form ref="form" label-width="80px">
                <el-form-item label="主语" style="width:250px">
                    <el-input v-model="relationInfo.s" placeholder="请输入主语"></el-input>
                </el-form-item>
                <el-form-item label="谓语" style="width:250px">
                    <el-input v-model="relationInfo.p" placeholder="请输入谓语"></el-input>
                </el-form-item>
                <el-form-item label="宾语" style="width:250px">
                    <el-input v-model="relationInfo.o" placeholder="请输入宾语"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="success" @click="saveRelationInfo()">提交</el-button>
                <el-button type="primary" @click="dialogVisible = false">取消</el-button>
            </span>
        </el-dialog>
        <el-dialog title="提示" style="text-align:left !important" :visible.sync="dialog2Visible"
            :before-close="handleClose">
            <span>你确定要删除这条关系吗?</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleDel()">提交</el-button>
                <el-button type="primary" @click="dialog2Visible = false">取消</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: "RelationTable",
    props: {
        activeGraphId: 1,
    },
    data() {
        return {
            dialogVisible: false,
            dialog2Visible: false,
            addFlag: true,
            page: 1,
            total: 3,
            size: 10,

            relationInfoList: [],
            relationInfo: {id:-1, id_s:-1, s:'', p:'', o:'', id_o:-1},
            search: '',
            curId: ''
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
                this.getRelationInfoList()
            }
        }
    },
    methods: {
        handleClose(done) {
            done();
        },
        handleSizeChange(val) {
            this.size = val
            this.getRelationInfoList()
        },
        handleCurrentChange(val) {
            this.page = val;
            this.getRelationInfoList();
        },
        editRelationInfo(index, row) {
            console.log(index, row);
            this.relationInfo = row;
            this.dialogVisible = true;
            this.addFlag = false;

        },

        delRelation(index, row) {
            this.addFlag = false;
            this.dialog2Visible = true;
            this.curId = row.id;
        },

        handleDel() {
            let that = this;
            this.$http
                .post("nasdaq/delrelation/", {
                    id: that.curId,
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.curId = "";
                        that.dialog2Visible = false;
                        that.getRelationInfoList();
                        that.$message({
                            message: "实体关系删除成功!",
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

        tarClose(tag) {
            this.relationInfo.type.splice(this.relationInfo.type.indexOf(tag), 1);
        },

        getRelationInfoList() {
            let that = this;
            this.$http
                .post("nasdaq/selfrelationlist/", {
                    graph_id: that.activeGraphId,
                })
                .then(function (res) {
                if (res.data.code === 200) {
                    that.relationInfoList = res.data['relation_info_list']
                    that.total = res.data['total']
                    //         page: this.page,
                    //         size: this.size
                    
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

        saveRelationInfo() {
            let that = this;
            this.$http
                .post("nasdaq/saverelationinfo/", {
                    user_id: that.userId,
                    graph_id: that.activeGraphId,
                    relation_id: that.relationInfo.id,
                    id_s: that.relationInfo.id_s,
                    s: that.relationInfo.s,
                    p: that.relationInfo.p,
                    o: that.relationInfo.o,
                    id_o: that.relationInfo.id_o,
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.dialogVisible = false;
                        that.relationInfo = {id:-1, id_s:-1, s:'', p:'', o:'', id_o:-1};
                        that.getRelationInfoList();
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


        handleDelete(index, row) {
            console.log(index, row);
        }
    },
    mounted() {
        this.getRelationInfoList();
    },
}
</script>

<style>
.el-tag+.el-tag {
    margin-left: 10px;
}

.button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
}

.input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
}
</style>
