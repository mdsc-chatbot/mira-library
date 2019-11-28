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
import {Header, Modal, Image, Divider} from "semantic-ui-react";

export class ResourceSubmissionHelp extends Component {
    render() {

        const show_image_text = (image, text) =>{
            return (
                <div>
                    {image}
                    <br/>
                    <p style={{color:"gray", fontSize:14}}>
                        {text}
                    </p>
                    <br/>
                </div>
            )
        }
        
        return (
            <Modal trigger={this.props.trigger} closeIcon size='small'>
                <Modal.Header>Resource Submission Help</Modal.Header>
                <Modal.Content image>
                    <Modal.Description>
                        
                        <Header dividing>Resource url input</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/1_search_resource.ico")} ui wrapped />
                        , "In order to input a url, you must search for a resource. This example searches Google for 'adhd resources'")}
                        {show_image_text(<Image size='big' src={require("./help_medias/2_goto_resource.ico")} ui wrapped />
                        , "If you found a resource you like, you can click on it to go to that resource")}
                        {show_image_text(<Image size='big' src={require("./help_medias/3_select_resource_url.ico")} ui wrapped />
                        , "Double click on the url to select all")}
                        {show_image_text(<Image size='big' src={require("./help_medias/4_copy_resource.ico")} ui wrapped />
                        , "Right click and select copy")}
                        {show_image_text(<Image size='big' src={require("./help_medias/5_paste_resource.ico")} ui wrapped />
                        , "Go back to your Resource Submission tab, Right click and select paste to paste the url into the input field")}
                        
                        <Header dividing>Resource usefulness input</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/7_resource_usefulness_rating.ico")} ui wrapped />
                        , "After the resource url is pasted, you can click on the stars to rate how useful the resource was to you")}
                        
                        <Header dividing>Resource category input</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/8_resource_category.ico")} ui wrapped />
                        , "You can click on the drop down to select the category or type of that resource")}
                        
                        <Header dividing>Resource tags input</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/9_resource_tag2.ico")} ui wrapped />
                        , "To search for tag, you can type in the tag you're looking for")}
                        {show_image_text(<Image size='big' src={require("./help_medias/9_resource_tag3.ico")} ui wrapped />
                        , "And click on the tag or hit Enter to select that tag")}

                        <Header dividing>Resource comment input</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/10_resource_comment.ico")} ui wrapped />
                        , "You can input a comment on how useful the resource was to you and how you think it will help others")}
                        
                        <Header dividing>Resource upload attachment</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/13_upload_attachment.ico")} ui wrapped />
                        , "Optionally, you can upload a pdf attachment related to the resource")}
                        
                        <Header dividing>Resource submission notice</Header>
                        {show_image_text(<Image size='big' src={require("./help_medias/11_resource_submit_successful.ico")} ui wrapped />
                        , "You can click on the submit button to submit the resource, a green notice should pop up ")}
                        {show_image_text(<Image size='big' src={require("./help_medias/12_resource_submit_unsuccessful.ico")} ui wrapped />
                        , "If you encounter an red error notice, check if you've entered the right url, or contact us for more information")}


                    </Modal.Description>

                </Modal.Content>
                
            </Modal>
                
        )
    }
}

export default ResourceSubmissionHelp
