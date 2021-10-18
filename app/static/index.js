
$("#demolist a").on('click', function(e) {
  e.preventDefault(); // cancel the link behaviour
  $('#linechart1').css("display","block");
  var selText = $(this).text();
  // call the get price function and pass the region into the url to get the route 
  getPrice(selText)
  getPriceRegion(selText)
  // check if the selection option and display the table 
  if (selText=="Perth") {$('#perth').css({"display":"table","width": "100%", "text-align":"center"})
    $('#south').css("display","none")  
    $('#north').css("display","none")}
  else if (selText=="South") {$('#south').css({"display":"table","width": "100%", "text-align":"center"})
    $('#perth').css("display","none")  
    $('#north').css("display","none")}
  else if (selText=="North") {$('#north').css({"display":"table","width": "100%", "text-align":"center"})
    $('#perth').css("display","none")  
    $('#south').css("display","none")}
  // display the text after making selection 
  $("#dropdownMenuButton1").text(selText);
});




const getPrice = (region="Perth") => {
  fetch('/get_cost/' + region ,{
    method:"GET",
    headers:{
      headers: {
        "Content-Type":"application/json"
      }
    }
  })
  .then(resp => resp.json())
  .then((data) =>
    bar(data)
  )
  .catch(error => 
    console.log(error))
}

const getWater = function() {
  fetch('/get_water' ,{
    method:"GET",
    headers:{
      headers: {
        "Content-Type":"application/json"
      }
    }
  })
  .then(resp => resp.json())
  .then((data) =>
    line(data)
  )
  .catch(error => 
    console.log(error))
}


const getPriceRegion = (region='Perth') => {
  fetch('/get_price/' + region ,{
    method:"GET",
    headers:{
      headers: {
        "Content-Type":"application/json"
      }
    }
  })
  .then(resp => resp.json())
  .then((data) =>
    writeData(data)
  )
  .catch(error => 
    console.log(error))
}

const writeData = function(data) {
  let price = '<h5 class="text" id="text">' + data[0][3] + '<small class="text-muted">/KL</small></h5>'
  document.getElementById('text').innerHTML =price
}


const line = function(data) {

  var dataArray = []
  for(var i = 0; i < data.length; i++){
    dataArray.push({"label":data[i][0], "y":data[i][1]})
  }


  var bar = document.getElementById("linechart")
  var chart =new CanvasJS.Chart(bar,
  {

    title:{
    text: "Water meter"
    },
    animationEnabled: true,
    data: [
      {
        type: "line",

        dataPoints: dataArray
      }
    ],
    axisY:{
      suffix: " KL",
    }     
  });

  chart.render();
}  

const bar = function(data) {
  var class1 = []
  var class2 = []
  var class3 = []
  var class4 = []
  var class5 = []
  for(var i = 0; i < data.length; i++){
    if (data[i][5]==="Class 1") {class1.push({"label":data[i][1], "y":data[i][3]}) }
    else if (data[i][5]==="Class 2") {class2.push({"label":data[i][1], "y":data[i][3]}) }
    else if (data[i][5]==="Class 3") {class3.push({"label":data[i][1], "y":data[i][3]}) }
    else if (data[i][5]==="Class 4") {class4.push({"label":data[i][1], "y":data[i][3]}) }
    else if (data[i][5]==="Class 5") {class5.push({"label":data[i][1], "y":data[i][3]}) }
  };


  var bar = document.getElementById("linechart1")
  var chart =new CanvasJS.Chart(bar,
  {

    title:{
    text: "Price per kiloliter"
    },
    animationEnabled: true,
    data: [
      {
        type: "column",
        name:"Class 1",
        showInLegend: true,
        dataPoints:class1
      },
      {
        type: "column",
        name:"Class 2",
        showInLegend: true,
        dataPoints:class2
      },
      {
        type: "column",
        name:"Class 3",
        showInLegend: true,
        dataPoints:class3
      },
      {
        type: "column",
        name:"Class 4",
        showInLegend: true,
        dataPoints:class4
      },
      {
        type: "column",
        name:"Class 5",
        showInLegend: true,
        dataPoints:class5
      }
      
    ],
    axisY:{
      prefix: "$",
      suffix:"/kl"
    }     
  });

  chart.render();
}  

getWater()

$('#start').on('click', function(e) {
  $('#end').css("display","block")
  $('#start').css("display","none")
  $('#volumn').css("display","inline-block")
})

$('#end').on('click', function(e) {
  $('#start').css("display","block")
  $('#end').css("display","none")
  $('#volumn').css("display","none")
})


