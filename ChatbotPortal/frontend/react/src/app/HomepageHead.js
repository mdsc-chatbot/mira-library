import React, { Component } from "react";
import { Container, Header, Button, Segment, Grid } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";

export class HomepageHead extends Component {
    render() {
        return (
            <div>
                <Segment
                    style={{ padding: "8em 0em", minHeight: 400 }}
                    textAlign="center"
                    vertical
                >
                    <Header
                        as="h1"
                        content="Welcome to Chatbot Resources"
                        style={{
                            fontSize: "2em",
                            fontWeight: "bold",
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

                    <Link to={baseRoute + "/resource"}>
                        <Button size="big" color="orange">
                            View all our resources
                        </Button>
                    </Link>
                    <Link to={baseRoute + "/login"}>
                        <Button size="big" color="green">
                            Log in to submit resources
                        </Button>
                    </Link>
                </Segment>
            </div>
        );
    }
}

export default HomepageHead;
