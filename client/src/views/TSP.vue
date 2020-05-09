<template>
  <div class="TSP">
    <v-row class="mt-4">
      <v-col cols="3">
        <!-- <h1 class="ma-3">Travelling Salesman problem</h1> -->
        <sidebar ref="sidebar" @run="run($event)" />
      </v-col>
      <v-col cols="9">
        <v-row>
          <v-col cols="5">
            <cartchart :chartData="tspdata"></cartchart>
            <v-sheet width="500">
              <p class="ma-5">
                {{this.solution}}
              </p>
            </v-sheet>
          </v-col>
          <v-col cols="6">
            <linechart :chartData="datacollection"></linechart>
            <div class="d-flex justify-end">
              <v-sheet width="500">
                <v-select
                  prepend-icon="mdi-map"
                  v-model="chosen_problem"
                  :hint="hint"
                  :items="problems"
                  label="Pick a problem"
                  item-text="cities"
                  persistent-hint
                  return-object
                  v-on:change="pick"
                ></v-select>
              </v-sheet>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <div class="d-flex justify-end ma-10">
          <results :solved_data="solved_data" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Sidebar from "@/components/Sidebar.vue";
import LineChart from "@/components/LineChart.vue";
import CartesianChart from "@/components/CartesianChart.vue";
import ResultsCard from "@/components/ResultsCard.vue";
// import ProblemBar from "@/components/ProblemBar.vue";

export default {
  name: "TSP",
  components: {
    sidebar: Sidebar,
    linechart: LineChart,
    cartchart: CartesianChart,
    results: ResultsCard
  },
  data() {
    return {
      picked: false,
      solution: null,
      chosen_problem: {},
      problems: [],
      problem_id: null,
      tspdata: null,
      datacollection: null,
      solved_data: [],
      solved_headers: []
    };
  },
  computed: {
    hint() {
      if (!this.picked) return "";
      return "Optimum: " + this.chosen_problem.optimum;
    }
  },
  methods: {
    clearGraphs() {
      this.datacollection = null;
      this.tspdata = null;
    },
    run(variables) {
      var entry = variables.reduce(
        (obj, item) => Object.assign(obj, { [item.name]: item.value }),
        {}
      );
      entry.problem = this.chosen_problem.name;
      const path = "http://localhost:5000/tsp";
      axios
        .post(path, {
          variables: variables,
          problem: this.chosen_problem.index
        })
        .then(res => {
          this.datacollection = {
            ...this.fitnessGraph(),
            labels: res.data.labels,
            datasets: this.fitnessGraph().datasets.map((ds, i) => {
              return { ...ds, data: res.data.datasets[i].data };
            })
          };
          this.tspdata = {
            ...this.tspGraph(),
            datasets: this.tspGraph().datasets.map(ds => {
              return {
                ...ds,
                data: res.data.route
              };
            })
          };
          entry.best = this.solution;
          this.solution = "Tour length: " + (
            Math.round(res.data.best_solution * 100) / 100
          ).toFixed(2);
          this.$refs.sidebar.loading = false;
          this.solved_data.push(entry);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    fitnessGraph() {
      return {
        labels: [],
        datasets: [
          {
            label: "max",
            data: [],
            fill: "none",
            borderColor: "#d18b19"
          },
          {
            label: "mean",
            data: [],
            fill: "none",
            borderColor: "#609e94"
          },
          {
            label: "min",
            data: [],
            fill: "none",
            borderColor: "#604280"
          }
        ]
      };
    },
    tspGraph() {
      return {
        datasets: [
          {
            data: [],
            borderWidth: 2,
            // borderColor: '#064380',
            pointRadius: 1,
            fill: false,
            tension: 0,
            showLine: true
          }
        ]
      };
    },
    pick() {
      this.picked = true;
      this.$refs.sidebar.problem_picked = true;
    },
    getProblems() {
      const path = "http://localhost:5000/tsp";
      axios
        .get(path)
        .then(res => {
          this.problems = res.data.problems;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  mounted() {
    this.tspdata = this.tspGraph();
    this.datacollection = this.fitnessGraph();
    this.getProblems();
  }
};
</script>