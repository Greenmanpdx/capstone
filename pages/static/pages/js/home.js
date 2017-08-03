$(function () {
    $("#dialog").dialog({
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

    $("#createEncounterButton").on("click", function () {
        $("#dialog").dialog("open");
    });
});

$(function () {
    $("#addEncounter").dialog({
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

    $("#addEncounterButton").on("click", function () {
        $("#addEncounter").dialog("open");
    });
});

$(function () {
    $("#createPlayer").dialog({
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

    $("#createPlayerButton").on("click", function () {
        $("#createPlayer").dialog("open");
    });
});

$(function () {
    $("#addPlayer").dialog({
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

    $("#addPlayerButton").on("click", function () {
        $("#addPlayer").dialog("open");
    });
});

$(function () {
    $("#loadSession").dialog({
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

    $("#loadSessionButton").on("click", function () {
        $("#loadSession").dialog("open");
    });
});

$(function () {
    $(".widget input[type=submit], .widget a, .widget button").button();
    $("button, input, a").click(function (event) {
        //event.preventDefault();
    });
});




