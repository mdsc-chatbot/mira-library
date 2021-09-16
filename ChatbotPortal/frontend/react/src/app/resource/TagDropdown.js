/**
 * @file: TagsDropDown.js
 * @summary: Component that allows user to search and input tags in ResourceSubmitForm.js
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
import PropTypes from 'prop-types';
import axios, {CancelToken} from 'axios';
import {Dropdown, Responsive, Segment, SegmentGroup} from 'semantic-ui-react';
import TagPopup from "./TagPopup";
import {SecurityContext} from "../contexts/SecurityContext";


export default class TagDropdown extends React.Component {
    static contextType = SecurityContext;

    static mapResponseToDropdownOption = tag => ({
        key: tag.id,
        text: tag.name,
        value: tag.id
    });

    constructor(props) {
        super(props);

        this.state = {
            searchQuery: ' ',
            tagOptions: [], // options to show to user (to click)
            selectedOptions: [], // selected options so that the current values don't 'disappear' in the UI
            searchRequestCancelToken: null,
        };
        this.tagCat = props.tagCat;
    }

    handleChange = (event, data) => {
        // Change value
        this.props.onChange(data.value);

        this.setState({
            searchQuery: ''
        });

        // Find out if the newest value was selected/unselected
        // If selected, add the selected option to selectedOptions
        // If unselected, remove the selected option in selectedOptions
        // This is to make sure the UI is consistent.
        // First, find the selected option using the text of the dropdown
        const selectedText = event.target.textContent;
        const selectedOption = data.options.find(option => option.text === selectedText);

        if (selectedOption !== undefined) {
            // Selected
            const newSelectedOptions = this.state.selectedOptions.slice();
            newSelectedOptions.push(selectedOption);
            this.setState({selectedOptions: newSelectedOptions})
            this.checkTagRelatedBooleans(selectedText);
        } else {
            // Unselected
            const indexOfSelectedOption = this.state.selectedOptions.find(option => option.text === selectedText);
            const newSelectedOptions = this.state.selectedOptions.slice();
            newSelectedOptions.splice(indexOfSelectedOption, 1);
            this.setState({selectedOptions: newSelectedOptions})
        }
    };

    handleSearchChange = (event, {searchQuery}) => {
        // Cancel previous search requests if possible
        if (this.state.searchRequestCancelToken) {
            this.state.searchRequestCancelToken.cancel()
        }

        // Prepare for promise cancellation
        const source = CancelToken.source();


        var keyDict;
        var fetchURL;
        if(this.tagCat == null)
        {
            fetchURL = "/chatbotportal/resource/fetch-tags"
            keyDict = {
                params: {
                    name: searchQuery
                },
                cancelToken: source.token
            }
        }
        else
        {
            fetchURL = "/chatbotportal/resource/fetch-tags-by-cat"
            keyDict = {
                params: {
                    name: searchQuery,
                    tag_category: this.tagCat
                },
                cancelToken: source.token
            }
        }
        

        // Fetch search results
        axios
            .get(
                fetchURL,
                keyDict,
                {
                    headers: {Authorization: `Bearer ${this.context.security.token}`}
                }
            )
            .then(response => {
                // Transform JSON tag into tag that semantic ui's dropdown can read
                let tagOptions = [];
                if (response.data) {
                    tagOptions = response.data.map(TagDropdown.mapResponseToDropdownOption);
                }

                // Add any options that didn't come back from the server, but is selected in the dropdown
                // This makes sure that the value is rendered properly in the UI
                if (this.state.selectedOptions) {
                    for (const selectedOption of this.state.selectedOptions) {
                        if (
                            tagOptions.find(
                                tagOption => tagOption.value === selectedOption.value
                            ) === undefined
                        ) {
                            tagOptions.push(selectedOption);
                        }
                    }
                }

                this.setState({
                    tagOptions
                });
            });

        this.setState({
            searchQuery: searchQuery,
            searchRequestCancelToken: source
        })
    };

    handleNewTagAdded = (tag) => {
        // Adding new tag to values
        const value = this.props.value.slice();
        value.push(tag.id);
        this.props.onChange(value);

        // Adding tag to selected options
        this.setState((prevState) => {
            const selectedOptions = prevState.selectedOptions.slice();
            selectedOptions.push(TagDropdown.mapResponseToDropdownOption(tag));
            const tagOptions = prevState.tagOptions.slice();
            tagOptions.push(TagDropdown.mapResponseToDropdownOption(tag));
            return {
                selectedOptions,
                tagOptions
            };
        });
    };

    checkTagRelatedBooleans = (tagName) => {
        if(tagName.toLowerCase().includes('email')){
            this.props.isRelatedToEmail('true');
            console.log('related to email', this.props);
        }else if(tagName.toLowerCase().includes('physical address')){
            this.props.isRelatedToAddress('true');
            console.log('related to address', this.props);
        }else if(tagName.toLowerCase().includes('phone number')){
            this.props.isRelatedToPhonenumber('true');
            console.log('related to Phone number', this.props);
        }else if(tagName.toLowerCase().includes('text message number')){
            this.props.isRelatedToEmail('true');
            console.log('related to text message number', this.props);
        }
    }

    componentDidUpdate(prevProps){
        if(this.props.initValue != prevProps.initValue){
            this.getAllTags();
        }
    }

    componentDidMount(prevProps){
        // fill the options so it is not empty when users clicks on it.
        this.handleSearchChange(null, {searchQuery:''})
    }

    getAllTags(){
         // Prepare for promise cancellation
         const source = CancelToken.source();
         var keyDict= {
            params: {
                name: ''
            },
            cancelToken: source.token
        };
        var fetchURL =  "/chatbotportal/resource/fetch-tags";

        axios
            .get(
                fetchURL,
                keyDict,
                {
                    headers: {Authorization: `Bearer ${this.context.security.token}`}
                }
            )
            .then(response => {
                // Transform JSON tag into tag that semantic ui's dropdown can read
                let allTags = [];
                if (response.data) {
                    console.log('getAllTags', response.data);
                    allTags = response.data;
                    const initValuePairs = allTags.filter(tagOption => this.props.initValue.includes(tagOption.name));
                    console.log('initValuePairs',initValuePairs);
                    if(initValuePairs.length>0){
                        initValuePairs.forEach(initValuePair=>this.handleNewTagAdded(initValuePair)) 
                    }
                }
            });
    }


    render() {
        return (
            <React.Fragment>
                <SegmentGroup size={"mini"} style={{width: "100%"}} compact horizontal>
                        <Segment style={{width: "100%"}}>
                            <Dropdown
                                spellcheck='true'
                                fluid
                                multiple
                                onChange={this.handleChange}
                                onSearchChange={this.handleSearchChange}
                                options={this.state.tagOptions}
                                placeholder='Enter tags'
                                search
                                searchQuery={this.state.searchQuery}
                                selection
                                value={this.props.value}
                            />
                        </Segment>
                        <Segment>
                            <TagPopup onNewTag={this.handleNewTagAdded}/>
                        </Segment>
                </SegmentGroup>
            </React.Fragment>
        );
    }
}

TagDropdown.propTypes = {
    value: PropTypes.array,
    initValue: PropTypes.array,
    onChange: PropTypes.func,
    tagCat: PropTypes.string
};