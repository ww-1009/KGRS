<template>
    <div>
        <el-row>
            <el-col :span="17">
                <el-card style="width: 97%; height: 800px">
                    <el-tabs type="border-card" v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="图谱信息" name="activeinfo">
                            <InfoTable v-if="activeName == 'activeinfo'" ref="activeinfo" @enter-graph="enterGraph"></InfoTable>
                        </el-tab-pane>
                        <el-tab-pane label="实体信息" name="activeentiey" :disabled="isDisabled">
                            <EntityTable v-if="activeName == 'activeentiey'" ref="activeentiey"></EntityTable>
                        </el-tab-pane>
                        <el-tab-pane label="实体关系" name="activerelation" :disabled="isDisabled">
                            <RelationTable v-if="activeName == 'activerelation'" ref="activerelation"></RelationTable>
                        </el-tab-pane>
                        <el-tab-pane label="图谱展示" name="activeshow" :disabled="isDisabled">
                            <GraphShow v-if="activeName == 'activeshow'" ref="activeshow"></GraphShow>
                        </el-tab-pane>
                    </el-tabs>
                    
                </el-card>
            </el-col>
            <el-col :span="7">
                <el-card style="height: 800px">
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import InfoTable from "./infoTable.vue";
import EntityTable from "./entityTable.vue";
import RelationTable from "./relationTable.vue";
import GraphShow from "./graphShow.vue";

export default {
    name: "TEMPLATE",
    components: {
        InfoTable,
        EntityTable,
        RelationTable,
        GraphShow
    },
    data(){
      return {
        activeName: 'activeinfo',
        isDisabled: true,
        activeGraphId:0
      };
    },
    mounted(){
      this.onQuery();
    },
    methods:{
      handleClick(tab, event) {
        this.activeName = tab.name;
        var that = this;
        setTimeout(function(){
            that.onQuery();
        },500);
      },
      
      onQuery() {
        this.$refs[this.activeName].getList();
      },

      enterGraph(data) {
        this.isDisabled = false;
        this.activeName = data.activeName;
        this.activeGraphId = data.graph_id;
      }
 
    }
}
</script>


<style>
.el-row {
    margin-bottom: 40px;

    &:last-child {
        margin-bottom: 0;
    }
}

.el-col {
    border-radius: 4px;
}
</style>