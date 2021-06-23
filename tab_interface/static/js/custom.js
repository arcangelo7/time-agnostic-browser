
function isURI(string) {
    let url;
    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }
    return true
}

function transformEntitiesInLinks(){
    $(".tripleObject").each(function(){
        tripleMember = $(this).html()
        if (isURI(tripleMember)) {
            $(this).wrapInner(`<a href='' class='entity'></a>`)
        }
    });
} 

function resolveEntity(res){
    $.get("/is_an_entity/" + res, function (data) {
        if (data["results"] == "error" || !data["results"]){
            if (data["results"] == "error"){
                message = "<strong>Oh snap!</strong> There are connection problems with the database."
            } else if (!data["results"]){
                message = "<strong>Oh snap!</strong> The entity does not exist."
            }
            $("#alert").empty();
            $("#alert").html(`
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <span class="fas fa-exclamation-circle"></span>
                    ${message}
                    <button type="button" class="btn-close" data-dismiss="alert" aria-label="Close"></button>
                </div>                 
            `)
            $("#exploreSubmit").html(`
                <span class="mr-1"><span class="fas fa-search"></span></span>
                Submit the query
            `);
            $("#exploreSubmit").blur();
        } else {
            window.location.href = "/entity/" + res;
        }
    })
}

// Click on exploreSubmit
$("#exploreSubmit").on("click", function () {
    var res = $("input#searchByURI").val()
    $("#exploreSubmit").html(`
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span class="ml-1">Loading...</span>
    `);
    resolveEntity(res)
    // $.get("/entity/" + res, function (data) {
    //     console.log(data)
    //     $("#alert").empty();
    //     if (!data["results"]){
    //         $("#alert").html(`
    //             <div class="alert alert-danger alert-dismissible fade show" role="alert">
    //                 <span class="fas fa-exclamation-circle"></span>
    //                 <strong>Oh snap!</strong> There are connection problems with the database.
    //                 <button type="button" class="btn-close" data-dismiss="alert" aria-label="Close"></button>
    //             </div>                
    //         `)
    //         $("#exploreSubmit").html(`
    //             <span class="mr-1"><span class="fas fa-search"></span></span>
    //             Submit the query
    //         `);
    //         $("#exploreSubmit").blur();
    //         return
    //     }
    //     else {
    //         window.location.href = "/entity/" + res;
    //     }
    // });
});

// Click on entity
$(document).on("click", "a.entity", function(e){
    e.preventDefault()
    var res = $(this).html()
    resolveEntity(res)
});

$(function() {
    transformEntitiesInLinks();
    $('.middle-line').first().remove();
});