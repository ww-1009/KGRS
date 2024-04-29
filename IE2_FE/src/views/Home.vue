<template>
  <el-container class="home-container">
    <el-header>
      <span>&nbsp;&nbsp;&nbsp;基于金融知识图谱的实体推荐系统</span>

    </el-header>
    <!-- 页面主体区域 -->
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <!-- 侧边栏菜单区域 -->
        <el-menu
          background-color="#333744"
          text-color="#fff"
          active-text-color="#409EFF"
          :collapse="isCollapse"
          :collapse-transition="false"
          router
          :default-active="activePath"
        >

        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>金融图谱</span>
          </template>
          <el-menu-item index="/entity">
            <i class="el-icon-share"></i>
            <span slot="title">实体关系图</span>
          </el-menu-item>
           <!-- <el-menu-item index="/type">
            <i class="el-icon-menu"></i>
            <span slot="title">类型关系图</span>
          </el-menu-item> -->
          <!-- <el-menu-item index="/porperty">
            <i class="el-icon-orange"></i>
            <span slot="title">属性图</span>
          </el-menu-item> -->
          </el-submenu>

          <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>我的空间</span>
          </template>
          <el-menu-item index="/selfgraph">
            <i class="el-icon-s-custom"></i>
            <span slot="title">自定义图谱</span>
          </el-menu-item>
           <el-menu-item index="/mycollect">
            <i class="el-icon-star-on"></i>
            <span slot="title">节点收藏</span>
          </el-menu-item>
          <el-menu-item index="/setting">
            <i class="el-icon-s-tools"></i>
            <span slot="title">个人设置</span>
          </el-menu-item>
        </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
        <!-- 主窗口 -->
        <el-main>
          <router-view></router-view>
        </el-main>
        <!-- <el-footer style="height: 30px"></el-footer> -->
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      // 是否折叠
      isCollapse: false,
       // 被激活的链接地址
      activePath: '/entity',
    };
  },
  created() {
    this.activePath = window.sessionStorage.getItem('activePath')
    this.getNewsTop()
  },
  computed:{
    newstop: {
      get() {
        return this.$store.state.newstop;
      },
      set(val) {
        this.$store.commit("changeNewsTop", val);
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
    newsimg: {
      get() {
        return this.$store.state.newsImg;
      },
      set(val) {
        this.$store.commit("changeNewsimg", val);
      },
    },
  },

  methods: {
    // 点击按钮，切换菜单的折叠与展开
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },
    
    // 保存链接的激活状态
    saveNavState(activePath) {
      window.sessionStorage.setItem('activePath', activePath)
      this.activePath = activePath
    },
    getNewsTop(){
      let that=this;
      this.$http
        .get("nasdaq/newstop/")
        .then(function (res) {
          if (res.data.code === 1) {
            that.newstop = res.data.data[0];
            that.newsimg=res.data.data[1];
            //提示：
          } else {
            //失败的提示！
            that.$message.error(res.data.msg);
          }
        })
        .catch(function (err) {
          console.log(err);
          that.$message.error("获取后端查询结果出现异常!");
        });
    }
  },
};
</script>

<style lang="less" scoped>
.home-container {
  height: 100%;
}
.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #fff;
  font-size: 20px;
  > div {
    display: flex;
    align-items: center;
    span {
      margin-left: 15px;
    }
  }
}

.el-aside {
  background-color: #333744;
  .el-menu {
    border-right: none;
  }
}

.el-main {
  background-color: #eaedf1;
}

.iconfont {
  margin-right: 10px;
}

.toggle-button {
  background-color: #4a5064;
  font-size: 10px;
  line-height: 24px;
  color: #fff;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}
</style>