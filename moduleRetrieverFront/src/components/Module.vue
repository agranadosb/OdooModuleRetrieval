<template>
    <div class="row">
        <div class="col-6 card" style="padding:10px;">
            <h1>Module Info</h1>
            <hr>
            <div>
                <ul class="list-group text-left">
                    <li class="list-group-item list-group-item-dark">
                        <div class="row">
                            <div class="col-4">Tecnical Name:</div>
                            <div class="col-8"><b v-on:click="emitClickName(moduleOdoo['tecName'])" class="moduleName">{{ moduleOdoo['tecName'] }}</b></div>
                        </div>
                    </li>
                    <li class="list-group-item list-group-item-dark">
                        <div class="row">
                            <div class="col-4">Name:</div>
                            <div class="col-8"><b>{{ moduleOdoo['name'] }}</b></div>
                        </div>
                    </li>
                    <li class="list-group-item list-group-item-dark">
                        <div class="row">
                            <div class="col-4">Path:</div>
                            <div class="col-8"><b>{{ moduleOdoo['path'] }}</b></div>
                        </div>
                    </li>
                    <li class="list-group-item list-group-item-dark">
                        <div class="row">
                            <div class="col-4">Found:</div>
                            <div class="col-8"><b>{{ moduleOdoo['found'] }}</b></div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <div class="col-6">
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
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Sons</a>
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
            this.$emit('searchModule', name);
        },
        emitClickName: function(name) {
            this.$emit('nameClicked', name);
        }
  }
}
</script>

<style>
    .moduleName:hover {
        cursor: pointer;
    }
</style>
