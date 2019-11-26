import React, { Component } from "react";
import { Container, Header, Accordion, Divider } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import styles from "./shared/Link.css";
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
            "What are resources again and How do I view them?": (
                <p>
                    Resources are information gathered regarding autism, intellectual disability and
                    learning disability. They are mainly website urls.
                    <br />
                    <br />
                    The resources approved by us are shown under{" "}
                    <Link to={baseRoute + "/public_resource"} className={styles.link}>
                        Public Resources
                    </Link>{" "}
                    . We encourage everyone to submit resources (website urls) they found useful
                    relating to autism, intellectual disability and learning disability.
                    <br />
                    The resources submitted by you are shown under{" "}
                    {conditionally_render("/resource", "My Resources")}
                </p>
            ),

            "What happens after I submit a resource?": (
                <p>
                    After you submit a resource, it will show up on{" "}
                    {conditionally_render("/resource", "My Resources")}. This is the page where all
                    your submitted resources are shown. You can track whether your submitted
                    resource is approved or rejected by clicking on a specific one.
                    <br /> <br />
                    The submitted resource will need to be reviewed/ approved by us or reviewers
                    before it is shown on{" "}
                    <Link to={baseRoute + "/public_resource"} className={styles.link}>
                        Public Resources
                    </Link>
                    .
                </p>
            ),

            "What is a Reviewer status and how do I obtain it?": (
                <p>
                    A reviewer status is given to users of our website by us. A reviewer can approve
                    or reject a submitted resource, they are also required to give a review comment.
                    <br /> Reviewer can see pending resources they need to review under{" "}
                    {conditionally_render("/review", "My Reviews")}
                </p>
            ),

            "What are points and How do I gain points?": (
                <p>
                    Points are used for various benefits. As a user you can gain points by having
                    your submitted resource approved. Each approved resource is worth 1 points.
                </p>
            ),

            "What are the rating on each resource and How is each submitted resource being rated?": (
                <p>
                    The rating on each resource shows how useful it is. Your submitted resource is
                    rated first by you, then manually adjusted by us or reviewers. Each resource is
                    rated from 0-5 stars.
                </p>
            )
        };

        for (const [key, value] of Object.entries(faq_title_content)) {
            panels.push({
                title: { content: key, icon: "question" },
                content: { content: value }
            });
        }

        return (
            <div
                style={{
                    paddingTop: 30,
                    paddingLeft: 100,
                    paddingRight: 100,
                    paddingBottom: 30
                }}
            >
                <Header
                    as="h3"
                    style={{
                        fontSize: "2em"
                    }}
                    color="blue"
                >
                    Frequently Asked Question (FAQ)
                </Header>
                <Divider />
                <div style={{ paddingBottom: 20 }}>
                    <Header as="h3" color="blue">
                        What is ChatbotResources and How do I use this site?
                    </Header>
                    <p>
                        ChatbotResources is a website dedicated to providing and gathering
                        information regarding autism, intellectual disability and learning
                        disability. These information are gathered from variety of sources such as
                        health professionals, educators and approved resource submission.
                        <br />
                        You can use this site either as a visitor or a logged in user.
                        <br />
                        <br /> As a visitor, you can view our{" "}
                        <Link to={baseRoute + "/public_resource"} className={styles.link}>
                            Public Resources
                        </Link>{" "}
                        for our approved resources and information.
                        <br />
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
                        How do I submit resources? What informations are required to submit a
                        resource?
                    </Header>
                    <p>
                        You must first{" "}
                        <Link to={baseRoute + "/login"} className={styles.link}>
                            SignUp{" "}
                        </Link>{" "}
                        and{" "}
                        <Link to={baseRoute + "/login"} className={styles.link}>
                            Login{" "}
                        </Link>
                        in order to submit a resource.
                        <br />
                        To submit a resource, you are required to input a website
                        url and rate how useful it was to you.
                        <br />
                        <br />
                        Optionally, you can search and select for tag to categorize
                        your resource (eg. autism, ADHD, age). 
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
                        How do I Signup to submit a resource?
                    </Header>
                    <p className={styles.inline}>
                        We require your name, email address and password for a successful signup.
                        <br />
                        Optionally, we would like to know your affiliation (your role, occupation in
                        relation to autism, intellectual disability and learning disability field).
                        This information helps us better tailor our website.
                        <br />
                        After you fill out the sign up form, we will send you and email for
                        verification. It is important that you read and consent to our{" "}  
                    </p>
                </div>
                <div style={{ paddingBottom: 20 }}>
                    <TermsOfService/>
                </div>

                <div style={{ paddingBottom: 20 }}>
                    <Header as="h3" color="blue">
                        Do I need to Signup and Login to submit a resource?
                    </Header>
                    <p>
                        Unfortunately, yes you will have to{" "}
                        <Link to={baseRoute + "/login"} className={styles.link}>
                            Login{" "}
                        </Link>
                        in order to submit a resource. This is to assure the quality
                        of resources submitted. 
                        <br />
                        As a logged in user, you will be able to track and see details of all
                        your submitted resources. You can also gain points from each
                        approved resource. 
                    </p>
                </div>

                <div>
                    <Header as="h3" color="blue">
                        Still confused? Check out our other FAQs:
                    </Header>
                    <Accordion defaultActiveIndex={[0, 1]} panels={panels} styled fluid />
                </div>
            </div>
        );
    }
}

export default FAQ;
