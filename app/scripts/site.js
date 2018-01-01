// import popper from 'popper.js'
// import $ from 'jquery'
// import moment from 'moment'
// import daterangepicker from 'daterangepicker'
// import bootstrap from 'bootstrap'


$(function () {
    //var start = moment().subtract(29, 'days');
    //var end = moment();

    $('input.daterange').daterangepicker({
        //autoUpdateInput: false,
        locale: {
            format: 'YYYY-MM-DD'
        },
        alwaysShowCalendars: true,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    });

    /*
        mark the active nav-item by comparing the current url to the nav link.
    */
    var getLocation = function (href) {
        var l = document.createElement("a");
        l.href = href;
        return l;
    };
    currentLocation = getLocation(window.location);
    // Now find the link with the current path.
    $("#leftnav").find("a[href='" + currentLocation.pathname + "']")
        .addClass("active");
    //console.log(found);
    
    // Activate select2 components.
    // $('select.select2').select2();
    // Use chosen.
    $('select.chosen').chosen();
});
