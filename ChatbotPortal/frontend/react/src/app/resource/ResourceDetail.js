import React, { Component } from "react";
import axios from "axios";
import { Header, Icon, Rating, Popup, Card } from "semantic-ui-react";

export default class ResourceDetail extends Component {
  constructor(props) {
    super(props);

    this.state = {
      resource: {}
    };
  }

  componentDidMount() {
    const resourceID = this.props.match.params.resourceID;
    axios
      .get(`http://127.0.0.1:8000/api/user/resources/${resourceID}`)
      .then(res => {
        this.setState({
          resource: res.data
        });
      });
  }

  render() {
    console.log(
      this.state.resource.usefulness_rating,
      typeof this.state.resource.usefulness_rating
    );

    return (
      <div>
        <Card fluid color="blue">
          <Card.Content>
            <Card.Header>
              {this.state.resource.title}
              <Popup
                trigger={
                  <a href={this.state.resource.url}>
                    <Icon name="globe"></Icon>
                  </a>
                }
              >
                <Popup.Content>{this.state.resource.url}</Popup.Content>
              </Popup>
            </Card.Header>
            <Card.Meta>
              <p> Created: {this.state.resource.timestamp}</p>
              {this.state.resource.usefulness_rating ? (
                <Rating
                  icon="star"
                  defaultRating={this.state.resource.usefulness_rating}
                  maxRating={5}
                  disabled
                />
              ) : (
                <div></div>
              )}
            </Card.Meta>
            <Card.Description>
              <Icon name="comment"></Icon> {this.state.resource.user_comment}
            </Card.Description>
          </Card.Content>
        </Card>
      </div>
    );
  }
}
