const line = function() {
  var bar = document.getElementById("linechart")
  var chart =new CanvasJS.Chart(bar,
  {

    title:{
    text: "Water per hour"
    },
    animationEnabled: true,
    data: [
      {
        type: "line",

        dataPoints: [
        { "label": "12:00am", y: 450 },
        { "label": "1:00am", y: 414 },
        { "label": "2:00am", y: 520 },
        { "label": "3:00am", y: 460 },
        { "label": "4:00am", y: 450 },
        { "label": "5:00am", y: 500 },
        { "label": "6:00am", y: 480 },
        { "label": "7:00am", y: 480 },
        { "label": "8:00am", y: 410 },
        { "label": "9:00am", y: 500 },
        { "label": "5:00pm", y: 480 },
        { "label": "6:00pm", y: 510 },
        { "label": "7:00pm", y: 510 },
        { "label": "8:00pm", y: 510 },
        { "label": "9:00pm", y: 510 },
        { "label": "10:00pm", y: 510 },
        ]
      }
    ]
  });

  chart.render();
}  

const line1 = function() {
  var bar = document.getElementById("linechart1")
  var chart =new CanvasJS.Chart(bar,
  {

    title:{
    text: "Price per day"
    },
    animationEnabled: true,
    data: [
      {
        type: "line",

        dataPoints: [
        { "label": "Monday", y: 450 },
        { "label": "Tuesday", y: 414 },
        { "label": "Wednesday", y: 520 },
        { "label": "Thursday", y: 460 },
        { "label": "Friday", y: 450 },
        { "label": "Saturday", y: 500 },
        { "label": "Sunday", y: 480 },
        ]
      }
    ]
  });

  chart.render();
}  

line()
line1()

function togglePopup(){
  document.getElementById("popup-1").classList.toggle("active");
  document.getElementById("popup-2").classList.toggle("active");
  document.getElementById("popup-3").classList.toggle("active");
}