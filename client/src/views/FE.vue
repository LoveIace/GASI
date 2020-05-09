<template>
  <div class="TSP">
    <v-row class="mt-4">
      <v-col cols="3">
        <!-- <h1 class="ma-3">Travelling Salesman problem</h1> -->
        <sidebar ref="sidebar" @run="run($event)" />
      </v-col>
      <v-col cols="9">
        <v-row>
          <v-col cols="4">
            <fchart :chartData="scatterpoints"></fchart>
            <v-sheet v-if="solution != null" max-width="300" class="mx-auto mt-3">
              <p class="text-center">
                max:
                <b>{{this.max}}</b>
              </p>
              <p class="text-center">
                min:
                <b>{{this.min}}</b>
              </p>
              <v-slider
                v-on:change="drawScatterGraph"
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
// import ProblemBar from '@/components/ProblemBar.vue'

export default {
  name: "FE",
  components: {
    sidebar: Sidebar,
    linechart: LineChart,
    fchart: FireflyChart,
    results: ResultsCard
    // pbar: ProblemBar
  },
  data() {
    return {
      chosen_problem: {},
      problems: [],
      picked: false,
      solution: null,
      scatterpoints: null,
      scatter_data: null,
      step: 0,
      maxStep: 0,
      datacollection: null,
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
        this.drawScatterGraph();
      }
    },
    decrement() {
      if (this.step > 0) {
        this.step--;
        this.drawScatterGraph();
      }
    },
    run(variables) {
      var entry = variables.reduce(
        (obj, item) => Object.assign(obj, { [item.name]: item.value }),
        {}
      );
      entry.problem = this.chosen_problem.name;
      const path = "http://localhost:5000/fe";
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
          this.scatter_data = res.data.points;
          this.step = 0;
          this.maxStep = res.data.points.length - 1;
          this.drawScatterGraph();
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
    scatterGraph() {
      return {
        datasets: [
          {
            data: [],
            borderWidth: 2,
            pointBackgroundColor: "#1976D2",
            borderColor: "#1976D2",
            pointRadius: 2,
            fill: false,
            tension: 0,
            showLine: false
          }
        ]
      };
    },
    drawScatterGraph() {
      this.min = this.datacollection.datasets[2].data[this.step];
      this.max = this.datacollection.datasets[0].data[this.step];

      this.scatterpoints = {
        ...this.scatterGraph(),
        datasets: this.scatterGraph().datasets.map(ds => {
          return {
            ...ds,
            data: this.scatter_data[this.step]
          };
        })
      };
    },
    getProblems() {
      const path = "http://localhost:5000/fe";
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
  }
};
</script>