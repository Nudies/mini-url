"use strict";
$(document).ready(function() {

  var CSS_COLOR_NAMES = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","Darkorange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"];
  var browsers, platforms, months;
  var browserData = [];
  var platformData = [];
  var monthData = [];
  var monthChart = document.getElementById("usage").getContext("2d");
  var browserChart = document.getElementById("browsers").getContext("2d");
  var platformChart = document.getElementById("platform").getContext("2d");
  var pieOptions = {
    segmentShowStroke : false,
    animateScale : true
  }

  function get_data(link, data, dataSet, chart) {
    $.getJSON(link, function(result){
      data = result;
      build_data(data, dataSet);
      new Chart(chart).Doughnut(dataSet, pieOptions);
    });
  }

  function build_data(data, dataSet) {
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        dataSet.push(
          {
            value: data[key],
            label: key,
            color: CSS_COLOR_NAMES.pop(Math.floor(Math.random() * CSS_COLOR_NAMES.length))
          }
        );
      }
    }
  }

  get_data('/data/browsers', browsers, browserData, browserChart);
  get_data('/data/platforms', platforms, platformData, platformChart);
  get_data('/data/months', platforms, monthData, monthChart);

});
