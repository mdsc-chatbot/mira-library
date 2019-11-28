/**
 * @file: PublicResourceCard.js
 * @summary: List item component for public resources
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
import React from 'react';
import PropTypes from 'prop-types'
import {Card, Rating} from "semantic-ui-react";
import {Link} from "react-router-dom";
import styles from './PublicResourceCard.css'

export function PublicResourceCard({resource, locationPrefix}) {
    return (
        <Card>
            <Card.Content>
                <Card.Header>
                    <Link to={location => ({...location, pathname: `${location.pathname}${locationPrefix}/${resource.id}`})}>
                        {resource.title}
                    </Link>
                </Card.Header>
                <Card.Meta className={styles.overflowText}>
                    <a href={resource.url} title={resource.url}>
                        {resource.url}
                    </a>
                </Card.Meta>
                <Card.Description>
                    <Rating
                        icon="star"
                        rating={resource.rating}
                        maxRating={5}
                        disabled
                    />
                    <div className={styles.overflowContentText} title={resource.website_summary_metadata}>
                        {resource.website_summary_metadata}
                    </div>
                </Card.Description>
            </Card.Content>
        </Card>
    );
}

PublicResourceCard.propTypes = {
    resource : PropTypes.object.isRequired,
    locationPrefix : PropTypes.string.isRequired,
};
