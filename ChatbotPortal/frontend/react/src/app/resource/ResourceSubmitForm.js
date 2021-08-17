/**
 * @file: ResourceSubmitForm.js
 * @summary: Component that allows user to inputs information to submit a resource (handle validations)
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

import React, {Component} from "react";
import axios from "axios";
import validator from "validator";
import {Container, Form, Header, Input, Message, Rating, Icon, Popup, Checkbox, Divider} from "semantic-ui-react";

import TagDropdown from "./TagDropdown";
import TitleDropdown from "./TitleDropdown";
import OrganizationNameDropdown from "./OrganizationNameDropdown";
import CategoryDropdown from './CategoryDropdown';
import HoursOfOperationWidget from "./HoursOfOperationWidget";
import ResourceTypeDropdown from './ResourceTypeDropdown';
import ResourceFormatDropdown from './ResourceFormatDropdown';
import {SecurityContext} from '../contexts/SecurityContext';
import styles from "./ResourceSubmitForm.css";
import ResourceSubmissionHelp from "./ResourceSubmissionHelp.js"

export default class ResourceSubmitForm extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            isFreeChecked: false,
            require_membership: false,
            title: "",
            informational_resource_text: "",
            resourceTypeIsInformative: false,
            organization_name: "",
            url: "",
            general_url: "",
            rating: 5,
            attachment: null,
            attachmentPath: "", // To clear the file after submitting it
            comments: "",
            definition: "",
            description: "",
            chatbot_text: "",
            email: "",
            phone_numbers: "",
            text_numbers: "",
            physical_address: "",
            distress_level_min: 1,
            distress_level_max: 1,
            resource_type: "SR",
            resource_format: "", //resource format = resource type in Front-End
            errors: {},
            category: 1,
            tags: [],
            langTags: [],
            url_validated: true,
            currentTags: null,
            submitted: 0,
            alwaysAvailable: true,
            hourBools : [
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
            ]
        };
        this.baseState = this.state;
    }

    create_resource = () => {
        // Get current logged in user
        let created_by_user = null;
        let created_by_user_pk = null;
        if (this.context.security.is_logged_in) {
            created_by_user = this.context.security.first_name;
            created_by_user_pk = this.context.security.id;
        }
        const resourceFormData = new FormData();

        resourceFormData.append("title", this.state.title);
        resourceFormData.append("informational_resource_text", this.state.informational_resource_text);
        resourceFormData.append("organization_name", this.state.organization_name);
        resourceFormData.append("url", this.state.url);
        resourceFormData.append("general_url", this.state.general_url);
        resourceFormData.append("rating", this.state.rating);
        resourceFormData.append("comments", this.state.comments);
        resourceFormData.append("created_by_user", created_by_user);
        resourceFormData.append("created_by_user_pk", created_by_user_pk);
        resourceFormData.append("category", this.state.category);
        resourceFormData.append("email", this.state.email);
        resourceFormData.append("definition", this.state.definition);
        resourceFormData.append("distress_level_min", this.state.distress_level_min);
        resourceFormData.append("distress_level_max", this.state.distress_level_max);
        resourceFormData.append("description", this.state.description);
        resourceFormData.append("chatbot_text", this.state.chatbot_text);
        resourceFormData.append("physical_address", this.state.physical_address);
        resourceFormData.append("resource_type", this.state.resource_type);
        resourceFormData.append("resource_format", this.state.resource_format);
        resourceFormData.append("phone_numbers", this.state.phone_numbers);
        resourceFormData.append("text_numbers", this.state.text_numbers);
        this.state.attachment !== null
            ? resourceFormData.append("attachment", this.state.attachment)
            : null;

        this.state.isFreeChecked
            ? resourceFormData.append("is_free", 1)
            : resourceFormData.append("is_free", 0);

        this.state.require_membership
            ? resourceFormData.append("require_membership", 1)
            : resourceFormData.append("require_membership", 0);

        // Submission for tags
        // Lists have to be submitted in a certain way in order for the server to recognize it
        if (this.state.tags && this.state.tags.length) {
            this.state.tags.forEach(value => {
                resourceFormData.append(`tags`, value);
            });
        }

        console.log(resourceFormData);

        //if we need to, deal with the hour bools
        if(!this.state.alwaysAvailable)
        {
            var hourstring = "";
            hourstring +="MON:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[0][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="TUE:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[1][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="WED:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[2][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="THU:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[3][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="FRI:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[4][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="SAT:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[5][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="SUN:";
            for(var i = 0; i < 24; i++)
                if(this.state.hourBools[6][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            resourceFormData.append(`hours_of_operation`, hourstring);
        }

        return resourceFormData;
    };

    post_resource = () => {
        const resourceFormData = this.create_resource();
        // let submitted = 1;

        axios
            .post("/chatbotportal/resource/", resourceFormData, {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(() => {
                this.set_submitted_state(1, "POST SUCESS");
            })
            .catch(error => {
                console.error(error.response);
                var errors = Object.keys(error.response.data).map(function (key) { 
                    return " " + error.response.data[key]; 
                  });
                this.set_submitted_state(-1, errors);
            });

    };

    set_submitted_state = (submitted_value, submitted_error) => {
        console.log(this.state, submitted_value)
        if (submitted_value === 1) {
            this.update_user_submissions();
            this.setState({submitted: submitted_value}, () => {
                setTimeout(() => {
                    this.setState(this.baseState);
                    setTimeout(()=>{
                        window.location.reload(false);
                    }, 900);
                }, 2500);
            });
        }else {
            this.setState({submitted: submitted_value, errors: submitted_error});
        }
        console.log(submitted_error);
    };

    update_user_submissions = () => {
        axios
            .put(`/chatbotportal/authentication/${this.context.security.id}/update/submissions/`, '', {
                headers: { 'Authorization': `Bearer ${this.context.security.token}` }
            })
            .then(
                () => {},
                error => {
                    console.log(error);
                }
            );
    };

    handleRate = (event, data) => {
        this.setState({rating: data.rating});
    };

    handleChange = event => {
        this.setState({[event.target.name]: event.target.value});
    };

    handleChangeResURL = event => {
        var baseUrl='';
        try{
            const urlOne = new URL(this.state.general_url);
            baseUrl = urlOne.origin;
        }catch(e){
            baseUrl = "";
        }
        
        if(baseUrl!=''){this.setState({url:baseUrl});}
        this.setState({general_url:event.target.value})
    };

    // event.target.value holds the pathname of a file
    handleFileChange = event => {
        this.setState({
            [event.nativeEvent.target.name]: event.nativeEvent.target.files[0],
            attachmentPath: event.nativeEvent.target.value
        });
    };

    addFieldTag(tagName){

        var fetchURL = "/chatbotportal/resource/fetch-tags-by-cat"
        var keyDict = {
            params: {
                name: tagName,
                tag_category: "Resource Format"
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
                let tags = [];
                if (response.data) {
                    tags = response.data.map(tag => (tag.id));
                }

                // Add any options that didn't come back from the server, but are selected
                if (this.state.tags) {
                    for (const selectedOption of this.state.tags) {
                        if (
                            tags.find(
                                tags => tags === selectedOption
                            ) === undefined
                        ) {
                            tags.push(selectedOption);
                        }
                    }
                }
                this.setState({tags});
            });

    }

    handleSubmit = event => {

        if(document.activeElement.getAttribute('name')!="submit")
        {
            this.setState({});
            return;
        } 

        //add field tags
        if(this.state.phone_numbers!= "") this.addFieldTag("Phone Number")
        if(this.state.text_numbers!= "") this.addFieldTag("Text Messaging")
        if(this.state.url!= "" || this.state.general_url!= "") this.addFieldTag("Website")
        if(this.state.definition!= "") this.addFieldTag("Definition/Stat")
        if(this.state.email!= "") this.addFieldTag("Email")

        //check field states before submitting
        // if(this.state.rating == 0)
        // {
        //     this.setState({submitted: -1, errors: "Please rate your resource usefulness."});
        //     return;
        // }
        if(this.state.tags.length<1||this.state.langTags.length<1)
        {
            this.setState({submitted: -1, errors: "Please enter at a language tag and at least one other tag."});
            return;
        }
        var localTags = this.state.tags;
        if (localTags) {
            for (const langtags of this.state.langTags) {
                if (
                    localTags.find(
                        localTags => localTags === langtags
                    ) === undefined
                ) {
                    localTags.push(langtags);
                }
            }
        }
        this.setState({tags: localTags});
        this.post_resource();
        event.preventDefault();
    };
    
    handleIsFreeCheckbox = () => {
        this.setState({isFreeChecked: !this.state.isFreeChecked})
    };

    handleReqMemCheckbox = () => {
        this.setState({require_membership: !this.state.require_membership})
    };

    handleResTypeChange = (resource_type) => {
        this.setState({ resource_type })
        if(resource_type != "SR"){
            this.setState({resourceTypeIsInformative: true});
        }else{
            this.setState({resourceTypeIsInformative: false});
            this.setState({informational_resource_text: ""});
        }
    }

    handleResFormatChange = (resource_format) => {
        this.setState({ resource_format })
    }

    toggle = () => this.setState((prevState) => ({ alwaysAvailable: !prevState.alwaysAvailable }))

    render() {

        var dateTabs=null;
        if(!this.state.alwaysAvailable)
        {
            dateTabs = <HoursOfOperationWidget hourBools={this.state.hourBools}/>
        }

        var dateTabs=null;
        if(!this.state.alwaysAvailable)
        {
            dateTabs = <HoursOfOperationWidget hourBools={this.state.hourBools}/>
        }

        return (
            <div style={{ paddingTop: "3%", paddingLeft: "10%", paddingRight: "10%", paddingBottom: "3%" }}>
                <SecurityContext.Consumer>
                    {securityContext => (
                        <Container vertical>
                            <Header
                                as="h3"
                                style={{
                                    fontSize: "2em"
                                }}
                                color="blue"
                            >
                                Resource Submission {/*<ResourceSubmissionHelp style={{display:'inline-block'}} trigger={
                                    (<Icon name='question circle'/>)
                                }/>*/}
                            </Header>
                            <Form onSubmit={this.handleSubmit} success error>
                                
                                {securityContext.security.is_logged_in ? (
                                    <div>
                                        {/*<Form.Input
                                                fluid
                                                required
                                                name="title"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.title}
                                                label="Resource Title"
                                                placeholder="title"
                                        />-->*/}
                                        <Form.Field>
                                            <label>Resource Title &nbsp;&nbsp;&nbsp;(Format: [name of organization][type of resource] - Example: Crisis Services Canada PhoneLine)</label>
                                            <TitleDropdown
                                                required
                                                name="title"
                                                value={this.state.title}
                                                label="Title"
                                                onChange={title => this.setState({ title })}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Name of Company or Organization Providing Resource &nbsp;&nbsp;&nbsp;(Example: Crisis Services Canada)</label>
                                            <OrganizationNameDropdown
                                                required
                                                name="organization_name"
                                                value={this.state.organization_name}
                                                label="Company or Organization name"
                                                onChange={organization_name => this.setState({ organization_name })}
                                                organization_description = {description => this.setState({ description })} 
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Brief description of the company or organization &nbsp;&nbsp;&nbsp;(up to 3 sentences.) <Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.TextArea
                                                name="description"
                                                onChange={this.handleChange}
                                                value={this.state.description}
                                                placeholder="Enter Company or Organization Description"
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Brief description of the service the resource provides &nbsp;&nbsp;&nbsp;(up to 3 sentences.) <Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.TextArea
                                                name="definition"
                                                onChange={this.handleChange}
                                                value={this.state.definition}
                                                placeholder="Enter Service Description."
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Source URL &nbsp;&nbsp;&nbsp;(Example: https://mdsc.ca/resources/56)<Popup content='URL pointing to where the resource was obtained from.' trigger={<Icon name='question circle'/>}/><Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="general_url"
                                                onChange={this.handleChangeResURL}
                                                onBlur={this.handleChangeResURL}
                                                width={16}
                                                value={this.state.general_url}
                                                placeholder="https://"
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Homepage URL &nbsp;&nbsp;&nbsp;(Example: https://mdsc.ca) <Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="url"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.url}
                                                placeholder="https://"
                                            />
                                        </Form.Field>

                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Is this service free?</label>
                                            <Checkbox
                                                name="is_free"
                                                label='Service is free'
                                                onChange={this.handleIsFreeCheckbox}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Does this resource/service require membership?</label>
                                            <Checkbox
                                                name="require_membership"
                                                label='This requires membership of some kind.'
                                                onChange={this.handleReqMemCheckbox}
                                            />
                                        </Form.Field>
                                        <Divider hidden />

                                        <Form.Field>
                                            <label>Resource Category <Popup content='Indicate if this resource is primarily a service, informational, or both.' trigger={<Icon name='question circle'/>}/></label>
                                            <ResourceTypeDropdown
                                                required
                                                value={this.state.resource_type}
                                                onChange={this.handleResTypeChange}
                                            />
                                        </Form.Field>

                                        <Form.Field>
                                            <label>Resource Type </label>
                                            <ResourceFormatDropdown
                                                required
                                                is_informational={this.state.resource_type}
                                                onChange={this.handleResFormatChange}
                                                value={this.state.resource_format}
                                            />
                                        </Form.Field>
                                        {(() => {
                                                if (this.state.resourceTypeIsInformative)
                                                    return (
                                                            <Form.Field>
                                                                <Form.TextArea
                                                                    name="informational_resource_text"
                                                                    onChange={this.handleChange}
                                                                    value={this.state.informational_resource_text}
                                                                    label="Informational Resource Text &nbsp;&nbsp;&nbsp;(example a definition or statistical information)"
                                                                    rows={2}
                                                                />  
                                                            </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                            })()}
                                        <Form.Field>
                                            <label>Resource Format <Popup content='Select the format this resource primarily falls under.' trigger={<Icon name='question circle'/>}/></label>
                                            <CategoryDropdown
                                                required
                                                value={this.state.category}
                                                onChange={category => this.setState({ category })}
                                            />
                                        </Form.Field>
                                        {/* <Form.Field>
                                            <label>Resource Usefulness Rating <Popup content='Rate the resource based on how useful you feel it is in general.' trigger={<Icon name='question circle'/>}/></label>
                                            <Rating
                                                name="rating"
                                                onRate={this.handleRate}
                                                onChange={this.handleChange}
                                                value={this.state.rating}
                                                defaultRating={0}
                                                maxRating={5}
                                                icon="star"
                                                size="massive"
                                            />
                                        </Form.Field> */}
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Age Tags <Popup content='Age groups tags to indicate who this resource might apply to.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Age Group"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Location Tags <Popup content='Locations/regions for physical/location relevent resources.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Locations"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Health Issue Tags <Popup content='Tags for any mental health issues this resource addresses, defines, etc.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Health Issue Group"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Language Tags <Popup content='Languages this resource is written/available in.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="langTags"
                                                    value={this.state.langTags}
                                                    tagCat="Language"
                                                    onChange={langTags => this.setState({ langTags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Other Tags <Popup content='For anything that might not fall under the other categories such as services provided, relevent gender groups, organizations, user groups, etc.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Minimum Distress Level(1-10) <Popup content='The lowest distress level this resource is relevent at. (1-Not distressed, 10-Extremely distressed)' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Input
                                                fluid
                                                required
                                                name="distress_level_min"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.distress_level_min}
                                                placeholder="1-10"
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Maximum Distress Level(1-10) <Popup content='The highest distress level this resource is relevent at. (1-Not distressed, 10-Extremely distressed)' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Input
                                                fluid
                                                required
                                                name="distress_level_max"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.distress_level_max}
                                                placeholder="1-10"
                                            />
                                        </Form.Field>
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Resource Email Address, &nbsp;&nbsp;&nbsp;if applicable (Example: j.m.nobel@ualberta.ca)<Popup content='this field is optional' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="email"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.email}
                                                placeholder="Enter Email (OPTIONAL)"
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Phone Number(s), &nbsp;&nbsp;&nbsp;if applicable (Example: 1234;...;)<Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="phone_numbers"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.phone_numbers}
                                                placeholder="Enter Phone Numbers (OPTIONAL)"
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Text Number(s), &nbsp;&nbsp;&nbsp;if applicable (Format: enter either just the text number, or include instructions if applicable - Example: text "help" to 1234;...;) <Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="text_numbers"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.text_numbers}
                                                placeholder='Enter Text Numbers (OPTIONAL)'
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Physical Address, &nbsp;&nbsp;&nbsp;FILL ONLY if services are in person (Example: 123 Jasper Avenue, Edmonton, AB, T4F 1A9, Canada)<Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                            fluid
                                            name="physical_address"
                                            onChange={this.handleChange}
                                            width={16}
                                            value={this.state.physical_address}
                                            placeholder="Enter Address (OPTIONAL)"
                                        />
                                        </Form.Field>
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Resource Availability <Popup content='If the resource is not always available, uncheck this and fill in the times below.' trigger={<Icon name='question circle'/>}/></label>
                                            <Checkbox
                                                label='Resource Available 24/7'
                                                onChange={this.toggle}
                                                checked={this.state.alwaysAvailable}
                                            />
                                        </Form.Field>
                                        {dateTabs}
                                        <Divider hidden />
                                        <Form.Field>
                                            <Form.TextArea
                                                name="chatbot_text"
                                                onChange={this.handleChange}
                                                value={this.state.chatbot_text}
                                                label="Chatbot Text"
                                                placeholder="Enter what the chatbot should say about this resource."
                                                rows={2}
                                            />  
                                        </Form.Field>
                                        <Form.Field>
                                            <Form.TextArea
                                                name="comments"
                                                onChange={this.handleChange}
                                                value={this.state.comments}
                                                label="Comments"
                                                placeholder="Enter any comments (Optional)"
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Upload an attachment</label>
                                            <Input
                                                type="file"
                                                name="attachment"
                                                value={this.state.attachmentPath}
                                                onChange={this.handleFileChange}
                                            />
                                        </Form.Field>

                                        <div>
                                            {(() => {
                                                if (this.state.submitted === 1)
                                                    return (
                                                        <Message success header="Submit success">
                                                            <Message.Content name="submit_success">
                                                                Thanks! Your resource has been submitted for review.
                                                            </Message.Content>
                                                        </Message>
                                                    );
                                                else if (this.state.submitted === -1)
                                                    return (
                                                        <Message
                                                            error header="Submit failure">
                                                            <Message.Content name="submit_failure">
                                                                Something went wrong! Your resource
                                                                was not submitted. {this.state.errors}
                                                            </Message.Content>
                                                        </Message>
                                                    );
                                                else return <div />;
                                            })()}
                                        </div>

                                        <Form.Button name="submit" content="Submit" color="green" />
                                    </div>
                                ) : null}
                            </Form>
                        </Container>
                    )}
                </SecurityContext.Consumer>
            </div>
        );
    }
}
