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
          <app-module :moduleOdoo="data" @searchModule="onSearchModule" @nameClicked="onNameClicked"></app-module>
        </div>
      </div>
    </div>
    <div v-if="nodes.length != 0" class="col-12" style="margin:10px;">
      <div class="row">
        <div class="col-6 overflow-auto">
          <h1>Sons</h1>
          <vue2-org-tree
            :data="treeDataSons"
            :horizontal="true"
            :collapsable="true"
            :renderContent="renderContent"
            @on-expand="onExpand"
            @on-node-click="onNodeClick"/>
        </div>
        <div class="col-6 overflow-auto">
          <h1>Depends</h1>
          <vue2-org-tree
            :data="treeDataDepends"
            :horizontal="true"
            :collapsable="true"
            :renderContent="renderContent"
            @on-expand="onExpand"
            @on-node-click="onNodeClick"/>
        </div>
      </div>
      <hr>
      <d3-network ref='net' :net-nodes="nodes" :net-links="links" :options="options" style="width:100%;"/>
    </div>
  </div>
</template>

<script>
import Module from './components/Module.vue';
import D3Network from 'vue-d3-network';
import Vue2OrgTree from 'vue2-org-tree';


export default {
  name: 'app',
  data () {
    return {
      res: {},
      search: '',
      searchEquals: false,
      nodes: [],
      links: [],
      netShowed: false,
      nodeSize: 20,
      canvas: false,
      treeDataSons: {},
      treeDataDepends: {},
    }
  },
  methods: {
    showNet() {
      this.axios.post('http://localhost:5000/moduleNet', this.search).then(response => {
        this.nodes = response['data']['nodes']
        this.links = response['data']['links']
      });

      this.axios.post('http://localhost:5000/moduleTree', this.search).then(response => {
        this.treeDataSons = response['data']['sons']
        this.treeDataDepends = response['data']['depends']
      });

      this.netShowed = true;
      this.searchEquals = true;
    },
    hideNet() {
      this.nodes = [];
      this.links = [];

      this.netShowed = false;
    },
    getModules() {
      this.axios.get('http://localhost:5000/info').then(response => (
        this.res = response
      ));

      this.search = '';
      this.searchEquals = false;
      this.hideNet();
    },
    onSearchModule(toSearch) {
      this.search = toSearch;
      this.hideNet();
    },
    onNameClicked(name) {
      this.search = name;
      this.searchEquals = true;
      this.hideNet();
    },
    renderContent: function(h, data) {
      return data.label
    },
    onExpand: function(e, node) {
      node.expand = !node.expand
      // Para cuando se actualiza un hijo
      this.$forceUpdate();
    },
    onNodeClick: function(e, data) {
      //console.log(this.treeData)
      //alert(data.label)
    }   
  },
  components: {
    appModule: Module,
    D3Network,
    Vue2OrgTree
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
