<template>
  <div>
    <el-breadcrumb
      style="margin-bottom: 0px"
      separator-class="el-icon-arrow-right"
    >
      <el-breadcrumb-item :to="{ path: '/type' }"
        >类型关系图</el-breadcrumb-item
      >
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item
          :index="item"
          v-for="item in hasSearched"
          :key="item"
          @click.native="searchagain(item)"
          >{{ item }}</el-breadcrumb-item
        >
      </el-breadcrumb>
    </el-breadcrumb>
    <el-row>
      <el-col :span="17">
        <el-card style="width: 97%">
          <Mysearch></Mysearch>
          <!-- 图谱 -->
          <div
            style="width: 100%; height: 640px; float: left"
            ref="graph"
            v-loading="loading"
            element-loading-text="拼命加载中"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0)"
          >
            <el-empty
              description="暂无图谱"
              :image-size="200"
              style="margin-top: 70px"
            ></el-empty>
          </div>
          <!-- 对话框 -->
          <el-dialog
            title="所含实体"
            :visible.sync="dialogVisible"
            width="30%"
            top="30vh"
          >
            <!-- 内层对话框 -->
            <el-dialog
              title="实体关系"
              :visible.sync="dialog_child"
              width="60%"
              top="20vh"
              append-to-body
              @open="openChildDialog()"
            >
              <!-- 内层图谱 -->
              <div
                style="width: 95%; height: 450px; float: left"
                ref="child_graph"
              ></div>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialog_child = false">取 消</el-button>
                <!-- <el-button type="primary" @click="dialogYes">确 定</el-button> -->
              </span>
            </el-dialog>
            <!-- 多选框 -->
            <template>
              <el-checkbox-group v-model="checkedEntities">
                <el-checkbox
                  v-for="entity in entities"
                  :label="entity"
                  :key="entity"
                  >{{ entity }}</el-checkbox
                >
              </el-checkbox-group>
            </template>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="dialogYes">确 定</el-button>
            </span>
          </el-dialog>
        </el-card>
      </el-col>
      <el-col :span="7">
        <el-card style="height: 800px">
          <Myimage></Myimage>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
import Myimage from "@/components/Image";
import Mysearch from "@/components/Search";

const { mapMutations, mapState, mapGetters, mapActions } =
  createNamespacedHelpers("mystrategy");
function myAerlt(val) {
  var obj = JSON.parse(val);
  console.log(obj);
}
window.myAerlt = myAerlt;
export default {
  components: { Myimage, Mysearch },
  data() {
    return {
      // checkAll: false,
      checkedEntities: [],
      entities: ["上海", "北京", "广州", "深圳"],
      isIndeterminate: true,
      Mychart: null,
      Childchart: null,
      possible_out: [],
      options: [
        {
          value: "1",
          label: "深度一",
        },
        {
          value: "2",
          label: "深度二",
        },
        {
          value: "3",
          label: "深度三",
        },
      ],
      loading: false,
      dialogVisible: false,
      dialog_child: false,
      childnodes:[],
      childlink:[],
    };
  },
  created() {},
  mounted() {
    this.path = "类型关系图";
    if (this.name != "") {
      this.upDatecharts();
    }
  },
  computed: {
    inputStr: {
      get() {
        return this.$store.state.inputStr;
      },
      set(val) {
        this.$store.commit("changeInputStr", val);
      },
    },
    value: {
      get() {
        return this.$store.state.value;
      },
      set(val) {
        this.$store.commit("changeValue", val);
      },
    },
    name: {
      get() {
        return this.$store.state.name;
      },
      set(val) {
        this.$store.commit("changeName", val);
      },
    },
    hasSearched: {
      get() {
        return this.$store.state.hasSearched;
      },
      set(val) {
        this.$store.commit("changeSearched", val);
      },
    },
    typeNode: {
      get() {
        return this.$store.state.typeNode;
      },
      set(val) {
        this.$store.commit("changeTypeNode", val);
      },
    },
    typeLinks: {
      get() {
        return this.$store.state.typeLinks;
      },
      set(val) {
        this.$store.commit("changeTypeLinks", val);
      },
    },
    typeMap: {
      get() {
        return this.$store.state.typeMap;
      },
      set(val) {
        this.$store.commit("changeTypeMap", val);
      },
    },
    entityNode: {
      get() {
        return this.$store.state.entityNode;
      },
      set(val) {
        this.$store.commit("changeEntityNode", val);
      },
    },
    entityLinks: {
      get() {
        return this.$store.state.entityLinks;
      },
      set(val) {
        this.$store.commit("changeEntityLinks", val);
      },
    },
    statu: {
      get() {
        return this.$store.state.statu;
      },
      set(val) {
        this.$store.commit("changeStatu", val);
      },
    },
    path: {
      get() {
        return this.$store.state.path;
      },
      set(val) {
        this.$store.commit("changePath", val);
      },
    },
    first: {
      get() {
        return this.$store.state.first;
      },
      set(val) {
        this.$store.commit("changeFirst", val);
      },
    },
  },
  methods: {
    dialogYes() {
      console.log(this.checkedEntities);
      if (this.checkedEntities.length == 1) {
        this.inputStr = this.checkedEntities[0];
        this.statu = !this.statu;
        this.dialogVisible = false;
        // this.$router.push('/entity')
      } else {
        let that = this;
        this.$http
          .post("nasdaq/childgraph/", {
            checkedEntities: that.checkedEntities,
            entity: that.entityNode,
            link: that.entityLinks,
          })
          .then(function (res) {
            if (res.data.code === 1) {
              that.childnodes = res.data.data[0];
              that.childlink = res.data.data[1];
              that.dialog_child = true;
              that.checkedEntities=[];
            } else {
              //失败的提示！
              that.$message(that.inputStr + "暂无数据");
            }
          })
          .catch(function (err) {
            console.log(err);
            that.$message.error("获取后端查询结果出现异常!");
          });
          
      }
    },
    openChildDialog(){
      this.$nextTick(() => {
          this.upDateChild();
        });
    },
    searchagain(item) {
      this.inputStr = item;
      this.statu = !this.statu;
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    //初始化图谱
    initechart() {
      this.Mychart = this.$echarts.init(this.$refs.graph);
    },
    //更新图谱
    upDatecharts() {
      this.initechart();
      let that = this;
      var data = this.typeNode;
      var links = this.typeLinks;
      var option = {
        // title: {
        //   text: that.inputStr+"类型图",
        // },
        tooltip: {
          // triggerOn: 'click',//点击才会出现提示框
          // enterable: true,//鼠标可以进入提示框
          formatter: function (params) {
            //回调函数
            var str = "所含实体节点：<br>" + that.typeMap[params.data["id"]][0];
            return str;
          },
        },
        // animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
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
              edgeLength: [200, 300],
              // layoutAnimation: true
            },
            // edgeSymbolSize: [4, 50],
            edgeLabel: {
              normal: {
                show: false,
                textStyle: {
                  fontSize: 10,
                },
                formatter: "{c}",
              },
            },
            data: data,
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
      this.first = true;
      this.loading = false;
      this.Mychart.off("click");
      //配置点击事件
      this.Mychart.on("click", function (params) {
        if (params.dataType == "node") {
          // console.log(that.typeMap[params.data["id"][1]])
          that.entities = that.typeMap[params.data["id"]][1];
          that.dialogVisible = true;
        }
      });
    },


    upDateChild() {
      this.Childchart = this.$echarts.init(this.$refs.child_graph);
      var data = this.childnodes;
      var links = this.childlink;
      var childoption = {
        // title: {
        //   text: that.inputStr+"类型图",
        // },
        tooltip: {
          // formatter: function (params) {
          //   //回调函数
          //   var str = "所含实体节点：<br>" + that.typeMap[params.data["id"]][0];
          //   return str;
          // },
        },
        // animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
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
              // layoutAnimation: true
            },
            // edgeSymbolSize: [4, 50],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 10,
                },
                formatter: "{c}",
              },
            },
            data: data,
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
      this.Childchart.setOption(childoption);
    },
  },
  watch: {
    typeNode(n, o) {
      if (n != []) {
        this.upDatecharts();
        let index = this.hasSearched.indexOf(this.name);
        if (index != -1) {
          this.hasSearched.splice(index, this.hasSearched.length - index);
        }
        if (this.hasSearched.length == 6) this.hasSearched.shift();
        this.hasSearched.push(this.name);
        //
      }
    },
    typeNode(n, o) {
      this.upDatecharts();
    },
  },
};
</script>
   