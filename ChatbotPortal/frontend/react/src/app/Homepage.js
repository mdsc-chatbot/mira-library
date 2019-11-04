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
            <div
                style={{
                    paddingTop: 30,
                    paddingLeft: 100,
                    paddingRight: 100
                }}
            >
                <HomepageHead />
                <HomepageContent />
            </div>
        );
    }
}
