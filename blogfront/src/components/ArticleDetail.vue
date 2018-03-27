<template>
    <div>
        <p>{{ msg }}</p>
        <p>{{ $route.params.id }}</p>
        <p>{{article.content}}</p>
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
          } else {
            this.$message.error('get articles error!')
            console.log(res.message)
          }
        })
    }
  }
}
</script>
