let background = (function () {
    let tmp = {};
    chrome.runtime.onMessage.addListener(function (request) {
        for (let id in tmp) {
            if (tmp[id] && (typeof tmp[id] === "function")) {
                if (request.path === "background-to-popup") {
                    if (request.method === id) tmp[id](request.data);
                }
            }
        }
    });

    return {
        "receive": function (id, callback) {
            tmp[id] = callback
        },
        "send": function (id, data) {
            chrome.runtime.sendMessage({"path": "popup-to-background", "method": id, "data": data})
        }
    }
})();

let load = function () {
    background.send("resize");
    background.send("storage-data");
    window.removeEventListener("load", load, false);
};

background.receive("resize", function (o) {
    document.body.style.width = o.width + "px";
    document.body.style.height = o.height + "px";
    document.documentElement.style.width = o.width + "px";
    document.documentElement.style.height = o.height + "px";
});

background.receive("storage-data", function () {

    chrome.tabs.query({active: true, currentWindow: true}, function (tabArray) {
        let iframe = document.querySelector("iframe");
        if (iframe) {
            console.log(`http://127.0.0.1:8000/chatbotportal/app/resource_submit/${encodeURIComponent(tabArray[0].url)}`);
            iframe.style.background = "none";
            if (iframe.src === "about:blank") iframe.src = `http://127.0.0.1:8000/chatbotportal/app/resource_submit/${encodeURIComponent(tabArray[0].url)}`;
        }
    });
});

window.addEventListener("load", load, false);