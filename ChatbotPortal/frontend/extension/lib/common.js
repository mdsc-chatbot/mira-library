let LOG = false;

/**
 * Setting up the storage data
 * @param event
 */
let popupsend = function (event) {
    app.popup.send("storage-data", {
        "force": event,
        "url": config.popup.url,
        "iframe": config.popup.iframe
    });
};

/**
 * Fires each time that an HTTP(S) response header is received.
 * Due to redirects and authentication requests this can happen multiple times per request.
 * This event is intended to allow extensions to add, modify, and delete response headers, such as incoming Content-Type headers.
 * @param callback = Being called after asynchronous operation (A function)
 */
app.onHeadersReceived(function (top, current, headers) {
    for (let i = 0; i < headers.length; i++) {
        let name = headers[i].name.toLowerCase();
        if (name === "x-frame-options" || name === "frame-options") {
            headers.splice(i, 1);
            if (LOG) console.error("> Header", name);
            return {"responseHeaders": headers};
        }
    }
});

/**
 * Fires when a request is about to occur and the initial headers have been prepared.
 * The event is intended to allow extensions to add, modify, and delete request headers.
 * @param callback = Being called after asynchronous operation (A function)
 */
app.onBeforeSendHeaders(function (top, current, headers) {
    for (let i = 0; i < headers.length; i++) {
        let name = headers[i].name.toLowerCase();
        if (name === "user-agent") {
            // Checking for mobile configuration
            let id = parseInt(config.popup.mobile);
            if (id < 5) {
                let value = "Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36";
                if (id === 0) value = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1";
                if (id === 1) value = "Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30";
                if (id === 2) value = "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586";
                if (id === 3) value = "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)";
                if (id === 4) value = "Mozilla/5.0 (Linux; U; Tizen 2.0; en-us) AppleWebKit/537.1 (KHTML, like Gecko) Mobile TizenBrowser/2.0";
                headers[i].value = value;

                if (LOG) console.error("> UA", value);
                return {"requestHeaders": headers};
            }
        }
    }
});

/**
 * Getting the storage data set by popup upon being initialized
 */
app.popup.receive("storage-data", function () {
    popupsend(false)
});

/**
 * Getting the resize parameters according the to popup width and height
 */
app.popup.receive("resize", function () {
    app.popup.send("resize", {"width": config.popup.width, "height": config.popup.height})
});