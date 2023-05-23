import React, { Component } from "react";
import { Responsive } from "semantic-ui-react";
import {Button, Container, Divider, Icon, Header, Menu} from "semantic-ui-react";

function normal_header(group, editable) {
    var data = [];
    data.push({name:"Group Name: ", value:group[0]});
    data.push({name:"Group Tags: ", value:group[1]});
    data.push({name:"Number Approved: ", value:group[2]});
    data.push({name:"Number Pending: ", value:group[3]});
    data.push({name:"Number Rejected ", value:group[4]});

    var menuEntries = [];
    for (var i = 0; i < data.length; i+=1) 
    {
        menuEntries.push(<Menu>
                            <Menu.Item>
                            {<a>{data[i].name}</a>}
                            </Menu.Item>
                            <Menu.Item>
                            {<a>{data[i].value}</a>}
                            </Menu.Item>
                        </Menu>);
    }
    return (
        <Container>
            {menuEntries}
        </Container>
    );
}


export function ResourceStatGroup(group) {
    // Common props for grid row, columns that are re-usable.
    // If we need this in more than one place, consider re-making this into several components.
    console.log(group.group)
    console.log(group.group[0])
    return (
            <Container>
                <Responsive>{normal_header(group.group)}</Responsive>
            </Container>
    )
}