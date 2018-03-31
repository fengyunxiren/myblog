<template>
  <div>
    <div class="detail-info">
      <p class="detail-title">{{ article.title }}</p>
      <p class="detail-author">
          <span>
              <i class="el-icon-edit-outline"></i>
              {{ article.author }}
          </span>
          <span>
              <i class="el-icon-time"></i>
              {{ article.update_time }}
          </span>
      </p>
    </div>
    <mavon-editor class="detail-editor"
      v-model="article.content"
      defaultOpen="preview"
      :subfield="false"
      :editable="false"
      :toolbarsFlag="false"
      :ishljs="true"
      ></mavon-editor>
  </div>
</template>

<script>
export default {
  name: 'ArticleDetail',
  data () {
    return {
      msg: 'Feng\'s blog',
      article: {}
    }
  },
  mounted: function () {
    this.showArticles()
  },
  methods: {
    showArticles () {
      var id = ''
      id = this.$route.params.id
      this.$http.get('http://127.0.0.1:8000/blog/article/' + id + '/')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.result === true) {
            this.article = res.data
            this.article.update_time = this.transDate(this.article.update_time)
          } else {
            this.$message.error('get articles error!')
            console.log(res.message)
          }
        })
    },
    transDate (timeString) {
      var newString = ''
      newString = timeString.replace(/T/, ' ')
      newString = newString.split('.')[0]
      return newString
    }
  }
}
</script>

<style>
  .detail-info {
    background-color: #fff;
  }
  .detail-title {
    margin-top: 20px;
    margin-bottom: 0px;
    color: #000;
    font-weight: 600;
    font-size: 60px;
    cursor: pointer;
  }
  .detail-author {
    margin-top: 15px;
    margin-bottom: 0px;
    font-size: 12px;
    color: #372d30;
    text-align: left;
    text-indent: 6px;
  }
</style>
