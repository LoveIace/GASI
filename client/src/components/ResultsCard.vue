<template>
  <v-data-table 
    dense 
    :headers="headers" 
    :items="runs" 
    item-key="name" 
    class="elevation-0"
    :items-per-page="5"
    group-by="Algorithm"
  />
</template>

<script>
export default {
  name: "ResultsCard",
  props: ["solved_data"],
  data() {
    return {
      runs: [],
      headers: [
        {
          text: "Algorithm",
          align: "start",
          value: "Algorithm"
        },
        { text: "Problem", value: "problem" },
        { text: "Iteration ceiling", value: "Iteration ceiling" },
        { text: "Generation ceiling", value: "Generation ceiling" },
        { text: "Population size", value: "Population size" },
        { text: "Alpha", value: "Alpha" },
        { text: "Beta", value: "Beta" },
        { text: "Gamma", value: "Gamma" },
        { text: "Delta", value: "Delta" },
        { text: "Mutation rate", value: "Mutation rate" },
        { text: "Selection type", value: "Selection type" },
        { text: "Elitism", value: "Elitism" },
        { text: "Best result", value: "best" }
      ]
    };
  },
  watch: {
    solved_data(newData) {
      this.runs = newData;
    }
  }
};
</script>
