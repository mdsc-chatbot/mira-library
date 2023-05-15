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

import React, { Component } from "react";
import axios from "axios";
import { Slider } from "react-semantic-ui-range";
import { Container, Form, Header, Input, Message, Icon, Popup, Checkbox, Divider, Dropdown, Dimmer, Segment, Image, Loader} from "semantic-ui-react";
import TagDropdown from "./TagDropdown";
import TitleDropdown from "./TitleDropdown";
import OrganizationNameDropdown from "./OrganizationNameDropdown";
import CategoryDropdown from './CategoryDropdown';
import HoursOfOperationWidget from "./HoursOfOperationWidget";
import ResourceTypeDropdown from './ResourceTypeDropdown';
import ResourceFormatDropdown from './ResourceFormatDropdown';
import { SecurityContext } from '../contexts/SecurityContext';
import styles from "./ResourceSubmitForm.css";

export default class ResourceSubmitForm extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            public_ident: "",
            token: "",
            dimmerLoading: false,
            timeZone:"-6 UTC",
            resourceTypeRelateTextnumber: false,
            resourceTypeRelateEmail: false,
            resourceTypeRelatePhonenumber: false,
            resourceTypeRelateAddress: false,
            ageArray: [0, 110],
            resourceId: null,
            title: "",
            catText: "",
            tagInitValue: "",
            definition: "",
            resourceTypeIsInformative: false,
            organization_name: "",
            url: "",
            general_url: "",
            rating: 5,
            attachment: null,
            attachmentPath: "", // To clear the file after submitting it
            comments: "",
            description: "",
            organization_description: "",
            email: "",
            phone_numbers: "",
            text_numbers: "",
            physical_address: "",
            resource_type: "SR",
            //resource format = resource type in Front-End
            errors: {},
            // category: 1,
            tags: [],
            url_validated: true,
            currentTags: null,
            submitted: 0,
            alwaysAvailable: true,
            zoneInd: 9,
            hourBools: [
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
            ],
            allTimeZones: [{key:"-11 UTC",value:0,text:"(GMT-11:00) Midway Island, Samoa"}, 
            {key:"-10 UTC",value:1,text:"(GMT-10:00) Hawaii"},
            {key:"-9 UTC",value:2,text:"(GMT-09:00) Alaska"},
            {key:"-8 UTC",value:3,text:"(GMT-08:00) Pacific Time (US & Canada)"},
            {key:"-8 UTC",value:4,text:"(GMT-08:00) Tijuana, Baja California"},  
            {key:"-7 UTC",value:5,text:"(GMT-07:00) Arizona"},
            {key:"-7 UTC",value:6,text:"(GMT-07:00) Chihuahua, La Paz, Mazatlan"}, 
            {key:"-7 UTC",value:7,text:"(GMT-07:00) Mountain Time (US & Canada)"},  
            {key:"-6 UTC",value:8,text:"(GMT-06:00) Central America"},
            {key:"-6 UTC",value:9,text:"(GMT-06:00) Central Time (US & Canada)"},
            {key:"-6 UTC",value:10,text:"(GMT-06:00) Guadalajara, Mexico City, Monterrey"},
            {key:"-6 UTC",value:11,text:"(GMT-06:00) Saskatchewan"},
            {key:"-5 UTC",value:12,text:"(GMT-05:00) Bogota, Lima, Quito, Rio Branco"},
            {key:"-5 UTC",value:13,text:"(GMT-05:00) Eastern Time (US & Canada)"}, 
            {key:"-5 UTC",value:14,text:"(GMT-05:00) Indiana (East)"},  
            {key:"-4 UTC",value:15,text:"(GMT-04:00) Atlantic Time (Canada)"}, 
            {key:"-4 UTC",value:16,text:"(GMT-04:00) Caracas, La Paz"}, 
            {key:"-4 UTC",value:17,text:"(GMT-04:00) Manaus"}, 
            {key:"-4 UTC",value:18,text:"(GMT-04:00) Santiago"},
            {key:"-3:30 UTC",value:19,text:"(GMT-03:30) Newfoundland"}, 
            {key:"-3 UTC",value:20,text:"(GMT-03:00) Brasilia"},
            {key:"-3 UTC",value:21,text:"(GMT-03:00) Buenos Aires, Georgetown"},
            {key:"-3 UTC",value:22,text:"(GMT-03:00) Greenland"},
            {key:"-3 UTC",value:23,text:"(GMT-03:00) Montevideo"},
            {key:"-2 UTC",value:24,text:"(GMT-02:00) Mid-Atlantic"}, 
            {key:"-1 UTC",value:25,text:"(GMT-01:00) Cape Verde Is."}, 
            {key:"-1 UTC",value:26,text:"(GMT-01:00) Azores"}, 
            {key:"0 UTC",value:27,text:"(GMT+00:00) Casablanca, Monrovia, Reykjavik"}, 
            {key:"0 UTC",value:28,text:"(GMT+00:00) Greenwich Mean Time : Dublin, Edinburgh, Lisbon, London"}, 
            {key:"+1 UTC",value:29,text:"(GMT+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna"},
            {key:"+1 UTC",value:30,text:"(GMT+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague"},
            {key:"+1 UTC",value:31,text:"(GMT+01:00) Brussels, Copenhagen, Madrid, Paris"},
            {key:"+1 UTC",value:32,text:"(GMT+01:00) Sarajevo, Skopje, Warsaw, Zagreb"},
            {key:"+1 UTC",value:33,text:"(GMT+01:00) West Central Africa"},
            {key:"+2 UTC",value:34,text:"(GMT+02:00) Amman"}, 
            {key:"+2 UTC",value:35,text:"(GMT+02:00) Athens, Bucharest, Istanbul"},
            {key:"+2 UTC",value:36,text:"(GMT+02:00) Beirut"},
            {key:"+2 UTC",value:37,text:"(GMT+02:00) Cairo"},
            {key:"+2 UTC",value:38,text:"(GMT+02:00) Harare, Pretoria"},
            {key:"+2 UTC",value:39,text:"(GMT+02:00) Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius"},
            {key:"+2 UTC",value:40,text:"(GMT+02:00) Jerusalem"},
            {key:"+2 UTC",value:41,text:"(GMT+02:00) Minsk"},
            {key:"+2 UTC",value:42,text:"(GMT+02:00) Windhoek"},
            {key:"+3 UTC",value:43,text:"(GMT+03:00) Kuwait, Riyadh, Baghdad"},
            {key:"+3 UTC",value:44,text:"(GMT+03:00) Moscow, St. Petersburg, Volgograd"},
            {key:"+3 UTC",value:45,text:"(GMT+03:00) Nairobi"},
            {key:"+3 UTC",value:46,text:"(GMT+03:00) Tbilisi"},
            {key:"+3:30 UTC",value:47,text:"(GMT+03:30) Tehran"},
            {key:"+4 UTC",value:48,text:"(GMT+04:00) Abu Dhabi, Muscat"}, 
            {key:"+4 UTC",value:49,text:"(GMT+04:00) Baku"}, 
            {key:"+4 UTC",value:50,text:"(GMT+04:00) Yerevan"}, 
            {key:"+4:30 UTC",value:51,text:"(GMT+04:30) Kabul"},
            {key:"+5 UTC",value:52,text:"(GMT+05:00) Yekaterinburg"}, 
            {key:"+5 UTC",value:53,text:"(GMT+05:00) Islamabad, Karachi, Tashkent"}, 
            {key:"+5:30 UTC",value:54,text:"(GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi"}, 
            {key:"+5:30 UTC",value:55,text:"(GMT+05:30) Sri Jayawardenapura"}, 
            {key:"+5:45 UTC",value:56,text:"(GMT+05:45) Kathmandu"}, 
            {key:"+6 UTC",value:57,text:"(GMT+06:00) Almaty, Novosibirsk"},
            {key:"+6 UTC",value:58,text:"(GMT+06:00) Astana, Dhaka"},
            {key:"+6:30 UTC",value:59,text:"(GMT+06:30) Yangon (Rangoon)"},
            {key:"+7 UTC",value:60,text:"(GMT+07:00) Bangkok, Hanoi, Jakarta"}, 
            {key:"+7 UTC",value:61,text:"(GMT+07:00) Krasnoyarsk"}, 
            {key:"+8 UTC",value:62,text:"(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi"}, 
            {key:"+8 UTC",value:63,text:"(GMT+08:00) Kuala Lumpur, Singapore"}, 
            {key:"+8 UTC",value:64,text:"(GMT+08:00) Irkutsk, Ulaan Bataar"}, 
            {key:"+8 UTC",value:65,text:"(GMT+08:00) Perth"}, 
            {key:"+8 UTC",value:66,text:"(GMT+08:00) Taipei"}, 
            {key:"+9 UTC",value:67,text:"(GMT+09:00) Osaka, Sapporo, Tokyo"},
            {key:"+9 UTC",value:68,text:"(GMT+09:00) Seoul"},
            {key:"+9 UTC",value:69,text:"(GMT+09:00) Yakutsk"},
            {key:"+9:30 UTC",value:70,text:"(GMT+09:30) Adelaide"},
            {key:"+9:30 UTC",value:71,text:"(GMT+09:30) Darwin"},
            {key:"+10 UTC",value:72,text:"(GMT+10:00) Brisbane"},
            {key:"+10 UTC",value:73,text:"(GMT+10:00) Canberra, Melbourne, Sydney"},
            {key:"+10 UTC",value:74,text:"(GMT+10:00) Hobart"},
            {key:"+10 UTC",value:75,text:"(GMT+10:00) Guam, Port Moresby"},
            {key:"+10 UTC",value:76,text:"(GMT+10:00) Vladivostok"},
            {key:"+11 UTC",value:77,text:"(GMT+11:00) Magadan, Solomon Is., New Caledonia"},
            {key:"+12 UTC",value:78,text:"(GMT+12:00) Auckland, Wellington"},
            {key:"+12 UTC",value:79,text:"(GMT+12:00) Fiji, Kamchatka, Marshall Is."},
            {key:"+13 UTC",value:80,text:"(GMT+13:00) Nuku'alofa"},
            ]
        };
        this.baseState = this.state;

    }

    settings = {
        start: [2, 30],
        min: 0,
        max: 120,
        step: 1,
        onChange: value => {
            this.setState({ ageArray: value });
        }
    };

    get_resource_details = (resourceID) => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}/`, { headers: options })
            .then(res => {
                console.log('I got resources', res.data)
                if (res.data.definition) {
                    this.setState({ resourceTypeIsInformative: true });
                } else {
                    this.setState({ resourceTypeIsInformative: false });
                }
                this.setState({ resource_type: res.data.resource_type });
                this.setState({ title: res.data.title });
                this.setState({ timeZone: res.data.time_zone });
                this.setState({ definition: res.data.definition });
                this.setState({ organization_name: res.data.organization_name });
                this.setState({ url: res.data.url });
                this.setState({ general_url: res.data.general_url });
                this.setState({ rating: res.data.rating });
                this.setState({ comments: res.data.comments });
                this.setState({ description: res.data.description });
                this.setState({ organization_description: res.data.organization_description });

                if(res.data.email!=null && res.data.email!=""){ 
                    this.setState({ resourceTypeRelateEmail: true });
                    this.setState({ email: res.data.email });
                }

                if(res.data.phone_numbers!=null && res.data.phone_numbers!=""){
                    this.setState({ resourceTypeRelatePhonenumber: true });
                    this.setState({ phone_numbers: res.data.phone_numbers });
                }

                if(res.data.text_numbers!=null && res.data.text_numbers!=""){ 
                    this.setState({ resourceTypeRelateTextnumber: true });
                    this.setState({ text_numbers: res.data.text_numbers });
                }

                if(res.data.physical_address!=null && res.data.physical_address!=""){
                    this.setState({ resourceTypeRelateAddress: true });
                    this.setState({ physical_address: res.data.physical_address });
                }

                this.setState({ tagInitValue: res.data.tags });
                this.setState({ hours_of_operation: res.data.hours_of_operation });
                this.setState({ ageArray: [res.data.min_age, res.data.max_age] });
                if (res.data.hours_of_operation != null && res.data.hours_of_operation != "MON:;TUE:;WED:;THU:;FRI:;SAT:;SUN:;") {
                    this.setState({ alwaysAvailable: false });
                    this.decodeHours(res.data.hours_of_operation);
                }
                // let submit btn know we are in edit mode
                this.setState({ resourceId: resourceID });
            });
    };

    componentDidMount() {
        //check if resource id is in url to know if we come to form for editing the resource or not
        const resourceId = this.props.location.search ? this.props.location.search.substring(4) : '';
        if (resourceId != '' && this.context.security.is_logged_in) this.get_resource_details(resourceId);
    }

    create_resource = () => {
        // Get current logged in user
        let created_by_user = null;
        let created_by_user_pk = null;
        
        const resourceFormData = new FormData();
        if (this.context.security.is_logged_in) {
            created_by_user = this.context.security.first_name;
            created_by_user_pk = this.context.security.id;
        }
        else
        {
            created_by_user = "Public|" + this.state.public_ident;
            created_by_user_pk = -2;
            resourceFormData.append("captcha", this.state.token);
        }

        resourceFormData.append("title", this.state.title);
        resourceFormData.append("time_zone", this.state.timeZone);
        resourceFormData.append("definition", this.state.definition);
        resourceFormData.append("organization_name", this.state.organization_name);
        resourceFormData.append("url", this.state.url);
        resourceFormData.append("general_url", this.state.general_url);
        resourceFormData.append("rating", this.state.rating);
        resourceFormData.append("comments", this.state.comments);
        resourceFormData.append("created_by_user", created_by_user);
        resourceFormData.append("created_by_user_pk", created_by_user_pk);
        resourceFormData.append("email", this.state.email);
        resourceFormData.append("description", this.state.description);
        resourceFormData.append("organization_description", this.state.organization_description);
        resourceFormData.append("physical_address", this.state.physical_address);
        resourceFormData.append("resource_type", this.state.resource_type);
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

        //if we need to, deal with the hour bools
        if (!this.state.alwaysAvailable) {
            var hourstring = "";
            hourstring += "MON:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[0][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            hourstring += "TUE:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[1][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            hourstring += "WED:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[2][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            hourstring += "THU:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[3][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            hourstring += "FRI:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[4][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            hourstring += "SAT:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[5][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            hourstring += "SUN:";
            for (var i = 0; i < 24; i++)
                if (this.state.hourBools[6][i]) hourstring += (i + 1).toString() + ",";
            hourstring += ";";
            resourceFormData.append(`hours_of_operation`, hourstring);
        }

        return resourceFormData;
    };

    //get string from db and represent it in the hour selection buttons
    decodeHours = (hoursFromDB) => {
        console.log('hoursFromDB', hoursFromDB);
        var weekIndex;
        var newHourBools = this.state.hourBools;
        var dayArray = hoursFromDB.split(';');
        dayArray.forEach((day, index) => {
            if (day == '') {
                return;
            }
            switch (dayArray[index].substring(0, 3)) {
                case "MON":
                    weekIndex = 0
                    break;
                case "TUE":
                    weekIndex = 1
                    break;
                case "WED":
                    weekIndex = 2
                    break;
                case "THU":
                    weekIndex = 3
                    break;
                case "FRI":
                    weekIndex = 4
                    break;
                case "SAT":
                    weekIndex = 5
                    break;
                case "SUN":
                    weekIndex = 6
                    break;
            }
            const hourArray = day.substring(4).split(',');
            hourArray.forEach(hour => {
                if (hour == '') {
                    return;
                }
                newHourBools[weekIndex][hour - 1] = true;
            });
        });

        console.log('new bool', newHourBools);
        this.setState({ hourBools: newHourBools });
    }

    encodeHours = (hoursBool) => {
        var hourstring = "";
        hourstring += "MON:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[0][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";
        hourstring += "TUE:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[1][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";
        hourstring += "WED:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[2][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";
        hourstring += "THU:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[3][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";
        hourstring += "FRI:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[4][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";
        hourstring += "SAT:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[5][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";
        hourstring += "SUN:";
        for (var i = 0; i < 24; i++)
            if (hoursBool[6][i]) hourstring += (i + 1).toString() + ",";
        hourstring += ";";

        if(hourstring == "MON:;TUE:;WED:;THU:;FRI:;SAT:;SUN:;"){
            return null;
        }
        return hourstring;
    }

    post_resource = () => {
        const resourceFormData = this.create_resource();
        // let submitted = 1;
        if(this.context.security.is_logged_in)
        {
            axios
                .post("/chatbotportal/resource/", resourceFormData, {
                    headers: { Authorization: `Bearer ${this.context.security.token}` }
                })
                .then(() => {
                    this.set_submitted_state(1, "POST SUCCESS");
                    axios
                        .get("/api/public/index-resources", {
                            headers: { Authorization: `Bearer ${this.context.security.token}` }
                        })
                })
                .catch(error => {
                    console.error(error.response);
                    var errors = Object.keys(error.response.data).map(function (key) {
                        return " " + error.response.data[key];
                    });
                    this.set_submitted_state(-1, errors);
                });
        }
        else
        {
            axios
                .post("/chatbotportal/resource/publicsubmit/", resourceFormData)
                .then(() => {
                    this.set_submitted_state(1, "POST SUCCESS");
                })
                .catch(error => {
                    console.error(error.response);
                    var errors = Object.keys(error.response.data).map(function (key) {
                        return " " + error.response.data[key];
                    });
                    this.set_submitted_state(-1, errors);
                });
        }
    };

    set_submitted_state = (submitted_value, submitted_error) => {
        console.log(this.state, submitted_value)
        if (submitted_value === 1) {
            if (this.context.security.is_logged_in)
                this.update_user_submissions();
            this.setState({ submitted: submitted_value }, () => {
                setTimeout(() => {
                    this.setState(this.baseState);
                    setTimeout(() => {
                        window.location.reload(false);
                    }, 900);
                }, 2500);
            });
        } else {
            this.setState({ submitted: submitted_value, errors: submitted_error });
        }
        console.log(submitted_error);
    };

    update_user_submissions = () => {
        axios
            .put(`/chatbotportal/authentication/${this.context.security.id}/update/submissions/`, '', {
                headers: { 'Authorization': `Bearer ${this.context.security.token}` }
            })
            .then(
                () => { },
                error => {
                    console.log(error);
                }
            );
    };

    handleRate = (event, data) => {
        this.setState({ rating: data.rating });
    };

    handleChange = event => {
        this.setState({ [event.target.name]: event.target.value });
    };

    handleChangeResURL = event => {
        var baseUrl = '';
        try {
            const urlOne = new URL(this.state.url);
            baseUrl = urlOne.origin;
        } catch (e) {
            baseUrl = "";
        }

        if (baseUrl != '') { this.setState({ general_url: baseUrl }); }
        this.setState({ url: event.target.value })
    };

    // event.target.value holds the pathname of a file
    handleFileChange = event => {
        this.setState({
            [event.nativeEvent.target.name]: event.nativeEvent.target.files[0],
            attachmentPath: event.nativeEvent.target.value
        });
    };

    addFieldTag(tagName) {

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
                    headers: { Authorization: `Bearer ${this.context.security.token}` }
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
                this.setState({ tags });
            });
    }

    handleSubmit = event => {
        if (document.activeElement.getAttribute('name') != "submit") {
            this.setState({});
            return;
        }
        this.setState({dimmerLoading:true});

        if (this.state.resourceId !== null) {
            this.update_resource_user();
            this.setState({dimmerLoading: false});
            return;
        }

        //add field tags
        if (this.state.phone_numbers != "") this.addFieldTag("Phone Number")
        if (this.state.text_numbers != "") this.addFieldTag("Text Messaging")
        if (this.state.url != "" || this.state.general_url != "") this.addFieldTag("Website")
        if (this.state.description != "") this.addFieldTag("Description")
        if (this.state.email != "") this.addFieldTag("Email")

        if(this.context.security.is_logged_in)
        {
            this.post_resource();
            event.preventDefault();
            this.setState({dimmerLoading:false});
        }
        else
        {
            this.getRecaptcha()
        }
    };


    handleReqMemCheckbox = () => {
        this.setState({ require_membership: !this.state.require_membership })
    };

    handleResTypeChange = (resource_type) => {
        this.setState({ resource_type })
    }

    update_resource_user = () => {
        var submitCmd = {
            'title': this.state.title,
            'url': this.state.url,
            'rating': this.state.rating,
            'comments': this.state.comments,
            'description': this.state.description,
            'email': this.state.email,
            'phone_numbers': this.state.phone_numbers,
            'refrences': this.state.refrences,
            'resource_type': this.state.resource_type,
            'organization_description': this.state.organization_description,
            'general_url': this.state.general_url,
            'physical_address': this.state.physical_address,
            'hours_of_operation': this.encodeHours(this.state.hourBools),
            'min_age': this.state.ageArray[0],
            'max_age': this.state.ageArray[1],
            'organization_name': this.state.organization_name,
            'definition': this.state.definition,
            'tags': this.state.tags,
            'time_zone': this.state.timeZone
            // 'attachment' : this.state.attachment ? this.state.attachment : '',
        };

        // if (this.state.tags && this.state.tags.length) {
        //     this.state.tags.forEach(value => {
        //         submitCmd.append(`tags`, value);
        //     });
        // }

        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };

        // Resource
        axios
            .put(
                "/chatbotportal/resource/" + this.state.resourceId + "/updatepartial/",
                submitCmd,
                { headers: options }
            ).then(
                response => {
                    axios
                    .get("/api/public/index-resources", {
                        headers: { Authorization: `Bearer ${this.context.security.token}` }
                    })
                    setTimeout(() => {
                        // this.setState(this.baseState);
                        setTimeout(() => {
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

    //recaptcha stuff
    postRecaptcha = (token) => {
        this.setState({token: token});
        this.post_resource();
        this.setState({dimmerLoading: false});
    }

    getRecaptcha = () => {
        var promise = new Promise((resolve, reject) => {
          var script = document.createElement('script')
          script.type = 'text/javascript';
          script.async = true;
          script.src = "https://www.google.com/recaptcha/api.js?render=6LeXmV4gAAAAAFPQDF59JJJxGhvw31zkgrkyL9Dm";
          script.onload = resolve;
          script.onerror = reject;
          document.head.appendChild(script);
        })

        promise
            .then(function() {
                grecaptcha.ready(function() {
                    grecaptcha.execute('6LeXmV4gAAAAAFPQDF59JJJxGhvw31zkgrkyL9Dm', {action: 'submit'}).then((token) => this.postRecaptcha(token));
                }.bind(this));
            }.bind(this))
            .catch(() =>{
                console.log("error with recaptcha")
            });
      }

    render() {
        var dateTabs = null;
        if (!this.state.alwaysAvailable) {
            dateTabs = [<Dropdown selection onChange={(event, data) => {this.setState({timeZone:data.options.find(o => o.value === data.value).key, zoneInd:data.value})}} text={this.state.allTimeZones[this.state.zoneInd].text} value={this.state.timeZone} options={this.state.allTimeZones}/>, <HoursOfOperationWidget hourBools={this.state.hourBools} />]
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
                                {//securityContext.security.is_logged_in ? (
                                    <div>
                                        {(() => 
                                            {
                                                if (!securityContext.security.is_logged_in)
                                                {
                                                    return (
                                                        <Form.Field>
                                                            <label>You're currently submitting this resource anonymously. If you'd like to expediate the approval process, you can add your name, your email address, or some other piece of identifying information</label>
                                                            <Form.Input
                                                                fluid
                                                                name="public_ident"
                                                                onChange={this.handleChange}
                                                                onBlur={this.handleChange}
                                                                width={16}
                                                                value={this.state.public_ident}
                                                                placeholder="Name/Email/Affiliation"
                                                            />
                                                        </Form.Field>);
                                                }
                                            })()
                                        }

                                        <Form.Field>
                                            <label>Resource Title <Popup content='(Format: [name of organization][type of resource] - Example: Crisis Services Canada PhoneLine)' trigger={<Icon name='question circle' />} /></label>
                                            <TitleDropdown
                                                required
                                                name="title"
                                                value={this.state.title}
                                                label="Title"
                                                onChange={title => this.setState({ title })}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Name of Company or Organization Providing Resource <Popup content='(Example: Crisis Services Canada)' trigger={<Icon name='question circle' />} /></label>
                                            <OrganizationNameDropdown
                                                required
                                                name="organization_name"
                                                value={this.state.organization_name}
                                                label="Enter Company or Organization name"
                                                onChange={organization_name => this.setState({ organization_name })}
                                                organization_description={organization_description => this.setState({ organization_description })}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Brief description of the company or organization &nbsp;(up to 3 sentences). </label>
                                            <Form.TextArea
                                                required
                                                spellcheck='true'
                                                name="organization_description"
                                                onChange={this.handleChange}
                                                value={this.state.organization_description}
                                                placeholder="Enter Company or Organization Description"
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Brief description of the service the resource provides &nbsp;(up to 3 sentences).</label>
                                            <Form.TextArea
                                                name="description"
                                                onChange={this.handleChange}
                                                value={this.state.description}
                                                placeholder="Enter Service Description."
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>Resource Category <Popup content='Indicate if this resource is primarily a service, informational, or both.' trigger={<Icon name='question circle' />} /></label>
                                            <ResourceTypeDropdown
                                                required
                                                value={this.state.resource_type}
                                                onChange={this.handleResTypeChange}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Type(s) </label>
                                            {(() => {
                                                if (this.state.resource_type != 'RS')
                                                    return (
                                                        <Form.Field>
                                                            <label>I) Resource Type(s) for Programs and Services</label>
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
                                                            <label>II) Resource Type(s) for Education/Informational</label>
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
                                            <label>Resource Format(s) <Popup content='Select the format this resource primarily falls under.' trigger={<Icon name='question circle' />} /></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Resource format"
                                                    isRelatedToEmail={resourceTypeRelateEmail => this.setState({ resourceTypeRelateEmail })}
                                                    isRelatedToPhonetext={resourceTypeRelateTextnumber => this.setState({ resourceTypeRelateTextnumber })}
                                                    isRelatedToPhonenumber={resourceTypeRelatePhonenumber => this.setState({ resourceTypeRelatePhonenumber })}
                                                    isRelatedToAddress={resourceTypeRelateAddress => this.setState({ resourceTypeRelateAddress })}
                                                    isRelatedToDefinition={resourceTypeIsInformative => this.setState({ resourceTypeIsInformative })}
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
                                                        <label>Informational Resource Text <Popup content='Example: a definition or statistical information' trigger={<Icon name='question circle' />} /> </label>
                                                        <Form.TextArea
                                                            spellcheck='true'
                                                            name="definition"
                                                            onChange={this.handleChange}
                                                            value={this.state.definition}
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
                                                        <label>Resource Email Address <Popup content='(Example: j.m.nobel@ualberta.ca)' trigger={<Icon name='question circle' />} /> </label>
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
                                                        <label>Resource Phone Number(s) <Popup content='Example: 1234;...;' trigger={<Icon name='question circle' />} /></label>
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
                                                        <label>Text Number(s) <Popup content='Format: enter either just the text number, or include instructions if applicable - Example: text "help" to 1234;...;' trigger={<Icon name='question circle' />} /> </label>
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
                                                        <label>Physical Address <Popup content='FILL ONLY if services are in person (Example: 10203 100 Avenue, Edmonton, AB, T4F 1A9, Canada)' trigger={<Icon name='question circle' />} /></label>
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
                                            <label>Resource URL<Popup content='URL pointing to where the resource was obtained from. (Example: https://mdsc.ca/resources/56)' trigger={<Icon name='question circle' />} /><Popup content='This field is OPTIONAL' trigger={<Icon name='flag' color='green' />} /></label>
                                            <Form.Input
                                                fluid
                                                name="url"
                                                onChange={this.handleChangeResURL}
                                                onBlur={this.handleChangeResURL}
                                                width={16}
                                                value={this.state.url}
                                                placeholder="https://mdsc.ca/resources/56"
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Homepage URL <Popup content='(Example: https://mdsc.ca)' trigger={<Icon name='question circle' />} /> <Popup content='this field is OPTIONAL' trigger={<Icon name='flag' color='green' />} /></label>
                                            <Form.Input
                                                fluid
                                                name="general_url"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.general_url}
                                                placeholder="https://mdsc.ca"
                                            />
                                        </Form.Field>
                                        <Divider hidden />
                                        <Form.Field>
                                            <label>What is the cost of this service? </label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    tagCat="Costs"
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
                                                    if ((event.target.value == this.state.ageArray[0]) || (event.target.value >= this.state.ageArray[1])) {
                                                        return;
                                                    }
                                                    var ageArray = [event.target.value, this.state.ageArray[1]];
                                                    this.setState({ ageArray });
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
                                                    if ((event.target.value == this.state.ageArray[1]) || (event.target.value <= this.state.ageArray[0])) {
                                                        return;
                                                    }
                                                    var ageArray = [this.state.ageArray[0], event.target.value];
                                                    this.setState({ ageArray });
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
                                            <label>Location(s) <Popup content='Locations/regions for physical/location relevent resources.' trigger={<Icon name='question circle' />} /></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Location"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Health Issue(s) <Popup content='Tags for any mental health issues this resource addresses, defines, etc.' trigger={<Icon name='question circle' />} /></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Health Issue"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Language(s) <Popup content='Languages this resource is written/available in.' trigger={<Icon name='question circle' />} /></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    required
                                                    name="langTags"
                                                    value={this.state.tags}
                                                    tagCat="Language"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Resource Audience(s) <Popup content='If this resource was made to support members of a particular group (e.g., LGBTQ2S+) or profession (e.g., doctors, veterans) please add group type here' trigger={<Icon name='question circle' /> } /><Popup content='This field is OPTIONAL' trigger={<Icon name='flag' color='green' />} /></label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="professionTags"
                                                    tagCat="Audience"
                                                    value={this.state.tags}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Other/All Tags <Popup content='For anything that might not fall under the other categories such as services provided, relevent gender groups, organizations, user groups, etc.' trigger={<Icon name='question circle' />} /> <Popup content='This field is OPTIONAL' trigger={<Icon name='flag' color='green' />} /></label>
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
                                            <label>Resource Availability <Popup content='If the resource is not always available, uncheck this and fill in the times below.' trigger={<Icon name='question circle' />} /></label>
                                            <Checkbox
                                                label='Resource Available 24/7'
                                                onChange={this.toggle}
                                                checked={this.state.alwaysAvailable}
                                            />
                                        </Form.Field>
                                        {dateTabs}
                                        <Divider hidden />
                                        <Form.Field>
                                        <label>Comments <Popup content='This field is OPTIONAL' trigger={<Icon name='flag' color='green' />} /></label>
                                            <Form.TextArea
                                                spellcheck='true'
                                                name="comments"
                                                onChange={this.handleChange}
                                                value={this.state.comments}
                                                placeholder="Enter any comments (Optional)"
                                                rows={2}
                                            />
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Upload an attachment <Popup content='This field is OPTIONAL' trigger={<Icon name='flag' color='green' />} /></label>
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

                                        {/* <Dimmer as={Segment} dimmed={this.state.dimmerLoading}> */}
                                            <Dimmer page="true" active={this.state.dimmerLoading} inverted>
                                                <Loader>Loading</Loader>
                                            </Dimmer>
                                        {/* </Dimmer> */}

                                        <Form.Button name="submit" content="Submit" color="green" />
                                    </div>
                                //) : null
                            }
                            </Form>
                        </Container>
                    )}
                </SecurityContext.Consumer>
            </div>
        );
    }
}
