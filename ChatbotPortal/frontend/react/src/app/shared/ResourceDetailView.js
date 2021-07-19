import React from "react";
import { Container, Divider, Icon, Label, Rating, Menu, Header, Grid, Responsive } from "semantic-ui-react";
import styles from "./ResourceDetailView.css";
import linkStyles from "../shared/Link.css";

// Originally copied from ResourceDetail
/**
 * @file: ResourceDetailView.js
 * @summary: A detail view of a resource
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
        computer: "3"
    };

    const gridValueColumnProps = {
        mobile: "8",
        tablet: "12",
        computer: "13"
    };

    return (
        <Grid.Row {...gridRowProps}>
            <Grid.Column {...gridKeyColumnProps}>{grid_key}</Grid.Column>
            <Grid.Column {...gridValueColumnProps}>{grid_value}</Grid.Column>
        </Grid.Row>
    );
}
function reviews(reviewComments){
    return (
        <Container>
            <Header as="h5" color="grey" className={styles.noMarginHeader}>
                <Header.Content>Reviewer Comments</Header.Content>
            </Header>
            <p id= "review_comment" style={{ color: "grey" }}>
                {reviewComments}
            </p>
        </Container>
    )
}

function normal_header(resource) {
    var data = [];
    if(resource.general_url!= null)data.push({name:"General URL: ", value:resource.general_url});
    if(resource.phone_numbers!= null)data.push({name:"Phone Number: ", value:resource.phone_numbers});
    if(resource.text_numbers!= null)data.push({name:"Text Numbers: ", value:resource.text_numbers});
    if(resource.email!= null)data.push({name:"Email: ",value:resource.email});
    if(resource.physical_address!= null)data.push({name:"Address: ",value:resource.physical_address});
    data.push({name:"Distress Level: ",value:resource.distress_level_min+"-"+resource.distress_level_max});
    data.push({name:"Resource Type: ",value:resource.resource_type});

    var numPresent = 0;
    var menuEntries = [];
    for (var i = 1; i < data.length; i+=2) 
    {
        menuEntries.push(<Menu>
                            <Menu.Item>
                                <h4>{data[i-1].name}{data[i-1].value}</h4>
                            </Menu.Item>
                            <Menu.Item>
                                <h4>{data[i].name}{data[i].value}</h4>
                            </Menu.Item>
                        </Menu>);
    }
    if(data.length%2==1)
    {
        menuEntries.push(<Menu>
                            <Menu.Item>
                                <h4>{data[data.length-1].name}{data[data.length-1].value}</h4>
                            </Menu.Item>
                        </Menu>);
    }
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
                    </Header>
                </Menu.Item>
                <Menu.Item position="right">
                    <Rating icon="star" rating={resource.rating} maxRating={5} disabled size="massive" />
                </Menu.Item>
            </Menu>
            {menuEntries}
            {resource.definition!=null && <p style={{display: "flex", flexWrap: "wrap"}}>Definition: {resource.definition}</p>}
            {resource.references!=null && <p style={{display: "flex", flexWrap: "wrap"}}>References: {resource.references}</p>}
            {resource.description!=null && <p style={{display: "flex", flexWrap: "wrap"}}>Description: {resource.description}</p>}
            {resource.chatbot_text!=null && <p style={{display: "flex", flexWrap: "wrap"}}>Chatbot Text: {resource.chatbot_text}</p>}
        </Container>
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

export function ResourceDetailView({ resource , tagsGot, viewer }) {
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
                              {tagsGot.map(tag => (
                                  tag.approved === true ?(
                                    <Label key={tag.name} size="large" stackable>
                                        {tag.name}
                                    </Label>
                                ):('')
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
                {resource.review_status === 'approved' && resource.review_comments !== 'No Comment' && resource.created_by_user_pk === viewer?(
                    reviews(resource.review_comments)
                ):(<p></p>)}
                {resource.review_status === 'rejected' && resource.created_by_user_pk === viewer?(
                    reviews(resource.review_comments)
                ):(<p></p>)}
            </Container>
    );
}
