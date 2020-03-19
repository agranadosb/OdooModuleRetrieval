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
    <div class="container" v-for="data in moduleList.modules" style="margin-bottom:10px;padding:20px;">
      <app-module :moduleOdoo="data" @searchModule="onSearchModule"></app-module>
    </div>
    <div class="col-12">
      <d3-network ref='net' :net-nodes="moduleList.nodes" :net-links="moduleList.links" :options="options" style="width:100%;"/>
    </div>
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
      nodes: [],
      links: [],
      nodeSize:20,
      canvas:false
    }
  },
  methods: {
    getModules() {
      this.axios.get('http://localhost:5000/info').then(response => (
        this.res = response
      ));
      this.axios.get('http://localhost:5000/links').then(response => (
        this.links = response['data']
      ));
      
      this.axios.get('http://localhost:5000/nodes').then(response => (
        this.nodes = response['data']
      ));
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
      let nodesList = []
      let linksList = []

      for (let i in this.links) {
        console.log(i)
        if (this.searchEquals && (this.links[i]['sid'] === this.search || this.links[i]['tid'] === this.search)){
          linksList.push(this.links[i])
        } else if (!this.searchEquals && (this.links[i]['sid'].includes(this.search) || this.links[i]['tid'].includes(this.search))){
          linksList.push(this.links[i])
        }
      }

      for (let i in this.res['data']) {
        if (this.searchEquals && i === this.search){
          moduleListRes.push(this.res['data'][i])
        } else if (!this.searchEquals && i.includes(this.search)){
          moduleListRes.push(this.res['data'][i])
        }
      }
      console.log(linksList);
      
      return {modules: moduleListRes, links: linksList, nodes: this.nodes}
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
