import React, { Component } from "react";
import { Statistic, Icon } from "semantic-ui-react";

export class Statistics extends Component {
  render() {
    return (
      <div>
        <Statistic size="mini" color="blue">
          <Statistic.Value>
            <Icon name="globe" />
            {this.props.submitted_resources}
          </Statistic.Value>
          <Statistic.Label> Submitted Resources</Statistic.Label>
        </Statistic>
        <Statistic size="mini" color="olive">
          <Statistic.Value>
            <Icon name="thumbs up" />
            10
          </Statistic.Value>
          <Statistic.Label> Approved Resources</Statistic.Label>
        </Statistic>
        <Statistic size="mini" color="brown">
          <Statistic.Value>
            <Icon name="eye" />
            5,0000
          </Statistic.Value>
          <Statistic.Label> Views</Statistic.Label>
        </Statistic>
      </div>
    );
  }
}

export default Statistics;
