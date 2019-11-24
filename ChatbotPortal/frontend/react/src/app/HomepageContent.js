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
                <Card.Content>
                    <Link to={location => ({...location, pathname: `${location.pathname}/public_resource`})}>
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
                            <Card.Group itemsPerRow={5}>
                                <Card>
                                    <Card.Content>
                                        <Card.Header>
                                            Matthew Harris
                                        </Card.Header>
                                        <Card.Meta>Co-Worker</Card.Meta>
                                        <Card.Description>
                                            Matthew is a pianist living in
                                            Nashville.
                                        </Card.Description>
                                    </Card.Content>
                                </Card>

                                <Card>
                                    <Card.Content>
                                        <Card.Header content="Jake Smith" />
                                        <Card.Meta content="Musicians" />
                                        <Card.Description content="Jake is a drummer living in New York." />
                                    </Card.Content>
                                </Card>

                                <Card>
                                    <Card.Content
                                        header="Elliot Baker"
                                        meta="Friend"
                                        description="Elliot is a music producer living in Chicago."
                                    />
                                </Card>

                                <Card
                                    header="Jenny Hess"
                                    meta="Friend"
                                    description="Jenny is a student studying Media Management at the New School"
                                />
                            </Card.Group>
                        </Grid.Row>

                        <Grid.Row>
                            <Header
                                as="h3"
                                style={{ fontSize: "2em", color: "#3075c9" }}
                            >
                                Recent Resources
                            </Header>
                            <Card.Group itemsPerRow={5}>
                                {this.state.recentResources.length ? (
                                    <React.Fragment>
                                        {this.state.recentResources.map(this.showCard)}
                                        {this.showMoreCard()}
                                    </React.Fragment>
                                ) : (
                                    <div>
                                        <Loader />
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
                            <Card.Group itemsPerRow={5}>
                                {this.state.ratingResources.length ? (
                                    <React.Fragment>
                                        {this.state.ratingResources.map(this.showCard)}
                                        {this.showMoreCard()}
                                    </React.Fragment>
                                ) : (
                                    <div>
                                        <Loader />
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
