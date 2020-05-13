<template>
  <div class="TSP">
    <v-row class="mt-4">
      <v-col cols="3">
        <sidebar :disable="true" ref="sidebar" @run="run($event)" />
      </v-col>
      <v-col cols="8">
        <v-col>
          <linechart :chartData="datacollection"></linechart>
          <div class="d-flex justify-space-between">
            <p class="ma-2">
              {{solution}}
              <b>{{satisfiable}}</b>
            </p>
            <v-sheet width="600">
              <v-select
                prepend-icon="mdi-ampersand"
                v-model="chosen_problem"
                :hint="hint"
                :items="problems"
                label="Pick a problem"
                item-text="name"
                persistent-hint
                return-object
                v-on:change="pick"
              ></v-select>
            </v-sheet>
          </div>
          <div class="d-flex justify-end ma-10">
            <results :solved_data="solved_data" />
          </div>
        </v-col>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
import Sidebar from "@/components/Sidebar.vue";
import LineChart from "@/components/LineChart.vue";
import ResultsCard from "@/components/ResultsCard.vue";

export default {
  name: "SAT",
  components: {
    sidebar: Sidebar,
    linechart: LineChart,
    results: ResultsCard
  },
  computed: {
    hint() {
      if (!this.picked) return "";
      return (
        "variables: " +
        this.chosen_problem.nv +
        "  clauses: " +
        this.chosen_problem.clauses
      );
    }
  },
  data() {
    return {
      chosen_problem: {},
      problems: [],
      solution: "",
      satisfiable: "",
      problem_id: null,
      datacollection: null,
      picked: false,
      solved_data: [],
      solved_headers: []
    };
  },
  methods: {
    clearGraphs() {
      this.datacollection = null;
    },
    run(variables) {
      var entry = variables.reduce(
        (obj, item) => Object.assign(obj, { [item.name]: item.value }),
        {}
      );
      entry.problem = this.chosen_problem.name;
      const path = "http://localhost:5000/sat";
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
          entry.best = res.data.best_solution;
          this.solved_data.push(entry);

          this.solution = res.data.best_solution + " clauses true: ";
          console.log(res.data.satisfiable);
          this.satisfiable = res.data.satisfiable
            ? "Satisfiable"
            : "Couldn't satisfy all clauses";
          this.$refs.sidebar.loading = false;
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
    getProblems() {
      const path = "http://localhost:5000/sat";
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
  }
};
</script>