

$(".table-button").click(function(e) {

   var line="./make_sim_table/" + document.getElementById('rum_index').value;

   $.getJSON(line, function(data) {

       $( ".panel_table" ).remove();       
/*
       for (var index = 0; index < data.nodes.length; index++) {
           console.log(data.nodes[index].name);
       }
*/
       var tag_html = "<table class=\"table\"> <tr> <th> Ranking </th> <th> Rum name </th> <th> Rating differences </th> <th> Common reviewers </th></tr>";

       for (var index = 0; index < data.nodes.length; index++) {
           var ranking = +index + +1;
           tag_html += "<tr> <td>" + ranking + "&nbsp &nbsp <img src=\"./static/images/ron_bottle_small.png\"> </img>" + "</td> <td> " + data.nodes[index].name + "</td> <td>" + data.nodes[index].rating.toFixed(3) + "</td> <td>" + data.nodes[index].users + "</td></tr>";
           //console.log(data.nodes[index].name);
       }
 
        tag_html += " </table>";       

//       tagElement = document.createElement("div");
       var root = document.getElementById("vis");
       var child = document.createElement("div");
       child.className = "panel_table panel-default";       
       child.innerHTML = tag_html;
       root.appendChild(child); 

//       tagElement = root.appendChild(child);
       //tagElement.className = "table_div container-fluid";
       //tagElement.innerHTML = tag_html;
       //document.body.appendChild(tagElement); 


   });
});
