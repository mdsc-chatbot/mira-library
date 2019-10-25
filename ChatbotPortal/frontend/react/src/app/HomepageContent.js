import React, { Component } from "react";
import {
    Header,
    List,
    Card,
    Segment,
    Container,
    Grid
} from "semantic-ui-react";

export class HomepageContent extends Component {
    render() {
        return (
            <div>
                <Segment style={{ padding: "8em 0em" }} vertical>
                    <Grid container stackable verticalAlign="middle">
                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{
                                    fontSize: "2em",
                                    color: "#3075c9"
                                }}
                            >
                                Popular Resources
                            </Header>
                            <Card.Group itemsPerRow={5}>
                                <Card>
                                    <Card.Content>
                                        <Card.Header>
                                            Matthew Harris
                                        </Card.Header>
                                        <Card.Meta>Co-Worker</Card.Meta>
                                        <Card.Description>
                                            Matthew is a pianist living in
                                            Nashville.
                                        </Card.Description>
                                    </Card.Content>
                                </Card>

                                <Card>
                                    <Card.Content>
                                        <Card.Header content="Jake Smith" />
                                        <Card.Meta content="Musicians" />
                                        <Card.Description content="Jake is a drummer living in New York." />
                                    </Card.Content>
                                </Card>

                                <Card>
                                    <Card.Content
                                        header="Elliot Baker"
                                        meta="Friend"
                                        description="Elliot is a music producer living in Chicago."
                                    />
                                </Card>

                                <Card
                                    header="Jenny Hess"
                                    meta="Friend"
                                    description="Jenny is a student studying Media Management at the New School"
                                />
                            </Card.Group>
                            <Header
                                as="h3"
                                style={{ fontSize: "2em", color: "#3075c9" }}
                            >
                                Recent Resources
                            </Header>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

export default HomepageContent;
