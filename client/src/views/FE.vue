<template>
  <div class="TSP">
    <v-row class="mt-4">
      <v-col cols="3">
        <!-- <h1 class="ma-3">Travelling Salesman problem</h1> -->
        <sidebar ref="sidebar" @run="run($event)" />
      </v-col>
      <v-col cols="8">
        <v-row>
          <v-col cols="6">
            <fchart :display="display" :chartData="scatterpoints" v-show="display == 'scatter'"></fchart>
            <dchart :display="display" :chartData="distpoints" v-show="display == 'dist'"></dchart>
            <v-sheet class="mx-auto mt-3">
              <v-btn-toggle v-model="display" mandatory color="primary" group>
                <v-btn height="30" value="dist">Distribution</v-btn>
                <v-btn height="30" value="scatter">Scatter</v-btn>
              </v-btn-toggle>
              <v-slider
                :disabled="solution == null"
                v-on:change="drawGraph"
                v-model="step"
                :max="maxStep"
                min="0"
                hide-details
              >
                <template v-slot:prepend>
                  <v-icon color="primary" @click="decrement">mdi-minus</v-icon>
                </template>
                <template v-slot:append>
                  <v-icon color="primary" @click="increment">mdi-plus</v-icon>
                </template>
              </v-slider>
            </v-sheet>
          </v-col>
          <v-col cols="6">
            <linechart :chartData="datacollection"></linechart>
            <v-sheet class="mx-auto mt-3" max-width="600">
              <v-select
                prepend-icon="mdi-function"
                v-model="chosen_problem"
                :hint="optimum"
                :items="problems"
                label="Pick a problem"
                item-text="name"
                persistent-hint
                return-object
                v-on:change="pick"
              ></v-select>
            </v-sheet>
          </v-col>
        </v-row>
        <div class="d-flex justify-end ma-10">
          <results :solved_data="solved_data" />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
import Sidebar from "@/components/Sidebar.vue";
import LineChart from "@/components/LineChart.vue";
import FireflyChart from "@/components/FireflyChart.vue";
import ResultsCard from "@/components/ResultsCard.vue";
import DistChart from "@/components/DistChart.vue";

export default {
  name: "FE",
  components: {
    sidebar: Sidebar,
    linechart: LineChart,
    fchart: FireflyChart,
    results: ResultsCard,
    dchart: DistChart
  },
  data() {
    return {
      display: "scatter",
      chosen_problem: {},
      problems: [],
      picked: false,
      solution: null,
      scatterpoints: null,
      scatter_data: null,
      step: 0,
      maxStep: 50,
      datacollection: null,
      dist_data: null,
      dist_labels: null,
      distpoints: null,
      min: NaN,
      max: NaN,
      solved_data: [],
      solved_headers: []
    };
  },
  computed: {
    optimum() {
      if (!this.picked) return "";
      return (
        "Optimum: " +
        (this.chosen_problem.minimize
          ? this.chosen_problem.minimum
          : this.chosen_problem.maximum)
      );
    }
  },
  methods: {
    increment() {
      if (this.step < this.maxStep) {
        this.step++;
        this.drawGraph();
      }
    },
    decrement() {
      if (this.step > 0) {
        this.step--;
        this.drawGraph();
      }
    },
    run(variables) {
      var entry = variables.reduce(
        (obj, item) => Object.assign(obj, { [item.name]: item.value }),
        {}
      );
      entry.problem = this.chosen_problem.name;
      const path = "/fe";
      axios
        .post(path, { variables: variables, problem: this.chosen_problem.name })
        .then(res => {
          this.datacollection = {
            ...this.fitnessGraph(),
            labels: res.data.labels,
            datasets: this.fitnessGraph().datasets.map((ds, i) => {
              return { ...ds, data: res.data.datasets[i].data };
            })
          };
          this.dist_data = res.data.distribution;
          this.dist_labels = res.data.dist_labels;
          this.scatter_data = res.data.points;
          this.step = 0;
          this.maxStep = res.data.points.length - 1;
          this.drawGraph();
          this.solution = res.data.best_solution;
          this.$refs.sidebar.loading = false;
          entry.best = this.solution;
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
            borderColor: "#4B4A5C"
          },
          {
            label: "mean",
            data: [],
            fill: "none",
            borderColor: "#F0AD9E"
          },
          {
            label: "min",
            data: [],
            fill: "none",
            borderColor: "#9594AE"
          }
        ]
      };
    },
    distGraph(data = [], labels = []) {
      return {
        labels: labels,
        datasets: [
          {
            label: "distribution",
            data: data,
            borderColor: "#4b4a5c",
            backgroundColor: "#9594ae"
          }
        ]
      };
    },
    scatterGraph(data = []) {
      return {
        datasets: [
          {
            data: data,
            borderWidth: 2,
            pointBackgroundColor: "#4b4a5c",
            borderColor: "#9594ae",
            pointRadius: 3,
            fill: false,
            tension: 0,
            showLine: false
          }
        ]
      };
    },
    drawGraph() {
      this.min = this.datacollection.datasets[2].data[this.step];
      this.max = this.datacollection.datasets[0].data[this.step];
      this.scatterpoints = this.scatterGraph(this.scatter_data[this.step]);
      this.distpoints = this.distGraph(
        this.dist_data[this.step],
        this.dist_labels
      );
    },
    getProblems() {
      const path = "/fe";
      axios
        .get(path)
        .then(res => {
          this.problems = res.data.problems;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    pick() {
      this.picked = true;
      this.$refs.sidebar.problem_picked = true;
    }
  },
  mounted() {
    this.getProblems();
    this.scatterpoints = this.scatterGraph();
    this.distpoints = this.distGraph();
  }
};
</script>