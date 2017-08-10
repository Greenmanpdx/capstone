$(function () {
    $("#charMenu").dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 1000
        },
        hide: {
            effect: "explode",
            duration: 1000
        }
    });

    $("#charListItem").on("click", function () {
        $("#charMenu").dialog("open");
    });
});

$(function () {
    $("button").button();

});