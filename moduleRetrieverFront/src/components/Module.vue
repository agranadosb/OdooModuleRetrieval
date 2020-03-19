<template>
    <div class="row">
        <div class="col-6 card" style="padding:10px;">
            <h1>Module Info</h1>
            <hr>
            <div>
                <ul class="list-group">
                    <li class="list-group-item list-group-item-dark">Tecnical Name: <b>{{ moduleOdoo['tecName'] }}</b></li>
                    <li class="list-group-item list-group-item-dark">Name: <b>{{ moduleOdoo['name'] }}</b></li>
                    <li class="list-group-item list-group-item-dark">Path: <b>{{ moduleOdoo['path'] }}</b></li>
                    <li class="list-group-item list-group-item-dark">Found: <b>{{ moduleOdoo['found'] }}</b></li>
                </ul>
            </div>
        </div>
        <div class="col-6 card">
            <div class="col-12" v-if="moduleOdoo['depends'].length != 0">
                <h1>Dependences</h1>
                <hr>

                <div class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Dependences</a>
                    <div class="dropdown-menu">
                        <span v-for="dep in moduleOdoo['depends']" class="dropdown-item moduleName" v-on:click="emitSearch(dep)">
                            {{ dep }}
                        </span>
                    </div>
                </div>
            </div>
            <div class="col-12" v-if="moduleOdoo['sons'].length != 0" style="margin-top:10px;">
                <h1>Sons</h1>
                <hr>

                <div class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Dependences</a>
                    <div class="dropdown-menu">
                        <span v-for="dep in moduleOdoo['sons']" class="dropdown-item moduleName" v-on:click="emitSearch(dep)">
                            {{ dep }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  props: ['moduleOdoo'],
  methods: {
      emitSearch: function(name) {
          console.log(name);
          this.$emit('searchModule', name);
      }
  }
}
</script>

<style>
    .moduleName:hover {
        cursor: pointer;
    }
</style>
