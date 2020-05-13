<script>
import { Scatter, mixins } from "vue-chartjs";

export default {
  extends: Scatter,
  mixins: [mixins.reactiveProp],
  props: ["chartData"],
  data() {
    return {
      options: {
        animation: {
          duration: 200,
          easing: 'linear'
        },
        legend: false,
        tooltips: false,
        scales: {
          xAxes: [
            {
              display: false,
              ticks: {
                min: 0,
                max: 10
              },
              gridLines: {
                color: "#888",
                drawOnChartArea: false
              }
            }
          ],
          yAxes: [
            {
              display: false,
              ticks: {
                min: 0,
                max: 10,
                padding: 10
              },
              gridLines: {
                color: "#888",
                drawOnChartArea: false
              }
            }
          ]
        },
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: "Best found route",
          poisiton: "bottom"
        }
      }
    };
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  }
};
</script>

<style>
</style>