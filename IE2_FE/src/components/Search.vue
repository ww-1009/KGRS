<template>
  <div>
    <el-row>
      <el-col :span="11">
        <div class="sub-title"></div>
        <el-autocomplete
          class="inline-input"
          v-model="inputStr"
          :fetch-suggestions="querySearch"
          placeholder="请输入内容"
          :trigger-on-focus="false"
          @select="handleSelect"
          style="width: 500px"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="queryButten()"
          ></el-button>
        </el-autocomplete>
      </el-col>
      <el-col :span="2">
        <!-- <el-button type="text">Elon Musk</el-button> -->
        <h4 style="margin-top:11px">Example:</h4>
        
      </el-col>
      <el-col :span="2">
        <el-link @click="inputStr='Elon Musk'" style="margin-top:13px">Elon Musk</el-link>
      </el-col>
      <el-col :span="2">
        <el-link @click="inputStr='Bill Gates'" style="margin-top:13px">Bill Gates</el-link>
      </el-col>
            <el-col :span="5">
        <el-link @click="inputStr='Mark Zuckerberg'" style="margin-top:13px">Mark Zuckerberg</el-link>
      </el-col>
    </el-row>
    <el-divider style="padding: 10px"></el-divider>
    <div style="margin: 0 auto">
      <el-row>
        <el-col :span="12">
          <h1 v-show="!first"></h1>
          <h1 v-show="first" style="font-size: 28px; margin: 0px; padding: 0">
            {{ name+path }}
          </h1>
        </el-col>
        <el-col :span="12">
          <div>
            <el-select v-model="value" placeholder="请选择查询深度">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
            <el-switch
              v-model="explore"
              active-text="explore"
              inactive-text="show"
              style="margin-left: 20px"
            >
            </el-switch>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
const { mapMutations, mapState, mapGetters, mapActions } =
  createNamespacedHelpers("mystrategy");
export default {
  data() {
    return {
      exp: false,
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
    };
  },
  mounted() {},
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
    porpertyNode: {
      get() {
        return this.$store.state.porpertyNode;
      },
      set(val) {
        this.$store.commit("changePorpertyNode", val);
      },
    },
    porpertyLinks: {
      get() {
        return this.$store.state.porpertyLinks;
      },
      set(val) {
        this.$store.commit("changePorpertyLinks", val);
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
    explore: {
      get() {
        return this.$store.state.explore;
      },
      set(val) {
        this.$store.commit("changeExplore", val);
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
    newstop: {
      get() {
        return this.$store.state.newstop;
      },
      set(val) {
        this.$store.commit("changeNewsTop", val);
      },
    },
  },
  methods: {
    //查询框
    querySearch(queryString, cb) {
      var possible_out = this.possible_out;
      cb(possible_out);
    },
    createFilter(queryString) {
      return (possible_out) => {
        return (
          possible_out.value
            .toLowerCase()
            .indexOf(queryString.toLowerCase()) === 0
        );
      };
    },
    handleSelect(item) {
      console.log(item);
    },
    //实现信息模糊查询
    // queryindex() {
    //   let that = this;
    //   this.$http
    //     .post("nasdaq/index/", {
    //       inputstr: that.inputStr,
    //     })
    //     .then(function (res) {
    //       if (res.data.code === 1) {
    //         that.possible_out = res.data.data;
    //         //提示：
    //       } else {
    //         //失败的提示！
    //         that.$message.error(res.data.msg);
    //       }
    //     })
    //     .catch(function (err) {
    //       console.log(err);
    //       that.$message.error("获取后端查询结果出现异常!");
    //     });
    // },
    queryButten(){
      this.hasSearched=[];
      this.queryNasdaq();
    },
    //查询按钮
    queryNasdaq() {
      // console.log(this.explore)
      let that = this;
      this.$http
        .post("nasdaq/entitydata/", {
          inputstr: that.inputStr,
          // depth: that.value,
          // oldNodes: that.entityNode,
          // oldLinks: that.entityLinks,
          // keywordid: that.key_word_id,
          // explore: that.explore,
        })
        .then(function (res) {
          if (res.data.code === 200) {
            // that.name = res.data.data[0];
            // that.img = res.data.data[1];
            // that.abstract = res.data.data[2];
            that.entityNode = res.data['entity_node'];
            that.entityLinks = res.data['entity_relation'];
            // that.porpertyNode = res.data.data[5];
            // that.porpertyLinks = res.data.data[6];
            // that.typeNode = res.data.data[7];
            // that.typeLinks = res.data.data[8];
            // that.typeMap = res.data.data[9];
            // that.newstop= res.data.data[10]
            console.log(that.entityNode)
            console.log(that.entityLinks)

            // console.log(that.typeMap)
          } else {
            //失败的提示！
            that.$message(that.inputStr + "暂无数据");
          }
        })
        .catch(function (err) {
          console.log(err);
          that.$message.error("获取后端查询结果出现异常!");
        });
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
  },
  watch: {
    inputStr(n, o) {
      this.queryindex();
    },
    statu(n, o) {
      this.queryNasdaq();
    },
    value(n, o) {
      this.queryNasdaq();
    },
    // explore(n, o) {
    //   this.exp=n;
    // },
  },
};
</script>