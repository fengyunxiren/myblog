<template>
    <div>
        <div class="demo-input-suffix">
            标题:
            <el-input v-model="title" max-length="200px"></el-input>
        </div>
        <div class="demo-input-suffix">
            作者:
            <el-input v-model="author"></el-input>
        </div>
        <mavon-editor
          v-model="content"
          :defaultOpen="defaultOpen"
          :subfield="false"
          :ishljs="true"
          @save="saveArticle">
        </mavon-editor>
    </div>
</template>

<script>
export default {
  name: 'CreateArticle',
  data () {
    return {
      defaultOpen: 'edit',
      title: '',
      author: '',
      content: '',
      id: ''
    }
  },
  methods: {
    saveArticle () {
      var postData
      postData = {
        title: this.title,
        abstract: 'test',
        author: '1',
        category: '1',
        content: this.content

      }
      console.log(postData)
      if (this.id !== '') {
        var putData
        putData = {
          title: this.title,
          abstract: 'test',
          content: this.content
        }
        this.$http.put('http://127.0.0.1:8000/blog/article/' + this.id + '/', putData, {emulateJSON: true})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.result === true) {
              this.defaultOpen = 'preview'
            } else {
              this.$message.error(res.message)
            }
          })
      } else {
        this.$http.post('http://127.0.0.1:8000/blog/article/', postData, {emulateJSON: true})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.result === true) {
              this.id = res.data.id
              this.defaultOpen = 'preview'
            } else {
              this.$message.error(res.message)
              console.log(res.message)
            }
          })
      }
    }
  }
}
</script>
