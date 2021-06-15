// Click on exploreSubmit
$("#exploreSubmit").on("click", function () {
    var res = $("input#searchByURI").val()
    $("#exploreSubmit").html(`
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span class="ml-1">Loading...</span>
    `);
    $.get("/entity/" + res, function (data) {
        $("#alert").empty();
        if (data["results"] == "error"){
            $("#alert").html(`
                <div class="alert alert-danger alert-dismissible shadow-soft fade show" role="alert">
                    <span class="alert-inner--icon"><span class="fas fa-exclamation-circle"></span></span>
                    <span class="alert-inner--text"><strong>Oh snap!</strong> Change a few things up and try
                        submitting again.</span>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>                
            `)
            $("#exploreSubmit").html(`
                <span class="mr-1"><span class="fas fa-search"></span></span>
                Submit the query
            `);
            $("#exploreSubmit").blur();
            return
        }
        else {
            window.location.href = "/entity/" + res;
        }
    });
});