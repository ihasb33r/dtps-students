
function rendersummary(jsonpage, table){
    var jqxhr = $.getJSON(jsonpage,
            function(data) {
                table1 = $("#summarylist");
                var februaryCourses =[];
                var juneCourses =[];
                var septemberCourses =[];
                var februaryTable = $("#februarysummary");
                var juneTable = $("#junesummary");
                var septemberTable = $("#septembersummary");
                $.each(data, function(key,val) {
                    if (val.hasFebr == true){
                        februaryCourses.push(val);
                    }
                    if (val.hasJune == true){
                        juneCourses.push(val);
                    }
                    if (val.hasSept == true){
                        septemberCourses.push(val);
                    }
                }
                );
                populatesummary(februaryTable, februaryCourses, 0);
                populatesummary(juneTable, juneCourses,1);
                populatesummary(septemberTable, septemberCourses,2);
            });
}

function getmili(time){

    m = time.match(/(\d+)-(\d+)-(\d+) (\d+):(\d+)/);
    date = new Date(m[1]-1, +m[2], +m[3], +m[4], +m[5]);

    return date.getTime();
}


function populatesummary(table,data,period){
    items = [];
    table.tablesorter();
    if(data.length >0){
        $.each(data, function(key,val) {
            if (period == 0){
                periodfield = "addedFebr";
                items.push('<tr><td class="date"><span class="date">'+getmili(val.addedFebr)+'</span></td><td><a href="course?id='+ val.id + '">' + val.name +  ' </td></tr>');
            }
            else if (period == 1){
                periodfield = "addedJune";
                items.push('<tr><td class="date"><span class="date">'+getmili(val.addedJune)+'</span></td><td><a href="course?id='+ val.id + '">' + val.name +  ' </td></tr>');
            }
            else {
                periodfield = "addedSept";
                items.push('<tr><td class="date"><span class="date">'+getmili(val.addedSept)+'</span></td><td><a href="course?id='+ val.id + '">' + val.name +  ' </td></tr>');
            }
        }

        );

        items.sort(function(a,b){
            if (a>b){
                return -1;
            }
            else {
                return 1;
            }
        }
        );

        try{
        table.find("tbody").append(items.join(''));
        table.trigger("update");
        var sorting = [[0,1]];
        table.trigger("sorton", [sorting]);
        }
        catch(err){

        }

    }

}

function renderstudent(jsonpage, sept, febr, june){
    var results = [];
    var jqxhr = $.getJSON(jsonpage,
            function(data) {
                var results = [];
                populatestudentgrades(sept,febr,june, data);
            });
}

function populatestudentgrades(sept, febr, june,data){
    febritems = [];
    septitems = [];
    juneitems = [];
    var table = febr;

    if(data!=null){
        $.each(data, function(key,val) {
            if (val.period == "ΦΕΒΡ"){
                febritems.push('<tr><td class="date"><span class="date">'+getmili(val.added)+'</span></td><td><a href="/course?id='+ val.cid + '">' + val.name +'</td><td> '+ val.grade + ' </td></tr>');
            }
            if (val.period == "ΙΟΥΝ"){
                juneitems.push('<tr><td class="date"><span class="date">'+getmili(val.added)+'</span></td><td><a href="/course?id='+ val.cid + '">' + val.name +'</td><td> '+ val.grade + ' </td></tr>');
            }
            if (val.period == "ΣΕΠΤ"){
                septitems.push('<tr><td class="date"><span class="date">'+getmili(val.added)+'</span></td><td><a href="/course?id='+ val.cid + '">' + val.name +'</td><td> '+ val.grade + ' </td></tr>');
            }
        }
        );
    }

    if (septitems.length>0){
        septitems.sort(function(a,b){
            if (a<=b){
                return 1;
            }
            else {
                return -1;
            }
        }
        );



        sept.find("tbody").append(septitems.join(''));
        sept.trigger("update");
    }

    if (febritems.length>0){
        febritems.sort(function(a,b){
            if (a<=b){
                return 1;
            }
            else {
                return -1;
            }
        }
        );

        febr.find("tbody").append(febritems.join(''));
        febr.trigger("update");
    } 
    if (juneitems.length>0){
        juneitems.sort(function(a,b){
            if (a<=b){
                return 1;
            }
            else {
                return -1;
            }
        }

        );
        june.find("tbody").append(juneitems.join(''));
        june.trigger("update");
    }


}
    var GLOB_PERIOD_DATA = {};
    GLOB_PERIOD_DATA['first'] = null;
    GLOB_PERIOD_DATA['second'] = null;
//function rendercourse(jsonpage, table, plot, pieall,piefailpass){

function rendercourse(){
    
    var results = [];
    var firstPeriodData = [];
    var secondPeriodData =[];
    var jqxhr = $.getJSON(jsonpage,
            function(data) {
                if(data!=null){

                    $.each(data, function(key,val) {
                        if (val.period=="ΙΟΥΝ"|| val.period=="ΦΕΒΡ"){
                            firstPeriodData.push(val);
                        }
                        else{
                            secondPeriodData.push(val);
                        }
                    }
                    );
                    firstPeriodTable = $("#firstgradelist");
                    secondPeriodTable = $("#secondgradelist");
                    populatecoursegrades(firstPeriodTable, firstPeriodData);
                    GLOB_PERIOD_DATA['first'] = firstPeriodData;
                    //renderplot("first"+plot,"first"+pieall,"first"+piefailpass,firstPeriodData);
                    GLOB_PERIOD_DATA['second'] = secondPeriodData;
                    populatecoursegrades(secondPeriodTable, secondPeriodData);
//                    renderplot("second"+plot,"second"+pieall,"second"+piefailpass,secondPeriodData);
                    renderplot()
                }

            });
}

function renderplot(){
    plot = "plot";
    pie = "pieall";
    piefailpass = "piefailpass";

    $.each(GLOB_PERIOD_DATA, function(key,data) { 
    items = [];
    for (i=0; i<=10; i++){
        items[i]=0;
    }
    fail=0;
    pass = 0;
    if(data!=null){
        $.each(data, function(key,val) {
            items[parseInt(val.grade)] = items[parseInt(val.grade)] + 1;
            if (val.grade<5) { fail = fail+1; }
            else { pass = pass +1; }
        }

        );
    }
//    $.jqplot(key + plot, [items]);
 //   $.jqplot(key + pie, [items]);
  //  $.jqplot(key + piefp, [items]);
  //

         var data = new google.visualization.DataTable();
         data.addColumn('string', 'Grade');
         data.addColumn('number', 'People');
      data.addRows([["0",items[0]],["1",items[1]], ["2", items[2]],
            ["3",items[3]], ["4",items[4]], ["5",items[5]],
            ["6",items[6]], ["7",items[7]],["8",items[8]],
            ["9",items[9]], ["10",items[10]]]);
          var chart = new google.visualization.ColumnChart(document.getElementById(key+plot));
    chart.draw(data, {width: 480, height: 480 });

         var data = new google.visualization.DataTable();
      data.addColumn('string', 'Grade');
      data.addColumn('number', 'Percent');
      data.addRows([["0",items[0]],["1",items[1]], ["2", items[2]],
            ["3",items[3]], ["4",items[4]], ["5",items[5]],
            ["6",items[6]], ["7",items[7]],["8",items[8]],
            ["9",items[9]], ["10",items[10]]]);
    var chart = new google.visualization.PieChart(document.getElementById(key+pie));
    chart.draw(data, {width: 480, height: 480, legend: 'top'});

         var data = new google.visualization.DataTable();
      data.addColumn('string', 'State');
      data.addColumn('number', 'People');
      data.addRows([['Fail', fail],['Pass',pass]]);
    var chart = new google.visualization.PieChart(document.getElementById(key+piefailpass));
    chart.draw(data, {width: 480, height: 480, legend: 'top'});


    });
    /*
    $.jqplot (pieall, [piedata], 
            { 
                seriesDefaults: {
                                    // Make this a pie chart.
                                    renderer: $.jqplot.PieRenderer, 
        rendererOptions: {
            showDataLabels: true
        }
                                },
        legend: { show:true, location: 'e' }
            }
            );
    $.jqplot (piefailpass, [[["fail",fail],["pass",pass]]], 
            { 
                seriesDefaults: {
                                    // Make this a pie chart.
                                    renderer: $.jqplot.PieRenderer, 
        rendererOptions: {
            showDataLabels: true
        }
                                },
        legend: { show:true, location: 'e' }
            }
            );
            */

}
function populatecoursegrades(table,data){
    items = [];
    firstmonth = [];
    secondmonth = [];
    if(data.length>0){
        $.each(data, function(key,val) {
            items.push('<tr><td><a href="/student?id=E'+val.sid + '"> E' + val.sid +'</td><td> '+ val.grade + ' </td></tr>');
        }
        );

        if (data[0].period=="ΦΕΒΡ"){
            $("#firstmonthlink").html("Φεβρουάριος");
        }
        else if (data[0].period=="ΙΟΥΝ"){
            $("#firstmonthlink").html("Ιούνιος");
        }

        table.find("tbody").append(items.join(''));
        table.trigger("update");

        table.trigger("applyWidgets",['zebra']);
    }
}
