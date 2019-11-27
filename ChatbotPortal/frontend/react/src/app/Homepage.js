import React from "react";
import HomepageHead from "./HomepageHead";
import HomepageContent from "./HomepageContent";
import styles from "./HomepageHead.css";
import {Responsive, Segment} from "semantic-ui-react";

export default class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <React.Fragment>
                <Segment.Group className={styles.segmentWeb}>

                    <Responsive minWidth={768}>
                        <HomepageHead/>
                        <HomepageContent/>
                    </Responsive>

                    <Responsive maxWidth={767}>
                        <HomepageHead/>
                    </Responsive>

                </Segment.Group>
            </React.Fragment>

        );
    }
}
