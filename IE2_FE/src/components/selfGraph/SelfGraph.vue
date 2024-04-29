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
                            <EntityTable v-if="activeName == 'activeentiey'" ref="activeentiey" :activeGraphId="activeGraphId"></EntityTable>
                        </el-tab-pane>
                        <el-tab-pane label="实体关系" name="activerelation" :disabled="isDisabled">
                            <RelationTable v-if="activeName == 'activerelation'" ref="activerelation" :activeGraphId="activeGraphId"></RelationTable>
                        </el-tab-pane>
                        <el-tab-pane label="图谱展示" name="activeshow" :disabled="isDisabled">
                            <GraphShow v-if="activeName == 'activeshow'" ref="activeshow" :activeGraphId="activeGraphId" @entity-info="getEntityInfo"></GraphShow>
                        </el-tab-pane>
                    </el-tabs>
                    
                </el-card>
            </el-col>
            <el-col :span="7">
                <el-card style="height: 800px">
                  <Entitydetail v-if="activeName == 'activeshow'" :entityInfo="entityInfo" :isSelf="true" :activeGraphId="activeGraphId"></Entitydetail>
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
import Entitydetail from "@/components/EntityDetail";

export default {
    name: "TEMPLATE",
    components: {
        InfoTable,
        EntityTable,
        RelationTable,
        GraphShow,
        Entitydetail
    },
    data(){
      return {
        activeName: 'activeinfo',
        isDisabled: true,
        activeGraphId:1,
        entityInfo: {}
      };
    },
    mounted(){
      this.onQuery();
    },
    methods:{
      handleClick(tab, event) {
        this.activeName = tab.name;
        console.log(this.activeName)
        var that = this;
        setTimeout(function(){
            that.onQuery();
        },500);
      },
      
      onQuery() {
        // this.$refs[this.activeName].getList();
      },

      enterGraph(data) {
        this.isDisabled = false;
        this.activeName = data.activeName;
        this.activeGraphId = data.graph_id;
        // this.getSelfGraph();
      },

      getEntityInfo(data){
        this.entityInfo = data.entityInfo;
      }
 
    }
}
</script>


<style>
.el-row {
    margin-bottom: 40px;


}

.el-col {
    border-radius: 4px;
}
</style>