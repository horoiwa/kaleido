from IPython.core.display import display, HTML
from string import Template
import pandas as pd
import json, random

#HTML('<script src="./d3.min.js"></script>')

def TestD3():
    filename = 'https://gist.githubusercontent.com/mbostock/3887118/raw/2e68ffbeb23fe4dadd9b0f6bca62e9def6ee9e17/data.tsv'
    iris = pd.read_csv(filename,sep="\t")

    iris_array_of_dicts = iris.to_dict(orient='records')

    css_text = '''
    .axis path,
    .axis line {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }

    .dot {
      stroke: #000;
    }
    '''

    js_text_template = Template('''

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    // ****    width = 960 - margin.left - margin.right, ****
    // ****    height = 500 - margin.top - margin.bottom; ****
        width = 720 - margin.left - margin.right,
        height = 375 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    // **** var svg = d3.select("body").append("svg") ****
    var svg = d3.select("#$graphdiv").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // **** d3.tsv("data.tsv", function(error, data) { ****
    // ****  if (error) throw error; ****

    var data = $python_data ;

      data.forEach(function(d) {
        d.sepalLength = +d.sepalLength;
        d.sepalWidth = +d.sepalWidth;
      });

      x.domain(d3.extent(data, function(d) { return d.sepalWidth; })).nice();
      y.domain(d3.extent(data, function(d) { return d.sepalLength; })).nice();

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
        .append("text")
          .attr("class", "label")
          .attr("x", width)
          .attr("y", -6)
          .style("text-anchor", "end")
          .text("Sepal Width (cm)");

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("class", "label")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Sepal Length (cm)")

      svg.selectAll(".dot")
          .data(data)
        .enter().append("circle")
          .attr("class", "dot")
          .attr("r", 3.5)
          .attr("cx", function(d) { return x(d.sepalWidth); })
          .attr("cy", function(d) { return y(d.sepalLength); })
          .style("fill", function(d) { return color(d.species); });

      var legend = svg.selectAll(".legend")
          .data(color.domain())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

      legend.append("rect")
          .attr("x", width - 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);

      legend.append("text")
          .attr("x", width - 24)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d; });

    // **** }); ****

    ''')
    html_template = Template('''
    <style > $css_text </style>
    <div id="graph-div"></div>
    <script > $js_text </script>
    ''')

    js_text = js_text_template.substitute({'python_data': json.dumps(iris_array_of_dicts),
                                           'graphdiv': 'graph-div'})
    my_plot = html_template.substitute({'css_text': css_text, 'js_text': js_text})
    d3_download = """ <script src="http://d3js.org/d3.v3.min.js" charset="utf-8" > </script>"""

    my_plot = d3_download + my_plot

    return my_plot