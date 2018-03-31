<template>
    <el-row type="flex" class="row-bg">
      <el-col :span="4"><div class="grid-content bg-purple">
          <p class="header-title" @click="goToIndex">{{ msg }}</p>
      </div></el-col>
      <el-col :span="16"><div class="grid-content bg-purple-light">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">首页</el-menu-item>
          <el-menu-item index="3" disabled>消息中心</el-menu-item>
          <el-menu-item index="4"><a href="https://www.ele.me" target="_blank">个人信息</a></el-menu-item>
        </el-menu>
      </div></el-col>
      <el-col :span="4"><div class="grid-content bg-purple">
          <el-button class="header-login" round>login</el-button>
      </div></el-col>
    </el-row>
</template>

<script>
export default {
  name: 'Header',
  data () {
    return {
      msg: 'Feng\'s blog',
      activeIndex: '1',
      headerLogin: 'header-login'
    }
  },
  methods: {
    handleSelect () {
      console.log('hello')
    },
    goToIndex () {
      var _this = this
      setTimeout(function () {
        _this.$router.push({path: '/'})
      }, 2000)
    }
  }
}
</script>

<style>
  .row-bg {
    background-color: #fefffa;
    max-height: 60px;
  }
  .header-title {
    color: #ea6f6f;
    font-size: 20px;
    text-align: left;
    vertical-align: middle;
    font-weight: 600;
    cursor: pointer;
  }
  .header-login {
    color: #ea6f6f;
    background-color: #fff;
    border-color: #ea6f6f;
    vertical-align: bottom;
    text-align: right;
    margin-left: 60px;
    margin-top: 10px;
  }
</style>
