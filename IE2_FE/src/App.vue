<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>
<style>
  #app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    
  }
  body{
    margin:0px;
  }
</style>
