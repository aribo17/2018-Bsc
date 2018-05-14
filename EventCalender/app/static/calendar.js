$(document).ready(function() {
    var oReq = new XMLHttpRequest();
    var data;

    oReq.open("GET", '/auth/get_event_data', true);
    oReq.send();

    oReq.onreadystatechange = function() {
        if (oReq.readyState == 4 && oReq.status == 200) {
            data = JSON.parse(oReq.responseText);
            console.log(data)
            var c_data = []; // list of all events
            var temp_obj = {}
            for(var i=0; i<Object.keys(data).length;i++){
              temp_obj= {
                title:data[i].name,
                start:moment(data[i].startDate.concat("T",data[i].startTime)),
                end:moment(data[i].endDate.concat("T",data[i].endTime))
              };
              c_data.push(temp_obj);
            };
            $('#calendar').fullCalendar({
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,basicWeek,basicDay'
                },
                defaultDate: moment(),
                editable: false,
                eventLimit: true, // allow "more" link when too many events
                events: c_data,
                displayEventTime: false
            });
            }

    }
 });
