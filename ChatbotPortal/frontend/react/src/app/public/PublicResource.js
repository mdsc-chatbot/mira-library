import React, { Component } from "react";
import {
    List,
    Header,
    Segment,
    Button,
    Grid,
    Card,
    Container
} from "semantic-ui-react";

export class PublicResource extends Component {
    render() {
        return (
            <div
                style={{
                    paddingTop: 30,
                    paddingLeft: 100,
                    paddingRight: 100
                }}
            >
                <Container
                    style={{ paddingBottom: 50 }}
                    textAlign="center"
                    vertical
                >
                    <Header
                        as="h3"
                        style={{
                            fontSize: "2em"
                        }}
                        color="blue"
                    >
                        Public Resources
                    </Header>
                </Container>
            </div>
        );
    }
}

export default PublicResource;
