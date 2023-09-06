/**
 * @file: ResourceTable.js
 * @summary: Component that renders a list of public resources
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
import {Card, Rating, Loader} from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import {PublicResourceCard} from "./PublicResourceCard";

export function ResourceTable({resources, loadingResources, handleTagInCardsSelected, selectedTags, allTags, handleTagInCardsDeselected, isEditor}) {
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
            [<h3>No resources found. Try a different query?</h3>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>
            ,<br/>]
        );
    } else {
        // CASE 3
        return (
            <React.Fragment>
                <Card.Group itemsPerRow="1" stackable>
                    {resources.map(resource => (
                        <PublicResourceCard resource={resource} handleTagInCardsSelected={handleTagInCardsSelected} selectedTags={selectedTags} allTags={allTags} 
                        handleTagInCardsDeselected={handleTagInCardsDeselected} isEditor={isEditor}
                        locationPrefix="/detail" />
                    ))}
                </Card.Group>
            </React.Fragment>
        );
    }
}