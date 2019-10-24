import React, { Component } from "react";
import { Header, List, Card, Segment } from "semantic-ui-react";

export class HomepageContent extends Component {
    render() {
        return (
            <div>
                <Segment>
                    <Header as="h1" dividing style={{ paddingLeft: 100 }}>
                        Popular Resources
                    </Header>
                    <List horizontal style={{ paddingLeft: 100 }}>
                        <List.Item>
                            <Card>
                                <Card.Content>
                                    <Card.Header>Matthew Harris</Card.Header>
                                    <Card.Meta>Co-Worker</Card.Meta>
                                    <Card.Description>
                                        Matthew is a pianist living in
                                        Nashville.
                                    </Card.Description>
                                </Card.Content>
                            </Card>
                        </List.Item>
                        <List.Item>
                            <Card>
                                <Card.Content>
                                    <Card.Header>Matthew Harris</Card.Header>
                                    <Card.Meta>Co-Worker</Card.Meta>
                                    <Card.Description>
                                        Matthew is a pianist living in
                                        Nashville.
                                    </Card.Description>
                                </Card.Content>
                            </Card>
                        </List.Item>
                    </List>
                </Segment>
                <Segment>
                    <Header as="h1" style={{ paddingLeft: 100 }}>
                        Recent Resources
                    </Header>
                </Segment>
                <Segment>
                    <Header as="h1" style={{ paddingLeft: 100 }}>
                        Rated Resources
                    </Header>
                </Segment>
            </div>
        );
    }
}

export default HomepageContent;
