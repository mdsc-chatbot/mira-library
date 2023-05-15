/**
 * @file: ReviewTable.js
 * @summary: Component that renders a list of reviews and sorting options
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
import { Table, Popup, Dropdown, Grid, Button, Icon } from "semantic-ui-react";
import { SecurityContext } from "../contexts/SecurityContext";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";
import ReviewPopover from "../review/ReviewPopover"
import { createMasonryCellPositioner } from "react-virtualized";


export default class ModerateResources extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            resources: [],
            tags: [],
            users: [],
            toggleResources: true,
            selectedTag: null,
            displayedFlags: null,
            displayedRelations: null,
            activeTag: -1,
            activeResource: -1,
            relationID: ''
        };
    }

    get_resources = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/chatbotportal/resource", { headers: options }).then(res => {
            this.setState({
                resources: res.data.sort((a,b) => {a.flags.length - b.flags.length})
            });
        });
    };

    get_tags = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/api/public/alltags", { headers: options }).then(res => {
            this.setState({
                tags: res.data
            });
        });
    }

    componentDidMount() {
        this.get_resources();
        this.get_tags();
    }


    handleOrder = (e, { value }) => { this.setState({ order: { value }.value }) }

    handleAssign = (field, value, rid) => {
        var submitCmd = {}
        submitCmd[field] = value;

        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios
            .put(
                "/chatbotportal/resource/" + rid + "/updatepartial/",
                submitCmd,
                { headers: options }
            )
            .then(
                response => {
                },
                error => {
                    console.log(error);
                }
            );
    }

    addRelation = (tag_id, parent_id) =>
    {
        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios
            .post(
                "/api/public/add-tag-relation",
                {'tag_id': tag_id, 'parent_id': parseInt(parent_id)},
                { headers: options }
            )
            .then(
                response => {
                    this.setSelectedTag(tag_id)
                },
                error => {
                    console.log(error);
                }
            );
    }

    setSelectedTag = (id) =>
    {
        this.setState({activeTag: id})
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.post(
            "/api/public/get-relations-by-tag", 
            {'tag_id' : id}, 
            { headers: options }
        ).then(res => {
            this.setState({displayedRelations: res.data})
        });
    }

    setSelectedResource = (resource) =>
    {
        this.setState({activeResource: resource.id})
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.post(
            "/chatbotportal/resource/get-flags-by-id", 
            {'flag_ids' : resource.flags}, 
            { headers: options }
        ).then(res => {
            this.setState({displayedFlags: res.data})
        });
    }

    showResourceFlags = () => 
    {
        const flags_get = this.state.displayedFlags.map(r => (
            (
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><h4>{r.description}</h4></td>
                </tr>
            )
        ));
        return flags_get
    }

    handleInputChange = e => {
        this.setState({ relationID: e.target.value });
    };
    showRelations = () => 
    {
        const relations_get = this.state.displayedRelations.map(r => (
            (
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><h4>{r.id}<button icon><Icon name="minus" /></button></h4></td>
                    <td><h4>{this.state.tags.filter(obj => {return id === r.id}).name}</h4></td>
                </tr>
            )
        ));
        //append add row
        relations_get.push(
            <tr>
                    <td><h4><input type="text" onChange={this.handleInputChange}/><button icon onClick={() => this.addRelation(this.state.activeTag, this.state.relationID)}><Icon name="plus" /></button></h4></td>
                    <td><h4><input type="text"/></h4></td>
            </tr>
        )
        return relations_get
    }

    showResourceData = () => {
        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            (
                <tr key={r.id} ref={tr => this.results = tr} className={r.id === this.state.activeResource ? 'active' : null}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>
                        <h4>{r.flags.length === 0 ? (<p></p>) : (<p><i class="yellow warning sign icon" onClick={() => this.setSelectedResource(r)}></i></p>)}</h4>
                    </td>
                    <td>
                        <h4>{r.visible === true ? (<p><i class="eye icon"></i> </p>) : (<p><i class="red eye slash icon"></i></p>)}</h4>
                    </td>
                </tr>
            )
        ));
        return resources_get
    }

    showTagData = () => {
        const tag_get = this.state.tags.length > 0 && this.state.tags.map(r => (
            (
                <tr key={r.id} ref={tr => this.results = tr} onClick={() => this.setSelectedTag(r.id)} className={r.id === this.state.activeTag ? 'active' : null}>
                    <td>{r.name}</td>
                    <td>
                        <h4>{r.approved === true ? (<p></p>) : (<p><i class="yellow warning sign icon"> </i></p>)}</h4>
                    </td>
                </tr>
            )
        ));
        return tag_get
    }

    resourceFlagHeader = () => {
        return <tr><th style={{ width: 250 }}>Flags</th></tr>
    }
    tagRelationHeader = () => {
        return <tr><th style={{ width: 250 }}>Parent ID</th><th style={{ width: 250 }}>Parent Name</th></tr>
    }
    resourceHeader = () => {
        return <tr><th style={{ width: 350 }}>Title</th><th>Flags</th><th>Visible</th></tr>
    }
    tagHeader = () => {
        return <tr><th style={{ width: 350 }}>Name</th><th>Status</th></tr>
    }

    idToUserString = (idnum) => {
        if (idnum == -1) return "Unassigned";
        for (var i = 0; i < this.state.users.length; i++) {
            if (this.state.users[i].id == idnum) return this.state.users[i].first_name + " " + this.state.users[i].last_name
        }
    }

    render() {
        // Get current logged in user, take this function out of format_data and consolidate it later
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";

        return (
            <div>
                <div style={{ paddingTop: '2%', paddingLeft: '6%', paddingRight: '6%' }}>
                    <div style={{ display: 'inline-block' }}>
                        <Button.Group>
                            <Button toggle active={this.state.toggleResources} onClick={() => this.setState({ toggleResources: true })}>Resources</Button>
                            <Button.Or />
                            <Button toggle active={!this.state.toggleResources} onClick={() => this.setState({ toggleResources: false })}>Tags</Button>
                        </Button.Group>
                    </div>
                    <Grid celled>
                        <Grid.Row>
                            <Grid.Column width={9}>
                                <div style={{ height: '700px', overflowX: "scroll", width: "100%" }}>
                                        {this.state.toggleResources ?
                                            <Table class="ui definition table">
                                                <thead>
                                                    {this.resourceHeader()}
                                                </thead>
                                                <tbody>
                                                    {this.showResourceData()}
                                                </tbody>
                                                <tfoot>
                                                    {/*this.getUsersFooter()*/}
                                                </tfoot>
                                            </Table>
                                        :
                                            <Table class="ui definition table">
                                                <thead>
                                                    {this.tagHeader()}
                                                </thead>
                                                <tbody>
                                                    {this.showTagData()}
                                                </tbody>
                                                <tfoot>
                                                    {/*this.getUsersFooter()*/}
                                                </tfoot>
                                            </Table>
                                        }
                                </div>
                            </Grid.Column>
                            <Grid.Column width={7}>
                                <div style={{ height: '700px', overflowX: "scroll", width: "100%" }}>
                                    {this.state.toggleResources ?
                                        <Table class="ui celled table">
                                            <thead>
                                                {this.resourceFlagHeader()}
                                            </thead>
                                            <tbody>
                                                {this.state.displayedFlags === null ? <p></p> : this.showResourceFlags()}
                                            </tbody>
                                        </Table>
                                    :
                                        <Table class="ui celled table">
                                            <thead>
                                                {this.tagRelationHeader()}
                                            </thead>
                                            <tbody>
                                            {this.state.displayedRelations === null ? <p></p> : this.showRelations()}
                                            </tbody>
                                        </Table>
                                    }
                                </div>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </div>
            </div>
        );
    }
}