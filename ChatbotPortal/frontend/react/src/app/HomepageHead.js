import React, { Component } from "react";
import { Container, Header, Button } from "semantic-ui-react";

export class HomepageHead extends Component {
    render() {
        return (
            <div>
                <Container text>
                    <Header
                        as="h1"
                        content="Welcome to Chatbot Resources"
                        style={{
                            fontSize: "2em",
                            fontWeight: "normal",
                            color: "#3075c9",
                            marginTop: "2em"
                        }}
                    />
                    <Header
                        as="h3"
                        content="Resources site provding information about autism, intellectual disability, and learning disability."
                        style={{
                            fontWeight: "normal"
                        }}
                    />
                    <Button size="big" color="orange">
                        View all our resources
                    </Button>
                    <Button size="big" color="green">
                        Log in to submit resources
                    </Button>
                </Container>
            </div>
        );
    }
}

export default HomepageHead;
