import React, { Component } from "react";
import { Container, Grid, Segment } from "semantic-ui-react";

export class Footer extends Component {
    render() {
        return (
            <div style={{position:"absolute",bottom:0,left:0,right:0}}>
                <Segment vertical inverted>
                    <Grid container stackable verticalAlign="middle">
                        <Grid.Row divided>
                            <Grid.Column>About </Grid.Column>
                            <Grid.Column> Contact </Grid.Column>
                        </Grid.Row>
                        <Grid.Row>© 2019 Powered by Chatbot resources</Grid.Row>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

export default Footer;
