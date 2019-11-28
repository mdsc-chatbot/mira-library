/**
 * @file: FilterList.js
 * @summary: Component that renders a list of checkbox for categories and tags
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

import React from 'react'
import PropTypes from 'prop-types';
import {Segment, Checkbox, Loader, List} from 'semantic-ui-react';
import styles from './FilterList.css';

// Stores tags and categories
export function FilterList({tags, categories, selectedTags, handleTagSelected, handleCategorySelected}) {

    if (tags.length > 0) {
        return (
            <Segment>
                <List className={styles.nonCenteredText}>
                    <List.Item>
                        <List.Header>Categories</List.Header>
                        <List.Content>
                            {categories.map(category => (
                                <List.Item>
                                    <Checkbox name={category.name} label={category.name} id={category.id} onChange={handleCategorySelected}/>
                                </List.Item>
                            ))}
                        </List.Content>
                    </List.Item>
                    <List.Item>
                        <List.Header>Tags</List.Header>
                        <List.Content>
                            {tags.map(tag => (
                                <List.Item>
                                    <Checkbox name={tag.name} label={tag.name} id={tag.id} onChange={handleTagSelected} defaultChecked={selectedTags.includes(tag.id)}/>
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
    selectedTags : PropTypes.array,
    handleTagSelected : PropTypes.func.isRequired,
    handleCategorySelected : PropTypes.func.isRequired,
};