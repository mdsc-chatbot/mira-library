import axios from "axios";
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

// chrome.cookies.getAll({},function (cookie){
//         console.log(cookie.length);
//         for(i=0;i<cookie.length;i++){
//             console.log(JSON.stringify(cookie[i]));
//         }
//     });

    axios
            .get('http://127.0.0.1:8000/authentication/auth/currentuser/')
            .then(
                response => {
                    console.log(response)
                    // if response.data !== null
                    // if (response.data !== '') {
                    //     response.data['is_logged_in'] = true;
                    //     this.setState({security: response.data});
                    //     console.log(this.state.security.is_logged_in);
                    // } else {
                    //     response.data = JSON.parse('{}');
                    //     response.data['is_logged_in'] = false;
                    //     this.setState({security: response.data});
                    //     console.log(this.state.security.is_logged_in);
                    // }
                },
                error => {
                    console.log(error);
                }
            );

    console.log("BABABABABAB")
    console.log(window.parent)

    /**
     * Extracting the current tab url
     */
    chrome.tabs.query({active: true, currentWindow: true}, function (tabArray) {
        let iframe = document.querySelector("iframe");

        chrome.cookies.get({"url": 'http://127.0.0.1', "name": 'sessionid'}, function (cook) {
            console.log(cook.value);
            chrome.cookies.set({'url': 'http://127.0.0.1', 'name': 'sessionid', 'value': cook.value}, function () {
                if (iframe) {
                    // Upon finding the iframe tag, set the src to the desired url that we want to show in the popup
                    iframe.style.background = "none";
                    // window.open('https://www.google.com/')
                    if (iframe.src === "about:blank") iframe.src = `http://127.0.0.1:8000/chatbotportal/app/resource_submit/${encodeURIComponent(tabArray[0].url)}`;
                }
            });
        });
    });
});

// function cookieinfo(){
//     chrome.cookies.getAll({},function (cookie){
//         console.log(cookie.length);
//         for(i=0;i<cookie.length;i++){
//             console.log(JSON.stringify(cookie[i]));
//         }
//     });
//     chrome.cookies.getAllCookieStores(function (cookiestores){
//         for(i=0;i<cookiestores.length;i++){
//             console.log(JSON.stringify(cookiestores[i]));
//         }
//     });
//     chrome.cookies.set({"name":"Sample1","url":"http://developer.chrome.com/extensions/cookies.html","value":"Dummy Data"},function (cookie){
//         console.log(JSON.stringify(cookie));
//         console.log(chrome.extension.lastError);
//         console.log(chrome.runtime.lastError);
//     });
//     chrome.cookies.onChanged.addListener(function (changeInfo){
//         console.log(JSON.stringify(changeInfo));
//     });
// }
// window.onload=cookieinfo;

// Adding event listener upon the window being loaded
window.addEventListener("load", load, false);