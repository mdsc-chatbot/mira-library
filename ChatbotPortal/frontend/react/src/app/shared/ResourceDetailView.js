import React from "react";
import { Container, Divider, Icon, Label, Rating, Menu, Header, Grid, Responsive } from "semantic-ui-react";
import styles from "./ResourceDetailView.css";
import linkStyles from "../shared/Link.css";

// Originally copied from ResourceDetail
// In the shared directory because potentially multiple components can use this view
// e.g. viewing own resources, public page, review
function normal_grid_element(grid_key, grid_value) {
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

export function ResourceDetailView({ resource }) {
    // Common props for grid row, columns that are re-usable.
    // If we need this in more than one place, consider re-making this into several components.

    return (
        <Container>
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
                        <Responsive {...Responsive.onlyMobile}>
                            <Rating
                                icon="star"
                                rating={resource.rating}
                                maxRating={5}
                                disabled
                                size="massive"
                                style={{ paddingTop: 10 }}
                            />
                        </Responsive>
                    </Header>
                </Menu.Item>
                <Menu.Item position="right">
                    <Responsive minWidth={768}>
                        <Rating icon="star" rating={resource.rating} maxRating={5} disabled size="massive" />
                    </Responsive>
                </Menu.Item>
            </Menu>

            <Divider className={styles.dividerPadding} />

            <Grid>
                {resource.created_by_user ? normal_grid_element("Submitted by:", resource.created_by_user) : null}
                {normal_grid_element("Date submitted:", resource.timestamp)}
                {normal_grid_element("Review status:", <p id="review_status"> {resource.review_status}</p>)}
                {normal_grid_element("Category:", <p id="category"> {resource.category} </p>)}
                {resource.tags && resource.tags.length > 0
                    ? normal_grid_element(
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
                                    <Header.Content>Download attachment</Header.Content>
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
        </Container>
    );
}
