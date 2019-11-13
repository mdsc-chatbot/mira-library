let config = {};

/**
 * Configuring popup width and height
 * @type {{width, height}}
 */
config.popup = {
    get width() {
        return +app.storage.read('width') || 400
    },
    get height() {
        return +app.storage.read('height') || 520
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
