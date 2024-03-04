<template>
  <div >
    <div class="block">
       <el-carousel trigger="click" height="190px" style="width: 285px;">
      <el-carousel-item v-for="item in this.newsimg" :key="item">
        <el-image :src="item" style="height:100%;"></el-image>
      </el-carousel-item>
    </el-carousel>
      <!-- <el-image :src="img"></el-image> -->
    </div>
    <div>
      <div :index="item[0]" :key="item[0]" v-for="item in newstop">
        <el-link
        style="margin-top:14px;"
          type="info"
          :href="item[1]"
          target="_blank"
          >{{item[0]}}</el-link
        >
        <br/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
    };
  },
  computed: {
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
    abstract: {
      get() {
        return this.$store.state.abstract;
      },
      set(val) {
        this.$store.commit("changeAbstract", val);
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
  methods: {},
};
</script>
<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
     background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
     background-color: #d3dce6;
  }
</style>
