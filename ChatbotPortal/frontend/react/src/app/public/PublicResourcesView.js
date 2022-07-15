/**
 * @file: PublicResourcesView.js
 * @summary: Component that renders search bar, filter list, and list of public resources
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
  Segment,
  Grid,
  Container,
  Input,
  Button,
  Dropdown,
  Sidebar,
  Label,
  Icon,
  Pagination,
  Responsive,
} from "semantic-ui-react";
import PropTypes from "prop-types";
import axios from "axios";
import { SecurityContext } from "../contexts/SecurityContext";
import styles from "./PublicResourcePage.css";
import { FilterList } from "./FilterList";
import { ResourceTable } from "./ResourceTable";
import ownStyles from "./PublicResourcesView.css";
import Autocomplete from "react-autocomplete";

class PublicResourcesView extends Component {
  static contextType = SecurityContext;
  // Static list of sort options
  // This list is reflected in the back-end code as well. Check out the view for retrieving resources.
  static resourceDropdownOptions = [
    // { key: 'By Most Recent', value: 0, text: 'By Most Recent' },
    // { key: 'By Most Popular', value: 1, text: 'By Most Popular' },
    // { key: 'By Highest Rated', value: 2, text: 'By Highest Rated' },
    // { key: 'By Least Recent', value: 3, text: 'By Least Recent' },
    // { key: 'By Least Popular', value: 4, text: 'By Least Popular' },
    // { key: 'By Lowest Rated', value: 5, text: 'By Lowest Rated' },
    { key: "By Most Related", value: 6, text: "By Most Related" },
  ];

  static propTypes = {
    tagId: PropTypes.string,
    mobileView: PropTypes.bool, // True if need to show a mobile view
  };

  constructor(props) {
    super(props);

    this.state = {
      resources: [],
      tags: [],
      selectedTags: props.tagId ? [parseInt(props.tagId)] : [],
      categories: [],
      selectedCategories: [],
      loadingResources: true,
      resourcePage: 1,
      search: "",
      value: "",
      totalResourceCount: 0,
      sortOption: 0,
      sidebarVisible: false,
    };
  }

  // Fetch resources and tags initially
  componentDidMount() {
    this.fetchResources(1);
    this.fetchTags();
    //this.fetchCategories();
  }

  fetchResources = (currentPage) => {
    this.setState({
      resourcePage: currentPage,
      loadingResources: false,
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
            sort: this.state.sortOption,
          },
        },
        {
          headers: { Authorization: `Bearer ${this.context.security.token}` },
        }
      )
      .then((res) => {
        if (res.data.results) {
          function compareByScore(a, b) {
            if (a.score < b.score) {
              return 1;
            } else if (a.score > b.score) {
              return -1;
            }
            return 0;
          }
          res.data.results = res.data.results.sort(compareByScore);
        }

        this.setState({
          resources: res.data.results || [],
          totalResourceCount: res.data.count || 0,
          loadingResources: false,
        });
      });
  };

  fetchTags = () => {
    const headers = {};
    if (this.context.security.token) {
      headers["Authorization"] = `Bearer ${this.context.security.token}`;
    }

    axios
      .get("/api/public/tags", {
        headers,
      })
      .then((res) => {
        this.setState({
          tags: res.data || [],
        });
      });
  };

  fetchCategories = () => {
    const headers = {};
    if (this.context.security.token) {
      headers["Authorization"] = `Bearer ${this.context.security.token}`;
    }

    axios
      .get("/api/public/categories", {
        headers,
      })
      .then((res) => {
        this.setState({
          categories: res.data || [],
        });
      });
  };

  handleSearchChange = (e, { value }) => {
    this.setState({
      search: e.target.value,
    });
  };

  handleTagSelected = (event, { tag_id, checked }) => {
    event.preventDefault();
    // Remove or add tag_id depending on whether checkbox was checked
    this.setState(
      (prevState) => {
        let selectedTags = prevState.selectedTags.slice();

        if (checked) {
          selectedTags.push(tag_id);
        } else {
          selectedTags = selectedTags.filter((value) => value !== tag_id);
        }

        return {
          selectedTags,
        };
      },
      () => {
        // Fetch new resources when new tags were selected
        this.fetchResources(1);
      }
    );
  };

  handleTagDeselected = (event, { tag_id }) => {
    event.preventDefault();
    this.setState(
      (prevState) => {
        let selectedTags = prevState.selectedTags.slice();
        selectedTags = selectedTags.filter((value) => value !== tag_id);

        return {
          selectedTags,
        };
      },
      () => {
        // Fetch new resources when new tags were selected
        this.fetchResources(1);
      }
    );
  };

  handleTagInCardsDeselected = (event, { tag_name }) => {
    event.preventDefault();
    // Remove or add tag_id depending on whether checkbox was checked
    this.setState(
      (prevState) => {
        let selectedTags = prevState.selectedTags.slice();
        selectedTags = selectedTags.filter(
          (value) =>
            value !==
            this.state.tags.filter((tag) => tag.name == tag_name)[0].id
        );
        return {
          selectedTags,
        };
      },
      () => {
        // Fetch new resources when new tags were selected
        this.fetchResources(1);
      }
    );
  };

  handleTagInCardsSelected = (event, { tag_name }) => {
    event.preventDefault();
    // Remove or add tag_id depending on whether checkbox was checked
    this.setState(
      (prevState) => {
        let selectedTags = prevState.selectedTags.slice();
        selectedTags.push(
          this.state.tags.filter((tag) => tag.name == tag_name)[0].id
        );
        return {
          selectedTags,
        };
      },
      () => {
        // Fetch new resources when new tags were selected
        this.fetchResources(1);
      }
    );
  };

  handleCategorySelected = (event, { category_id, checked }) => {
    event.preventDefault();
    // Remove or add category_id depending on whether checkbox was checked
    this.setState(
      (prevState) => {
        let selectedCategories = prevState.selectedCategories.slice();

        if (checked) {
          selectedCategories.push(category_id);
        } else {
          selectedCategories = selectedCategories.filter(
            (value) => value !== category_id
          );
        }

        return {
          selectedCategories,
        };
      },
      () => {
        // Fetch new resources when new categories were selected
        this.fetchResources(1);
      }
    );
  };

  handleSortDropdownChange = (event, { value }) => {
    this.setState(
      {
        sortOption: value,
      },
      () => {
        this.fetchResources(this.state.resourcePage);
      }
    );
  };

  handlePageChange = (event, { activePage }) => {
    this.fetchResources(activePage);
  };

  showResourceHeader = () => {
    return (
      <React.Fragment>
        {/* <Dropdown selection placeholder={"Sort by"} value={this.state.sortOption} onChange={this.handleSortDropdownChange} options={PublicResourcesView.resourceDropdownOptions} /> */}
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
      <Container style={{ paddingBottom: 50 }} textAlign="center" vertical>
        <Sidebar.Pushable as="segment" vertical style={{ overflow: "hidden" }}>
          <Sidebar
            animation="overlay"
            direction="left"
            visible={this.state.sidebarVisible}
            icon="labeled"
            vertical
            onHide={() => this.setState({ sidebarVisible: false })}
            width={this.props.mobileView ? "thin" : "wide"}
          >
            <FilterList
              tags={this.state.tags}
              categories={this.state.categories}
              selectedTags={this.state.selectedTags}
              handleTagSelected={this.handleTagSelected}
              handleCategorySelected={this.handleCategorySelected}
              handleTagDeselected={this.handleTagDeselected}
            />
          </Sidebar>
          <Sidebar.Pusher>
            <Segment basic>
              <Grid>
                <Grid.Row>
                  {this.props.mobileView
                    ? [
                        <form
                          className={styles.searchBarContainer}
                          onSubmit={(event) => {
                            event.preventDefault();
                            this.fetchResources(1);
                          }}
                        >
                          <Input
                            name="searchBar"
                            className={styles.searchBarFlex}
                            size="large"
                            placeholder="Search poop ..."
                            value={this.state.search}
                            onChange={this.handleSearchChange}
                          />

                          <Button
                            floated="right"
                            primary
                            name="searchButton"
                            size="large"
                          >
                            <Icon name="search" />
                          </Button>
                        </form>,
                        <Button
                          floated="left"
                          size="large"
                          onClick={() => {
                            this.setState({
                              sidebarVisible: !this.state.sidebarVisible,
                            });
                          }}
                        >
                          <Icon name="filter" />{" "}
                          {this.state.selectedTags.length > 0 ? (
                            <Label color="blue" size="small">
                              {this.state.selectedTags.length}
                            </Label>
                          ) : null}
                        </Button>,
                      ]
                    : [
                        <Button
                          floated="left"
                          size="huge"
                          onClick={() => {
                            this.setState({
                              sidebarVisible: !this.state.sidebarVisible,
                            });
                          }}
                        >
                          Filters{" "}
                          {this.state.selectedTags.length > 0 ? (
                            <Label color="blue" size="small">
                              {this.state.selectedTags.length}
                            </Label>
                          ) : null}
                        </Button>,
                        <form
                          className={styles.searchBarContainer}
                          onSubmit={(event) => {
                            event.preventDefault();
                            console.log("ya hasan");
                            this.fetchResources(1);
                          }}
                        >
                          {/* <Input
                            name="searchBar"
                            className={styles.searchBarFlex}
                            size="huge"
                            placeholder="Search for poopee resources..."
                            value={this.state.search}
                            onChange={this.handleSearchChange}
                          /> */}
                          <Autocomplete
                            //className={styles.searchBarFlex}
                            inputProps={{
                              placeholder: "Search...",
                              name: "searchBar",
                            }}
                            wrapperProps={{
                              className: `ui huge input ${styles.searchBarFlex}`,
                            }}
                            wrapperStyle={{}}
                            items={[
                              { id: 1, label: "COVID-19" },
                              { id: 2, label: "Depression" },
                              { id: 3, label: "Domestic Violence" },
                              { id: 4, label: "Anxiety" },
                              { id: 5, label: "Abuse" },
                              { id: 6, label: "Saskatchewan" },
                              { id: 7, label: "Nova Scotia" },
                              { id: 8, label: "Nunavut" },
                              { id: 9, label: "Prince Edward Island" },
                              { id: 10, label: " Newfoundland and Labrador" },
                              { id: 11, label: "Northwest Territories" },
                              { id: 12, label: "Yukon" },
                              { id: 13, label: "New Brunswick" },
                              {
                                id: 14,
                                label: "Acquired Immune Deficiency Syndrome",
                              },
                              { id: 15, label: "AIDS" },
                              { id: 16, label: "Addictions" },
                              { id: 17, label: "Drugs Addictions" },
                              { id: 18, label: "Alcohol Addictions" },
                              { id: 19, label: "Gambling Addictions" },
                              { id: 20, label: "Adjustment disorders" },
                              { id: 21, label: "Anger" },
                              { id: 22, label: "Anorexia" },
                              {
                                id: 23,
                                label: "Antisocial Personality Disorder",
                              },
                              { id: 24, label: "ASPD" },
                              { id: 25, label: "Manitoba" },
                              { id: 26, label: "Asperger Syndrome" },
                              { id: 27, label: "Attachment Disorders" },
                              { id: 28, label: "Attention Deficit Disorders" },
                              { id: 29, label: "ADD/ADHD" },
                              { id: 30, label: "ADD" },
                              { id: 31, label: "ADHD" },
                              { id: 32, label: "Auditory Processing Disorder" },
                              { id: 33, label: "APD" },
                              { id: 34, label: "Autism" },
                              { id: 35, label: "Bipolar Disorders" },
                              {
                                id: 36,
                                label: "Borderline Personality Disorder",
                              },
                              { id: 37, label: "BPD" },
                              { id: 38, label: "Bulimia" },
                              { id: 39, label: "Bullying" },
                              { id: 40, label: "Burnout" },
                              { id: 41, label: "Cancer" },
                              { id: 42, label: "Chronic Pain" },
                              { id: 43, label: "Conduct Disorder" },
                              { id: 44, label: "Ontario" },
                              { id: 45, label: "Delirium" },
                              { id: 46, label: "Dementia" },
                              { id: 47, label: "Alzheimer's" },
                              { id: 48, label: "Alberta" },
                              { id: 49, label: "Quebec" },
                              { id: 50, label: "Down syndrome" },
                              { id: 51, label: "Eating Disorders" },
                              { id: 52, label: "Elimination Disorders" },
                              { id: 53, label: "Fatigue" },
                              {
                                id: 54,
                                label: "Fetal Alcohol Spectrum Disorders",
                              },
                              { id: 55, label: "FASD" },
                              { id: 56, label: "Firesetting" },
                              { id: 57, label: "Gender Identity" },
                              { id: 58, label: "Distress" },
                              { id: 59, label: "Supports for Children" },
                              { id: 60, label: "well-being" },
                              { id: 61, label: "Generalized Anxiety Disorder" },
                              { id: 62, label: "Grief and Bereavement" },
                              { id: 63, label: "Harassment" },
                              { id: 64, label: "Hoarding" },
                              { id: 65, label: "Housing" },
                              { id: 66, label: "Human Trafficking" },
                              { id: 67, label: "Early Childhood" },
                              { id: 68, label: "Insomnia" },
                              { id: 69, label: "Learning Disorders" },
                              { id: 70, label: "Legal" },
                              { id: 71, label: "Mental Health" },
                              { id: 72, label: "Mood Disorders" },
                              {
                                id: 73,
                                label: "Obsessive Compulsive Disorder",
                              },
                              { id: 74, label: "OCD" },
                              { id: 75, label: "Operational Stress Injury" },
                              { id: 76, label: "Opositional defiant disorder" },
                              { id: 77, label: "ODD" },
                              { id: 78, label: "Overweight and Obesity" },
                              { id: 79, label: "Pandemic" },
                              { id: 80, label: "Panic" },
                              { id: 81, label: "Panic Attack" },
                              { id: 82, label: "Parenting" },
                              { id: 83, label: "Personality disorders" },
                              { id: 84, label: "Phobia" },
                              { id: 85, label: "Nutrition" },
                              {
                                id: 86,
                                label: "Post-Traumatic Stress Disorder",
                              },
                              { id: 87, label: "PTSD" },
                              { id: 88, label: "Trauma" },
                              { id: 89, label: "Psychopathy" },
                              { id: 90, label: "Resiliency" },
                              { id: 91, label: "Schizophrenia" },
                              { id: 92, label: "Psychosis" },
                              { id: 93, label: "School Refusal" },
                              { id: 94, label: "Self-care" },
                              { id: 95, label: "Self-harm" },
                              { id: 96, label: "Self-Regulation" },
                              { id: 97, label: "Sensory Processing Disorders" },
                              { id: 98, label: "Separation" },
                              { id: 99, label: "Sexual Health" },
                              { id: 100, label: "Sexual Violence" },
                              { id: 101, label: "Sleep Disorders" },
                              { id: 102, label: "Smoking Cessation" },
                              { id: 103, label: "Somatoform Disorders" },
                              { id: 104, label: "Speech and Language" },
                              { id: 105, label: "Stigma" },
                              { id: 106, label: "Stress" },
                              { id: 107, label: "Substance use" },
                              { id: 108, label: "Suicidal Ideation" },
                              { id: 109, label: "Tourette Syndrome" },
                              { id: 110, label: "Workplace" },
                              { id: 111, label: "Agoraphobia" },
                              { id: 112, label: "Post-Partum Depression" },
                              { id: 113, label: "Seasonal Affective Disorder" },
                              { id: 114, label: "Gambling" },
                              { id: 115, label: "Social Anxiety Disorder" },
                              { id: 116, label: "Anxiety Disorder" },
                              { id: 117, label: "Intellectual Disability" },
                              { id: 118, label: "Communication Disorders" },
                              {
                                id: 119,
                                label:
                                  "Attention-Deficit/Hyperactivity Disorder",
                              },
                              { id: 120, label: "Personality Disorder" },
                              { id: 121, label: "Delusional Disorder" },
                              { id: 122, label: "Psychotic Disorder" },
                              { id: 123, label: "Catatonia" },
                              { id: 124, label: "Major Depressive Disorder" },
                              {
                                id: 125,
                                label: "Persisten Depressive Disorder",
                              },
                              { id: 126, label: "social phobia" },
                              { id: 127, label: "panic disorder" },
                              { id: 128, label: "acute stress disorder" },
                              { id: 129, label: "adjustment disorders" },
                              { id: 130, label: "enuresis" },
                              { id: 131, label: "resilience" },
                              {
                                id: 132,
                                label: "Human Immunodeficiency Virus",
                              },
                              { id: 133, label: "HIV" },
                            ]}
                            shouldItemRender={(item, value) =>
                              item.label
                                .toLowerCase()
                                .indexOf(value.toLowerCase()) > -1
                            }
                            getItemValue={(item) => item.label}
                            renderItem={(item, highlighted) => (
                              <div
                                key={item.id}
                                style={{
                                  backgroundColor: highlighted
                                    ? "#eee"
                                    : "transparent",
                                }}
                              >
                                {item.label}
                              </div>
                            )}
                            // onChange={(e) =>
                            //   this.setState({ search: e.target.value })
                            // }

                            value={this.state.search}
                            onChange={this.handleSearchChange}
                            onSelect={(value) =>
                              this.setState({ search: value })
                            }
                          />
                          <Button
                            floated="right"
                            primary
                            name="searchButton"
                            size="huge"
                          >
                            Search
                          </Button>
                        </form>,
                      ]}
                </Grid.Row>
                <Grid.Row columns="1">
                  <Grid.Column
                    className={ownStyles.noPaddingResourceColumn}
                    width="16"
                  >
                    <Segment>
                      <span
                        className={
                          this.props.mobileView
                            ? styles.mobileTopBarContainer
                            : styles.topBarContainer
                        }
                      >
                        {this.showResourceHeader()}
                      </span>
                      <ResourceTable
                        resources={this.state.resources}
                        loadingResources={this.state.loadingResources}
                        handleTagInCardsSelected={this.handleTagInCardsSelected}
                        handleTagInCardsDeselected={
                          this.handleTagInCardsDeselected
                        }
                        selectedTags={this.state.selectedTags}
                        allTags={this.state.tags}
                      />
                    </Segment>
                  </Grid.Column>
                </Grid.Row>
              </Grid>
            </Segment>
          </Sidebar.Pusher>
        </Sidebar.Pushable>
      </Container>
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
}
