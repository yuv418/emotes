<template>
  <div id="app">
    <link rel="stylesheet" type="text/css" href="./styles/style.css"/>
    <Navbar/>
    <Search/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Search from './components/Search.vue'
export default {
  name: 'App',
  components: {
    Navbar,
    Search
  }
}
</script>


<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 960px;
  margin: 0 auto;
  height: auto;
}

#app h1, h2, h3, h4, h5, h6 {
  font-family: Montserrat;
}
#app p,a{
  font-family: Raleway;
}
body{
  margin:0;
  padding:0;
}
</style>
