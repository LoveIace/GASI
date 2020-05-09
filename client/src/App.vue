<template>
  <v-app>
    <v-app-bar app dense color="primary" dark>
      <v-btn text large to="/" class="ma-5">
        <v-icon>mdi-home</v-icon>
        <span>GA|SI</span>
      </v-btn>
      <v-tabs>
        <v-tab to="/SAT">
          <span>Satisfiability</span>
          <v-icon>mdi-format-letter-matches</v-icon>
        </v-tab>
        <v-tab to="/TSP">
          <span>Travelling Salesman</span>
          <v-icon>mdi-graphql</v-icon>
        </v-tab>
        <v-tab to="/FE">
          <span>Function Extreme</span>
          <v-icon>mdi-function-variant</v-icon>
        </v-tab>
      </v-tabs>
      <v-spacer></v-spacer>

      <v-btn href="https://github.com/vuetifyjs/vuetify/releases/latest" target="_blank" text>
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
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