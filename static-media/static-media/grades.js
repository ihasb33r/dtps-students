function showmessage(message){
    $('body').append('<span id="result"></span>');
    $('#result').addClass(message);
    $('#result').html(message);
    setTimeout(function(){
        $("#result").fadeOut("slow", function () {
            $("#result").remove();
        });
    }, 1000);

}

var resultstable = [" <table id='gradelist' class='tablesorter'>",
        "<thead>",
            "<tr>",
                "<th>Όνομα Μαθήματος</th>",
               " <th>Βαθμός</th>",
               " <th>Εξεταστική</th>",
           " </tr>",
        "</thead>",
        "<tbody>",
        "</tbody>",
    "</table>"
].join("\n");


function getgrades(jsonpage,params, cache) { 
    var updatelink = $('#update-link');
    updatelink.html("Waaait for iiit");
    if (cache==true){
        jsonpage = jsonpage + "?cache=yes" + params ; 
    }
    else
    {
        jsonpage = jsonpage + "?cache=no" + params ; 
    }
    var results = [];

    var jqxhr = $.getJSON(jsonpage,
            function(data) {
                var items = [];
                var results = [];
                if(data!=null){
                    $.each(data, function(key,val) {
                        if (val.grade != "-"){

                            items.push('<tr><td> ' + val.sid +'</td><td> '+ val.grade + ' </td><td> ' + val.period + '</td></tr>');
                        };
                    });
                }

                updatelink.html("Update");

                if (items.length==0){
                    showmessage("fail");
                }
                else{
                    $("#gradelist").remove();
                    $("#main").append(resultstable);

                    $("#gradelist").find("tbody").append(items.join(''));
                    showgraph(results);
                    $("#gradelist").tablesorter({sortList: [[3,1]], widgets:['zebra']}); 

                    showmessage("success");

                }
            });

}

function showgraph(grades){

    var counts = [];
    var byperiod = [];
    var periods = {"ΦΕΒΡ":1,"ΙΟΥΝ":2,"ΣΕΠΤ":3};

    $.each(grades, function(key,item){
        byperiod[item.name + item.period] = {"total":0, "average":0, "count":0};
    });
    $.each(grades, function(key,item){
        byperiod[item.name + item.period].total += parseInt(item.grade);
        byperiod[item.name + item.period].count ++;
    });
    byperiod.sort();
    averagebyperiod = [];
    countsbyperiod = [];
    $.each( byperiod, function(key,value){
        averagebyperiod.push(key,value.total/value.count);
        countsbyperiod.push(key,value.count);
    });

    for (i=0;i<=10;i++){
        counts[i]=1;
    }
    $.each(grades, function(key,item){
        counts[parseInt(item.grade)]++;
    });

    var results = [];
    for (i=0;i<=10;i++){
        results[i] = [i,counts[i]];
    }

//    $.jqplot("container", [averagebyperiod,countsbyperiod]);
    $.jqplot("container", [results]);
}


