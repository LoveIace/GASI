<template>
    <v-sheet
      class="mx-auto mt-3"
      max-width="600"
    >
      <v-select
          prepend-icon=mdi-map
          v-model="chosen_problem"
          :hint="`optimum: ${chosen_problem.optimum}`"
          :items="problems"
          label="Pick a problem"
          item-text="cities"
          persistent-hint
          return-object
          v-on:change="pick"
        ></v-select>
    </v-sheet>
</template>

<script>
export default {
  // props: [problems],
  data: () => ({
    chosen_problem: {},
    problems: [
      {
        id:1,
        cities:"29 cities",
        optimum:27603
      },
      {
        id:2,
        cities:"194 cities",
        optimum:9352
      },
      {
        id:3,
        cities:"929 cities",
        optimum:95345
      },
      {
        id:4,
        cities:"980 cities",
        optimum:11340
      },
      {
        id:5,
        cities:"38 cities",
        optimum:6656
      },
      {
        id:6,
        cities:"9152 cities",
        optimum:837479
      },
      {
        id:7,
        cities:"7146 cities",
        optimum:172387
      },
      {
        id:8,
        cities:"734 cities",
        optimum:79114
      },
      {
        id:9,
        cities:"71009 cities",
        optimum:4566563
      }
    ]
  }),
  methods: {
    pick(){
      this.$emit('input', this.chosen_problem.id)
    }
  }
};
</script>