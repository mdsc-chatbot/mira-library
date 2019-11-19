import React, { Component } from "react";
import { Icon, Grid, Segment } from "semantic-ui-react";

export class Footer extends Component {
    render() {
        return (
            <div>
                <Segment inverted attached='bottom'>
                    <Grid container stackable verticalAlign='middle'>
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
                </Segment>
            </div>
        );
    }
}

export default Footer;
