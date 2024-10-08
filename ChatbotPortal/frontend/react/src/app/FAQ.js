/**
 * @file: FAQ.js
 * @summary: Component for frequently asked question page
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
import { Container, Header, Accordion, Divider, Responsive } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import * as styles from "./shared/Link.css";
import { SecurityContext } from "./contexts/SecurityContext";
import TermsOfService from "./authentication/TermsOfService";

export class FAQ extends Component {
    static contextType = SecurityContext;

    render() {
        const conditionally_render = (link_name, link_place_holder) => {
            let link = null;
            if (this.context.security.is_logged_in) {
                link = (
                    <Link to={baseRoute + link_name} className={styles.link}>
                        {link_place_holder}{" "}
                    </Link>
                );
            } else {
                link = (
                    <Link to={baseRoute + "/login"} className={styles.link}>
                        {link_place_holder}{" "}
                    </Link>
                );
            }
            return link;
        };

        const panels = [];
        const faq_title_content = {
            
            "What are resources and how do I view them?": (
                <p>
                    Resources are any useful information gathered regarding mental health. They are mainly website urls.
                    <br />
                    <br />
                    The resources approved by us are shown under{" "}
                    <Link to={baseRoute + "/public_resource"} className={styles.link}>
                        Public Resources
                    </Link>{" "}
                    . We encourage everyone to submit resources they've found useful
                    relating to mental health/wellbeing.
                    <br />
                    The resources submitted by you are shown under{" "}
                    {conditionally_render("/resource", "My Resources")}
                </p>
            ),

            "How are the resources used?": (
                <p>
                    High quality resources will be made accessible from the {" "}
                    <Link to={baseRoute + "/public_resource"} className={styles.link}>
                        public resource repository
                    </Link>{" "}
                    , and contextually made available to the MIRA chatbot.
                </p>),

            "What happens after I submit a resource?": (
                <p>
                    After you submit a resource, it will show up on{" "}
                    {conditionally_render("/resource", "My Resources")}. This is the page where all
                    your submitted resources are shown.
                    <br /> <br />
                    The submitted resource will need to be reviewed/ approved by reviewers
                    before it is shown on{" "}
                    <Link to={baseRoute + "/public_resource"} className={styles.link}>
                        Public Resources
                    </Link>
                    .
                </p>
            ),

            "What is the review process?": (
                <p>
                    Reviewers will check the quality of submitted resources according to a carefully
                    chosen set of metrics. After two seperate reviewers approve a resource, they will
                    eventually be available under {" "}
                    <Link to={baseRoute + "/public_resource"} className={styles.link}>
                        Public Resources
                    </Link>.
                    <br /> Reviewers can see pending resources they need to review under{" "}
                    {conditionally_render("/review", "My Reviews")}
                </p>
            ),



            "What are the rating on each resource and how is each submitted resource being rated?": (
                <p>
                    The rating on each resource shows how useful it is. Your submitted resource is
                    rated first by you, then manually adjusted by reviewers. Each resource is
                    rated from 0-5 stars.
                </p>
            )
        };

        for (const [key, value] of Object.entries(faq_title_content)) {
            panels.push({
                title: { content: key, icon: "dropdown" },
                content: { content: value }
            });
        }

        const faq = () =>{
            return (
                <div>
                    <Header
                        as="h3"
                        style={{
                            fontSize: "2em"
                        }}
                        color="blue"
                    >
                        Frequently Asked Questions (FAQs)
                    </Header>
                    <Divider />
                    <div style={{ paddingBottom: 20 }}>
                        <Header as="h3" color="blue">
                            What is the MIRA Resource Library and how do I use this site?
                        </Header>
                        <p>
                            The MIRA Resource Library is a website dedicated to providing and gathering
                            information regarding mental health. This information is gathered and reviewed by a 
                            variety of sources such as health professionals, experts, and educators.
                            <br />
                            You can use this site either as a visitor or a logged in user.
                            <br />
                            <br /> As a visitor, you can view our{" "}
                            <Link to={baseRoute + "/public_resource"} className={styles.link}>
                                Public Resources
                            </Link>{" "}
                            for our approved resources and information.
                            <br /><br/>
                            As a logged in user, you can view{" "}
                            {conditionally_render("/profile", "My Profile")}
                            which shows your profile, number of resource submission, points and status.
                            You can also view {conditionally_render("/resource", "My Resources")}, which
                            shows your submitted resources and their details. If you are approved by us,
                            you can also see {conditionally_render("/review", "My Reviews")}, which
                            shows the pending resources waiting for you to review.
                        </p>
                    </div>

                    <div style={{ paddingBottom: 20 }}>
                        <Header as="h3" color="blue">
                            How do I submit resources? What information is required to submit a
                            resource?
                        </Header>
                        <p>
                            You must first{" "}
                            <Link to={baseRoute + "/login"} className={styles.link}>
                                Sign Up{" "}
                            </Link>{" "}
                            and{" "}
                            <Link to={baseRoute + "/login"} className={styles.link}>
                                Login{" "}
                            </Link>
                            in order to submit a resource.
                            <br />
                            To submit a resource, you are required to input a url, definition, etc
                            and provide any additional information you feel is relevent using tags. 
                            Finally, you can rate how useful you feel the resource is.
                            <br />
                            <br />
                            If you cannot find a tag that
                            accurately categorize your resource, you can submit
                            a new tag for us to review. We will try to add it to our
                            database so that you can search and select it later.
                            <br />
                            <br />
                            Optionally, you can also upload a file attachment related to the resource.
                        </p>
                    </div>

                    <div>
                        <Header as="h3" color="blue">
                            How do I sign up to submit a resource?
                        </Header>
                        <p className={styles.inline}>
                            We require your name, email address and password for a successful signup.
                            <br />
                            Optionally, we would like to know your affiliation (your role or occupation in
                            the mental health field). This information helps us better maintain the portal.
                            <br />
                            After you fill out the sign up form, we will send you and email for
                            verification. It is important that you read and consent to our{" "}  
                        </p>
                    </div>
                    <div style={{ paddingBottom: 20, paddingTop: 5 }}>
                        <TermsOfService/>
                    </div>

                    <div style={{ paddingBottom: 20 }}>
                        <Header as="h3" color="blue">
                            Do I need to sign up and login to submit a resource?
                        </Header>
                        <p>
                            Yes, you will need to{" "}
                            <Link to={baseRoute + "/login"} className={styles.link}>
                                Login{" "}
                            </Link>
                            in order to submit a resource. This is to assure the quality
                            of resources submitted. 
                            <br />
                            As a logged in user, you will be able to track and see details of all
                            your submitted resources.
                        </p>
                    </div>

                    <div>
                        <Header as="h3" color="blue">
                            Still confused? Check out our other FAQs:
                        </Header>
                        <Accordion defaultActiveIndex={[0, 1]} panels={panels} styled fluid />
                    </div>
            </div>
            )
        }

        return (
            <div>
                <Responsive {...Responsive.onlyMobile}>
                    <div style={{ paddingTop: 30, paddingLeft: 15, paddingRight: 15, paddingBottom: 30 }}>
                        {faq()}
                    </div>
                </Responsive>
                <Responsive minWidth={768}>
                    <div style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30 }}>
                        {faq()}
                    </div>
                </Responsive>
            </div>
        );
    }
}

export default FAQ;


