import React, { Component } from "react";
import axios from "axios";
import {
    Header,
    Icon,
    Menu,
    Container,
    Divider,
    Label,
    Rating,
    Grid
} from "semantic-ui-react";
import fileDownload from "js-file-download";

import styles from "./ResourceDetail.css";

export default class ResourceDetail extends Component {
    constructor(props) {
        super(props);

        this.state = {
            resource: {}
        };
    }

    componentDidMount() {
        const resourceID = this.props.match.params.resourceID;
        axios
            .get(`http://127.0.0.1:8000/api/resource/retrieve/${resourceID}`)
            .then(res => {
                this.setState({
                    resource: res.data
                });
            });
    }

    downloadAttachment = () => {
        axios
            .get(
                `/chatbotportal/resource/download-attachment/${this.state.resource.id}`
            )
            .then(response => {
                const fileName = response.headers["content-disposition"].split(
                    '"'
                )[1];
                fileDownload(response.data, fileName);
            });
    };

    render() {
        // Common props for grid row, columns that are re-usable.
        // If we need this in more than one place, consider re-making this into several components.
        const gridRowProps = {
            className: styles.smallRowPadding,
            columns: "2"
        };

        const gridKeyColumnProps = {
            className: styles.greyColumn,
            floated: "left",
            textAlign: "right",
            width: "2"
        };

        const gridValueColumnProps = {
            width: "14"
        };

        return (
            <div
                style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100 }}
            >
                <Container>
                    <Menu text>
                        <Menu.Item>
                            <Header as="h2">
                                <div>
                                    <span>
                                        <Icon name="globe" />
                                        <Header.Content id="title_header">
                                            {this.state.resource.title}
                                        </Header.Content>
                                    </span>
                                    <a
                                        href={this.state.resource.url}
                                        target="_blank"
                                    >
                                        <h4 className={styles.link}>
                                            {this.state.resource.url}
                                        </h4>
                                    </a>
                                </div>
                            </Header>
                        </Menu.Item>
                        <Menu.Item position="right">
                            <Rating
                                icon="star"
                                rating={this.state.resource.rating}
                                maxRating={5}
                                disabled
                                size="massive"
                            />
                        </Menu.Item>
                    </Menu>

                    <Divider className={styles.dividerPadding} />

                    <Grid>
                        <Grid.Row {...gridRowProps}>
                            <Grid.Column {...gridKeyColumnProps}>
                                Submitted by:
                            </Grid.Column>
                            <Grid.Column {...gridValueColumnProps}>
                                {this.state.resource.created_by_user}
                            </Grid.Column>
                        </Grid.Row>

                        <Grid.Row {...gridRowProps}>
                            <Grid.Column {...gridKeyColumnProps}>
                                Date submitted:
                            </Grid.Column>
                            <Grid.Column {...gridValueColumnProps}>
                                {this.state.resource.timestamp}
                            </Grid.Column>
                        </Grid.Row>

                        <Grid.Row {...gridRowProps}>
                            <Grid.Column {...gridKeyColumnProps}>
                                Review status:
                            </Grid.Column>
                            <Grid.Column {...gridValueColumnProps}>
                                {this.state.resource.final_review}
                            </Grid.Column>
                        </Grid.Row>

                        {this.state.resource.tags &&
                        this.state.resource.tags.length > 0 ? (
                            <Grid.Row {...gridRowProps}>
                                <Grid.Column {...gridKeyColumnProps}>
                                    Tags:
                                </Grid.Column>
                                <Grid.Column {...gridValueColumnProps}>
                                    {this.state.resource.tags.map(tag => (
                                        <Label key={tag} size="large">
                                            {tag}
                                        </Label>
                                    ))}
                                </Grid.Column>
                            </Grid.Row>
                        ) : null}

                        {this.state.resource.attachment ? (
                            <Grid.Row>
                                <Grid.Column>
                                    <Header as="h5" color="grey">
                                        <a
                                            href="#"
                                            onClick={this.downloadAttachment}
                                        >
                                            <Icon name="download" />
                                            <Header.Content>
                                                Download attachment
                                            </Header.Content>
                                        </a>
                                    </Header>
                                </Grid.Column>
                            </Grid.Row>
                        ) : null}
                    </Grid>

                    <Divider />

                    <Header
                        as="h5"
                        color="grey"
                        className={styles.noMarginHeader}
                    >
                        <Icon name="comment" />
                        <Header.Content>Comment:</Header.Content>
                    </Header>
                    <p id="comments" style={{ color: "grey", marginTop: -10 }}>
                        {this.state.resource.comments}
                    </p>
                </Container>
            </div>
        );
    }
}
