/**
 * @file: ResourceSubmissionHelp.js
 * @summary: Help page with picture and text for resource submission specifically
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
import React, { Component } from 'react'
import {Header, Modal, Image} from "semantic-ui-react";

export class ResourceSubmissionHelp extends Component {
    render() {

        const show_image_text = (image, text) =>{
            return (
                <div>
                    <Image size='big' src={require({image})} ui wrapped />
                    <p>
                        {text}
                    </p>
                </div>
            )
        }
        const show_image_text = (image, text) =>{
            return (
                <Image size='big' src={require("./help_medias/1_search_resource.ico")} ui wrapped />
                <p>
                    
                </p>
            )
        }
        return (
            <Modal trigger={this.props.trigger} closeIcon>
                <Modal.Header>Resource Submission Help</Modal.Header>
                <Modal.Content image scrolling>
                    <Modal.Description>
                        <Header>Url input</Header>
                        {this.show_image_text("./help_medias/1_search_resource.ico", "In order to input a url, you must search for a resource. This example searches Google for 'adhd resources'")}
                        {this.show_image_text("./help_medias/1_search_resource.ico", "If you found a resource you like, you can click on it to go to that resource")}
                        {this.show_image_text("./help_medias/1_search_resource.ico", "Double click on the url to select all")}
                        {this.show_image_text("./help_medias/1_search_resource.ico", "Right click and select copy")}
                        {this.show_image_text("./help_medias/1_search_resource.ico", "Go back to your Resource Submission tab, Right click and select paste to paste the url into the input field")}

                    </Modal.Description>

                </Modal.Content>
                
            </Modal>
                
        )
    }
}

export default ResourceSubmissionHelp
