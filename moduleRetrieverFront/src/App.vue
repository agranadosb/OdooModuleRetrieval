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
      <button v-if="!netShowed" @click="showNet" class="btn btn-primary">Show Net</button>
      <button v-if="netShowed" @click="hideNet" class="btn btn-primary">Hide Net</button>
    </div>
    <div id="accordion" style="margin-bottom:10px;">
      <div class="" v-for="data in moduleList">
        <div class="card-header" :id="'heading' + data['tecName']">
          <button class="btn collapsed" data-toggle="collapse" :data-target="'#collapse' + data['tecName']" aria-expanded="true" :aria-controls="'collapse' + data['tecName']" style="width:100%;">
            {{ data['tecName'] }}
          </button>
        </div>
        <div :id="'collapse' + data['tecName']" class="collapse" :aria-labelledby="'heading' + data['tecName']" data-parent="#accordion">
          <app-module :moduleOdoo="data" @searchModule="onSearchModule"></app-module>
        </div>
      </div>
    </div>
    <div v-if="nodesSearchShow.length != 0" class="col-12 border border-primary" style="margin:10px;">
      <d3-network ref='net' :net-nodes="nodesSearchShow" :net-links="linksSearchShow" :options="options" style="width:100%;"/>
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
      nodesSearch: [],
      linksSearch: [],
      nodesSearchShow: [],
      linksSearchShow: [],
      netShowed: false,
      nodeSize:20,
      canvas:false
    }
  },
  methods: {
    showNet() {
      let nodesList = []
      let linksList = []

      for (let i in this.links) {
        if (this.searchEquals && (this.links[i]['sid'] === this.search || this.links[i]['tid'] === this.search)){
          linksList.push(this.links[i])
          if(!nodesList.some(e => e.id == this.links[i]['sid'])) {
            nodesList.push({id: this.links[i]['sid'], name: this.links[i]['sid']})
          }
          if(!nodesList.some(e => e.id == this.links[i]['tid'])) {
            nodesList.push({id: this.links[i]['tid'], name: this.links[i]['tid']})
          }
        } else if (!this.searchEquals && (this.links[i]['sid'].includes(this.search) || this.links[i]['tid'].includes(this.search))){
          linksList.push(this.links[i])
          if(!nodesList.some(e => e.id == this.links[i]['sid'])) {
            nodesList.push({id: this.links[i]['sid'], name: this.links[i]['sid']})
          }
          if(!nodesList.some(e => e.id == this.links[i]['tid'])) {
            nodesList.push({id: this.links[i]['tid'], name: this.links[i]['tid']})
          }
        }
      }

      this.nodesSearch = nodesList
      this.linksSearch = linksList

      this.nodesSearchShow = this.nodesSearch;
      this.linksSearchShow = this.linksSearch;
      this.netShowed = true;
    },
    hideNet() {
      this.nodesSearchShow = [];
      this.linksSearchShow = [];
      this.netShowed = false;
    },
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
      this.hideNet();
    },
    onSearchModule(toSearch) {
      console.log(toSearch);
      
      this.search = toSearch;
      this.hideNet();
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
        if (this.searchEquals && i === this.search){
          moduleListRes.push(this.res['data'][i])
        } else if (!this.searchEquals && i.includes(this.search)){
          moduleListRes.push(this.res['data'][i])
        }
      }

      this.hideNet();

      return moduleListRes
    },
    options(){
      return{
        force: 3000,
        size:{h:1300},
        nodeSize: this.nodeSize,
        nodeLabels: true,
        linkLabels: true,
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
