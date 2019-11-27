import React, { Component } from "react";
import { Statistic, Icon } from "semantic-ui-react";

export class ResourceStatistic extends Component {
    render() {
        let total_resources = 0;
        let approved_resources = 0;
        let pending_resources = 0;
        let rejected_resources = 0;

        this.props.resources.forEach((resource) => {
            total_resources += 1;
            if (resource.review_status === "approved"){
                approved_resources += 1;
            }else if (resource.review_status === "pending"){
                pending_resources += 1;
            } else if (resource.review_status === "rejected") {
                rejected_resources += 1;
            }
        });

        return (
            <div>
                <Statistic size="mini" color="blue">
                    <Statistic.Value id="total_resources">
                        <Icon name="globe" />
                        {total_resources}
                    </Statistic.Value>
                    <Statistic.Label> Total Submitted Resources</Statistic.Label>
                </Statistic>
                <Statistic size="mini" color="yellow">
                    <Statistic.Value id="pending_resources">
                        <Icon name="sync alternate" />
                        {pending_resources}
                    </Statistic.Value>
                    <Statistic.Label> Pending Resources</Statistic.Label>
                </Statistic>
                <Statistic size="mini" color="olive">
                    <Statistic.Value id="approved_resources">
                        <Icon name="thumbs up" />
                        {approved_resources}
                    </Statistic.Value>
                    <Statistic.Label> Approved Resources</Statistic.Label>
                </Statistic>
                <Statistic size="mini" color="red">
                    <Statistic.Value id="rejected_resources">
                        <Icon name="thumbs down" />
                        {rejected_resources}
                    </Statistic.Value>
                    <Statistic.Label> Rejected Resources</Statistic.Label>
                </Statistic>
            </div>
        );
    }
}

export default ResourceStatistic;
