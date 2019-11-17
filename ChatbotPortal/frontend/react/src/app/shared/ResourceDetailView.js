import React from 'react';
import {Container, Divider, Icon, Label, Rating, Menu, Header, Grid} from 'semantic-ui-react';
import styles from './ResourceDetailView.css';
import linkStyles from "../shared/Link.css";

// Originally copied from ResourceDetail
// In the shared directory because potentially multiple components can use this view
// e.g. viewing own resources, public page, review
export function ResourceDetailView({resource}) {

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
                                            {resource.title}
                                        </Header.Content>
                                    </span>
                                <a
                                    href={resource.url}
                                    target="_blank"
                                >
                                    <h4 className={linkStyles.link}>
                                        {resource.url}
                                    </h4>
                                </a>
                            </div>
                        </Header>
                    </Menu.Item>
                    <Menu.Item position="right">
                        <Rating
                            icon="star"
                            rating={resource.rating}
                            maxRating={5}
                            disabled
                            size="massive"
                        />
                    </Menu.Item>
                </Menu>

                <Divider className={styles.dividerPadding} />

                <Grid>
                    {resource.created_by_user ? (
                        <Grid.Row {...gridRowProps}>
                            <Grid.Column {...gridKeyColumnProps}>
                                Submitted by:
                            </Grid.Column>
                            <Grid.Column {...gridValueColumnProps}>
                                {resource.created_by_user}
                            </Grid.Column>
                        </Grid.Row>
                    ) : null}

                    <Grid.Row {...gridRowProps}>
                        <Grid.Column {...gridKeyColumnProps}>
                            Date submitted:
                        </Grid.Column>
                        <Grid.Column {...gridValueColumnProps}>
                            {resource.timestamp}
                        </Grid.Column>
                    </Grid.Row>

                    <Grid.Row {...gridRowProps}>
                        <Grid.Column {...gridKeyColumnProps}>
                            Review status:
                        </Grid.Column>
                        <Grid.Column {...gridValueColumnProps}>
                            {resource.review_status}
                        </Grid.Column>
                    </Grid.Row>

                    {resource.tags &&
                    resource.tags.length > 0 ? (
                        <Grid.Row {...gridRowProps}>
                            <Grid.Column {...gridKeyColumnProps}>
                                Tags:
                            </Grid.Column>
                            <Grid.Column {...gridValueColumnProps}>
                                {resource.tags.map(tag => (
                                    <Label key={tag} size="large">
                                        {tag}
                                    </Label>
                                ))}
                            </Grid.Column>
                        </Grid.Row>
                    ) : null}

                    {resource.attachment ? (
                        <Grid.Row>
                            <Grid.Column>
                                <Header as="h5" color="grey">
                                    <a
                                        href={`/chatbotportal/resource/download-attachment/${resource.id}`}
                                        // onClick={downloadAttachment}
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
                <p id="comments" style={{ color: "grey" }}>
                    {resource.comments}
                </p>
            </Container>
        </div>
    );
}