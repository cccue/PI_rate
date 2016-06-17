var width = 600,
    height = 600;

var color = d3.scale.category20();

var force = d3.layout.force()
     .charge(-150)
     .size([width, height]);

$(".graph-button").click(function(e) {
   $.getJSON("./make_graph", function(graph) {

    // Next two variables for self-scaling svg
    /*
    var width = $(window).width();
    var force = d3.layout.force()
         .charge(-150)
         .size([width, height]);
    */

    /* Delete svg if it exists */
    d3.select("svg").remove();

    var svg = d3.select("#vis").append("svg")
         /* For svg scaling
         .attr("viewBox","0 0 " + (width+40) + " " + height)
         .attr("preserveAspectRatio","xMinYMin");
         */
         .attr("width", width)
         .attr("height", height);

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .linkDistance( function(d) { return Math.pow((d.value),1.8); })
        .start();

    var link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke", "black")
        .style("stroke-width", function(d) { return (3); });

    var node = svg.selectAll("g.node")
       .data(graph.nodes);

    var node_g = node.enter().append("svg:g")
       .attr("class", "node")
       .call(force.drag);

    var circles = node_g.append("svg:circle")
       .attr("r", 20)
       .style("fill", function(d) { return color(d.group); });

    var anchor = node_g.append("svg:a")
         .attr("xlink:href",  function(d) { return d.page;});

    var image = anchor.append("svg:image")
        .attr("xlink:href",  function(d) { return d.value;})
        .attr("x", function(d) { return -50; })
        .attr("y", function(d) { return -50; })
        .attr("height", 25)
        .attr("width", 25);

    node.append("title")
        .text(function(d) { return d.name; });

    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      circles.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

      image.attr("x", function(d) { return d.x - 12.5; })
          .attr("y", function(d) { return d.y - 12.5; });

    });
   });
});

