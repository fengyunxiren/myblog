<template>
  <div id="app">
    <el-container>
      <el-aside width="19.1%"></el-aside>
      <el-container>
        <el-header>
          <Header></Header>
        </el-header>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
      <el-aside width="19.1%"></el-aside>
    </el-container>
  </div>
</template>

<script>
import Header from './components/Header'
export default {
  name: 'App',
  components: {Header}
}
</script>

<style>
  .el-header, .el-footer {
    background-color: #fff;
    color: #333;
    text-align: center;
    padding: 0;
  }

  .el-aside {
    background-color: #fefffa;
    color: #333;
    text-align: center;
    padding: 0;
  }

  .el-main {
    background-color: #f3fdf8;
    color: #333;
    text-align: center;
    min-height: 800px;
  }
</style>
