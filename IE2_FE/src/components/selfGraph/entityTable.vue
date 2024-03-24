<template>
    <div>
        <el-table
            :data="EntityInfoList.filter(data => !search || data.entity.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%">
            <el-table-column label="id" prop="id" width="80">
            </el-table-column>
            <el-table-column label="entity" prop="entity" width="100">
            </el-table-column>
            <el-table-column label="Description" prop="description" width="500">
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
                    <el-button size="mini" @click="editEntityInfo(scope.$index, scope.row)" round>Edit</el-button>
                    <el-button size="mini" type="danger" @click="delEntity(scope.$index, scope.row)"
                        round>Del</el-button>
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
                    <el-input v-model="entityInfo.entity" placeholder="请输入实体名称"></el-input>
                </el-form-item>
                <el-form-item label="实体类型" style="width:500px">
                    <el-tag :key="tag" v-for="tag in entityInfo.type" closable :disable-transitions="false"
                        @close="tarClose(tag)">
                        {{ tag }}
                    </el-tag>
                    <el-input class="input-new-tag" v-if="tarinputVisible" v-model="tarinputValue" ref="saveTagInput"
                        size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm">
                    </el-input>
                    <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
                </el-form-item>
                <el-form-item label="实体描述" style="width:500px">
                    <el-input v-model="entityInfo.description" type="textarea" :rows="3"
                        placeholder="请输入实体描述"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="success" @click="saveEntity()">提交</el-button>
                <el-button type="primary" @click="dialogVisible = false">取消</el-button>
            </span>
        </el-dialog>
        <el-dialog title="提示" style="text-align:left !important" :visible.sync="dialog2Visible"
            :before-close="handleClose">
            <span>你确定要删除这个实体吗?</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleDel()">提交</el-button>
                <el-button type="primary" @click="dialog2Visible = false">取消</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: "EntityTable",
    data() {
        return {
            dialogVisible: false,
            dialog2Visible: false,
            addFlag: true,
            page: 1,
            total: 3,
            size: 10,

            tarinputVisible: false,
            tarinputValue: '',
            EntityInfoList: [{
                id: 0,
                entity: '贾宝玉',
                type: ["人", "男人", "主角"],
                description: '是一个帮助了解红楼梦中人物关系的图谱',
                img: ""
            }, {
                id: 1,
                entity: '林黛玉',
                type: ["人", "女人", "主角"],
                description: '是一个帮助了解红楼梦中人物关系的图谱',
                img: ""
            }, {
                id: 2,
                entity: '薛宝钗',
                type: ["人", "女人", "主角"],
                description: '是一个帮助了解红楼梦中人物关系的图谱',
                img: ""
            }],
            entityInfo: {},
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
                this.getEntityInfoList()
            }
        }
    },
    methods: {
        handleClose(done) {
            done();
        },
        handleSizeChange(val) {
            this.size = val
            this.getEntityInfoList()
        },
        handleCurrentChange(val) {
            this.page = val;
            this.getEntityInfoList();
        },
        editEntityInfo(index, row) {
            console.log(index, row);
            this.entityInfo = row;
            this.dialogVisible = true;
            this.addFlag = false;

        },

        delEntity(index, row) {
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

        tarClose(tag) {
            this.entityInfo.type.splice(this.entityInfo.type.indexOf(tag), 1);
        },

        showInput() {
            this.tarinputVisible = true;
            this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },

        handleInputConfirm() {
            let tarinputValue = this.tarinputValue;
            if (tarinputValue) {
                this.entityInfo.type.push(tarinputValue);
            }
            this.tarinputVisible = false;
            this.tarinputValue = '';
        },

        async getEntityInfoList() {
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
        async saveEntity() {
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
                this.entityInfo = {};
                // this.$message({
                //     message: res.data.Msg,
                //     type: "success"
                // });
                this.getEntityInfoList();
            } catch (e) {
                console.log(e);
            }
        },

        handleDelete(index, row) {
            console.log(index, row);
        }
    },
    mounted() {
        this.getEntityInfoList();
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
