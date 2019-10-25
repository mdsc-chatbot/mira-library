import React, { Component } from "react";
import { List, Rating, Card, Icon } from "semantic-ui-react";
import { Link } from "react-router-dom";
import { baseRoute } from "../App";

export default class ResourceListItem extends Component {
    render() {
        const resource = this.props.resource;

        return (
            <Card as={Link} to={baseRoute + "/resource/" + resource.id}>
                <Card.Content>
                    <Card.Header>
                        <Icon name="globe" size="large" />
                        {resource.title}
                    </Card.Header>
                    <Card.Meta>
                        Submitted by {resource.created_by_user}
                    </Card.Meta>
                    <Card.Description>
                        <Rating
                            icon="star"
                            defaultRating={resource.rating}
                            maxRating={5}
                            disabled
                        />
                    </Card.Description>
                </Card.Content>
            </Card>
        );
    }
}
