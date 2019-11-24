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
