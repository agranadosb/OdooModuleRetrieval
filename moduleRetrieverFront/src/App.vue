<template>
  <div id="app">
    <div>
      <h1>Odoo Module Tracker</h1>
      <hr>
    </div>
    <div class="search-wrapper" style="margin-bottom:10px;">
      <input type="text" v-model="search" placeholder="Search module.." style="margin-right:5px;width:300px;"/>
      <button @click="getModules" class="btn btn-primary">GetModules</button>
      <button v-if="!searchEquals" @click="searchEquals = true" class="btn btn-primary">Equals</button>
      <button v-if="searchEquals" @click="searchEquals = false" class="btn btn-primary">Similars</button>
    </div>
    <div class="container" v-for="data in moduleList" style="margin-bottom:10px;padding:20px;">
      <app-module :moduleOdoo="data" @searchModule="onSearchModule"></app-module>
    </div>
    <d3-network ref='net' :net-nodes="nodes" :net-links="links" :options="options" />
  </div>
</template>

<script>
import Module from './components/Module.vue';
import D3Network from 'vue-d3-network';

export default {
  name: 'app',
  data () {
    return {
      res: {},
      search: '',
      searchEquals: false,
      nodes: [
            {id: 1, name:'base'},
            {id: 2, name:'account'}
        ],
      links: [
        {sid: 1, tid: 2, _color: 'red'},
      ],
      nodeSize:20,
      canvas:false
    }
  },
  methods: {
    getModules() {
      this.axios.get('http://localhost:5000/').then(response => (
        this.res = response
      ))
    },
    onSearchModule(toSearch) {
      console.log(toSearch);
      
      this.search = toSearch
    }
  },
  components: {
    appModule: Module,
    D3Network
  },
  computed: {
    moduleList() {
      let moduleListRes = []
      for (let i in this.res['data']) {
        if (this.searchEquals && i === this.search)
          moduleListRes.push(this.res['data'][i])
        if (!this.searchEquals && i.includes(this.search))
          moduleListRes.push(this.res['data'][i])
      }

      return moduleListRes
    },
    options(){
      return{
        force: 3000,
        size:{ w:600, h:600},
        nodeSize: this.nodeSize,
        nodeLabels: true,
        linkLabels:true,
        canvas: this.canvas
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
