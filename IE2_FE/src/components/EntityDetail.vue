<template>
    <div>
        <div class="block">
            <el-image :src="entityInfo.img_url"></el-image>
        </div>
        <el-descriptions class="margin-top" title="详细信息" :column="2" direction="vertical">
            <el-descriptions-item label="实体id">{{entityInfo.id}}</el-descriptions-item>
            <el-descriptions-item label="实体名">{{entityInfo.entity}}</el-descriptions-item>
        </el-descriptions> 
        <el-descriptions class="margin-top" :column="1" direction="vertical">
            <el-descriptions-item label="类型">
                <el-tag :key="tag" v-for="tag in entityInfo.relatedType" >
                        {{ tag }}
                    </el-tag>
            </el-descriptions-item>
            <br>
            <el-descriptions-item label="简介">{{entityInfo.abstract}}</el-descriptions-item>
        </el-descriptions> 
        <i class="fr " v-if=isSelf style="font-size: 30px; color: gold;" v-bind:class="entityInfo.iscollect ? 'el-icon-star-on importicon':'el-icon-star-off'" @click.stop="changeStart()"></i>
    </div>
</template>

<script>
export default {
    props: {
        entityInfo: {},
        isSelf: true,
        activeGraphId: 0
    },
    data() {
        return {
            src: '',
        };
    },
    methods: {
        changeStart(){
            console.log(this.activeGraphId)
            let that = this;
            this.$http
                .post("nasdaq/changecollect/", {
                    graph_id: that.graphInfo.id,
                    iscollect: that.entityInfo.iscollect
                })
                .then(function (res) {
                    if (res.data.code === 200) {
                        that.entityInfo.iscollect = res.data['iscollect'];
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

    },
};
</script>