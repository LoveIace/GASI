<script>
import { Scatter, mixins } from "vue-chartjs";
import zoom from "chartjs-plugin-zoom";

export default {
  extends: Scatter,
  mixins: [mixins.reactiveProp],
  props: ["chartData", "display"],
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
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: "Firefly movement"
        }
      }
    };
  },
  watch:{
    display(newval, oldval){
      if (newval == oldval)
        return
      if(newval=="scatter")
        this.renderChart(this.chartData, this.options);
    }
  },
  mounted() {
    this.addPlugin(zoom);
    this.renderChart(this.chartdata, this.options);
  }
};
</script>

<style>
</style>