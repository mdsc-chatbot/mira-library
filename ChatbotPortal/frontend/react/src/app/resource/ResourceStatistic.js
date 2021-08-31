/**
 * @file: ResourceStatistic.js
 * @summary: Semanitc UI Statistic component that shows number of user's total, approved, pending, rejected resources
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
import { Statistic, Icon } from "semantic-ui-react";

export class ResourceStatistic extends Component {
    render() {
        let total_resources = 0;
        let reviewed_resources = 0;
        let pending_resources = 0;

        this.props.resources.forEach((resource) => {
            total_resources += 1;
            if (resource.review_status !== "pending" && resource.review_status_2 !== "pending"){
                reviewed_resources += 1;
            }else{
                pending_resources += 1;
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
                        {reviewed_resources}
                    </Statistic.Value>
                    <Statistic.Label> Reviewed Resources</Statistic.Label>
                </Statistic>
            </div>
        );
    }
}

export default ResourceStatistic;
