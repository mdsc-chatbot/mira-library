import React, { Component } from "react";
import { Container, Grid } from "semantic-ui-react";

export class Footer extends Component {
    render() {
        return (
            <div>
                <Container style={{ paddingLeft: 50 }}>
                    <Grid>
                        <Grid.Row divided>
                            <Grid.Column>About </Grid.Column>
                            <Grid.Column> Contact </Grid.Column>
                        </Grid.Row>
                        <Grid.Row>© 2019 Powered by Chatbot resources</Grid.Row>
                    </Grid>
                </Container>
            </div>
        );
    }
}

export default Footer;
