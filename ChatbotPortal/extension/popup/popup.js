/**
 * @file: popup.js
 * @summary: Performs the operations as the popup gets mounted. It calls the logged in user and retrieve the JWT token.
 *              Depending on its success, it renders a resource submission page or redirects to the login page in a new tab.
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

const BASE_URL = 'http://162.246.157.169:8000';

/**
 * Initializing the background communication object
 * that the popup will use to interact with the background
 * @type {{receive: background.receive, send: background.send}}
 */
let background = (function () {
    let temporary = {};
    // Setting up the communication ground from background to popup
    chrome.runtime.onMessage.addListener(function (request) {
        for (let id in temporary) {
            if (temporary.hasOwnProperty(id)) {
                if (temporary[id] && (typeof temporary[id] === "function")) {
                    if (request.path === "background-to-popup") {
                        if (request.method === id) temporary[id](request.data);
                    }
                }
            }
        }
    });

    return {
        // Receiving information from the background upon sending query
        "receive": function (id, callback) {
            temporary[id] = callback
        },
        // Sending the query to the background for a required method and data
        "send": function (id, data) {
            chrome.runtime.sendMessage({"path": "popup-to-background", "method": id, "data": data})
        }
    }
})();

/**
 * Set the initial loading status, communicating with the background
 * for required parameter to render the page and redirect the URL.
 */
let load = function () {
    background.send("resize");
    background.send("storage-data");
    window.removeEventListener("load", load, false);
};

/**
 * This function loads an iframe in the popup html with our desired page and parameters
 * @param dataAsJson = Jsonified data
 * @param url = url that would be passed along as a parameter
 */
let iframing = function (dataAsJson, url) {
    let iframe = document.querySelector("iframe");
    if (iframe) {
        // Upon finding the iframe tag, set the src to the desired url that we want to show in the popup
        iframe.style.background = "none";
        if (iframe.src === "about:blank") {
            // iframe.onload = function() { alert('myframe is loaded'); console.log(iframe.contentDocument) };
            if (!!dataAsJson.first_name) {
                iframe.src = `${BASE_URL}/chatbotportal/app/resource_submit/extension/${dataAsJson.id}/${dataAsJson.first_name}/${dataAsJson.token}/${encodeURIComponent(url)}`;
            } else {
                iframe.src = `${BASE_URL}/chatbotportal/app/resource_submit/extension/${dataAsJson.id}/''/${dataAsJson.token}/${encodeURIComponent(url)}`;
            }
        }
    }
};

/**
 * Resizing the popup to provide responsiveness
 */
background.receive("resize", function (o) {
    document.body.style.width = o.width + "px";
    document.body.style.height = o.height + "px";
    document.documentElement.style.width = o.width + "px";
    document.documentElement.style.height = o.height + "px";
});

/**
 * Sending storage data from background to popup
 */
background.receive("storage-data", function () {
    // Fetch the current user from the backend
    fetch(`${BASE_URL}/chatbotportal/authentication/currentuser/`)
        .then(function (response) {
            if (response.status === 200) {
                // Upon finding a logged in user, return the jsonified details.
                return response.json();
            } else {
                // If not logged in user is found, redirect to login page
                chrome.tabs.create({url: `${BASE_URL}/chatbotportal/app/login`});
            }
        })
        .then(function (responseAsJson) {
            // Finding the current tab url
            chrome.tabs.query({active: true, currentWindow: true}, function (tabArray) {
                // Upon finding the current tab url call the iframing function to show our desired url with specified parameters
                iframing(responseAsJson, tabArray[0].url)
            });
        })
        .catch(function (error) {
            console.log('Looks like there was a problem: \n', error);
        });
});

// Adding event listener upon the window being loaded
window.addEventListener("load", load, false);