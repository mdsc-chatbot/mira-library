/**
 * @file: common.js
 * @summary: Registers the APIs required for background and popup communication.
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