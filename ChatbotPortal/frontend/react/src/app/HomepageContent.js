import React, { Component } from "react";
import {
    Header,
    List,
    Loader,
    Card,
    Segment,
    Container,
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
                    <Grid container stackable verticalAlign="middle">
                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{
                                    fontSize: "2em",
                                    color: "#3075c9"
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
                                        <Loader active inline />
                                    </div>
                                )}
                            </Card.Group>
                        </Grid.Row>

                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{ fontSize: "2em", color: "#3075c9" }}
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
                                        <Loader active inline />
                                    </div>
                                )}
                            </Card.Group>
                        </Grid.Row>

                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{ fontSize: "2em", color: "#3075c9" }}
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
                                        <Loader active inline />
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
