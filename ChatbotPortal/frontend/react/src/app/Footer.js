import React, { Component } from "react";
import { Icon, Grid, Segment } from "semantic-ui-react";
import styles from "./profile/ProfilePage.css";

export class Footer extends Component {
    render() {
        return (
                <Grid container className={styles.segmentWeb} stackable verticalAlign='middle'>
                    <Grid.Row>
                        <Grid.Column>About</Grid.Column>
                        <Grid.Column>Contact</Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column>
                            <Icon name='copyright outline' />Powered by Chatbot Resources
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
        );
    }
}

export default Footer;
