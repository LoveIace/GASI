<template>
  <div>
    <v-card :loading="loading" max-width="400" class="mx-auto">
      <v-card-title class="pb-0">Algo variables</v-card-title>
      <v-list>
        <v-list-item v-for="item in sliders" :key="item.name">
          <v-list-item-content class="pa-4">
            <v-list-item-title v-text="item.name"></v-list-item-title>
            <v-slider
              v-model="item.value"
              :step="item.step"
              :max="item.max"
              :min="item.min"
              hide-details
            >
              <template v-slot:append>
                <v-text-field
                  v-model="item.value"
                  class="mt-0 pt-0"
                  hide-details
                  single-line
                  type="number"
                  style="width: 70px"
                ></v-text-field>
              </template>
            </v-slider>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-for="item in selects" :key="item.name">
          <v-select
            v-model="item.value"
            :items="item.values"
            :label="item.name"
            class="pa-4"
          ></v-select>
        </v-list-item>
        <v-list-item v-for="item in switches" :key="item.name">
          <v-switch
            class="pl-4"
            v-model="item.value"
            :label="item.name"
          ></v-switch>
        </v-list-item>
      </v-list>

      <v-card-actions>
        <v-btn-toggle v-model="algo" mandatory color="primary" group>
          <v-btn value="genetic">Genetic</v-btn>
          <v-btn :disabled="disable" value="firefly">Firefly</v-btn>
        </v-btn-toggle>
        <v-spacer />
        <v-btn
          class="ma-2"
          :loading="loading"
          :disabled="loading || !problem_picked"
          color="primary"
          @click="run"
        >
          Run
          <template v-slot:loader>
            <span>...</span>
          </template>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
  props: ["disable"],
  data() {
    return {
      chosen_problem: {},
      problem_picked: false,
      loading: false,
      firefly: {
        variables: [
          {
            name: "Iteration ceiling",
            value: 50,
            min: 10,
            max: 500,
            type: "slider",
            step: 10
          },
          {
            name: "Population size",
            value: 25,
            min: 10,
            max: 80,
            type: "slider"
          },
          {
            name: "Alpha",
            value: 1,
            min: 0,
            max: 10,
            type: "slider",
            step: 0.1
          },
          {
            name: "Beta",
            value: 0.6,
            min: 0,
            max: 1,
            type: "slider",
            step: 0.1
          },
          {
            name: "Gamma",
            value: 0.0005,
            min: 0,
            max: 1,
            type: "slider",
            step: 0.00001
          },
          {
            name: "Delta",
            value: 0.97,
            min: 0,
            max: 1,
            type: "slider",
            step: 0.001
          }
        ]
      },
      genetic: {
        variables: [
          {
            name: "Generation ceiling",
            value: 100,
            min: 10,
            max: 1000,
            type: "slider"
          },
          {
            name: "Population size",
            value: 50,
            min: 10,
            max: 200,
            type: "slider"
          },
          {
            name: "Mutation rate",
            value: 0.1,
            min: 0,
            max: 1,
            type: "slider",
            step: 0.01
          },
          {
            name: "Selection type",
            value: "Tournament",
            values: ["Roulette", "Tournament", "Uniform"],
            type: "select"
          },
          {
            name: "Elitism",
            value: 0.02,
            min: 0,
            max: 1,
            type: "slider",
            step: 0.01
          }
        ]
      },
      algo: "genetic"
    };
  },
  computed: {
    enabled(name) {
      return this.algorithms.contains(name) ? true : false;
    },
    selects() {
      return this[this.algo].variables.filter(
        variable => variable.type == "select"
      );
    },
    sliders() {
      return this[this.algo].variables.filter(
        variable => variable.type == "slider"
      );
    },
    switches() {
      return this[this.algo].variables.filter(
        variable => variable.type == "switch"
      );
    }
  },
  methods: {
    run() {
      this.loading = true;
      this.$emit(
        "run",
        this[this.algo].variables.concat({
          name: "Algorithm",
          value: this.algo
        })
      );
    }
  }
};
</script>
