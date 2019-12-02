<template>
  <div :id="plotId" style="text-align: center" />
</template>

<script type="text/javascript">

  import * as d3 from 'd3'
  import dateFormat from 'dateformat'
  
  // Canvas size and padding
  const WRAPPER = {
    width: 1200,
    height: 400,
    padding: {
      top: 20,
      right: 60,
      bottom: 80,
      left: 80,
      bubbleLegend: 320,
    }
  }

  // Chart size
  const CHART = {
    width: WRAPPER.width - WRAPPER.padding.right - WRAPPER.padding.left,
    height: WRAPPER.height - WRAPPER.padding.top - WRAPPER.padding.bottom,
  }

  export default {
    name: 'PdmVBarChart',
    data () {
      return {
        plot: {},
        axis: {
          x: undefined,
          y: undefined,
          xAxis: undefined,
          yAxis: undefined
        },
        plotId: 'plot-' + Math.round(Math.random() * 1000000),
        timestamps: [],
        points: [],
        // Color cache
        colors: {},
        plotMode: 'cumulative',
        plotScale: 'linear',
        bubbleLegend: 'off',
        timeRange: 'week'
      }
    },

    props: {
      plotData: {
        type: Object,
        default: () => {}
      },
      eventBus: {
        type: Object,
        default: () => undefined
      }
    },
    watch: {
      plotData () {
        this.prepareData();
      },
    },
    methods: {
      prepareData () {
        let previousWasEmpty = this.points.length == 0;
        // Points are subpieces of a single bar
        this.points = [];
        // Number of histogram bars
        let numberOfBars = this.plotData.timestamps.length - 1;
        // Sort campaigns by their sum
        let data = this.plotData.data;
        let campaignNames = Object.keys(data).sort(function(a, b) { return data[a].sum - data[b].sum;})
        // Make a list of objects that each represent one piece of a bar
        for (let i = 0; i < numberOfBars; i++) {
          var startY = 0.1;
          for (let campaignName of campaignNames) {
            let value = data[campaignName]['values'][i]
            if (this.plotMode === 'cumulative') {
              for (let j = 0; j < i; j++) {
                value += data[campaignName]['values'][j];
              }
            }
            if (value > 0) {
              var campaignBar = {'name': campaignName,
                                 'value': value,
                                 'start': startY,
                                 'end': startY + value,
                                 'column': i,
                                 'color': data[campaignName]['color'],
                                 'class': data[campaignName]['class']};
              startY += value;
              this.points.push(campaignBar);
            }
          }
        }

        this.draw(previousWasEmpty);
      },

      scaleChange(newScale) {
        this.plotScale = newScale;
        let maxValue = d3.max(this.points, function(e) { return e.start + e.value})
        this.axis.x = d3.scaleLinear().range([0, CHART.width - (this.bubbleLegend === 'on' ? WRAPPER.padding.bubbleLegend : 0)]).domain([0, (this.plotData.timestamps.length - 1)]);
        this.axis.xAxis = d3.axisBottom(this.axis.x).ticks(this.plotData.timestamps.length).tickFormat(this.formatTimestamp);
        this.axis.xAxis.scale(this.axis.x);

        if (newScale === 'log') {
          if (isNaN(maxValue) || maxValue < 1) {
            maxValue = 1;
          } else {
            maxValue = maxValue * 10;
          }
          this.axis.y = d3.scaleLog().range([0, CHART.height]).domain([maxValue, 0.1]);
        } else {
          if (isNaN(maxValue) || maxValue < 1) {
            maxValue = 1;
          } else {
            maxValue = maxValue * 1.05;
          }
          this.axis.y = d3.scaleLinear().range([0, CHART.height]).domain([maxValue, 0]);
        }

        this.axis.yAxis = d3.axisLeft(this.axis.y).ticks(6).tickFormat(this.formatBigNumber);
        this.axis.yAxis.scale(this.axis.y);
      },

      formatBigNumber (number) {
        if (number < 1 || number % 1 !== 0) {
            return ''
        }
        var result = ''
        if (number >= 1e9) {
            result = (Math.round(number / 10000000.0) / 100.0).toFixed(2) + 'G'
        } else if (number >= 1e6) {
            result = (Math.round(number / 10000.0) / 100.0).toFixed(2) + 'M'
        } else if (number >= 1e3) {
            result = (Math.round(number / 10.0) / 100.0).toFixed(2) + 'k'
        } else {
            result = number.toString()
        }
        return result.replace('.00', '')
                     .replace('.10', '.1')
                     .replace('.20', '.2')
                     .replace('.30', '.3')
                     .replace('.40', '.4')
                     .replace('.50', '.5')
                     .replace('.60', '.6')
                     .replace('.70', '.7')
                     .replace('.80', '.8')
                     .replace('.90', '.9')
      },

      formatTimestamp (data, index) {
        let datetime = new Date(this.plotData.timestamps[index]);
        if (this.timeRange == 'week') {
          return dateFormat(datetime, 'mmm dS, HH') + 'h';
        } else {
          return dateFormat(datetime, 'mmm dS, yyyy');
        }
      },

      /**
       * Draw bars on chart
       */
      draw (previousWasEmpty) {
        this.scaleChange(this.plotScale);
        var x = this.axis.x;
        var y = this.axis.y;
        let xAxis = this.axis.xAxis;
        let yAxis = this.axis.yAxis;

        let chart = this.plot.chart;

        let y0 = y(0.1);
        let x005 = x(0.05);

        if (!previousWasEmpty) {
          chart.selectAll('rect.bar').transition()
               .duration(100)
               .delay((data, index) => data.column * 20)
               .ease(d3.easeQuadIn)
               .attr('height', function(d) { return 0 })
               .attr('transform', function(d) {
                 return 'translate(' + (x(d.column) + x005) + ',' + (WRAPPER.padding.top + y0) + ')';
               })
               .remove()

        }
        chart.selectAll('.legend.bar').remove()

        let component = this;
        let tooltip = this.plot.tooltip;
        chart.selectAll('.x.axis')
             .transition()
             .delay(previousWasEmpty ? 0 : 100)
             .duration(400)
             .call(xAxis);

        chart.selectAll('.y.axis')
             .transition()
             .delay(previousWasEmpty ? 0 : 100)
             .duration(400)
             .call(yAxis);

        chart.selectAll('.x.axis .tick>text')
             .attr('transform', 'rotate(-35)')

        if (this.points.length == 0) {
          return;
        }
        // All rects that have bar class
        chart.selectAll('rect .bar')
             .data(this.points)
             .enter()
             .append('rect')
             // Initial bar position and size
             .attr('class', function(d) { return 'bar ' + d.class; })
             .style('opacity', 1)
             .attr('fill', function(d) { return d.color; })
             .attr('transform', function(d) {
               return 'translate(' + (x(d.column) + x005) + ',' + (WRAPPER.padding.top + y0) + ')';
             })
             .attr('width', function(d) { return x(0.9) })
             .attr('height', function(d) { return 0})
             // Mouse gestures
             .on('mousemove', function(d) {
               let tooltipX = d3.event.pageX + 5;
               let tooltipY = d3.event.pageY + 5;
               tooltip.html(d.name +
                            '<br>Events ' + component.formatBigNumber(d.value))
                      .style('left', `${tooltipX}px`)
                      .style('top', `${tooltipY}px`)
                      .style('display', 'block')
               component.eventBus.$emit('campaignHover', d)
             })
             .on('mouseout', function(d) {
               tooltip.html('')
                      .style('display', 'none')
               component.eventBus.$emit('campaignHover', undefined)
             })
             .on('mousedown', function(d) {
               component.eventBus.$emit('campaignClick', d);
             })
             // Animation
             .transition()
             .delay((data, index) => data.column * 25 + (previousWasEmpty ? 0 : 100))
             .duration(400)
             .ease(d3.easeBackOut.overshoot(1.7))
             .attr('height', function(d) { return y(d.start) - y(d.end) })
             .attr('transform', function(d) {
               return 'translate(' + (x(d.column) + x005) + ',' + (WRAPPER.padding.top + y(d.end)) + ')';
             })

        if (this.bubbleLegend === 'on') {
          let campaignColors = []
          var legendCircleY = WRAPPER.padding.top;
          var legendCircleX = CHART.width + 40 - WRAPPER.padding.bubbleLegend;
          for (let campaignName in this.plotData.data) {
            var item = {'name': campaignName,
                        'color': this.plotData.data[campaignName]['color'],
                        'class': this.plotData.data[campaignName]['class'],
                        'x': legendCircleX,
                        'sum': this.plotData.data[campaignName]['sum'],
                        'niceSum': this.plotData.data[campaignName]['niceSum']}

            campaignColors.push(item)
          }
          campaignColors.sort(function(a, b) { return a.sum > b.sum ? -1 : 1})
          if (campaignColors.length > 18) {
            // Take first 18 elements
            campaignColors = campaignColors.slice(0, 18);
          }
          for (let item of campaignColors) {
            item['y'] = legendCircleY;
            legendCircleY += 18;
          }
          if (campaignColors.length > 1 && this.plotData.summary.monteCarloSum > 0 && this.plotData.summary.rerecoSum > 0) {
            campaignColors.push({'name': 'Total Monte Carlo',
                                 'color': 'white',
                                 'class': 'summary-bubble',
                                 'x': legendCircleX,
                                 'y': legendCircleY,
                                 'sum': this.plotData.summary.monteCarloSum,
                                 'niceSum': this.plotData.summary.monteCarloNiceSum,
            })
            legendCircleY += 18;
          }
          if (campaignColors.length > 1 && this.plotData.summary.monteCarloSum > 0 && this.plotData.summary.rerecoSum > 0) {
            campaignColors.push({'name': 'Total Data ReReco',
                                 'color': 'white',
                                 'class': 'summary-bubble',
                                 'x': legendCircleX,
                                 'y': legendCircleY,
                                 'sum': this.plotData.summary.rerecoSum,
                                 'niceSum': this.plotData.summary.rerecoNiceSum,
            })
            legendCircleY += 18;
          }
          if (campaignColors.length > 1 && (this.plotData.summary.monteCarloSum > 0 || this.plotData.summary.rerecoSum > 0)) {
            campaignColors.push({'name': 'Total',
                                 'color': 'white',
                                 'class': 'summary-bubble',
                                 'x': legendCircleX,
                                 'y': legendCircleY,
                                 'sum': this.plotData.summary.monteCarloSum + this.plotData.summary.rerecoSum,
                                 'niceSum': this.plotData.summary.totalNiceSum,
            })
            legendCircleY += 18;
          }

          var legendCircle = this.plot.chart.selectAll("circle")
                                        .data(campaignColors)
                                        .enter()

          legendCircle.append("circle")
                      .attr("cx", function(d) {return d.x })
                      .attr("cy", function (d) { return d.y})
                      .attr('class', function(d) { return 'legend bar ' + d.class; })
                      .attr("r", 8)
                      .style("fill", function (d) { return d.color; })
                      .attr('display', 'none')
                      .on('mousemove', function(d) {
                        if (d.class !== 'summary-bubble') {
                          component.eventBus.$emit('campaignHover', d)
                        }
                      })
                      .on('mouseout', function(d) {
                        if (d.class !== 'summary-bubble') {
                          component.eventBus.$emit('campaignHover', undefined)
                        }
                      })
                      .on('mousedown', function(d) {
                        if (d.class !== 'summary-bubble') {
                          component.eventBus.$emit('campaignClick', d);
                        }
                      })
                      .transition()
                      .delay(500)
                      .duration(100)
                      .attr('display', 'block')

          legendCircle.append("text")
                      .attr("transform", function (d) { return "translate(" + (d.x + 12) + ", " + (d.y + 4) + ")"})
                      .text(function (d) { return d.name + ' (' + d.niceSum + ')'; })
                      .attr('class', function(d) { return 'legend bar ' + d.class; })
                      .attr('display', 'none')
                      .on('mousemove', function(d) {
                        if (d.class !== 'summary-bubble') {
                          component.eventBus.$emit('campaignHover', d)
                        }
                      })
                      .on('mouseout', function(d) {
                        if (d.class !== 'summary-bubble') {
                          component.eventBus.$emit('campaignHover', undefined)
                        }
                      })
                      .on('mousedown', function(d) {
                        if (d.class !== 'summary-bubble') {
                          component.eventBus.$emit('campaignClick', d)
                        }
                      })
                      .transition()
                      .delay(500)
                      .duration(100)
                      .attr('display', 'block')
        }
      }
    },
    mounted () {
      d3.select('#' + this.plotId)
        .append('svg')
        .attr('width', WRAPPER.width)
        .attr('height', WRAPPER.height)
        .attr('viewBox', '0 0 ' + WRAPPER.width + ' ' + WRAPPER.height)
        .attr('xmlns', 'http://www.w3.org/2000/svg')
        .attr('class', 'svg')
        .style('max-width', WRAPPER.width + 'px')
      this.plot.svg = d3.select('#' + this.plotId + ' svg');
      this.plot.tooltip = d3.select('body')
                            .append('div')
                            .attr('class', 'tooltip elevation-3')

      this.plot.chart = this.plot.svg.append('g')
                                     .attr('transform', 'translate(' + (WRAPPER.padding.left + 15) + ', 0)')

      this.plot.chart.append('svg:g')
                     .attr('class', 'x axis')
                     .attr('transform', 'translate(0,' + (WRAPPER.padding.top + CHART.height) + ')')

      this.plot.chart.append('svg:g')
                     .attr('class', 'y axis')
                     .attr('transform', 'translate(-10,' + WRAPPER.padding.top + ')')

      this.plot.chart.append("text")
                     .text('EVENTS')
                     .attr("class", "y-label")
                     .attr("transform", "rotate(-90) translate(-"+WRAPPER.padding.top+", 2)")

      let component = this;
      this.eventBus.$on('campaignHover', function(campaign) {
        if (campaign){
          component.plot.chart.selectAll(".bar").style("opacity", "0.3")
          // Set only some to opaque, based on campaign name
          component.plot.chart.selectAll(".bar." + campaign.class).style("opacity", "1")
        } else {
          component.plot.chart.selectAll(".bar").style("opacity", "1")
        }
      })
      this.eventBus.$on('plotModeChange', function(mode) {
        component.plotMode = mode;
        component.prepareData();
      })
      this.eventBus.$on('plotScaleChange', function(scale) {
        component.plotScale = scale;
        component.draw(component.points.length === 0)
      })
      this.eventBus.$on('bubbleLegendChange', function(bubbleLegend) {
        component.bubbleLegend = bubbleLegend;
        component.draw(component.points.length === 0)
      })
      this.eventBus.$on('timeRangeChange', function(timeRange) {
        component.timeRange = timeRange;
      })
    }
};

</script>

<style>
  .svg {
    width: 100%;
    height: 100%;
  }

  .tick > text {
    text-anchor: end;
    font-size: 1.4em;
    fill: #333;
  }

  .legend {
    font-family: Roboto;
    fill: #333;
    font-size: 0.85em;
  }

  .tooltip {
    position: absolute;
    top: 0px;
    left: -50%;
    padding: 8px 4px;
    border-radius: 5px;
    background: #1976D2;
    text-align: center;
    color: white;
    font-family: Roboto;
    opacity: 0.9;
  }

  .y-label {
    text-anchor: end;
    font-size: 0.85em;
    fill: #333;
    font-family: Roboto;
  }

  .bar {
    cursor: pointer;
  }

  .summary-bubble {
    cursor: auto;
    fill: rgba(0, 0, 0, 0.6);
    font-style: italic;
  }

  @media only screen and (max-width: 600px) {
    .tooltip {
      display: none;
    }
  }

</style>
