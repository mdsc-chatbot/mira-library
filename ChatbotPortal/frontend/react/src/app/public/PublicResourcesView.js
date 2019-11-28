import React, { Component } from "react";
import {
    Segment,
    Grid,
    Container,
    Input,
    Button,
    Dropdown,
    Pagination, Responsive,
} from "semantic-ui-react";
import PropTypes from 'prop-types';
import axios from 'axios';
import {SecurityContext} from '../contexts/SecurityContext';
import styles from './PublicResourcePage.css';
import {FilterList} from './FilterList';
import {ResourceTable} from './ResourceTable';
import ownStyles from './PublicResourcesView.css'

class PublicResourcesView extends Component {
    static contextType = SecurityContext;
    // Static list of sort options
    // This list is reflected in the back-end code as well. Check out the view for retrieving resources.
    static resourceDropdownOptions = [
        {key : 'By Most Recent', value: 0, text: 'By Most Recent'},
        {key : 'By Most Popular', value: 1, text: 'By Most Popular'},
        {key : 'By Highest Rated', value: 2, text: 'By Highest Rated'},
        {key : 'By Least Recent', value: 3, text: 'By Least Recent'},
        {key : 'By Least Popular', value: 4, text: 'By Least Popular'},
        {key : 'By Lowest Rated', value: 5, text: 'By Lowest Rated'},
    ];

    static propTypes = {
        tagId : PropTypes.string,
        mobileView : PropTypes.bool, // True if need to show a mobile view
    };

    constructor(props) {
        super(props);

        this.state = {
            resources : [],
            tags : [],
            selectedTags : props.tagId ? [parseInt(props.tagId)] : [],
            categories : [],
            selectedCategories : [],
            loadingResources : true,
            resourcePage : 1,
            search : '',
            totalResourceCount : 0,
            sortOption : 0,
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

        axios
            .get(
                `/api/public/resources`,
                {
                    params: {
                        page: currentPage,
                        search: this.state.search,
                        tags: this.state.selectedTags.toString(),
                        categories: this.state.selectedCategories.toString(),
                        sort: this.state.sortOption
                    }
                },
                {
                    headers: { Authorization: `Bearer ${this.context.security.token}` }
                }
            )
            .then(res => {
                this.setState({
                    resources: res.data.results || [],
                    totalResourceCount: res.data.count || 0,
                    loadingResources: false
                });
            });
    };

    fetchTags = () => {
        const headers = {};
        if (this.context.security.token) {
            headers['Authorization'] = `Bearer ${this.context.security.token}`;
        }

        axios
            .get("/api/public/tags", {
                headers
            })
            .then(res => {
                this.setState({
                    tags: res.data || []
                });
            });
    };

    fetchCategories = () => {
        const headers = {};
        if (this.context.security.token) {
            headers['Authorization'] = `Bearer ${this.context.security.token}`;
        }

        axios
            .get("/api/public/categories", {
                headers
            })
            .then(res => {
                this.setState({
                    categories: res.data || []
                });
            });
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
            this.fetchResources(1)
        });
    };

    handleCategorySelected = (event, {id, checked}) => {
        // Remove or add id depending on whether checkbox was checked
        this.setState((prevState) => {
            let selectedCategories = prevState.selectedCategories.slice();

            if (checked) {
                selectedCategories.push(id);
            } else {
                selectedCategories = selectedCategories.filter(value => value !== id);
            }

            return {
                selectedCategories
            };
        }, () => {
            // Fetch new resources when new categories were selected
            this.fetchResources(1)
        });
    };

    handleSortDropdownChange = (event, {value}) => {
        this.setState({
            sortOption : value
        }, () => {
            this.fetchResources(this.state.resourcePage);
        });
    };

    handlePageChange = (event, {activePage}) => {
        this.fetchResources(activePage)
    };

    showResourceHeader = () => {
        return (
            <React.Fragment>
                <Dropdown selection placeholder={"Sort by"} value={this.state.sortOption} onChange={this.handleSortDropdownChange} options={PublicResourcesView.resourceDropdownOptions} />
                <Pagination
                    activePage={this.state.resourcePage}
                    totalPages={Math.ceil(this.state.totalResourceCount / 100)}
                    onPageChange={this.handlePageChange}
                />
            </React.Fragment>
        );
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
                                <Input name="searchBar" className={styles.searchBarFlex} size="huge" placeholder='Search for resources...' value={this.state.search} onChange={this.handleSearchChange}/>
                                <Button name="searchButton" size="huge">Search</Button>
                            </form>
                        </Grid.Row>
                        <Grid.Row columns="2">
                            <Grid.Column className={ownStyles.noPaddingTagColumn} width={this.props.mobileView ? "5" : "3"}>
                                <FilterList
                                    tags={this.state.tags}
                                    categories={this.state.categories}
                                    selectedTags={this.state.selectedTags}
                                    handleTagSelected={this.handleTagSelected}
                                    handleCategorySelected={this.handleCategorySelected}
                                />
                            </Grid.Column>

                            <Grid.Column className={ownStyles.noPaddingResourceColumn} width={this.props.mobileView ? "11" : "13"}>
                                <Segment>
                                    <span className={this.props.mobileView ? styles.mobileTopBarContainer : styles.topBarContainer}>
                                            {this.showResourceHeader()}
                                        </span>
                                    <ResourceTable
                                        resources={this.state.resources}
                                        loadingResources={this.state.loadingResources}
                                    />
                                </Segment>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Container>
            </Segment>
        );
    }
}

export default function ResponsiveResourcesView(props) {
    return (
        <React.Fragment>
            <Responsive maxWidth={767}>
                <PublicResourcesView mobileView={true} {...props} />
            </Responsive>

            <Responsive minWidth={768}>
                <PublicResourcesView mobileView={false} {...props} />
            </Responsive>
        </React.Fragment>
    );
};
