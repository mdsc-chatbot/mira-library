import React from "react";
import HomepageHead from "./HomepageHead";
import HomepageContent from "./HomepageContent";

export default class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div>
                <HomepageHead />
                <HomepageContent />
            </div>
        );
    }
}
