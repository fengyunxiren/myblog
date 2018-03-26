<template>
    <el-row type="flex" class="row-bg">
      <el-col :span="4"><div class="grid-content bg-purple">
          <p class="title">{{ msg }}</p>
      </div></el-col>
      <el-col :span="16"><div class="grid-content bg-purple-light">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">处理中心</el-menu-item>
          <el-submenu index="2">
            <template slot="title">我的工作台</template>
            <el-menu-item index="2-1">选项1</el-menu-item>
            <el-menu-item index="2-2">选项2</el-menu-item>
            <el-menu-item index="2-3">选项3</el-menu-item>
            <el-submenu index="2-4">
              <template slot="title">选项4</template>
              <el-menu-item index="2-4-1">选项1</el-menu-item>
              <el-menu-item index="2-4-2">选项2</el-menu-item>
              <el-menu-item index="2-4-3">选项3</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-menu-item index="3" disabled>消息中心</el-menu-item>
          <el-menu-item index="4"><a href="https://www.ele.me" target="_blank">订单管理</a></el-menu-item>
        </el-menu>
      </div></el-col>
      <el-col :span="4"><div class="grid-content bg-purple">
          <el-button class="login" round>login</el-button>
      </div></el-col>
    </el-row>
</template>

<script>
export default {
  name: 'Header',
  data () {
    return {
      msg: 'Feng\'s blog'
    }
  }
}
</script>

<style>
  .row-bg {
    background-color: #fefffa;
    max-height: 60px;
  }
  .title {
    color: #ea6f6f;
    font-size: 20px;
    text-align: left;
    vertical-align: middle;
    font-weight: 600;
  }
  .login {
    color: #ea6f6f;
    background-color: #fff;
    border-color: #ea6f6f;
    vertical-align: bottom;
    text-align: right;
  }
</style>
