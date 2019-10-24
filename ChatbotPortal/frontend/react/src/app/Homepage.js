import React from "react";
import { Segment } from "semantic-ui-react";
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
                <Segment textAlign="center" style={{ minHeight: 400 }}>
                    <HomepageHead />
                </Segment>
                <HomepageContent />
                <Footer />
            </div>
        );
    }
}
