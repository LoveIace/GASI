<template>
  <div class="home">
    <v-row>
      <v-col cols="3"></v-col>
      <v-col cols="6" class="grey lighten-4">
        <v-row class="text-center">
          <v-col class="d-flex align-end" cols="4">
            <h1 class="ml-4 display-1">Genetic algorithm</h1>
          </v-col>
          <v-col cols="4">
            <h1 class="display-4 font-weight-bold text-center">GASI</h1>
          </v-col>
          <v-col class="d-flex align-end" cols="4">
            <h1 class="display-1">Swarm intelligence</h1>
          </v-col>
        </v-row>
        <div class="primary text-center">
          <span class="white--text">
            <h1 class="display-1 pa-3">CLIENT SIDE</h1>
          </span>
        </div>
        <v-row>
          <v-col class="d-flex justify-center" cols="4">
            <img alt="Vue logo" src="../assets/vue-logo.svg" width="80%" />
          </v-col>
          <v-col class="d-flex justify-center" cols="4">
            <img alt="Chartjs logo" src="../assets/chartjs-logo.svg" width="100%" />
          </v-col>
          <v-col class="d-flex justify-center" cols="4">
            <img alt="Vuetify logo" src="../assets/logo.svg" width="60%" />
          </v-col>
        </v-row>
        <div class="primary text-center">
          <span class="white--text">
            <h1 class="display-1 pa-3">VISUALIZE</h1>
          </span>
        </div>
        <div class="ma-10">
          <p>
            This web application serves as a means to visualize fitness progress of Evolutionary
            algorithms. Implemented algorithms at the moment are firefly and genetic algorithm.
            Currently capable of solving 3 categories of optimization problems - the travelling
            salesman problem, satisfiability problem and search for global function extremes.
          </p>
        </div>
      </v-col>
      <v-col cols="3"></v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "Home"
};
</script>

<style scoped>
</style>