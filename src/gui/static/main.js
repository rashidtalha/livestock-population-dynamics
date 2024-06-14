$(document).ready(function(){

$('#sim_form').on('submit',function (e) {
     e.preventDefault();
     $.ajax({
      type: 'post',
      url: '/model',
      data: $('#sim_form').serialize(),
       success: function (q) {
        var alpha = q.alpha;
        var beta = q.beta;
        var gamma = q.gamma;
        document.getElementById("result_info").innerHTML= alpha;
        document.getElementById("result_stats").innerHTML= beta;
        document.getElementById("result_plot_a").innerHTML= gamma;
       }
      });
     });
})