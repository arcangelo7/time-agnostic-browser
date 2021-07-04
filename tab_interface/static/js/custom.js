
function isURI(string) {
    let url;
    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }
    return true
}

function showHumanReadableEntities(){
    config = $.get("/get_config", function(data){
        base_urls = data["base_urls"]
        $(".tripleObject, .resName").each(function(){
            tripleMemberElement = $(this)
            tripleMember = $(this).html()
            if (base_urls.length) {
                $.each(base_urls, function(i, base_url){
                    if (tripleMember.includes(base_url)){
                        tripleMemberElement
                            .html(tripleMember.replace(base_url, ""))
                            .attr("title", tripleMember)
                        if (tripleMemberElement.hasClass("tripleObject")){
                            tripleMemberElement
                                .addClass("tripleObjectRes")
                                .wrapInner(`<a href='${tripleMember}' class='entity'></a>`)
                        }  
                    }        
                });
            } else {
                if (isURI(tripleMember) && tripleMemberElement.hasClass("tripleObject")) {
                    $(tripleMemberElement)
                        .addClass("tripleObjectRes")
                        .wrapInner(`<a href='${tripleMember}' class='entity'></a>`)
                }    
            }
        });
        $(".triplePredicate, .tripleObject").not(".tripleObjectRes").each(function(){
            original_uri = $(this).html()
            slash = $(this).html().split("/")
            no_slash = slash[slash.length - 1]
            hashtag = no_slash.split("#")
            no_hashtag = hashtag[hashtag.length - 1]
            camelCase = no_hashtag.replace(/^[a-z]|[A-Z]/g, function(v, i) {
                return i === 0 ? v.toUpperCase() : " " + v.toLowerCase();
            });  
            $(this)
                .attr("title", original_uri)
                .html(camelCase)
        });    
    });
}

function showProvMetadataAsLink(){
    $(".responsibleAgent, .primarySource").each(function(){
        provMetadata = $(this) 
        provMetadataText = provMetadata.html()
        if (isURI(provMetadata.html())){
            provMetadata.wrapInner(`<a href="${provMetadataText}" class="provMetadataUrl" target="_blank"></a>`)
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
    var res = $(this).attr("href")
    resolveEntity(res)
});

$(function() {
    if(location.pathname != "/"){
        showHumanReadableEntities();
        showProvMetadataAsLink();
        $('.middle-line').first().remove();    
    }
});