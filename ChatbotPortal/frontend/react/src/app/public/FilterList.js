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

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Segment, Checkbox, Loader, List, Accordion, Label, Icon, Tab } from 'semantic-ui-react';
import * as styles from './FilterList.css';

// Language category mappings
const LANGUAGE_CATEGORIES = {
  en: [
    'Audience',
    'Costs',
    'Health Issue',
    'Language',
    'Location',
    'Resource Format',
    'Resource Type for Education/Informational',
    'Resource Type for Programs and Services'
  ],
  fr: [
    'Coûts',
    'Langue',
    'Problème de santé',
    'Type de ressource',
    'Public',
  ]
};

export function FilterList({ tags, categories, selectedTags, handleTagSelected, handleCategorySelected, handleTagDeselected }) {
  // Helper function to get tags for a specific language
  const getLanguageTags = (tags, language) => {
    const categoryList = LANGUAGE_CATEGORIES[language] || [];
    return tags.filter(tag => categoryList.includes(tag.tag_category));
  };

  // Get uncategorized tags
  const getUncategorizedTags = (tags) => {
    const allMappedCategories = [...LANGUAGE_CATEGORIES.en, ...LANGUAGE_CATEGORIES.fr];
    return tags.filter(tag => !allMappedCategories.includes(tag.tag_category));
  };

  // Create accordion panels for a specific set of tags
  const createAccordionPanels = (filteredTags) => {
    const distinctCategories = [...new Set(filteredTags.map(tag => tag.tag_category))].sort();
    
    return distinctCategories.map(category => {
      const categoryTags = filteredTags.filter(tag => tag.tag_category === category);
      const selectedCount = categoryTags.filter(tag => selectedTags.includes(tag.id)).length;
      const counter = selectedCount > 0 ? `(${selectedCount})` : '';
      
      return {
        title: { content: `${category} ${counter}`, icon: "dropdown" },
        content: {
          content: (
            <List>
              {categoryTags.map(tag => (
                <List.Item key={tag.id}>
                  <Checkbox
                    name={tag.name}
                    label={tag.name}
                    tag_id={tag.id}
                    onChange={handleTagSelected}
                    checked={selectedTags.includes(tag.id)}
                  />
                </List.Item>
              ))}
            </List>
          )
        }
      };
    });
  };

  if (tags.length === 0) {
    return (
      <React.Fragment>
        <Loader active inline />
        Loading Filters ...
      </React.Fragment>
    );
  }

  // Create tab panes
  const panes = [
    {
      menuItem: 'English',
      render: () => (
        <Tab.Pane>
          <Accordion
            defaultActiveIndex={[0]}
            panels={createAccordionPanels(getLanguageTags(tags, 'en'))}
            styled
            fluid
          />
        </Tab.Pane>
      )
    },
    {
      menuItem: 'Français',
      render: () => (
        <Tab.Pane>
          <Accordion
            defaultActiveIndex={[0]}
            panels={createAccordionPanels(getLanguageTags(tags, 'fr'))}
            styled
            fluid
          />
        </Tab.Pane>
      )
    }
  ];

  // Add Uncategorized tab only if there are uncategorized tags
  const uncategorizedTags = getUncategorizedTags(tags);
  if (uncategorizedTags.length > 0) {
    panes.push({
      menuItem: 'Uncategorized',
      render: () => (
        <Tab.Pane>
          <Accordion
            defaultActiveIndex={[0]}
            panels={createAccordionPanels(uncategorizedTags)}
            styled
            fluid
          />
        </Tab.Pane>
      )
    });
  }

  return (
    <Segment>
      <List className={styles.nonCenteredText}>
        <List.Header className={styles.centeredText}>
          <h3>Filters</h3>
        </List.Header>
        <List.Item className={styles.filterHeader}>
          {selectedTags.map(selectedTag => (
            <Label
              key={selectedTag}
              color='grey'
              className={styles.tagsLineHeight}
              tag_id={selectedTag}
              onClick={handleTagDeselected}
              tiny
              horizontal
            >
              {tags.find(tag => tag.id === selectedTag)?.name} &nbsp;
              <Icon name="x" color="yellow" />
            </Label>
          ))}
        </List.Item>
        <List.Item>
          <Tab panes={panes} />
        </List.Item>
      </List>
    </Segment>
  );
}

FilterList.propTypes = {
  tags: PropTypes.array,
  categories: PropTypes.array,
  selectedTags: PropTypes.array,
  handleTagSelected: PropTypes.func.isRequired,
  handleCategorySelected: PropTypes.func.isRequired,
  handleTagDeselected: PropTypes.func.isRequired,
};