<script>
import { Line, mixins } from 'vue-chartjs'
import zoom from "chartjs-plugin-zoom"

export default {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: ["chartData"],
  data() {
    return {
      options: {
        tooltips: {
            mode: 'index',
            intersect: true
        },
        zoom: {
          enabled: true,
          // drag: true
        },
        pan:{
          enabled: true
        },
        elements: {
          point:{
              radius: 1
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              }
            }
          ],
          xAxes: [
            { 
              gridLines: {
                display: false
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
            display:true,
            text:"Fitness Values"
        }
      }
    };
  },
  mounted () {
    this.addPlugin(zoom);
    this.renderChart(this.chartdata, this.options)
  }
}
</script>

<style>
</style>