import React, { Component } from "react";
import {
    List,
    Header,
    Segment,
    Loader,
    Grid,
    Card,
    Container,
    Input,
    Checkbox,
    Button, Rating
} from "semantic-ui-react";
import axios from 'axios';
import {SecurityContext} from '../security/SecurityContext';
import styles from './PublicResourcePage.css';

export class PublicResourcePage extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resources : [],
            tags : [],
            selected_tags : [],
            loadingResources : true
        };
    }

    // Fetch resources and tags initially
    componentDidMount() {
        this.fetchResources();
        this.fetchTags();
    }

    fetchResources = () => {
        this.setState({
            loadingResources : false
        });

        axios.get('/api/public/resources')
            .then(res => {
                this.setState({
                    resources : res.data || [],
                    loadingResources : false
                })
            });
    };

    fetchTags = () => {
        axios.get('/api/public/tags')
            .then(res => {
                this.setState({
                    tags : res.data || []
                })
            });
    };

    // Render code for showing tags
    showTags = (tags) => {
        if (tags.length > 0) {
            return (
                <React.Fragment>
                    <span className={styles.searchBarMargin}>
                        <Input placeholder='Search for tags...' className={styles.flexInput} />
                    </span>
                    <List>
                        {tags.map(tag => (
                            <List.Item>
                                <Checkbox label={tag.name}/>
                            </List.Item>
                        ))}
                    </List>
                </React.Fragment>
            );
        } else {
            return (
                <React.Fragment>
                    <Loader active inline />
                    Loading Tags
                </React.Fragment>
            );
        }
    };

    // Render code for showing resources
    showResources = (resources, loadingResources) => {
        /**
         * Three possible cases, each with different shown UI:
         * CASE 1: Resources is not loaded
         * CASE 2: Resources is loaded, but there's no resources found.
         * CASE 3: Resources is loaded, and there are resources found.
         */

        const searchBar = (
            <span className={styles.searchBarMargin}>
                <Input placeholder='Search for tags...' />
                <Button>Search</Button>
            </span>
        );

        if (loadingResources === true) {
            // CASE 1
            return (
                <React.Fragment>
                    {searchBar}
                    <Loader active inline />
                    Loading Resources...
                </React.Fragment>
            )
        } else if (resources.length === 0) {
            // CASE 2
            return (
                <React.Fragment>
                    {searchBar}
                    <p>No resources found. Try a different query?</p>
                </React.Fragment>
            );
        } else {
            // CASE 3
            return (
                <React.Fragment>
                    {searchBar}
                    <Card.Group>
                        {resources.map(resource => (
                            <Card>
                                <Card.Content>
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
                                </Card.Content>
                            </Card>
                        ))}
                    </Card.Group>
                </React.Fragment>
            );
        }
    };

    render() {
        return (
            <Segment vertical>
                <Container
                    style={{ paddingBottom: 50 }}
                    textAlign="center"
                    vertical
                >
                    <Header
                        as="h3"
                        style={{
                            fontSize: "2em"
                        }}
                        color="blue"
                    >
                        Public Resources
                    </Header>

                    <Grid>
                        <Grid.Row columns="2">
                            <Grid.Column width="3">
                                <Segment>
                                    {this.showTags(this.state.tags)}
                                </Segment>
                            </Grid.Column>

                            <Grid.Column width="13">
                                {this.showResources(this.state.resources, this.state.loadingResources)}
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Container>
            </Segment>
        );
    }
}

export default PublicResourcePage;
