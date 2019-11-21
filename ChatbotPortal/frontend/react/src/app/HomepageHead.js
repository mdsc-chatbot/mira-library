import React, { Component } from "react";
import { Container, Header, Button, Segment, Grid } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import { SecurityContext } from "./contexts/SecurityContext";
import styles from './HomepageHead.css'

export class HomepageHead extends Component {
    static contextType = SecurityContext;

    render() {
        return (
            <div>
                <Segment style={{ paddingBottom: 50, minHeight: 300 }} textAlign="center" vertical>
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
                        content="Resources site providing information about autism, intellectual disability, and learning disability."
                        style={{
                            fontWeight: "normal"
                        }}
                    />

                    <Button.Group>
                        <Button.Group vertical>
                            <Link to={baseRoute + "/public_resource"}>
                                <Button size="big" color="orange">
                                    View all our public resources
                                </Button>
                            </Link>
                            <Link to={baseRoute + "/public_resource/59"}>
                                <Button className={styles.smallButtonStyle} compact floated="right" size="medium" color="google plus">
                                    View resources about funding
                                </Button>
                            </Link>
                            <Link to={baseRoute + "/public_resource/46"}>
                                <Button className={styles.smallButtonStyle} compact floated="right" size="medium" color="google plus">
                                    View resources about stress
                                </Button>
                            </Link>
                            <Link to={baseRoute + "/public_resource/47"}>
                                <Button className={styles.smallButtonStyle} compact floated="right" size="medium" color="google plus">
                                    View resources about sleep
                                </Button>
                            </Link>
                        </Button.Group>

                        {!this.context.security.is_logged_in ? (
                            <Link to={baseRoute + "/login"}>
                                <Button size="big" color="green">
                                    Log in to submit resources
                                </Button>
                            </Link>
                        ) : (
                            <div></div>
                        )}
                    </Button.Group>
                </Segment>
            </div>
        );
    }
}

export default HomepageHead;
