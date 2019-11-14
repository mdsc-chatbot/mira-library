import React from 'react'
import PropTypes from 'prop-types';
import {Segment, Checkbox, Loader, List} from 'semantic-ui-react';
import styles from './FilterList.css';

// Stores tags and categories
export function FilterList({tags, categories, handleTagSelected}) {

    if (tags.length > 0) {
        return (
            <Segment>
                <List className={styles.nonCenteredText}>
                    <List.Item>
                        <List.Header>Categories</List.Header>
                        <List.Content>
                            {categories.map(category => (
                                <List.Item>
                                    <Checkbox label={category.name}/>
                                </List.Item>
                            ))}
                        </List.Content>
                    </List.Item>
                    <List.Item>
                        <List.Header>Tags</List.Header>
                        <List.Content>
                            {tags.map(tag => (
                                <List.Item>
                                    <Checkbox label={tag.name} id={tag.id} onChange={handleTagSelected}/>
                                </List.Item>
                            ))}
                        </List.Content>
                    </List.Item>
                </List>
            </Segment>
        );
    } else {
        return (
            <React.Fragment>
                <Loader active inline />
                Loading Tags
            </React.Fragment>
        );
    }
}

FilterList.propTypes = {
    tags : PropTypes.array,
    categories : PropTypes.array,
    handleTagSelected : PropTypes.func,
};