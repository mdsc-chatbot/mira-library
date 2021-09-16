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
import { Slider } from "react-semantic-ui-range";
import {Container, Form, Header, Input, Message, Icon, Popup, Checkbox, Divider, Rating} from "semantic-ui-react";
import TagDropdown from "./TagDropdown";
import TitleDropdown from "./TitleDropdown";
import OrganizationNameDropdown from "./OrganizationNameDropdown";
import CategoryDropdown from './CategoryDropdown';
import HoursOfOperationWidget from "./HoursOfOperationWidget";
import ResourceTypeDropdown from './ResourceTypeDropdown';
import ResourceFormatDropdown from './ResourceFormatDropdown';
import {SecurityContext} from '../contexts/SecurityContext';
import styles from "./ResourceSubmitForm.css";

export default class ResourceSubmitForm extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            resourceTypeRelateTextnumber: false,
            resourceTypeRelateEmail: false,
            resourceTypeRelatePhonenumber: false,
            resourceTypeRelateAddress: false,
            ageArray: [0,110],
            resourceId: null,
            title: "",
            catText: "",
            tagInitValue: "",
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
            email: "",
            phone_numbers: "",
            text_numbers: "",
            physical_address: "",
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

    settings = {
        start: [2,30],
        min: 0,
        max: 120,
        step: 1,
        onChange: value => {
            this.setState({ageArray:value});
        }
    };

    get_resource_details = (resourceID) => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}`, {headers: options})
            .then(res => {
                console.log('I got resources', res.data)
                if(res.data.resource_type != "SR"){
                    this.setState({resourceTypeIsInformative: true});
                }else{
                    this.setState({resourceTypeIsInformative: false});
                }
                this.setState({resource_type:res.data.resource_type}); 
                this.setState({title:res.data.title});
                this.setState({informational_resource_text:res.data.informational_resource_text});
                this.setState({organization_name:res.data.organization_name});
                this.setState({url:res.data.url});
                this.setState({general_url:res.data.general_url});
                this.setState({rating:res.data.rating});
                this.setState({comments:res.data.comments});
                this.setState({definition:res.data.definition});
                this.setState({description:res.data.description});

                res.data.email &&
                this.setState({resourceTypeRelateEmail:true}) &&
                this.setState({email:res.data.email});

                res.data.phone_numbers &&
                this.setState({resourceTypeRelatePhonenumber:true}) &&
                this.setState({phone_numbers:res.data.phone_numbers});

                res.data.text_numbers &&
                this.setState({resourceTypeRelateTextnumber:true}) &&
                this.setState({text_numbers:res.data.text_numbers});

                res.data.physical_address && 
                this.setState({resourceTypeRelateAddress:true}) &&
                this.setState({physical_address:res.data.physical_address});

                this.setState({resource_format:res.data.resource_format});
                this.setState({catText:res.data.category});
                this.setState({tagInitValue:res.data.tags});
                this.setState({hours_of_operation:res.data.hours_of_operation});
                this.setState({ageArray:[res.data.min_age, res.max_age]});
                if(res.data.hours_of_operation!=null){
                    this.setState({alwaysAvailable:false});
                    this.decodeHours(res.data.hours_of_operation);
                }
                // let submit btn know we are in edit mode
                this.setState({resourceId:resourceID});
            });
    };

    componentDidMount(){
        //check if resource id is in url to know if we come to form for editing the resource or not
        const resourceId = this.props.location.search ? this.props.location.search.substring(4) : '';
        if(resourceId != '') this.get_resource_details(resourceId);
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
        resourceFormData.append("description", this.state.description);
        resourceFormData.append("physical_address", this.state.physical_address);
        resourceFormData.append("resource_type", this.state.resource_type);
        resourceFormData.append("resource_format", this.state.resource_format);
        resourceFormData.append("phone_numbers", this.state.phone_numbers);
        resourceFormData.append("text_numbers", this.state.text_numbers);
        resourceFormData.append("min_age", this.state.ageArray[0]);
        resourceFormData.append("max_age", this.state.ageArray[1]);
        this.state.attachment !== null
            ? resourceFormData.append("attachment", this.state.attachment)
            : null;

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

        console.log('inja' , resourceFormData);

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

    //get string from db and represent it in the hour selection buttons
    decodeHours = (hoursFromDB) => {
        console.log('hoursFromDB', hoursFromDB);
        var weekIndex ;    
        var newHourBools = this.state.hourBools;
        var dayArray = hoursFromDB.split(';');
        dayArray.forEach((day, index) => {
            if(day==''){
                return;
            }
            switch (dayArray[index].substring(0,3)) {
                case "MON":
                    weekIndex=0
                    break;
                case "TUE":
                    weekIndex=1
                    break;
                case "WED":
                    weekIndex=2
                    break;
                case "THU":
                    weekIndex=3
                    break;
                case "FRI":
                    weekIndex=4
                    break;
                case "SAT":
                    weekIndex=5
                    break;
                case "SUN":
                    weekIndex=6
                    break;
            }
            const hourArray = day.substring(4).split(',');
            hourArray.forEach(hour => {
                if(hour==''){
                    return;
                }
                newHourBools[weekIndex][hour-1] = true;
            });
        });

        console.log('new bool', newHourBools);
        this.setState({hourBools:newHourBools});
    }

    encodeHours = (hoursBool) => {
            var hourstring = "";
            hourstring +="MON:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[0][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="TUE:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[1][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="WED:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[2][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="THU:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[3][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="FRI:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[4][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="SAT:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[5][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";
            hourstring +="SUN:";
            for(var i = 0; i < 24; i++)
                if(hoursBool[6][i]) hourstring += (i+1).toString() + ",";
            hourstring +=";";

            return hourstring;
    }

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

        if(this.state.resourceId !== null){
            this.update_resource_user();
            return;
        }

        //add field tags
        if(this.state.phone_numbers!= "") this.addFieldTag("Phone Number")
        if(this.state.text_numbers!= "") this.addFieldTag("Text Messaging")
        if(this.state.url!= "" || this.state.general_url!= "") this.addFieldTag("Website")
        if(this.state.definition!= "") this.addFieldTag("Definition/Stat")
        if(this.state.email!= "") this.addFieldTag("Email")

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

    update_resource_user = () => {

        var submitCmd = { 
            'title':this.state.title,
            'url':this.state.url,
            'rating':this.state.rating,
            'comments': this.state.comments,
            'category_id': this.state.category,
            'definition': this.state.definition,
            'email' : this.state.email,
            'phone_numbers' : this.state.phone_numbers,
            'refrences' : this.state.refrences,
            'resource_type' : this.state.resource_type,
            'description' : this.state.description,
            'general_url' : this.state.general_url,
            'physical_address' : this.state.physical_address,
            'hours_of_operation' : this.encodeHours(this.state.hourBools),
            'min_age' : this.state.ageArray[0],
            'max_age' : this.state.ageArray[1],
            'organization_name' : this.state.organization_name,
            'informational_resource_text' : this.state.informational_resource_text,
            'resource_format' : this.state.resource_format,
            // 'attachment' : this.state.attachment ? this.state.attachment : '',
        };

        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };

        // Resource
        axios
            .put(
                "/chatbotportal/resource/" + this.state.resourceId + "/updatepartial/",
                submitCmd,
                {headers: options}
            ).then(
                response => {
                    setTimeout(() => {
                        // this.setState(this.baseState);
                        setTimeout(()=>{
                            var url = window.location.origin + '/chatbotportal/app/resource';
                            window.location.href = url;
                        }, 900);
                    }, 1000);
                },
                error => {
                    console.log('error', error);
                }
            );
    };

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
                                        <Form.Field>
                                            <label>Resource Title <Popup content='(Format: [name of organization][type of resource] - Example: Crisis Services Canada PhoneLine)' trigger={<Icon name='question circle'/>}/></label>
                                            <TitleDropdown
                                                required
                                                name="title"
                                                value={this.state.title}
                                                label="Title"
                                                onChange={title => this.setState({ title })}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Name of Company or Organization Providing Resource <Popup content='(Example: Crisis Services Canada)' trigger={<Icon name='question circle'/>}/></label>
                                            <OrganizationNameDropdown
                                                required
                                                name="organization_name"
                                                value={this.state.organization_name}
                                                label="Enter Company or Organization name"
                                                onChange={organization_name => this.setState({ organization_name })}
                                                organization_description = {description => this.setState({ description })} 
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Brief description of the company or organization &nbsp;(up to 3 sentences). </label>
                                            <Form.TextArea
                                                required
                                                spellcheck='true'
                                                name="description"
                                                onChange={this.handleChange}
                                                value={this.state.description}
                                                placeholder="Enter Company or Organization Description"
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Brief description of the service the resource provides &nbsp;(up to 3 sentences).</label>
                                            <Form.TextArea
                                                name="definition"
                                                onChange={this.handleChange}
                                                value={this.state.definition}
                                                placeholder="Enter Service Description."
                                                rows={2}
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
                                            <label>Resource Types </label>
                                            {(() => {
                                                if (this.state.resource_type != 'RS')
                                                    return (
                                                            <Form.Field>
                                                                <label>I) Resource Type for Programs and Services</label>
                                                                <Form.Group className={styles.dropdownPadding}>
                                                                    <TagDropdown
                                                                        required
                                                                        name="tags"
                                                                        value={this.state.tags}
                                                                        tagCat="Resource Type for Programs and Services"
                                                                        onChange={tags => this.setState({ tags })}
                                                                    />
                                                                </Form.Group>  
                                                            </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                            })()}
                                            {(() => {
                                                if (this.state.resource_type != 'SR')
                                                    return (
                                                            <Form.Field>
                                                                <label>II) Resource Type for Education/Informational</label>
                                                                <Form.Group className={styles.dropdownPadding}>
                                                                    <TagDropdown
                                                                        required
                                                                        name="tags"
                                                                        value={this.state.tags}
                                                                        tagCat="Resource Type for Education/Informational"
                                                                        onChange={tags => this.setState({ tags })}
                                                                    />
                                                                </Form.Group> 
                                                            </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                            })()}
                                            {/* <ResourceFormatDropdown
                                                required
                                                is_informational={this.state.resource_type}
                                                onChange={this.handleResFormatChange}
                                                value={this.state.resource_format}
                                            /> */}
                                            

                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Format <Popup content='Select the format this resource primarily falls under.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Resource format"
                                                    isRelatedToEmail={resourceTypeRelateEmail => this.setState({resourceTypeRelateEmail})}
                                                    isRelatedToPhonetext={resourceTypeRelateTextnumber => this.setState({resourceTypeRelateTextnumber})}
                                                    isRelatedToPhonenumber={resourceTypeRelatePhonenumber => this.setState({resourceTypeRelatePhonenumber})}
                                                    isRelatedToAddress={resourceTypeRelateAddress => this.setState({resourceTypeRelateAddress})}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                            {/* <CategoryDropdown
                                                required
                                                catText={this.state.catText}
                                                value={this.state.category}
                                                onChange={category => {
                                                    if(category.includes('Email') || category.includes('email')){

                                                    }
                                                    this.setState({ category })
                                                }}
                                            /> */}
                                            
                                        </Form.Field>
                                        {(() => {
                                                if (this.state.resourceTypeIsInformative)
                                                    return (
                                                            <Form.Field>
                                                                <label>Informational Resource Text <Popup content='Example a definition or statistical information' trigger={<Icon name='question circle'/>}/> </label>
                                                                <Form.TextArea
                                                                    spellcheck='true'
                                                                    name="informational_resource_text"
                                                                    onChange={this.handleChange}
                                                                    value={this.state.informational_resource_text}
                                                                    label=""
                                                                    rows={2}
                                                                />  
                                                            </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                        })()}
                                        <Divider hidden />
                                        {(() => {
                                                if (this.state.resourceTypeRelateEmail)
                                                    return (
                                                        <Form.Field>
                                                        <label>Resource Email Address <Popup content='(Example: j.m.nobel@ualberta.ca)' trigger={<Icon name='question circle'/>}/> </label>
                                                        <Form.Input
                                                            fluid
                                                            name="email"
                                                            onChange={this.handleChange}
                                                            width={16}
                                                            value={this.state.email}
                                                            placeholder="j.m.nobel@ualberta.ca"
                                                        />
                                                        </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                        })()}
                                        {(() => {
                                                if (this.state.resourceTypeRelatePhonenumber)
                                                    return (
                                                        <Form.Field>
                                                            <label>Resource Phone Number(s) <Popup content='Example: 1234;...;' trigger={<Icon name='question circle'/>}/></label>
                                                            <Form.Input
                                                                fluid
                                                                name="phone_numbers"
                                                                onChange={this.handleChange}
                                                                width={16}
                                                                value={this.state.phone_numbers}
                                                                placeholder="1234;...;"
                                                            />
                                                        </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                        })()}
                                        {(() => {
                                                if (this.state.resourceTypeRelateTextnumber)
                                                    return (
                                                        <Form.Field>
                                                            <label>Text Number(s) <Popup content='Format: enter either just the text number, or include instructions if applicable - Example: text "help" to 1234;...;' trigger={<Icon name='question circle'/>}/> </label>
                                                            <Form.Input
                                                                fluid
                                                                name="text_numbers"
                                                                onChange={this.handleChange}
                                                                width={16}
                                                                value={this.state.text_numbers}
                                                                placeholder='text "help" to 1234;...;'
                                                            />
                                                        </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                        })()}
                                        {(() => {
                                                if (this.state.resourceTypeRelateAddress)
                                                    return (
                                                        <Form.Field>
                                                            <label>Physical Address <Popup content='FILL ONLY if services are in person (Example: 10203 100 Avenue, Edmonton, AB, T4F 1A9, Canada)' trigger={<Icon name='question circle'/>}/></label>
                                                            <Form.Input
                                                            fluid
                                                            name="physical_address"
                                                            onChange={this.handleChange}
                                                            width={16}
                                                            value={this.state.physical_address}
                                                            placeholder="10203 100 Avenue, Edmonton, AB, T4F 1A9, Canada"
                                                        />
                                                        </Form.Field>
                                                    );
                                                else 
                                                    return ('')                                                    
                                        })()}
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Resource URL<Popup content='URL pointing to where the resource was obtained from. (Example: https://mdsc.ca/resources/56)' trigger={<Icon name='question circle'/>}/><Popup content='This field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="general_url"
                                                onChange={this.handleChangeResURL}
                                                onBlur={this.handleChangeResURL}
                                                width={16}
                                                value={this.state.general_url}
                                                placeholder="https://mdsc.ca/resources/56"
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Homepage URL <Popup content='(Example: https://mdsc.ca)' trigger={<Icon name='question circle'/>}/> <Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green'/>}/></label>
                                            <Form.Input
                                                fluid
                                                name="url"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.url}
                                                placeholder="https://mdsc.ca"
                                            />
                                        </Form.Field>
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>What is the cost of this service? </label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    tagCat="freeTag"
                                                    value={this.state.tags}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        {/* <Form.Field>
                                            <label>11) Is this service free?</label>
                                            <Checkbox
                                                name="is_free"
                                                label='Service is free'
                                                checked={this.state.isFreeChecked}
                                                onChange={this.handleIsFreeCheckbox}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>12) Does this resource/service require membership?</label>
                                            <Checkbox
                                                name="require_membership"
                                                label='This requires membership of some kind.'
                                                onChange={this.handleReqMemCheckbox}
                                                checked={this.state.require_membership}
                                            />
                                        </Form.Field> */}
                                        
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
                                            {/* <Slider multiple value={this.state.ageArray} color="blue" settings={this.settings} /> */}
                                            <Form.Field>
                                                <label>Age</label>
                                            </Form.Field>
                                            <Form.Group>
                                                <Form.Input
                                                    inline
                                                    label="Min"
                                                    name="minAge"
                                                    onChange={event => {
                                                        if((event.target.value == this.state.ageArray[0]) || (event.target.value >= this.state.ageArray[1])){
                                                            return;
                                                        }
                                                        var ageArray = [event.target.value, this.state.ageArray[1]];
                                                        this.setState({ageArray});
                                                        }
                                                    }
                                                    width={2}
                                                    value={this.state.ageArray[0]}
                                                    placeholder="min age"
                                                />
                                                <Form.Input
                                                    inline
                                                    name="maxAge"
                                                    label="Max"
                                                    width={2}
                                                    value={this.state.ageArray[1]}
                                                    onChange={event => {
                                                        if((event.target.value == this.state.ageArray[1]) || (event.target.value <= this.state.ageArray[0])){
                                                            return;
                                                        }
                                                        var ageArray = [this.state.ageArray[0], event.target.value];
                                                        this.setState({ageArray});
                                                        }
                                                    
                                                    }
                                                    placeholder="max age"
                                                />
                                                <Form.Input 
                                                    inline
                                                    width={12}
                                                    className="invisiblee"
                                                    // style="visibility: hidden;"
                                                />
                                            </Form.Group>
                                        {/* <Form.Field>
                                            <label>15) Age Tags <Popup content='Age groups tags to indicate who this resource might apply to.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Age Group"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field> */}
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Location <Popup content='Locations/regions for physical/location relevent resources.' trigger={<Icon name='question circle'/>}/></label>
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
                                            <label>Health Issues <Popup content='Tags for any mental health issues this resource addresses, defines, etc.' trigger={<Icon name='question circle'/>}/></label>
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
                                            <label>Language <Popup content='Languages this resource is written/available in.' trigger={<Icon name='question circle'/>}/></label>
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
                                            <label>Resource Audience <Popup content='If this resource was made to support members of a particular group (e.g., LGBTQ2S+) or profession (e.g., doctors, veterans) please add group type here' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="professionTags"
                                                    tagCat="professionTags"
                                                    value={this.state.tags}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Other/All Tags <Popup content='For anything that might not fall under the other categories such as services provided, relevent gender groups, organizations, user groups, etc.' trigger={<Icon name='question circle'/>}/></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    initValue={this.state.tagInitValue}
                                                    name="tags"
                                                    value={this.state.tags}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
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
                                                spellcheck='true' 
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
