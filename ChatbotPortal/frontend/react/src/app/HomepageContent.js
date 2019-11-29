/**
 * @file: HomepageContent.js
 * @summary: Showing Popular, Recent, Highest rated resources
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
import {
    Header,
    Loader,
    Card,
    Segment,
    Grid, Rating
} from "semantic-ui-react";
import axios from 'axios';
import {Link} from 'react-router-dom';
import styles from './HomepageContent.css';
import {PublicResourceCard} from './public/PublicResourceCard';

/**
 * Includes:
 * - Popular resources, recent resources, highest rated resources as a card
 */
export class HomepageContent extends Component {

    constructor(props) {
        super(props);

        this.state = {
            recentResources : [],
            popularResources : [],
            ratingResources : [],
        };
    }

    componentDidMount() {
        // More info on sortOption on the public resource page
        this.resourceNetworkRequest('recentResources', 0);
        this.resourceNetworkRequest('popularResources', 1);
        this.resourceNetworkRequest('ratingResources', 2);
    }

    resourceNetworkRequest = (resourceField, sortOption) => {
        axios.get(
            `/api/public/homepage-resources`,
            {
                params: {
                    page: 1,
                    sort: sortOption
                }
            },
        ).then(res => {
            this.setState({
                [resourceField]: res.data.results
            });
        });
    };

    showCard = (resource) => {
        return (
            <Card>
                <Card.Content>
                    <Link to={location => ({...location, pathname: `${location.pathname}/public_resource/detail/${resource.id}`})}>
                        <Card.Header>
                            {resource.title}
                        </Card.Header>
                        <Card.Meta>{resource.url}</Card.Meta>
                        <Card.Description>
                            <Rating
                                icon="star"
                                rating={resource.rating}
                                maxRating={5}
                                disabled
                            />
                        </Card.Description>
                    </Link>
                </Card.Content>
            </Card>
        );
    };

    showMoreCard = () => {
        return (
            <Card>
                <Card.Content className={styles.centerAlignment}>
                    <Link className={styles.centerAlignment} to={location => ({...location, pathname: `${location.pathname}/public_resource`})}>
                        <Card.Header>
                            Show More...
                        </Card.Header>
                    </Link>
                </Card.Content>
            </Card>
        );
    };

    render() {
        return (
            <div>
                <Segment vertical>
                    <Grid className={styles.alignment} container stackable verticalAlign="middle">
                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{
                                    fontSize: "1.5em",
                                    color: "#0072BB"
                                }}
                            >
                                Popular Resources
                            </Header>
                            <Card.Group itemsPerRow={5} stackable>
                                {this.state.popularResources.length ? (
                                    <React.Fragment>
                                        {this.state.popularResources.map((resource) => (
                                            <PublicResourceCard resource={resource} locationPrefix="/public_resource/detail" />
                                        ))}
                                        {this.showMoreCard()}
                                    </React.Fragment>
                                ) : (
                                    <div>
                                        <Loader className={styles.inlineLoader}  active inline />
                                    </div>
                                )}
                            </Card.Group>
                        </Grid.Row>

                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{ fontSize: "1.5em", color: "#0072BB" }}
                            >
                                Recent Resources
                            </Header>
                            <Card.Group itemsPerRow={5} stackable>
                                {this.state.recentResources.length ? (
                                    <React.Fragment>
                                        {this.state.recentResources.map((resource) => (
                                            <PublicResourceCard resource={resource} locationPrefix="/public_resource/detail" />
                                        ))}
                                        {this.showMoreCard()}
                                    </React.Fragment>
                                ) : (
                                    <div>
                                        <Loader className={styles.inlineLoader} active inline />
                                    </div>
                                )}
                            </Card.Group>
                        </Grid.Row>

                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{ fontSize: "1.5em", color: "#0072BB" }}
                            >
                                Highest Rated Resources
                            </Header>
                            <Card.Group itemsPerRow={5} stackable>
                                {this.state.ratingResources.length ? (
                                    <React.Fragment>
                                        {this.state.ratingResources.map((resource) => (
                                            <PublicResourceCard resource={resource} locationPrefix="/public_resource/detail" />
                                        ))}
                                        {this.showMoreCard()}
                                    </React.Fragment>
                                ) : (
                                    <div>
                                        <Loader className={styles.inlineLoader} active inline />
                                    </div>
                                )}
                            </Card.Group>
                        </Grid.Row>

                    </Grid>
                </Segment>
            </div>
        );
    }
}

export default HomepageContent;
