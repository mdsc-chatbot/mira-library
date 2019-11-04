import React, { Component } from "react";
import { Container, Grid, Segment } from "semantic-ui-react";

export class Footer extends Component {
    render() {
        return (
            <div>
                <Segment vertical inverted>
                    <Grid container stackable verticalAlign="middle">
                        <Grid.Row divided>
                            <Grid.Column>About </Grid.Column>
                            <Grid.Column> Contact </Grid.Column>
                        </Grid.Row>
                        <Grid.Row>© 2019 Powered by Chatbot Resources</Grid.Row>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

export default Footer;
