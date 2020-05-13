<script>
import { Line, mixins } from "vue-chartjs";

export default {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: ["chartData", "display"],
  data() {
    return {
      options: {
        tooltips: {
          mode: "index",
          intersect: true
        },
        elements: {
          point: {
            radius: 0
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                display: false
              },
              gridLines: {
                display: true,
                drawOnChartArea: false
              }
            }
          ],
          xAxes: [
            {
              ticks: {
                display: false
              },
              gridLines: {
                display: true,
                drawOnChartArea: false
              }
            }
          ]
        },
        legend: {
          display: true
        },
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: "Fitness Distribution"
        }
      }
    };
  },
  watch:{
    display(newval, oldval){
      if (newval == oldval)
        return
      if(newval=="dist")
        this.renderChart(this.chartData, this.options);
    }
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  }
};
</script>

<style>
</style>