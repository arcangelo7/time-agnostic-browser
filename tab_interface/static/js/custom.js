
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
    config = $.get("/get_config", function(data){
        base_urls = data["base_urls"]
        $(".tripleObject").each(function(){
            tripleMemberElement = $(this)
            tripleMember = $(this).html()
            if (base_urls.length) {
                $.each(base_urls, function(i, base_url){
                    if (tripleMember.includes(base_url)){
                        $(tripleMemberElement).wrapInner(`<a href='' class='entity'></a>`)
                    }        
                });
            } else {
                if (isURI(tripleMember)) {
                    $(this).wrapInner(`<a href='' class='entity'></a>`)
                }    
            }
        });
    });
}

function showHumanReadablePredicate(){
    $(".triplePredicate").each(function(){
        original_uri = $(this).html()
        slash = $(this).html().split("/")
        no_slash = slash[slash.length - 1]
        hashtag = no_slash.split("#")
        no_hashtag = hashtag[hashtag.length - 1]
        camelCase = no_hashtag.replace(/^[a-z]|[A-Z]/g, function(v, i) {
            return i === 0 ? v.toUpperCase() : " " + v.toLowerCase();
        });  
        $(this)
            // .attr("data-toggle", "tooltip")
            // .attr("data-placement", "right")
            .attr("title", original_uri)
            .html(camelCase)
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
    showHumanReadablePredicate();
    transformEntitiesInLinks();
    $('[data-toggle="tooltip"]').tooltip()
    $('.middle-line').first().remove();
});