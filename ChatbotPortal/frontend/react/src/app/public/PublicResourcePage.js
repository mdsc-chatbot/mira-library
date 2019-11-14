import React, { Component } from "react";
import {
    Segment,
    Grid,
    Container,
    Input,
    Button,
} from "semantic-ui-react";
import axios from 'axios';
import {SecurityContext} from '../security/SecurityContext';
import styles from './PublicResourcePage.css';
import {FilterList} from './FilterList';
import {ResourceTable} from './ResourceTable';

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
                            <form className={styles.searchBarContainer} onSubmit={(event) => {event.preventDefault(); this.fetchResources(1);}}>
                                <Input className={styles.searchBarFlex} size="huge" placeholder='Search for resources...' value={this.state.search} onChange={this.handleSearchChange}/>
                                <Button size="huge">Search</Button>
                            </form>
                        </Grid.Row>
                        <Grid.Row columns="2">
                            <Grid.Column width="3">
                                <FilterList
                                    tags={this.state.tags}
                                    categories={this.state.categories}
                                    handleTagSelected={this.handleTagSelected}
                                />
                            </Grid.Column>

                            <Grid.Column width="13">
                                <ResourceTable
                                    resources={this.state.resources}
                                    loadingResources={this.state.loadingResources}
                                />
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Container>
            </Segment>
        );
    }
}

export default PublicResourcePage;
