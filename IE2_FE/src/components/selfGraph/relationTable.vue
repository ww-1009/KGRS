<template>
    <div>
        <el-table
            :data="RelationInfoList.filter(data => !search || data.s.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">
            <el-table-column label="id" prop="id" width="80">
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
                <el-button type="success" @click="saveRelation()">提交</el-button>
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
    data() {
        return {
            dialogVisible: false,
            dialog2Visible: false,
            addFlag: true,
            page: 1,
            total: 3,
            size: 10,

            RelationInfoList: [{
                id: 0,
                id_s: 0,
                s: '贾宝玉',
                p: '爱人',
                o: '林黛玉',
                id_o: 1
            }],
            relationInfo: {},
            search: '',
            curId: ''
        }
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
                this.getRelationInfoList();
            } catch (e) {
                console.log(e);
            }
        },

        tarClose(tag) {
            this.relationInfo.type.splice(this.relationInfo.type.indexOf(tag), 1);
        },

        async getRelationInfoList() {
            try {
                // let res = await axios.post(
                //     "http://127.0.0.1:8848/api/v1/book/list",
                //     qs.stringify({
                //         page: this.page,
                //         size: this.size
                //     })
                // );
                // this.total = res.data.Data.Total;
                // this.GraphInfoList = res.data.Data.List;
                console.log("getBookList");
            } catch (e) {
                console.log(e);
            }
        },
        async saveRelation() {
            try {
                // let res = await axios.post(
                //     "http://127.0.0.1:8848/api/v1/book/save",
                //     qs.stringify({
                //         id: this.graphInfo.id,
                //         name: this.graphInfo.name,
                //         type: this.graphInfo.description
                //     })
                // );
                this.dialogVisible = false;
                this.relationInfo = {};
                // this.$message({
                //     message: res.data.Msg,
                //     type: "success"
                // });
                this.getRelationInfoList();
            } catch (e) {
                console.log(e);
            }
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
