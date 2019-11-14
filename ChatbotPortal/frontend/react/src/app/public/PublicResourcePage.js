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
    Button,
    Rating,
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
            selectedTags : [],
            categories : [],
            loadingResources : true,
            resourcePage : 1,
            search : ''
        };
    }

    // Fetch resources and tags initially
    componentDidMount() {
        this.fetchResources(1);
        this.fetchTags();
        this.fetchCategories();
    }

    fetchResources = (currentPage) => {
        this.setState({
            resourcePage : currentPage,
            loadingResources : false
        });

        axios.get(`/api/public/resources`, {
            params : {
                page : currentPage,
                search : this.state.search,
                tags : this.state.selectedTags.toString(),
            },
        })
            .then(res => {
                this.setState({
                    resources : res.data.results || [],
                    loadingResources : false
                });
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

    fetchCategories = () => {
        //TODO: Axios get categories
    };

    handleSearchChange = (e, {value}) => {
        this.setState({
            search : value
        });
    };

    handleTagSelected = (event, {id, checked}) => {
        // Remove or add id depending on whether checkbox was checked
        this.setState((prevState) => {
            let selectedTags = prevState.selectedTags.slice();

            if (checked) {
                selectedTags.push(id);
            } else {
                selectedTags = selectedTags.filter(value => value !== id);
            }

            return {
                selectedTags
            };
        }, () => {
            // Fetch new resources when new tags were selected
            this.fetchResources(this.state.resourcePage)
        });
    };

    showResourceSearchBar = () => {
        return (
            <form className={styles.searchBarContainer} onSubmit={(event) => {event.preventDefault(); this.fetchResources(1);}}>
                <Input className={styles.searchBarFlex} size="huge" placeholder='Search for resources...' value={this.state.search} onChange={this.handleSearchChange}/>
                <Button size="huge">Search</Button>
            </form>
        );
    };

    // Render code for showing tags
    showTagsAndCategories = (tags, categories) => {
        if (tags.length > 0) {
            return (
                <React.Fragment>
                    {/*<span className={styles.searchBarMargin}>*/}
                        {/*<Input placeholder='Search for tags...' className={styles.flexInput} />*/}
                    {/*</span>*/}
                    <List className={styles.nonCenteredText}>
                        <List.Item>
                            <List.Header>Categories</List.Header>
                            <List.Content>
                                {categories.map(category => (
                                    <List.Item>
                                        <Checkbox label={category.name}/>
                                    </List.Item>
                                ))}
                            </List.Content>
                        </List.Item>
                        <List.Item>
                            <List.Header>Tags</List.Header>
                            <List.Content>
                                {tags.map(tag => (
                                    <List.Item>
                                        <Checkbox label={tag.name} id={tag.id} onChange={this.handleTagSelected}/>
                                    </List.Item>
                                ))}
                            </List.Content>
                        </List.Item>
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

        if (loadingResources === true) {
            // CASE 1
            return (
                <React.Fragment>
                    <Loader active inline />
                    Loading Resources...
                </React.Fragment>
            )
        } else if (resources.length === 0) {
            // CASE 2
            return (
                <p>No resources found. Try a different query?</p>
            );
        } else {
            // CASE 3
            return (
                <React.Fragment>
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
                    <Grid>
                        <Grid.Row>
                            {this.showResourceSearchBar()}
                        </Grid.Row>
                        <Grid.Row columns="2">
                            <Grid.Column width="3">
                                <Segment>
                                    {this.showTagsAndCategories(this.state.tags, this.state.categories)}
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
