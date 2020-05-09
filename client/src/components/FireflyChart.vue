<script>
import { Scatter, mixins } from "vue-chartjs";
import zoom from "chartjs-plugin-zoom";

export default {
  extends: Scatter,
  mixins: [mixins.reactiveProp],
  props: ["chartData"],
  data() {
    return {
      options: {
        zoom: {
          enabled: true
        },
        pan: {
          enabled: true
        },
        animation: {
          duration: 200,
          easing: "linear"
        },
        legend: false,
        tooltips: false,
        scales: {
          //   xAxes: [
          //     {
          //       ticks: {
          //         min: -5,
          //         max: 5,
          //       },
          //       gridLines: {
          //       }
          //     }
          //   ],
          //   yAxes: [
          //     {
          //       ticks: {
          //         min: -5,
          //         max: 5,
          //         padding: 10
          //       },
          //       gridLines: {
          //       }
          //     }
          //   ]
        },
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: "Firefly movement"
        }
      }
    };
  },
  mounted() {
    this.addPlugin(zoom);
    this.renderChart(this.chartdata, this.options);
  }
};
</script>

<style>
</style>