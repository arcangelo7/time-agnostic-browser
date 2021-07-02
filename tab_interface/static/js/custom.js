
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
    window.location.href = `/entity/${res}` 
}

// Click on exploreSubmit
$("#exploreSubmit").on("click", function () {
    var res = $("input#searchByURI").val()
    $("#exploreSubmit").html(`
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span class="ml-1">Loading...</span>
    `);
    resolveEntity(res)
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