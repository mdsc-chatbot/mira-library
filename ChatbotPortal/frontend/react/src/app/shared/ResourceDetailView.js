import React from "react";
import { Container, Divider, Icon, Label, Rating, Menu, Header, Grid, Responsive } from "semantic-ui-react";
import styles from "./ResourceDetailView.css";
import linkStyles from "../shared/Link.css";

// Originally copied from ResourceDetail
// In the shared directory because potentially multiple components can use this view
// e.g. viewing own resources, public page, review
function grid_element(grid_key, grid_value) {
    const gridRowProps = {
        className: styles.smallRowPadding,
        columns: "2"
    };

    const gridKeyColumnProps = {
        className: styles.greyColumn,
        floated: "left",
        mobile: "8",
        tablet: "4",
        computer: "2"
    };

    const gridValueColumnProps = {
        mobile: "8",
        tablet: "12",
        computer: "14"
    };

    return (
        <Grid.Row {...gridRowProps}>
            <Grid.Column {...gridKeyColumnProps}>{grid_key}</Grid.Column>
            <Grid.Column {...gridValueColumnProps}>{grid_value}</Grid.Column>
        </Grid.Row>
    );
}

function normal_header(resource) {
    return (
        <Menu text>
            <Menu.Item>
                <Header as="h2">
                    <div>
                        <span>
                            <Icon name="globe" />
                            <Header.Content id="title_header">{resource.title}</Header.Content>
                        </span>
                        <a href={resource.url} target="_blank" id="url">
                            <h4 className={linkStyles.link}>{resource.url}</h4>
                        </a>
                    </div>
                </Header>
            </Menu.Item>
            <Menu.Item position="right">
                <Rating icon="star" rating={resource.rating} maxRating={5} disabled size="massive" />
            </Menu.Item>
        </Menu>
    );
}

function mobile_header(resource) {
    // Wrap text
    return (
        <div>
            <Header as="h3">
                <Icon name="globe" size="small" />
                <Header.Content id="title_header">{resource.title}</Header.Content>
                <a href={resource.url} target="_blank" id="url">
                    <h4 className={linkStyles.link}>{resource.url}</h4>
                </a>
                <Rating
                    icon="star"
                    rating={resource.rating}
                    maxRating={5}
                    disabled
                    size="massive"
                    style={{ paddingTop: 10 }}
                />
            </Header>
        </div>
    );
}

export function ResourceDetailView({ resource }) {
    // Common props for grid row, columns that are re-usable.
    // If we need this in more than one place, consider re-making this into several components.

    return (
        <Container>
            <Responsive minWidth={768}>{normal_header(resource)}</Responsive>
            <Responsive {...Responsive.onlyMobile}>{mobile_header(resource)}</Responsive>

            <Divider className={styles.dividerPadding} />

            <Grid>
                {resource.created_by_user ? grid_element("Submitted by:", resource.created_by_user) : null}
                {grid_element("Date submitted:", resource.timestamp)}
                {grid_element("Review status:", <p id="review_status"> {resource.review_status}</p>)}
                {grid_element("Category:", <p id="category"> {resource.category} </p>)}
                {resource.tags && resource.tags.length > 0
                    ? grid_element(
                          "Tags:",
                          <div id="tags">
                              {resource.tags.map(tag => (
                                  <Label key={tag} size="large" stackable>
                                      {tag}
                                  </Label>
                              ))}
                          </div>
                      )
                    : null}

                    {resource.attachment ? (
                        <Grid.Row>
                            <Grid.Column>
                                <Header as="h5" color="grey">
                                    <a
                                        href={`/chatbotportal/resource/download-attachment/${resource.id}`}
                                        // onClick={downloadAttachment}
                                    >
                                        <Icon name="download" />
                                        <Header.Content id="attachment">Download attachment</Header.Content>
                                    </a>
                                </Header>
                            </Grid.Column>
                        </Grid.Row>
                    ) : null}
                </Grid>

            <Divider />

                <Header as="h5" color="grey" className={styles.noMarginHeader}>
                    <Icon name="comment" />
                    <Header.Content>Comment:</Header.Content>
                </Header>
                <p id="comments" style={{ color: "grey" }}>
                    {resource.comments}
                </p>

                <Header as="h5" color="grey" className={styles.noMarginHeader}>
                    <Icon name="book" />
                    <Header.Content>Resource Summary:</Header.Content>
                </Header>
                <p id="website_summary_metadata" style={{ color: "grey" }}>
                    {resource.website_summary_metadata}
                </p>
            </Container>
    );
}
