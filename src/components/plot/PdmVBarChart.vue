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
      right: 20,
      bottom: 80,
      left: 100
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
        axis: {
          // Functions to calculate coordinates
          x: {},
          y: {},
          // Axes themselves
          xAxis: undefined,
          yAxis: undefined,
        },
        plot: {},
        plotId: 'plot-' + Math.round(Math.random() * 1000000),
        timestamps: [],
        points: [],
        // Color cache
        colors: {},
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
        let previousWasEmpty = this.points.length == 0;
        // Points are subpieces of a single bar
        this.points = [];
        // Value of highest bar
        var maxValue = 1;
        // Number of histogram bars
        let numberOfBars = this.plotData.timestamps.length - 1;
        // Make a list of objects that each represent one piece of a bar
        for (let i = 0; i < numberOfBars; i++) {
          var startY = 0;
          for (let campaignName in this.plotData.data) {
            let value = this.plotData.data[campaignName]['values'][i]
            if (value > 0) {
              var campaignBar = {'name': campaignName,
                                 'value': value,
                                 'start': startY,
                                 'column': i,
                                 'color': this.plotData.data[campaignName]['color'],
                                 'class': this.plotData.data[campaignName]['class']};
              startY += value;
              this.points.push(campaignBar);
              maxValue = Math.max(maxValue, startY)
            }
          }
        }
        maxValue = maxValue * 1.05;

        var x = d3.scaleLinear().range([0, CHART.width]).domain([0, (this.plotData.timestamps.length - 1)]);
        var xAxis = d3.axisBottom(x).ticks(this.plotData.timestamps.length).tickFormat(this.formatTimestamp);
        xAxis.scale(x);
        this.axis.x = x;
        this.axis.xAxis = xAxis;

        var y = d3.scaleLinear().range([0, CHART.height]).domain([maxValue, 0]);
        var yAxis = d3.axisLeft(y).ticks(10).tickFormat(this.formatBigNumber);
        yAxis.scale(y);
        this.axis.y = y;
        this.axis.yAxis = yAxis;

        this.draw(previousWasEmpty);
      },
    },
    methods: {
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
        return dateFormat(datetime, 'yyyy-mm-dd HH:MM');
      },

      /**
       * Draw bars on chart
       */
      draw (previousWasEmpty) {
        // translate(x, y) specifies where bar begins, +1 to move right of y axis
        let x = this.axis.x;
        let y = this.axis.y;
        var chart = this.plot.chart;

        var y0 = y(0);
        var x01 = x(0.1);
        var x005 = x(0.05);
        let component = this;
        let tooltip = this.plot.tooltip;

        if (!previousWasEmpty) {
          chart.selectAll('rect.bar').transition()
               .duration(150)
               .delay((data, index) => data.column * 20)
               .ease(d3.easeQuadIn)
               .attr('height', function(d) { return 0 })
               .attr('transform', function(d) {
                 return 'translate(' + (x(d.column) + x005) + ',' + (WRAPPER.padding.top + y0) + ')';
               })
        }

        chart.selectAll('.x.axis')
             .transition()
             .duration(650)
             .call(this.axis.xAxis);

        chart.selectAll('.y.axis')
             .transition()
             .duration(650)
             .call(this.axis.yAxis);

        chart.selectAll('.x.axis .tick>text')
             .attr('transform', 'rotate(-25)')

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
             .style('opacity', '1')
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
               tooltip.html(d.name + '<br> ' + component.formatBigNumber(d.value))
                      .style('left', `${tooltipX}px`)
                      .style('top', `${tooltipY}px`)
               tooltip.style('opacity', 0.95)
               component.eventBus.$emit('campaignHover', d)
             })
             .on('mouseout', function(d) {
               tooltip.html('')
                      .style('opacity', 0)
               component.eventBus.$emit('campaignHover', undefined)
             })
             .on('mousedown', function(d) {
               component.eventBus.$emit('campaignClick', d);
             })
             // Animation
             .transition()
             .delay((data, index) => data.column * 25 + (previousWasEmpty ? 0 : 150))
             .duration(500)
             .ease(d3.easeBackOut.overshoot(1.7))
             .attr('height', function(d) { return y0 - y(d.value) })
             .attr('transform', function(d) {
               return 'translate(' + (x(d.column) + x005) + ',' + (WRAPPER.padding.top + y(d.value) - y0 + y(d.start)) + ')';
             })
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
                            .style('opacity', 0);

      this.plot.chart = this.plot.svg.append('g')
                                     .attr('transform', 'translate(' + (WRAPPER.padding.left + 1) + ', 0)')

      this.plot.chart.append('svg:g')
                     .attr('class', 'x axis')
                     .attr('fill', '#666')
                     .attr('transform', 'translate(0,' + (WRAPPER.padding.top + CHART.height) + ')')

      this.plot.chart.append('svg:g')
                     .attr('class', 'y axis')
                     .attr('fill', '#666')
                     .attr('transform', 'translate(0,' + WRAPPER.padding.top + ')')

      let component = this
      this.eventBus.$on('campaignHover', function(campaign) {
        if (campaign){
          component.plot.chart.selectAll(".bar").style("opacity", "0.3")
          // Set only some to opaque, based on campaign name
          component.plot.chart.selectAll(".bar." + campaign.class).style("opacity", "1")
        } else {
          component.plot.chart.selectAll(".bar").style("opacity", "1")
        }
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

  .tooltip {
    position: absolute;
    top: 0px;
    left: -50%;
    padding: 8px 4px;
    border-radius: 5px;
    background: #2e6da4;
    text-align: center;
    color: white;
    font-family: Roboto;
  }

  .bar {
    cursor: pointer;
  }

  @media only screen and (max-width: 600px) {
  .tooltip {
    display: none;
  }
}

</style>