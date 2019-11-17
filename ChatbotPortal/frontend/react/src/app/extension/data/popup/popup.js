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

    /**
     * Extracting the current tab url
     */
    chrome.tabs.query({active: true, currentWindow: true}, function (tabArray) {
        let iframe = document.querySelector("iframe");

        fetch('http://127.0.0.1:8000/authentication/auth/currentuser/')
            .then(function (response) {
                if (!response.ok) {
                    throw Error(response.statusText);
                }
                // Read the response as json.
                return response.json();
            })
            .then(function (responseAsJson) {
                // Do stuff with the JSON
                console.log(responseAsJson.email);
                if (iframe) {
                        // Upon finding the iframe tag, set the src to the desired url that we want to show in the popup
                        iframe.style.background = "none";
                        if (iframe.src === "about:blank") {
                            iframe.src = `http://127.0.0.1:8000/chatbotportal/app/resource_submit/extension/${responseAsJson.id}/''/${responseAsJson.token}/${encodeURIComponent(tabArray[0].url)}`;
                        }
                    }
                chrome.cookies.get({"url": 'http://127.0.0.1', "name": 'sessionid'}, function (cookie) {
                    console.log(cookie);
                    window.document.cookie = cookie;
                    console.log(window.document.cookie);

                });
            })
            .catch(function (error) {
                console.log('Looks like there was a problem: \n', error);
            });


    });
});

// Adding event listener upon the window being loaded
window.addEventListener("load", load, false);