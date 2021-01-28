<template>
  <v-app>
    <v-app-bar
      color="green"
      dark
      app
    >
      <v-spacer/>
      <v-toolbar-title class="align-center">
        CO₂
      </v-toolbar-title>
      <v-spacer/>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row class="text-center" justify="center">
          <v-col cols="8" class="align-center col-xs-12 col-sm-12">
            <div class="text-h3">
              {{ ppmNow }}
            </div>
            ppm
          </v-col>
        </v-row>
        <v-row class="text-center" justify="center" >
          <v-col cols="12" class="align-center col-xl-8 col-lg-8 col-md-8">
            <Graph v-if="chartData" :chart-data="chartData" :options="options" :height="height" :width="width"/>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import Graph from './components/Graph';
  import moment from "moment";

  export default {
    name: 'App',

    components: {
      Graph
    },

    data() {
      return {
        chartData: null,
        //Chart.js options that controls the appearance of the chart
        options: null,
        ppmNow: 0,
        height: window.innerHeight * 0.75,
        width: window.innerHeight * 0.75
      }
    },
    created() {
      this.getPPMHistory();
      this.getPPMNow();
      setInterval(this.getPPMNow, 10000);
      setInterval(this.getPPMHistory, 300000)
    },
    methods: {
      getPPMHistory() {
        this.axios.get("/api/day").then((res) => {
          const ppm = res.data.map(rec => rec.ppm);
          const createdAt = res.data.map(rec => rec.created_at);
          this.chartData = {
            //Data to be represented on x-axis
            labels: createdAt,
            datasets: [
              {
                data: ppm,
                backgroundColor: '#f87979',
                pointBackgroundColor: 'white'
              }
            ]
          };
          this.options = {
            animation: false,
            maintainAspectRatio: false,
            scales: {
              yAxes: [{
                ticks: {
                  beginAtZero: true
                },
                gridLines: {
                  display: true
                }
              }],
              xAxes: [{
                type: 'time',
                gridLines: {
                  display: false
                },
                ticks: {
                  min: moment().add(-1, 'days').format("YYYY-MM-DD HH:mm:ss"),
                  max: moment().format("YYYY-MM-DD HH:mm:ss"),
                  maxTicksLimit: 12
                },
                time: {
                  unit: 'hour',
                  displayFormats: {
                    hour: 'HH'
                  }
                }
              }]
            },
            legend: {
              display: false
            },
          }
        })
      },
      getPPMNow() {
        this.axios.get("/api/now").then((res) => {
          document.title = res.data.ppm + "ppm";
          this.ppmNow = res.data.ppm
        })
      }
    }
  };
</script>
