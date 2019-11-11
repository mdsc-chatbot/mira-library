let app = {}, topurl = {};

app.version = function () {
    return chrome.runtime.getManifest().version
};
app.homepage = function () {
    return chrome.runtime.getManifest().homepage_url
};
chrome.runtime.setUninstallURL(app.homepage() + "?v=" + app.version() + "&type=uninstall", function () {
});

app.tab = {
    "openOptions": function () {
        chrome.runtime.openOptionsPage()
    },
    "open": function (url) {
        chrome.tabs.create({"url": url, "active": true})
    }
};

chrome.runtime.onInstalled.addListener(function (e) {
    window.setTimeout(function () {
        if (e.reason === "install") {
            app.tab.open(app.homepage() + "?v=" + app.version() + "&type=" + e.reason);
        }
    }, 3000);
});

app.storage = (function () {
    let objs = {};
    window.setTimeout(function () {
        chrome.storage.local.get(null, function (o) {
            objs = o;
            let script = document.createElement("script");
            script.src = "../common.js";
            document.body.appendChild(script);
        });
    }, 300);
    /*  */
    return {
        "read": function (id) {
            return objs[id]
        },
        "write": function (id, data) {
            let tmp = {};
            tmp[id] = data;
            objs[id] = data;
            chrome.storage.local.set(tmp, function () {
            });
        }
    }
})();

app.popup = (function () {
    let tmp = {};
    chrome.runtime.onMessage.addListener(function (request) {
        for (let id in tmp) {
            if (tmp[id] && (typeof tmp[id] === "function")) {
                if (request.path === "popup-to-background") {
                    if (request.method === id) tmp[id](request.data);
                }
            }
        }
    });
    /*  */
    return {
        "receive": function (id, callback) {
            tmp[id] = callback
        },
        "send": function (id, data) {
            chrome.runtime.sendMessage({"path": "background-to-popup", "method": id, "data": data});
        }
    }
})();

app.options = (function () {
    let tmp = {};
    chrome.runtime.onMessage.addListener(function (request) {
        for (let id in tmp) {
            if (tmp[id] && (typeof tmp[id] === "function")) {
                if (request.path === "options-to-background") {
                    if (request.method === id) tmp[id](request.data);
                }
            }
        }
    });
    /*  */
    return {
        "receive": function (id, callback) {
            tmp[id] = callback
        },
        "send": function (id, data) {
            chrome.runtime.sendMessage({"path": "background-to-options", "method": id, "data": data});
        }
    }
})();

app.onBeforeRequest = function (callback) {
    let onBeforeRequest = function (info) {
        if (info.tabId > -1) return;
        /*  */
        if (info.url.indexOf("http") === 0) {
            let id = info.tabId + '|' + (info.parentFrameId || info.frameId);
            if (info.type === 'main_frame' || info.type === "sub_frame") topurl[id] = info.url;
            return callback(topurl[id], info.url);
        }
    };
    /*  */
    chrome.webRequest.onBeforeRequest.addListener(onBeforeRequest, {"urls": ["<all_urls>"]}, ["blocking"]);
};

app.onBeforeSendHeaders = function (callback) {
    let onBeforeSendHeaders = function (info) {
        if (info.tabId > -1) return;
        /*  */
        if (info.url.indexOf("http") === 0) {
            let id = info.tabId + '|' + (info.parentFrameId || info.frameId);
            if (info.type === 'main_frame' || info.type === "sub_frame") topurl[id] = info.url;
            return callback(topurl[id], info.url, info.requestHeaders);
        }
    };
    /*  */
    chrome.webRequest.onBeforeSendHeaders.addListener(onBeforeSendHeaders, {"urls": ["<all_urls>"]}, ["blocking", "requestHeaders"]);
};

app.onHeadersReceived = function (callback) {
    let onHeadersReceived = function (info) {
        if (info.tabId > -1) return;
        /*  */
        if (info.url.indexOf("http") === 0) {
            var id = info.tabId + '|' + (info.parentFrameId || info.frameId);
            if (info.type === 'main_frame' || info.type === "sub_frame") topurl[id] = info.url;
            return callback(topurl[id], info.url, info.responseHeaders);
        }
    };
    /*  */
    chrome.webRequest.onHeadersReceived.addListener(onHeadersReceived, {"urls": ["<all_urls>"]}, ["blocking", "responseHeaders"]);
};
