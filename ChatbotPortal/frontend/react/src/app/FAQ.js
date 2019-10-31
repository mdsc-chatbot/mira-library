import React, { Component } from "react";
import { Container, Header, Accordion } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import styles from "./resource/Resource.css";

export class FAQ extends Component {
    render() {
        const panels = [];
        const faq_title_content = {
            "What is ChatbotResources?": (
                <p>
                    ChatbotResources is a website dedicated to providing and
                    gathering information regarding autism, intellectual
                    disability and learning disability. These information are
                    gathered from variety of sources such as health
                    professionals, educators and approved resource submission.
                </p>
            ),

            "What are resources?": (
                <p>
                    Resources are information gathered regarding autism,
                    intellectual disability and learning disability. They are
                    mainly website urls.
                </p>
            ),

            "How do I see these resources?": (
                <p>
                    The resources approved by us are shown under{" "}
                    <Link
                        to={baseRoute + "/public_resource"}
                        className={styles.link}
                    >
                        Public Resources
                    </Link>{" "}
                    . We encourage everyone to submit resources (website urls)
                    they found useful relating to autism, intellectual
                    disability and learning disability.
                </p>
            ),

            "How do I submit resources?": (
                <p>
                    You must first{" "}
                    <Link to={baseRoute + "/login"} className={styles.link}>
                        SignUp{" "}
                    </Link>{" "}
                    and{" "}
                    <Link to={baseRoute + "/login"} className={styles.link}>
                        Login{" "}
                    </Link>
                    in order to submit a resource. We require your name, email
                    address and password for a successful signup. <br />
                    <br />
                    Optionally, we would like to know your affiliation (your
                    role, occupation in relation to autism, intellectual
                    disability and learning disability field). This information
                    helps us better tailor our website. <br />
                    <br />
                    To complete the signup process, you will have to verify an
                    email link we send you.
                </p>
            ),

            "Do I need to Signup and Login to submit a resource?": (
                <p>
                    Unfortunately, yes you will have to{" "}
                    <Link to={baseRoute + "/login"} className={styles.link}>
                        Login{" "}
                    </Link>
                    in order to submit a resource. This is to assure the quality
                    of resources submitted. <br />
                    <br />
                    As a user, you will be able to track and see details of all
                    your submitted resources. You can also gain points from each
                    approved resource. These points are used for various
                    benefits such as an upgrade to reviewer status, where you
                    can approve other’s submitted resources.
                </p>
            ),

            "What information do I need to submit a resource?": (
                <p>
                    To submit a resource, you are required to input a website
                    url and rate how useful it was to you. <br />
                    <br />
                    Optionally, you can search and select for tag to categorize
                    your resource (eg. autism, ADHD, age). If you cannot find a
                    tag that accurately categorize your resource, you can submit
                    a new tag for us to review. We will try to add it to our
                    database so that you can search and select it later. <br />
                    <br />
                    Optionally, you can also upload a file attachment related to
                    the resource.
                </p>
            ),

            "What happens after I submit a resource?": (
                <p>
                    After you submit a resource, it will show up on your{" "}
                    <Link to={baseRoute + "/resource"} className={styles.link}>
                        My resources{" "}
                    </Link>
                    page. This is the page where all your submitted resources
                    are shown. You can track whether your submitted resource is
                    approved or rejected by clicking on a specific one.
                    <br />
                    <br /> The submitted resource will need to be reviewed and
                    approved by us or reviewers before it is shown on{" "}
                    <Link
                        to={baseRoute + "/public_resource"}
                        className={styles.link}
                    >
                        Public Resources
                    </Link>
                    . It will need 2 approvals to be approved and 2 rejections
                    to be rejected. We will provide a review comment after an
                    approval or rejection.
                </p>
            ),

            "What is a Reviewer status and how do I obtain it?": (
                <p>
                    A reviewer status is given to users of our website who
                    gained 5000 points (or submitted approximately 1000
                    resources). A reviewer can approve or reject a submitted
                    resource, they are also required to give a review comment as
                    <br />
                    <br /> Reviewer can see pending resources they need to
                    review under{" "}
                    <Link to={baseRoute + "/review"} className={styles.link}>
                        My reviews{" "}
                    </Link>
                </p>
            ),

            "How do I gain points?": (
                <p>
                    As a user you can gain points by having your submitted
                    resource approved. Each approved resource is worth 5 points.
                    <br />
                    <br />
                    You can also gain 5 extra points if your approved resource
                    is rated higher than 2 stars and 10 extra points if your
                    approved resource is rated 5 stars.
                </p>
            ),

            "What does it mean for my submitted resource to be approved or rejected?": (
                <p>
                    Your submitted resource is approved if it receives 2
                    approvations from us or reviewers. It is rejected if it
                    received 2 rejections from us or reviewers.
                </p>
            ),

            "How is each submitted resource being rated?": (
                <p>
                    Your submitted resource is rated manually by us or
                    reviewers. It is rated from 0-5 stars.
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
                    paddingRight: 100
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
                <Accordion
                    defaultActiveIndex={[0, 1]}
                    panels={panels}
                    styled
                    fluid
                    exclusive={false}
                />
            </div>
        );
    }
}

export default FAQ;
