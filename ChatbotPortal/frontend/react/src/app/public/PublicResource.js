import React, { Component } from "react";
import {
    List,
    Header,
    Segment,
    Button,
    Grid,
    Card,
    Container,
    Search,
    Form,
    Icon
} from "semantic-ui-react";
import axios from "axios";
import ResourceListItem from "../resource/ResourceListItem.js";

export class PublicResource extends Component {
    constructor(props) {
        super(props);

        this.state = {
            resources: [],
            search_keyword: ""
        };
    }

    handle_search_submit = () => {
        console.log(this.state.search_keyword);
        axios
            .get(`/chatbotportal/resource/search/?search=${this.state.search_keyword}`)
            .then(res => {
                this.setState({ resources: res.data }, error => {
                    console.error(error);
                });
            });
    };

    handle_search_change = event => {
        this.setState({ [event.target.name]: event.target.value });
    };

    render() {
        const resources = this.state.resources.map(resource => (
            <ResourceListItem key={resource.id} resource={resource} />
        ));

        return (
            <div
                style={{
                    paddingTop: 30,
                    paddingLeft: 100,
                    paddingRight: 100
                }}
            >
                <Container style={{ paddingBottom: 50 }} textAlign="center" vertical>
                    <Header
                        as="h3"
                        style={{
                            fontSize: "2em"
                        }}
                        color="blue"
                    >
                        Public Resources
                    </Header>

                    <Form>
                        <Form.Group>
                            <Form.Input
                                fluid
                                placeholder="Search for resource by title, url"
                                name="search_keyword"
                                value={this.state.search_keyword}
                                onChange={this.handle_search_change}
                            />
                            <Button color="green" onClick={this.handle_search_submit}>
                                Search
                            </Button>
                        </Form.Group>
                    </Form>

                    <Card.Group itemsPerRow={3} vertical stackable>
                        {resources}
                    </Card.Group>
                </Container>
            </div>
        );
    }
}

export default PublicResource;
