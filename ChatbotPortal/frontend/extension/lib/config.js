let config = {};

config.popup = {
    set unload(val) {
        app.storage.write("unload", val)
    },
    set url(val) {
        app.storage.write("website-url", val)
    },
    get width() {
        return +app.storage.read('width') || 400
    },
    get height() {
        return +app.storage.read('height') || 520
    },
    get url() {
        return app.storage.read("website-url") || ''
    },
    set iframe(val) {
        app.storage.write("popup-iframe", val)
    },
    set scrollbar(val) {
        app.storage.write("scrollbar", val)
    },
    set mobile(val) {
        app.storage.write("mobile-view-index", val)
    },
    get mobile() {
        return app.storage.read("mobile-view-index") || 0
    },
    get unload() {
        return app.storage.read("unload") !== undefined ? app.storage.read("unload") : false
    },
    get scrollbar() {
        return app.storage.read("scrollbar") !== undefined ? app.storage.read("scrollbar") : false
    },
    get iframe() {
        return app.storage.read("popup-iframe") !== undefined ? app.storage.read("popup-iframe") : true
    },
    set width(val) {
        val = +val;
        if (val < 200) val = 400;
        app.storage.write("width", val);
    },
    set height(val) {
        val = +val;
        if (val < 200) val = 500;
        app.storage.write("height", val);
    }
};
