/**
 * @file: ResourceListItem.js
 * @summary: Component for each element of the ResourceList.js
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
import { List, Rating, Card, Icon } from "semantic-ui-react";
import { Link } from "react-router-dom";
import { baseRoute } from "../App";
import * as styles from "../shared/Link.css";
import ResourceReviewStatus from "./ResourceReviewStatus";

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
                    <Card.Meta className={styles.inline}>
                        Submitted by {resource.created_by_user}
                        <ResourceReviewStatus resource={resource}/>
                    </Card.Meta>
                    <Card.Description>
                        <a href={resource.url} target="_blank">
                            <p className={styles.link}>
                                Open new tab to go to url
                            </p>
                        </a>
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
