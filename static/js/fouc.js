function getScript(url, integrity, crossorigin){
    var script = document.createElement("script")
    script.type = "text/javascript";
    script.src = url;
    script.defer = true;
    script.integrity = integrity;
    script.crossOrigin = crossorigin;
    document.getElementsByTagName("head")[0].appendChild(script);
}

function setClass(selector, myClass) {
    element = document.querySelector(selector);
    console.log(element)
    element.className = myClass;
}

function removeClass(selector, myClass) {
    element = document.querySelector(selector);
    var reg = new RegExp('(^| )'+myClass+'($| )','g');
    element.className = element.className.replace(reg,' ');
}

// hide the html when the page loads, but only if js is turned on.
setClass('html', 'prevent_fouc');

// when the DOM has finished loading, unhide the html
document.onreadystatechange = function () {
    if (document.readyState == "interactive") {
        removeClass('html', 'prevent_fouc');
        getScript(
            'https://pro.fontawesome.com/releases/v5.0.9/js/all.js',
            'sha384-DtPgXIYsUR6lLmJK14ZNUi11aAoezQtw4ut26Zwy9/6QXHH8W3+gjrRDT+lHiiW4',
            'anonymous'
        )
    }
}