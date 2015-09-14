var ctx = document.getElementById("browsers").getContext("2d");
new Chart(ctx).Line(buyerData);
var buyerData = {
  labels : ["January","February","March","April","May","June"],
  datasets : [
    {
      fillColor : "rgba(172,194,132,0.4)",
      strokeColor : "#ACC26D",
      pointColor : "#fff",
      pointStrokeColor : "#9DB86D",
      data : [203,156,99,251,305,247]
    }
  ]
}
