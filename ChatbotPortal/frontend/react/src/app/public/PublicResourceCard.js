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
import {Card, Rating, Icon, Label, CardDescription} from "semantic-ui-react";
import {Link} from "react-router-dom";
import styles from './PublicResourceCard.css'
import FlagPopup from '../resource/FlagPopup';

export function PublicResourceCard({resource, locationPrefix, handleTagInCardsSelected, selectedTags=[], allTags, handleTagInCardsDeselected}) {
    return (
        <Card>
            <Card.Content className=" ui left aligned">
                <Card.Header>
                    {/* <Link to={location => ({...location, pathname: `${location.pathname}${locationPrefix}/${resource.id}`})}>
                        {resource.title}
                    </Link> */}
                    <a target="_blank" href={resource.url}>{resource.title}</a>
                    {/*<s className="ui seminvisiblee">{resource.score}</s>*/}
                </Card.Header>
                <Card.Meta className={styles.overflowText}>
                    {resource.description}
                </Card.Meta>
                <Card.Description>
                    {resource.phone_numbers ? (
                    <p><Icon color='grey' name="call" />&nbsp;&nbsp;
                    <a target="_blank" href={"tel:"+resource.phone_numbers} >
                        {resource.phone_numbers}
                    </a></p>
                    ) : null}
                    {resource.text_numbers  ? (
                        <p><Icon color='grey' name="text telephone"/>&nbsp;&nbsp;
                            {resource.text_numbers}
                        </p>
                    ) : null}
                    {resource.email  ? (
                        <p><Icon color='grey' name="mail"/>&nbsp;&nbsp;
                            <a target="_blank" href={"mailto:"+resource.email} >
                            {resource.email}
                    </a></p>
                    ) : null}
                    <Link target="_blank" to={location => ({...location, pathname: `${location.pathname}${locationPrefix}/${resource.id}`})}>
                        <p>More Detail</p>
                    </Link>

                    <Link target="_blank" to= {"/resource/"+resource.id}>
                        <p>Edit Resource</p>
                    </Link>

                    {   
                        resource.tags.map( tag => (allTags.filter(t=>(selectedTags.includes(t.id) && t.name == tag)).length > 0) ? 
                        (<Label color='grey' className={styles.tagsLineHeight} tag_name={tag} onClick={handleTagInCardsDeselected} tiny horizontal>{tag}&nbsp;<Icon name="x" color="yellow"></Icon></Label>) :
                        (<Label className={styles.tagsLineHeight} onClick={handleTagInCardsSelected} tag_name={tag} tiny horizontal>{tag}</Label>))
                    }
                    <div style={{float: "right"}}><FlagPopup resource_id={resource.id}></FlagPopup></div>
                </Card.Description>
            </Card.Content>
  

            {/* <Card.Content extra>
                {window.screen.width <= 767 ?
                    (
                        <Button.Group className="ui left floated">
                            {resource.url ? (<Button target="_blank" href={resource.url} as='a'><Icon fitted name="globe" /></Button>) : null}
                            {resource.email  ? (<Button target="_blank" href={"mailto:"+resource.email} as='a'> <Icon fitted name="mail" /></Button>) : null}
                        </Button.Group>    
                    ) : (
                        <Button.Group className="ui left floated">
                            {resource.url ? (<Button compact animated='fade' target="_blank" href={resource.url} as='a'> <Button.Content compact visible><Icon fitted name="globe" /> Resource URL</Button.Content><Button.Content compact hidden>Open URL</Button.Content></Button>) : null}
                            {resource.email  ? (<Button compact animated='fade' target="_blank" href={"mailto:"+resource.email} as='a'> <Button.Content compact visible><Icon fitted name="mail" /> Resource Email</Button.Content><Button.Content compact hidden>Send Email</Button.Content></Button>) : null}
                        </Button.Group>
                    )
                }
                
                {window.screen.width <= 767 ?
                    (
                        <Link className="ui right floated" to={location => ({...location, pathname: `${location.pathname}${locationPrefix}/${resource.id}`})}>
                            <Button color='blue'>Details</Button>
                        </Link>  
                    ) : (
                        <Link className="ui right floated" to={location => ({...location, pathname: `${location.pathname}${locationPrefix}/${resource.id}`})}>
                            <Button compact color='blue'>Details</Button>
                        </Link>
                    )
                }
                
            </Card.Content> */}
        </Card>
    );
}

PublicResourceCard.propTypes = {
    resource : PropTypes.object.isRequired,
    locationPrefix : PropTypes.string.isRequired,
};
