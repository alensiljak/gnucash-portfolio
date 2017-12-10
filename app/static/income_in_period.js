$(function () {
    // read the dates, if any.
    var date_from = $("#datefrom").val();
    if (date_from) {
        $('#period').data('daterangepicker').setStartDate(date_from);
    } else {
        var startDate = $("#period").data('daterangepicker').startDate.format('YYYY-MM-DD');
        $("#datefrom").val(startDate);
    }

    var date_to = $("#dateto").val();
    if (date_to) {
        $("#period").data('daterangepicker').setEndDate(date_to);
    } else {
        var endDate = $("#period").data('daterangepicker').endDate.format('YYYY-MM-DD');
        $("#dateto").val(endDate);
    }

    $("#period").on("apply.daterangepicker", function (ev, picker) {
        $("#datefrom").val(picker.startDate.format('YYYY-MM-DD'));
        $("#dateto").val(picker.endDate.format('YYYY-MM-DD'));
    });
});
