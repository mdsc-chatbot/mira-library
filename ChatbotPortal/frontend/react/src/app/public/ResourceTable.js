import React from 'react';
import {Card, Rating, Loader} from 'semantic-ui-react';

export function ResourceTable({resources, loadingResources}) {
    /**
     * Three possible cases, each with different shown UI:
     * CASE 1: Resources is not loaded
     * CASE 2: Resources is loaded, but there's no resources found.
     * CASE 3: Resources is loaded, and there are resources found.
     */

    if (loadingResources === true) {
        // CASE 1
        return (
            <React.Fragment>
                <Loader active inline />
                Loading Resources...
            </React.Fragment>
        )
    } else if (resources.length === 0) {
        // CASE 2
        return (
            <p>No resources found. Try a different query?</p>
        );
    } else {
        // CASE 3
        return (
            <React.Fragment>
                <Card.Group itemsPerRow="2">
                    {resources.map(resource => (
                        <Card>
                            <Card.Content>
                                <Card.Header>
                                    {resource.title}
                                </Card.Header>
                                <Card.Meta>{resource.url}</Card.Meta>
                                <Card.Description>
                                    <Rating
                                        icon="star"
                                        rating={resource.rating}
                                        maxRating={5}
                                        disabled
                                    />
                                </Card.Description>
                            </Card.Content>
                        </Card>
                    ))}
                </Card.Group>
            </React.Fragment>
        );
    }
}