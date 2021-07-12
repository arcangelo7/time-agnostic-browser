acronymns = ["doi", "orcid"]
orcid = /orcid\.org\/\d{4}\-\d{4}\-\d{4}\-\d{4}/

function isURI(string) {
    let url;
    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }
    return true
}

function isAnIdentifier(str, schema) {
    return schema.exec(str)
}

function unicodeToChar(text) {
    return text.replace(/\\\\u[\dA-F]{4}/gi,
        function (match) {
            return String.fromCharCode(parseInt(match.replace(/\\\\u/g, ''), 16));
        });
}

function wrapEntitiesInLinks(baseUrls) {
    $(".tripleObject, .resName, #sparqlResults td, .se_description").each(function () {
        tripleMemberElement = $(this)
        tripleMember = $(this).html()
        if (baseUrls.length) {
            $.each(baseUrls, function (i, baseUrl) {
                if (tripleMember.includes(baseUrl)) {
                    Array.from(tripleMember.matchAll(`${baseUrl}\\w+/\\d+`), function(m){
                        shortenedUri = m[0].replace(baseUrl, "")
                        if (tripleMemberElement.hasClass("resName")) {
                            tripleMember = tripleMember
                            .replace(m, `<span class="shortenedUri">${shortenedUri}</span>`)
                        } else {
                            tripleMember = tripleMember
                            .replace(m, `<a href='${m}' title='${m}' class='entity'><span class="shortenedUri">${shortenedUri}</span></a>`)
                        }
                        tripleMemberElement.html(tripleMember)
                    });
                }
            });
        } else {
            if (isURI(tripleMember) && tripleMemberElement.hasClass("tripleObject")) {
                $(tripleMemberElement)
                    .addClass("tripleRes")
                    .wrapInner(`<a href='${tripleMember}' class='entity'></a>`)
            }
        }
    });
}

function beautifyURIs() {
    $(".triplePredicate, .tripleObject, #sparqlResults td").not(".shortenedUri").each(function () {
        original_text = $(this).html()
        if (isAnIdentifier(original_text, orcid)) {
            $(this).wrapInner(`<a href='${original_text}' class="identifier" target="_blank"></a>`)
        }
        else if (isURI(original_text)) {
            slash = $(this).html().split("/")
            no_slash = slash[slash.length - 1]
            hashtag = no_slash.split("#")
            no_hashtag = hashtag[hashtag.length - 1]
            camelCase = no_hashtag.replace(/^[a-z]|[A-Z]/g, function (v, i) {
                return i === 0 ? v.toUpperCase() : " " + v.toLowerCase();
            });
            if (acronymns.includes(camelCase.toLowerCase())) {
                camelCase = camelCase.toUpperCase()
            }
            $(this)
                .attr("title", original_text)
                .html(camelCase)
        } else {
            toChar = unicodeToChar(original_text)
            $(this).html(toChar)
        }
    });
}

function showHumanReadableEntities() {
    config = $.get("/get_config", function (data) {
        baseUrls = data["base_urls"]
        wrapEntitiesInLinks(baseUrls);
        beautifyURIs();
    });
}

function showProvMetadataAsLink() {
    $(".responsibleAgent, .primarySource").each(function () {
        provMetadata = $(this)
        provMetadataText = provMetadata.html()
        if (isURI(provMetadata.html())) {
            provMetadata.wrapInner(`<a href="${provMetadataText}" class="provMetadataUrl" target="_blank"></a>`)
        }
    });
}

function resolveEntity(res) {
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

const App = new Vue({
    el: '#sparqlResults',
    vuetify: new Vuetify(),
    delimiters: ['<%', '%>'],
    data: {
        response: [],
        headers: []
    },
    methods: {
        submitQuery() {
            $("#querySubmit").html(`
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span class="ml-1">Loading...</span>
            `);
            $(".sparqlResults .row").empty();
            var query = $("textarea#sparqlEndpoint").val()
            this.$http.post("/query", { "query": query }, { 'emulateJSON': true }).then(function (data) {
                this.response = data["body"]["response"]
                headers = []
                $(this.response).each(function (_, snapshots) {
                    $.each(snapshots, function (_, values) {
                        $(values).each(function (_, value) {
                            $.each(value, function (key, _) {
                                header = { "text": key, "value": key, "sortable": true }
                                if (!headers.some(header => header.text == key && header.value == key)) {
                                    headers.push(header)
                                }
                            });
                        });
                    });
                });
                this.headers = headers
                showHumanReadableEntities();
                $("#querySubmit")
                    .html(`
                        <span class="mr-1"><span class="fas fa-search"></span></span>
                        Submit the query
                    `)
                    .blur();
            });
        }
    },
    updated: function(){
        $('.middle-line').first().remove();
    }
})

// Click on entity
$(document).on("click", "a.entity", function (e) {
    e.preventDefault()
    var res = $(this).attr("href")
    resolveEntity(res)
});

$(function () {
    if (location.pathname != "/") {
        showHumanReadableEntities();
        showProvMetadataAsLink();
        $('.middle-line').first().remove();
    }
});