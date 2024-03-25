<template>
  <div>
    <el-breadcrumb
      style="margin-bottom: 0px"
      separator-class="el-icon-arrow-right"
    >
      <el-breadcrumb-item :to="{ path: '/entity' }">实体图</el-breadcrumb-item>
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item
          :index="item"
          v-for="item in hasSearched"
          :key="hasSearched.indexOf(item)"
          @click.native="searchagain(item)"
          >{{ item }}</el-breadcrumb-item
        >
      </el-breadcrumb>
    </el-breadcrumb>
    <el-row>
      <el-col :span="17">
        <el-card style="width: 97%">
          <Mysearch></Mysearch>
         
          <div
            style="width: 100%; height: 640px; float: left"
            ref="graph"
            v-loading="loading"
            element-loading-text="拼命加载中"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0)"
          >
            <el-empty description="暂无图谱" :image-size="200" style="margin-top:70px"></el-empty>
          </div>
          <el-dialog
            :title="this.inputStr"
            :visible.sync="dialogVisible"
            width="35%"
            :before-close="handleClose"
          >
          <el-card :body-style="{ padding: '0px' }">
          <el-row :gutter="20">
            <el-col :span="9">
              <div class="grid-content bg-purple">
                <el-image :src="img">
                  <div slot="placeholder" class="image-slot">
                    <i class="el-icon-picture-outline"></i>
                  </div>
                </el-image>
              </div>
            </el-col>
            <el-col :span="15">
              <div class="grid-content bg-purple">
                {{this.abstract}}
              </div>
            </el-col>
          </el-row>
          </el-card>
            <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="dialogVisible = false"
                >确 定</el-button
              >
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

export default {
  components: { Myimage, Mysearch },
  data() {
    return {
      Mychart: null,
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
    };
  },
  created() {},
  mounted() {
    this.path="实体图"
    if (this.name != "") {
      this.upDatecharts();
    }
    // console.log(this.entityNode.length)
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
    img: {
      get() {
        return this.$store.state.img;
      },
      set(val) {
        this.$store.commit("changeImg", val);
      },
    },
    abstract: {
      get() {
        return this.$store.state.abstract;
      },
      set(val) {
        this.$store.commit("changeAbstract", val);
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
    key_word_id: {
      get() {
        return this.$store.state.key_word_id;
      },
      set(val) {
        this.$store.commit("changeKey_word_id", val);
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
    searchagain(item) {
      this.inputStr = item;
      this.statu=!this.statu;
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
      // console.log("porpertyinitecharts");
    },
    //更新图谱
    upDatecharts() {
      this.initechart();
      let that = this;
      var data = this.entityNode;     
      var links = this.entityLinks;
      var option = {
        // title: {
        //   text: that.inputStr + "实体图",
        // },
        tooltip: {},
        animationDurationUpdate: 200,
        // animationEasingUpdate: "quinticInOut",
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
            legendHoverLink:true,
            roam: true,
            draggable:true,
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
              gravity:0.03,
              edgeLength: [10, 50],
              layoutAnimation:true
            },
            // edgeSymbolSize: [40, 50],
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
      this.Mychart.setOption(option);
      this.first=true;
      this.loading = false;
      this.Mychart.off('click')
      //配置点击事件
      this.Mychart.on("click", function (params) {
        if (params.dataType == "node") {
          if (params.name == that.name) {
            that.dialogVisible = true;
          } else{
            // console.log(params.data["id"])
            that.key_word_id=params.data["id"]
            that.inputStr = params.name;
            that.statu=!that.statu;
            // console.log(that.statu)
          } 
        }
      });

    },
  },
  watch: {
    name(n, o) {
      if (n != []) {
        this.upDatecharts();
        // console.log("gen")
        let index=this.hasSearched.indexOf(this.name)
        if(index!=-1){
          this.hasSearched.splice(index, this.hasSearched.length-index);
        }
        if(this.hasSearched.length==6)
          this.hasSearched.shift();
        this.hasSearched.push(this.name);
        
      }
    },
    entityNode(n, o) {
      this.upDatecharts();
    },
  },
};
</script>
<style>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }
</style>
   