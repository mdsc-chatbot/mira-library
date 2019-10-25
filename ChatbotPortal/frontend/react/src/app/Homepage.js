import React from "react";
import { Divider } from "semantic-ui-react";
import HomepageHead from "./HomepageHead";
import Footer from "./Footer";
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
                <Divider />
                <Footer />
            </div>
        );
    }
}
