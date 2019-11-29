/**
 * @file: chrome.js
 * @summary: Registers the chrome APIs required for background and popup communication.
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

let app = {}, topurl = {};

/**
 * Getting the version from the manifest
 * @returns {string}
 */
app.version = function () {
    return chrome.runtime.getManifest().version
};

/**
 * Getting the homepage url from the manifest
 * @returns {string}
 */
app.homepage = function () {
    return chrome.runtime.getManifest().homepage_url
};

/**
 * App tab will create a new tab with the url specified
 * @type {{open: app.tab.open}}
 */
app.tab = {
    "open": function (url) {
        chrome.tabs.create({"url": url, "active": true})
    }
};

/**
 * Setting up app installation status
 */
chrome.runtime.onInstalled.addListener(function (event) {
    window.setTimeout(function () {
        if (event.reason === "install") {
            //  Upon installing for the first time, redirect to the ChatbotPortal homepage
            app.tab.open(app.homepage());
        }
    }, 3000);
});

/**
 * Setting up app uninstall status
 */
chrome.runtime.setUninstallURL(app.homepage() + "?v=" + app.version() + "&type=uninstall", function () {
});

/**
 * Setting up the app storage with required data
 * @type {{read: (function(*): *), write: app.storage.write}}
 */
app.storage = (function () {
    let objs = {};
    // Injecting common.js script
    window.setTimeout(function () {
        chrome.storage.local.get(null, function (o) {
            objs = o;
            let script = document.createElement("script");
            script.src = "../common.js";
            document.body.appendChild(script);
        });
    }, 300);

    return {
        // Reading from the storage
        "read": function (id) {
            return objs[id]
        },

        // Writing in the local storage
        "write": function (id, data) {
            let temporary = {};
            temporary[id] = data;
            objs[id] = data;
            chrome.storage.local.set(temporary, function () {
            });
        }
    }
})();

/**
 * Initializing the popup communication object
 * that the background will use to interact with the popup
 * @type {{receive: app.popup.receive, send: app.popup.send}}
 */
app.popup = (function () {
    let temporary = {};
    // Setting up the communication ground from popup to background
    chrome.runtime.onMessage.addListener(function (request) {
        for (let id in temporary) {
            if (temporary.hasOwnProperty(id)) {
                if (temporary[id] && (typeof temporary[id] === "function")) {
                    if (request.path === "popup-to-background") {
                        if (request.method === id) temporary[id](request.data);
                    }
                }
            }
        }
    });

    return {
        // Receiving information from the popup upon sending query
        "receive": function (id, callback) {
            temporary[id] = callback
        },
        // Sending the query to the popup for a required method and data
        "send": function (id, data) {
            chrome.runtime.sendMessage({"path": "background-to-popup", "method": id, "data": data});
        }
    }
})();

/**
 * Fires when a request is about to occur.
 * This event is sent before any TCP connection is made and can be used to cancel or redirect requests.
 * @param callback = Being called after asynchronous operation
 */
app.onBeforeRequest = function (callback) {
    let onBeforeRequest = function (info) {
        if (info.tabId > -1) return;
        if (info.url.indexOf("http") === 0) {
            let id = info.tabId + '|' + (info.parentFrameId || info.frameId);
            if (info.type === 'main_frame' || info.type === "sub_frame") topurl[id] = info.url;
            return callback(topurl[id], info.url);
        }
    };
    chrome.webRequest.onBeforeRequest.addListener(onBeforeRequest, {"urls": ["<all_urls>"]}, ["blocking"]);
};

/**
 * Fires when a request is about to occur and the initial headers have been prepared.
 * The event is intended to allow extensions to add, modify, and delete request headers.
 * @param callback = Being called after asynchronous operation
 */
app.onBeforeSendHeaders = function (callback) {
    let onBeforeSendHeaders = function (information) {
        if (information.tabId > -1) return;
        if (information.url.indexOf("http") === 0) {
            let id = information.tabId + '|' + (information.parentFrameId || information.frameId);
            if (information.type === 'main_frame' || information.type === "sub_frame") topurl[id] = information.url;
            return callback(topurl[id], information.url, information.requestHeaders);
        }
    };
    chrome.webRequest.onBeforeSendHeaders.addListener(onBeforeSendHeaders, {"urls": ["<all_urls>"]}, ["blocking", "requestHeaders"]);
};

/**
 * Fires each time that an HTTP(S) response header is received.
 * Due to redirects and authentication requests this can happen multiple times per request.
 * This event is intended to allow extensions to add, modify, and delete response headers, such as incoming Content-Type headers.
 * @param callback = Being called after asynchronous operation
 */
app.onHeadersReceived = function (callback) {
    let onHeadersReceived = function (information) {
        if (information.tabId > -1) return;
        if (information.url.indexOf("http") === 0) {
            let id = information.tabId + '|' + (information.parentFrameId || information.frameId);
            if (information.type === 'main_frame' || information.type === "sub_frame") topurl[id] = information.url;
            return callback(topurl[id], information.url, information.responseHeaders);
        }
    };
    chrome.webRequest.onHeadersReceived.addListener(onHeadersReceived, {"urls": ["<all_urls>"]}, ["blocking", "responseHeaders"]);
};
