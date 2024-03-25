<template>
    <div>
        <el-table
            :data="GraphInfoList.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">
            <el-table-column label="UpDate" prop="update" width="120">
            </el-table-column>
            <el-table-column label="Name" prop="name" width="180">
            </el-table-column>
            <el-table-column label="Description" prop="description">
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
                    <el-button size="mini" type="primary" @click="enterGraph(scope.$index, scope.row)"
                        round>Enter</el-button>
                    <el-button size="mini" @click="editGraphInfo(scope.$index, scope.row)" round>Edit</el-button>
                    <el-button size="mini" type="danger" @click="delGraph(scope.row)" round>Del</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="page"
            :page-sizes="[5, 10, 20]" :page-size="size" style="float:right"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
        <el-dialog :title="addFlag ? '新增图谱' : '修改图谱'" style="text-align:left !important" :visible.sync="dialogVisible"
            :before-close="handleClose">
            <el-form ref="form" label-width="80px">
                <el-form-item label="图谱名称" style="width:300px">
                    <el-input v-model="graphInfo.name" placeholder="请输入名称"></el-input>
                </el-form-item>
                <el-form-item label="图谱描述" style="width:500px">
                    <el-input v-model="graphInfo.description" type="textarea" :rows="3" placeholder="请输入描述"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="success" @click="saveGraph()">提交</el-button>
                <el-button type="primary" @click="dialogVisible = false">取消</el-button>
            </span>
        </el-dialog>
        <el-dialog title="提示" style="text-align:left !important" :visible.sync="dialog2Visible"
            :before-close="handleClose">
            <span>你确定要删除这个图谱吗?</span>
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
            GraphInfoList: [],
            graphInfo: {},
            search: '',
            curId: ""
        }
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
            this.getBookList()
        },
        handleCurrentChange(val) {
            this.page = val;
            this.getGraphInfoList();
        },
        editGraphInfo(index, row) {
            console.log(index, row);
            this.graphInfo = row;
            this.dialogVisible = true;
            this.addFlag = false;
        },

        delGraph(row) {
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
                this.getGraphInfoList();
            } catch (e) {
                console.log(e);
            }
        },

        async saveGraph() {
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
                this.book = {};
                // this.$message({
                //     message: res.data.Msg,
                //     type: "success"
                // });
                this.getGraphInfoList();
            } catch (e) {
                console.log(e);
            }
        },

    getGraphInfoList() {
      let that = this;
      this.$http
        .post("nasdaq/graphinfolist/", {
          user_id: 1,
        })
        .then(function (res) {
          if (res.data.code === 200) {
            that.GraphInfoList = res.data['graph_info_list']
            that.total = res.data['total']
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

    enterGraph(index, row) {
        console.log(row.id)
        this.$emit('enter-graph', { activeName: "activeentiey", graph_id: row.id });
    },

        // handleDelete(index, row) {
        //     console.log(index, row);
        // }
    },
    mounted() {
        this.getGraphInfoList();
    },
}
</script>