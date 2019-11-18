let LOG = false;

/**
 * Setting up the storage data
 * @param event
 */
let popupsend = function (event) {
    app.popup.send("storage-data", {
        "force": event
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