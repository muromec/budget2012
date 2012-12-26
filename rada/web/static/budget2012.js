var chart;
$(document).ready(function() {
   function round(rnum, rlength) {
          return Math.round(rnum*Math.pow(10,rlength))/Math.pow(10,rlength);
   }
   var hm = function(val) {
       if(val > 1000000000) {
           return Math.round(val / 1000000000) + ' Млрд';
       } 
   }
   var full = 312814237900;

   var options = {
      chart: {
         renderTo: 'container_budget2012',
         plotBackgroundColor: null,
         plotBorderWidth: null,
         plotShadow: false
      },
      title: {
         text: 'Бюджет Украины на 2012й год, расходы ' + hm(full) + ' Гр',
      },
      tooltip: {
         formatter: function() {
             var money = hm(this.point.config.money);

             return '<b>'+ this.point.name +'</b>: '+ money +' Гр';
         }
      },
      plotOptions: {
         pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
               enabled: true,
               color: Highcharts.theme.textColor || '#000000',
               connectorColor: Highcharts.theme.textColor || '#000000',
               formatter: function() {
                  var money = hm(this.point.config.money);
                  return '<b>'+ this.point.name +'</b>: '+ money + ' Гр';
               }
            }
         }
      },
       series: [{
         type: 'pie',
         name: 'Категории',
         data: []
      }]
   };

   var show_it = function(file) {
       $.get(file, null,  parse);
   };

   var parse = function(tsv) {
        tsv = tsv.split(/\n/g);
        var data = [];
        var small = 0.0;
        var small_m = 0.0;

        $.each(tsv, function(i, line) {
            line = line.split(/ /g);
            var title = line.slice(4).join(' ');
            var money = parseFloat(line[3]);
            var perc = (money / full) * 100;

            if(perc.toString() == "NaN") { return  }

            if(line[0]=='category' && perc < 0.6) { 
                small += perc;
                small_m += money;
                return;
            }

            data.push( {
                name: title, 
                y: perc,
                money: money,
            });
        })
        if(small > 0) {
            data.push( {
                name: 'Все остальное (сумма малых процентов)',
                y: small,
                money: small_m,
            });
        }
        options.series[0].data = data;
        data[0].sliced = true;
        data[0].selected = true;
        var chart = new Highcharts.Chart(options);
   };

   var file = $('a.chart_style').attr('file');
   show_it(file);
   $('a.chart_style').click(function() {
        var file = $(this).attr('file');
        show_it(file);

        return false;
        
   });

});
   
