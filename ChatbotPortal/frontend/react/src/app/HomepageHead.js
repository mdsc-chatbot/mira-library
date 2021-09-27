/**
 * @file: HomepageHead.js
 * @summary: Top of Homepage showing website description, buttons for viewing all resources or log in
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
import React, { Component } from "react";
import {Header, Button, Segment, Grid, Responsive, Icon} from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import { SecurityContext } from "./contexts/SecurityContext";
import styles from './HomepageHead.css'

export class HomepageHead extends Component {
    static contextType = SecurityContext;

    // The constant homepage data
    homePageData = () => {
        return(
            <React.Fragment>
                <Header
                    as="h1"
                    content="Welcome to the MIRA Resource Portal"
                    style={{
                        fontSize: "2em",
                        fontWeight: "bold",
                        color: "#0072BB",
                        marginTop: "1em"
                    }}
                />
                <Header
                    as="h3"
                    content="An information repository for mental health resources."
                    style={{
                        fontWeight: "normal",
                        marginBottom: "1em"
                    }}
                />

                <Segment className={styles.segmentWeb} textAlign="center" vertical>
                    {this.context.security.is_logged_in ? (
                        <Button.Group className={styles.buttonAlign} fluid widths='2' size ='large'>
                            <Link to={baseRoute + "/public_resource"}>
                                <Button fluid className={styles.publicResource} color="yellow">
                                    View all our public resources
                                </Button>
                            </Link>
                            <Link to={baseRoute + "/resource_submit"}>
                                <Button className={styles.loginButton} color='yellow'>
                                    Submit a resource
                                </Button>
                            </Link>
                        </Button.Group>
                    ) : (
                        <Button.Group className={styles.buttonAlign} fluid widths='2' size ='large'>
                            <Link to={baseRoute + "/public_resource"}>
                                <Button className={styles.publicResource} fluid color="yellow">
                                    View all our public resources
                                </Button>
                            </Link>
                            <Link to={baseRoute + "/login"}>
                                <Button className={styles.loginButton} fluid color="yellow">
                                    Log in to submit resources
                                </Button>
                            </Link>
                        </Button.Group>
                    )
                    }
                </Segment>
            </React.Fragment>
        );
    };

    // Home page layout and Data for Web & Tab Orientation
    homePageWeb = () => {
        return(
            <Segment className={styles.segmentWeb} textAlign="center" vertical>
                {this.homePageData()}
            </Segment>

        );
    };

    // Home page Layout and Data for Mobile Orientation
    homePageMobile = () => {
        return(
            <React.Fragment>
                <Grid centered stackable columns={2} className={styles.segmentWeb}>
                    <Grid.Column>
                        <Header
                            as="h1"
                            content="Welcome to the MIRA Resource Portal"
                            style={{
                                fontWeight: "bold",
                                color: "#3075c9",
                                marginTop: "0.5em"
                            }}
                        /></Grid.Column>
                    <Grid.Column>
                        <Header
                            as="h3"
                            content="An information repository for mental health resources."
                            className={styles.header3}
                        />
                    </Grid.Column>
                </Grid>


                {this.context.security.is_logged_in ? (
                    <Button.Group className={styles.buttonAlign} fluid widths='2' size ='medium'>
                        <Link to={baseRoute + "/public_resource"}>
                            <Button fluid className={styles.publicResource} color='yellow'>
                                View all our public resources
                            </Button>
                        </Link>
                        <Link to={baseRoute + "/resource_submit"}>
                            <Button className={styles.loginButton} color='yellow'>
                                Submit a resource
                            </Button>
                        </Link>
                    </Button.Group>
                ) : (
                    <Button.Group className={styles.buttonAlign} fluid widths='2' size ='small'>
                        <Link to={baseRoute + "/public_resource"}>
                            <Button className={styles.publicResource} color='yellow'>
                                View all our public resources
                            </Button>
                        </Link>
                        <Link to={baseRoute + "/login"}>
                            <Button className={styles.loginButton} color='yellow'>
                                Log in to submit resources
                            </Button>
                        </Link>
                    </Button.Group>
                )
                }
            </React.Fragment>
        );
    };


    /**
     * This renders the HomepPage
     * @returns {React.Fragment}
     */
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
