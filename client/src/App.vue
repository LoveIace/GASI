<template>
  <v-app>
    <v-app-bar app dense color="primary" dark>
      <v-btn text large to="/" class="ma-5">
        <v-icon>mdi-home</v-icon>
        <span>GA|SI</span>
      </v-btn>
      <v-tabs class="ml-10">
        <v-tab to="/SAT">
          <span>SAT</span>
          <v-icon>mdi-format-letter-matches</v-icon>
        </v-tab>
        <v-tab to="/TSP">
          <span>TSP</span>
          <v-icon>mdi-graphql</v-icon>
        </v-tab>
        <v-tab to="/FE">
          <span>FE</span>
          <v-icon>mdi-function-variant</v-icon>
        </v-tab>
      </v-tabs>
    </v-app-bar>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      activeBtn: 1,
      showNav: true
    };
  }
};
</script>
