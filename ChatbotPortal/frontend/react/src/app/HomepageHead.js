import React, { Component } from "react";
import {Container, Header, Button, Segment, Grid, Responsive, Divider,Icon} from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import { SecurityContext } from "./security/SecurityContext";
import styles from './HomepageHead.css'



export class HomepageHead extends Component {
    static contextType = SecurityContext;

    homePageData = () => {
        return(
            <Segment>

                <Header
                    as="h1"
                    content="Welcome to Chatbot Resources"
                    style={{
                        fontSize: "2em",
                        fontWeight: "bold",
                        color: "#3075c9",
                        marginTop: "1em"
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

                    {!this.context.security.is_logged_in && (
                        <Link to={baseRoute + "/login"}>
                            <Button size="big" color="green">
                                Log in to submit resources
                            </Button>
                        </Link>

                    )}
                </Button.Group>

            </Segment>


        );
    };
    homePageWeb = () => {
        return(
            <Segment className={styles.segmentWeb} textAlign="center" vertical>
                {this.homePageData()}
            </Segment>

        );
    };
    homePageMobile = () => {
        return(
            <React.Fragment>
                <Grid centered stackable columns={2} className={styles.segmentWeb}>
                    <Grid.Column>
                        <Header
                            as="h1"
                            content="Welcome to Chatbot Resources"
                            style={{
                                fontWeight: "bold",
                                color: "#3075c9",
                                marginTop: "0.5em"
                            }}
                        /></Grid.Column>
                    <Grid.Column>
                        <Header
                            as="h3"
                            content="Resources site providing information about autism, intellectual disability, and learning disability."
                            style={{
                                fontWeight: "normal"
                            }}
                        />
                    </Grid.Column>
                </Grid>

                <Divider/>

                <Button.Group fluid widths='2' size ='medium'>
                    <Link to={baseRoute + "/public_resource"}>
                        <Button fluid color="orange">
                            View all our public resources
                        </Button>
                    </Link>

                    {!this.context.security.is_logged_in &&(<Link to={baseRoute + "/login"}>
                        <Button fluid color="green">
                            Log in to submit resources
                        </Button>
                    </Link>)}
                </Button.Group>

                <Button.Group widths='3' size='tiny'>
                    <Link to={baseRoute + "/public_resource/59"}>
                        <Button  color="google plus">
                            View resources about funding
                        </Button>
                    </Link>
                    <Link to={baseRoute + "/public_resource/46"}>
                        <Button color="google plus">
                            View resources about stress
                        </Button>
                    </Link>
                    <Link to={baseRoute + "/public_resource/47"}>
                        <Button color="google plus">
                            View resources about sleep
                        </Button>
                    </Link>
                </Button.Group>
            </React.Fragment>
        );
    };

    render() {
        return (
            <Segment.Group className={styles.segmentWeb}>

                <Responsive minWidth={768}>
                    {this.homePageWeb()}
                </Responsive>

                <Responsive maxWidth={767}>
                    {this.homePageMobile()}
                </Responsive>

            </Segment.Group>
        );
    }
}

export default HomepageHead;
