$(".hist-button").click(function(e) {

   var line="./make_hists/" + document.getElementById('rum_index').value;

   $.getJSON(line, function(data_hist) {
      //console.log(data_hist.rating[0].local,data_hist.rating[0].full);

      d3.select("#svg_rat").remove();
      var values = data_hist.rating[0];
      var formatCount = d3.format("0.2f");

      var margin = {top: 30, right: 30, bottom: 40, left: 40},
          width = 480 - margin.left - margin.right,
          height = 300 - margin.top - margin.bottom;

      var x = d3.scale.linear()
         .domain([0, 10])
         .range([0, width]);

      var data_loc = d3.layout.histogram()
         .bins(x.ticks(10))
         .frequency(false)
         (values.local);
    
      var data_full = d3.layout.histogram()
         .bins(x.ticks(10))
         .frequency(false)
         (values.full);

      for (var index = 0; index < data_loc.length; index++) {
          data_loc[index].y *= 100
          data_full[index].y *= 100;
      }   

      var y = d3.scale.linear()
          .domain([0, d3.max(data_loc.concat(data_full), function(d) { return d.y + 15; })])
          .range([height, 0]);

      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");

      var svg = d3.select("#vis").append("svg")
         .attr("id","svg_rat")
         .attr("width", width + margin.left + margin.right)
         .attr("height", height + margin.top + margin.bottom)
         .append("g")
         .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var bar = svg.selectAll(".bars")
         .data(data_loc)
         .enter().append("g")
         .attr("class", "bar")
         .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

	 bar.append("rect")
    	 .attr("x", 1)
         .style('fill', 'blue')
    	 .attr("width", x(data_loc[0].dx) - 1)
    	 .attr("height", function(d) { return height - y(d.y); });

	 bar.append("text")
    	 .attr("dy", ".75em")
         .attr("y", function(d) { return -y(d.y); })
    	 .attr("x", x(data_loc[0].dx) / 2)
    	 .attr("text-anchor", "middle")
         .style('fill', 'blue')
    	 .text(function(d) { return formatCount(d.y); });

       var bar1 = svg.selectAll(".bars")
         .data(data_full)
         .enter().append("g")
         .attr("class", "bar")
         .attr("data-legend","Site distribution")
         .attr("data-legend-color","red")
         .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

         bar1.append("rect")
         .attr("x", 5)
         .style('fill', 'red')
         .attr("width", x(data_full[0].dx) - 10)
         .attr("height", function(d) { return height - y(d.y); });

         bar1.append("text")
         .attr("dy", ".75em")
         .attr("y", function(d) { return 15 - y(d.y); })
         .attr("x", x(data_full[0].dx) / 2)
         .attr("text-anchor", "middle")
         .style('fill', 'red')
         .text(function(d) { return formatCount(d.y); });

      svg.append("g")
    	 .attr("class", "x axis")
    	 .attr("transform", "translate(0," + height + ")")
    	 .call(xAxis)
         .append("text")
         .style("text-anchor", "middle")
         .attr("transform", function(d) { return "translate(200," + (margin.bottom - 5) + ")"; })
         .text("Rating scale");

      svg.append("g")
         .attr("class", "y axis")
         .call(yAxis)
         .append("text")
         .attr("transform", "rotate(-90), translate(-100)")
         .attr("y", 6)
         .attr("dy", ".71em")
         .style("text-anchor", "middle")
         .text("Probability (%)");

      svg.append("g")
    	.attr("class","legend")
    	.attr("transform", "translate(20,50)")
    	.style("fill","red")
    	.call(d3.legend);


      d3.select("#svg_sent").remove();
      var values = data_hist.sentiment[0];
      var formatCount = d3.format("0.2f");

      var x = d3.scale.linear()
         .domain([0, 1])
         .range([0, width]);

      var data_loc = d3.layout.histogram()
         .bins(x.ticks(10))
         .frequency(false)
         (values.local);

      var data_full = d3.layout.histogram()
         .bins(x.ticks(10))
         .frequency(false)
         (values.full);

      for (var index = 0; index < data_loc.length; index++) {
          data_loc[index].y *= 100
          data_full[index].y *= 100;
      }

      var y = d3.scale.linear()
          .domain([0, d3.max(data_loc.concat(data_full), function(d) { return d.y + 15; })])
          .range([height, 0]);

      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");

      var svg = d3.select("#vis").append("svg")
         .attr("id","svg_sent")
         .attr("width", width + margin.left + margin.right)
         .attr("height", height + margin.top + margin.bottom)
         .append("g")
         .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var bar = svg.selectAll(".bars")
         .data(data_loc)
         .enter().append("g")
         .attr("class", "bar")
         .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

         bar.append("rect")
         .attr("x", 1)
         .style('fill', 'blue')
         .attr("width", x(data_loc[0].dx) - 1)
         .attr("height", function(d) { return height - y(d.y); });

         bar.append("text")
         .attr("dy", ".75em")
         .attr("y", function(d) { return -y(d.y); })
         .attr("x", x(data_loc[0].dx) / 2)
         .attr("text-anchor", "middle")
         .style('fill', 'blue')
         .text(function(d) { return formatCount(d.y); });

       var bar1 = svg.selectAll(".bars")
         .data(data_full)
         .enter().append("g")
         .attr("class", "bar")
         .attr("data-legend","Site distribution")
         .attr("data-legend-color","red")
         .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

         bar1.append("rect")
         .attr("x", 5)
         .style('fill', 'red')
         .attr("width", x(data_full[0].dx) - 10)
         .attr("height", function(d) { return height - y(d.y); });

         bar1.append("text")
         .attr("dy", ".75em")
         .attr("y", function(d) { return 15 - y(d.y); })
         .attr("x", x(data_full[0].dx) / 2)
         .attr("text-anchor", "middle")
         .style('fill', 'red')
         .text(function(d) { return formatCount(d.y); });

      svg.append("g")
         .attr("class", "x axis")
         .attr("transform", "translate(0," + height + ")")
         .call(xAxis)
         .append("text")
         .style("text-anchor", "middle")
         //.attr("transform", "translate(200,35)")
          .attr("transform", function(d) { return "translate(200," + (margin.bottom - 5) + ")"; })
         .text("Sentiment scale");


      svg.append("g")
         .attr("class", "y axis")
         .call(yAxis)
         .append("text")
         .attr("transform", "rotate(-90), translate(-100)")
         .attr("y", 6)
         .attr("dy", ".71em")
         .style("text-anchor", "middle")
         .text("Probability (%)");

      svg.append("g")
         .attr("class","legend")
         .attr("transform", "translate(20,50)")
         .style("fill","red")
         .call(d3.legend);

 });
});

                 
