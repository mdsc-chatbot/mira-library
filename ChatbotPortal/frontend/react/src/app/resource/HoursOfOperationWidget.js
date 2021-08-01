import React from 'react';
import PropTypes from 'prop-types';
import axios, {CancelToken} from 'axios';
import {Table, Tab, Button, SegmentGroup} from 'semantic-ui-react';
import {SecurityContext} from "../contexts/SecurityContext";


export default class HoursOfOperationWidget extends React.Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
        };
    }

    render()
    {
        this.props.hourBools = this.props.hourBools

        //I'm sorry for the mess, but it's 5am and my programatic solution isn't working
        return (
            <div>
                <h4>Enter hours of operation for this resource (GMT-6)</h4>
                <Tab
                    panes= 
                    {
                            [
                                { menuItem: 'Monday', render: () => 
                                    <Tab.Pane>
                                        <Table mondayhours>
                                            <Table.Body>
                                            <Table.Row>
                                                <Table.Cell>AM</Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][0]} onClick={() => this.props.hourBools[0][0] = !this.props.hourBools[0][0]}>
                                                        1 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][1]} onClick={() => this.props.hourBools[0][1] = !this.props.hourBools[0][1]}>
                                                        2 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][2]} onClick={() => this.props.hourBools[0][2] = !this.props.hourBools[0][2]}>
                                                        3 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][3]} onClick={() => this.props.hourBools[0][3] = !this.props.hourBools[0][3]}>
                                                        4 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][4]} onClick={() => this.props.hourBools[0][4] = !this.props.hourBools[0][4]}>
                                                        5 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][5]} onClick={() => this.props.hourBools[0][5] = !this.props.hourBools[0][5]}>
                                                        6 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][6]} onClick={() => this.props.hourBools[0][6] = !this.props.hourBools[0][6]}>
                                                        7 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][7]} onClick={() => this.props.hourBools[0][7] = !this.props.hourBools[0][7]}>
                                                        8 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][8]} onClick={() => this.props.hourBools[0][8] = !this.props.hourBools[0][8]}>
                                                        9 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][9]} onClick={() => this.props.hourBools[0][9] = !this.props.hourBools[0][9]}>
                                                        10 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][10]} onClick={() => this.props.hourBools[0][10] = !this.props.hourBools[0][10]}>
                                                        11 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][11]} onClick={() => this.props.hourBools[0][11] = !this.props.hourBools[0][11]}>
                                                        12 AM
                                                    </Button>
                                                </Table.Cell>
                                            </Table.Row>
                                            <Table.Row>
                                                <Table.Cell>PM</Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][12]} onClick={() => this.props.hourBools[0][12] = !this.props.hourBools[0][12]}>
                                                        1 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][13]} onClick={() => this.props.hourBools[0][13] = !this.props.hourBools[0][13]}>
                                                        2 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][14]} onClick={() => this.props.hourBools[0][14] = !this.props.hourBools[0][14]}>
                                                        3 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][15]} onClick={() => this.props.hourBools[0][15] = !this.props.hourBools[0][15]}>
                                                        4 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][16]} onClick={() => this.props.hourBools[0][16] = !this.props.hourBools[0][16]}>
                                                        5 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][17]} onClick={() => this.props.hourBools[0][17] = !this.props.hourBools[0][17]}>
                                                        6 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][18]} onClick={() => this.props.hourBools[0][18] = !this.props.hourBools[0][18]}>
                                                        7 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][19]} onClick={() => this.props.hourBools[0][19] = !this.props.hourBools[0][19]}>
                                                        8 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][20]} onClick={() => this.props.hourBools[0][20] = !this.props.hourBools[0][20]}>
                                                        9 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][21]} onClick={() => this.props.hourBools[0][21] = !this.props.hourBools[0][21]}>
                                                        10 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][22]} onClick={() => this.props.hourBools[0][22] = !this.props.hourBools[0][22]}>
                                                        11 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[0][23]} onClick={() => this.props.hourBools[0][23] = !this.props.hourBools[0][23]}>
                                                        12 PM
                                                    </Button>
                                                </Table.Cell>
                                            </Table.Row>
                                            </Table.Body>
                                        </Table>
                                    </Tab.Pane> },
                                { menuItem: 'Tuesday', render: () => 
                                    <Tab.Pane>
                                        <Table tuesdayhours>
                                            <Table.Body>
                                            <Table.Row>
                                                <Table.Cell>AM</Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][0]} onClick={() => this.props.hourBools[1][0] = !this.props.hourBools[1][0]}>
                                                        1 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][1]} onClick={() => this.props.hourBools[1][1] = !this.props.hourBools[1][1]}>
                                                        2 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][2]} onClick={() => this.props.hourBools[1][2] = !this.props.hourBools[1][2]}>
                                                        3 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][3]} onClick={() => this.props.hourBools[1][3] = !this.props.hourBools[1][3]}>
                                                        4 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][4]} onClick={() => this.props.hourBools[1][4] = !this.props.hourBools[1][4]}>
                                                        5 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][5]} onClick={() => this.props.hourBools[1][5] = !this.props.hourBools[1][5]}>
                                                        6 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][6]} onClick={() => this.props.hourBools[1][6] = !this.props.hourBools[1][6]}>
                                                        7 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][7]} onClick={() => this.props.hourBools[1][7] = !this.props.hourBools[1][7]}>
                                                        8 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][8]} onClick={() => this.props.hourBools[1][8] = !this.props.hourBools[1][8]}>
                                                        9 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][9]} onClick={() => this.props.hourBools[1][9] = !this.props.hourBools[1][9]}>
                                                        10 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][10]} onClick={() => this.props.hourBools[1][10] = !this.props.hourBools[1][10]}>
                                                        11 AM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][11]} onClick={() => this.props.hourBools[1][11] = !this.props.hourBools[1][11]}>
                                                        12 AM
                                                    </Button>
                                                </Table.Cell>
                                            </Table.Row>
                                            <Table.Row>
                                                <Table.Cell>PM</Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][12]} onClick={() => this.props.hourBools[1][12] = !this.props.hourBools[1][12]}>
                                                        1 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][13]} onClick={() => this.props.hourBools[1][13] = !this.props.hourBools[1][13]}>
                                                        2 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][14]} onClick={() => this.props.hourBools[1][14] = !this.props.hourBools[1][14]}>
                                                        3 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][15]} onClick={() => this.props.hourBools[1][15] = !this.props.hourBools[1][15]}>
                                                        4 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][16]} onClick={() => this.props.hourBools[1][16] = !this.props.hourBools[1][16]}>
                                                        5 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][17]} onClick={() => this.props.hourBools[1][17] = !this.props.hourBools[1][17]}>
                                                        6 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][18]} onClick={() => this.props.hourBools[1][18] = !this.props.hourBools[1][18]}>
                                                        7 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][19]} onClick={() => this.props.hourBools[1][19] = !this.props.hourBools[1][19]}>
                                                        8 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][20]} onClick={() => this.props.hourBools[1][20] = !this.props.hourBools[1][20]}>
                                                        9 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][21]} onClick={() => this.props.hourBools[1][21] = !this.props.hourBools[1][21]}>
                                                        10 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][22]} onClick={() => this.props.hourBools[1][22] = !this.props.hourBools[1][22]}>
                                                        11 PM
                                                    </Button>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Button toggle active={this.props.hourBools[1][23]} onClick={() => this.props.hourBools[1][23] = !this.props.hourBools[1][23]}>
                                                        12 PM
                                                    </Button>
                                                </Table.Cell>
                                            </Table.Row>
                                            </Table.Body>
                                        </Table>
                                    </Tab.Pane> },
                                { menuItem: 'Wednesday', render: () => 
                                    <Tab.Pane>
                                        <Table wednesdayhours>
                                                <Table.Body>
                                                <Table.Row>
                                                    <Table.Cell>AM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][0]} onClick={() => this.props.hourBools[2][0] = !this.props.hourBools[2][0]}>
                                                            1 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][1]} onClick={() => this.props.hourBools[2][1] = !this.props.hourBools[2][1]}>
                                                            2 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][2]} onClick={() => this.props.hourBools[2][2] = !this.props.hourBools[2][2]}>
                                                            3 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][3]} onClick={() => this.props.hourBools[2][3] = !this.props.hourBools[2][3]}>
                                                            4 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][4]} onClick={() => this.props.hourBools[2][4] = !this.props.hourBools[2][4]}>
                                                            5 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][5]} onClick={() => this.props.hourBools[2][5] = !this.props.hourBools[2][5]}>
                                                            6 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][6]} onClick={() => this.props.hourBools[2][6] = !this.props.hourBools[2][6]}>
                                                            7 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][7]} onClick={() => this.props.hourBools[2][7] = !this.props.hourBools[2][7]}>
                                                            8 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][8]} onClick={() => this.props.hourBools[2][8] = !this.props.hourBools[2][8]}>
                                                            9 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][9]} onClick={() => this.props.hourBools[2][9] = !this.props.hourBools[2][9]}>
                                                            10 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][10]} onClick={() => this.props.hourBools[2][10] = !this.props.hourBools[2][10]}>
                                                            11 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][11]} onClick={() => this.props.hourBools[2][11] = !this.props.hourBools[2][11]}>
                                                            12 AM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                <Table.Row>
                                                    <Table.Cell>PM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][12]} onClick={() => this.props.hourBools[2][12] = !this.props.hourBools[2][12]}>
                                                            1 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][13]} onClick={() => this.props.hourBools[2][13] = !this.props.hourBools[2][13]}>
                                                            2 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][14]} onClick={() => this.props.hourBools[2][14] = !this.props.hourBools[2][14]}>
                                                            3 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][15]} onClick={() => this.props.hourBools[2][15] = !this.props.hourBools[2][15]}>
                                                            4 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][16]} onClick={() => this.props.hourBools[2][16] = !this.props.hourBools[2][16]}>
                                                            5 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][17]} onClick={() => this.props.hourBools[2][17] = !this.props.hourBools[2][17]}>
                                                            6 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][18]} onClick={() => this.props.hourBools[2][18] = !this.props.hourBools[2][18]}>
                                                            7 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][19]} onClick={() => this.props.hourBools[2][19] = !this.props.hourBools[2][19]}>
                                                            8 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][20]} onClick={() => this.props.hourBools[2][20] = !this.props.hourBools[2][20]}>
                                                            9 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][21]} onClick={() => this.props.hourBools[2][21] = !this.props.hourBools[2][21]}>
                                                            10 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][22]} onClick={() => this.props.hourBools[2][22] = !this.props.hourBools[2][22]}>
                                                            11 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[2][23]} onClick={() => this.props.hourBools[2][23] = !this.props.hourBools[2][23]}>
                                                            12 PM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                </Table.Body>
                                            </Table>
                                    </Tab.Pane> },
                                { menuItem: 'Thursday', render: () => 
                                    <Tab.Pane>
                                        <Table thursdayhours>
                                                <Table.Body>
                                                <Table.Row>
                                                    <Table.Cell>AM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][0]} onClick={() => this.props.hourBools[3][0] = !this.props.hourBools[3][0]}>
                                                            1 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][1]} onClick={() => this.props.hourBools[3][1] = !this.props.hourBools[3][1]}>
                                                            2 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][2]} onClick={() => this.props.hourBools[3][2] = !this.props.hourBools[3][2]}>
                                                            3 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][3]} onClick={() => this.props.hourBools[3][3] = !this.props.hourBools[3][3]}>
                                                            4 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][4]} onClick={() => this.props.hourBools[3][4] = !this.props.hourBools[3][4]}>
                                                            5 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][5]} onClick={() => this.props.hourBools[3][5] = !this.props.hourBools[3][5]}>
                                                            6 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][6]} onClick={() => this.props.hourBools[3][6] = !this.props.hourBools[3][6]}>
                                                            7 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][7]} onClick={() => this.props.hourBools[3][7] = !this.props.hourBools[3][7]}>
                                                            8 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][8]} onClick={() => this.props.hourBools[3][8] = !this.props.hourBools[3][8]}>
                                                            9 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][9]} onClick={() => this.props.hourBools[3][9] = !this.props.hourBools[3][9]}>
                                                            10 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][10]} onClick={() => this.props.hourBools[3][10] = !this.props.hourBools[3][10]}>
                                                            11 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][11]} onClick={() => this.props.hourBools[3][11] = !this.props.hourBools[3][11]}>
                                                            12 AM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                <Table.Row>
                                                    <Table.Cell>PM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][12]} onClick={() => this.props.hourBools[3][12] = !this.props.hourBools[3][12]}>
                                                            1 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][13]} onClick={() => this.props.hourBools[3][13] = !this.props.hourBools[3][13]}>
                                                            2 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][14]} onClick={() => this.props.hourBools[3][14] = !this.props.hourBools[3][14]}>
                                                            3 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][15]} onClick={() => this.props.hourBools[3][15] = !this.props.hourBools[3][15]}>
                                                            4 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][16]} onClick={() => this.props.hourBools[3][16] = !this.props.hourBools[3][16]}>
                                                            5 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][17]} onClick={() => this.props.hourBools[3][17] = !this.props.hourBools[3][17]}>
                                                            6 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][18]} onClick={() => this.props.hourBools[3][18] = !this.props.hourBools[3][18]}>
                                                            7 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][19]} onClick={() => this.props.hourBools[3][19] = !this.props.hourBools[3][19]}>
                                                            8 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][20]} onClick={() => this.props.hourBools[3][20] = !this.props.hourBools[3][20]}>
                                                            9 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][21]} onClick={() => this.props.hourBools[3][21] = !this.props.hourBools[3][21]}>
                                                            10 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][22]} onClick={() => this.props.hourBools[3][22] = !this.props.hourBools[3][22]}>
                                                            11 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[3][23]} onClick={() => this.props.hourBools[3][23] = !this.props.hourBools[3][23]}>
                                                            12 PM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                </Table.Body>
                                            </Table>
                                    </Tab.Pane> },
                                { menuItem: 'Friday', render: () => 
                                    <Tab.Pane>
                                        <Table fridayhours>
                                                    <Table.Body>
                                                    <Table.Row>
                                                        <Table.Cell>AM</Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][0]} onClick={() => this.props.hourBools[4][0] = !this.props.hourBools[4][0]}>
                                                                1 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][1]} onClick={() => this.props.hourBools[4][1] = !this.props.hourBools[4][1]}>
                                                                2 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][2]} onClick={() => this.props.hourBools[4][2] = !this.props.hourBools[4][2]}>
                                                                3 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][3]} onClick={() => this.props.hourBools[4][3] = !this.props.hourBools[4][3]}>
                                                                4 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][4]} onClick={() => this.props.hourBools[4][4] = !this.props.hourBools[4][4]}>
                                                                5 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][5]} onClick={() => this.props.hourBools[4][5] = !this.props.hourBools[4][5]}>
                                                                6 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][6]} onClick={() => this.props.hourBools[4][6] = !this.props.hourBools[4][6]}>
                                                                7 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][7]} onClick={() => this.props.hourBools[4][7] = !this.props.hourBools[4][7]}>
                                                                8 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][8]} onClick={() => this.props.hourBools[4][8] = !this.props.hourBools[4][8]}>
                                                                9 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][9]} onClick={() => this.props.hourBools[4][9] = !this.props.hourBools[4][9]}>
                                                                10 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][10]} onClick={() => this.props.hourBools[4][10] = !this.props.hourBools[4][10]}>
                                                                11 AM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][11]} onClick={() => this.props.hourBools[4][11] = !this.props.hourBools[4][11]}>
                                                                12 AM
                                                            </Button>
                                                        </Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>PM</Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][12]} onClick={() => this.props.hourBools[4][12] = !this.props.hourBools[4][12]}>
                                                                1 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][13]} onClick={() => this.props.hourBools[4][13] = !this.props.hourBools[4][13]}>
                                                                2 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][14]} onClick={() => this.props.hourBools[4][14] = !this.props.hourBools[4][14]}>
                                                                3 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][15]} onClick={() => this.props.hourBools[4][15] = !this.props.hourBools[4][15]}>
                                                                4 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][16]} onClick={() => this.props.hourBools[4][16] = !this.props.hourBools[4][16]}>
                                                                5 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][17]} onClick={() => this.props.hourBools[4][17] = !this.props.hourBools[4][17]}>
                                                                6 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][18]} onClick={() => this.props.hourBools[4][18] = !this.props.hourBools[4][18]}>
                                                                7 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][19]} onClick={() => this.props.hourBools[4][19] = !this.props.hourBools[4][19]}>
                                                                8 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][20]} onClick={() => this.props.hourBools[4][20] = !this.props.hourBools[4][20]}>
                                                                9 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][21]} onClick={() => this.props.hourBools[4][21] = !this.props.hourBools[4][21]}>
                                                                10 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][22]} onClick={() => this.props.hourBools[4][22] = !this.props.hourBools[4][22]}>
                                                                11 PM
                                                            </Button>
                                                        </Table.Cell>
                                                        <Table.Cell>
                                                            <Button toggle active={this.props.hourBools[4][23]} onClick={() => this.props.hourBools[4][23] = !this.props.hourBools[4][23]}>
                                                                12 PM
                                                            </Button>
                                                        </Table.Cell>
                                                    </Table.Row>
                                                    </Table.Body>
                                                </Table>
                                    </Tab.Pane> },
                                { menuItem: 'Saturday', render: () => 
                                    <Tab.Pane>
                                        <Table saturdayhours>
                                                <Table.Body>
                                                <Table.Row>
                                                    <Table.Cell>AM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][0]} onClick={() => this.props.hourBools[5][0] = !this.props.hourBools[5][0]}>
                                                            1 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][1]} onClick={() => this.props.hourBools[5][1] = !this.props.hourBools[5][1]}>
                                                            2 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][2]} onClick={() => this.props.hourBools[5][2] = !this.props.hourBools[5][2]}>
                                                            3 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][3]} onClick={() => this.props.hourBools[5][3] = !this.props.hourBools[5][3]}>
                                                            4 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][4]} onClick={() => this.props.hourBools[5][4] = !this.props.hourBools[5][4]}>
                                                            5 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][5]} onClick={() => this.props.hourBools[5][5] = !this.props.hourBools[5][5]}>
                                                            6 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][6]} onClick={() => this.props.hourBools[5][6] = !this.props.hourBools[5][6]}>
                                                            7 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][7]} onClick={() => this.props.hourBools[5][7] = !this.props.hourBools[5][7]}>
                                                            8 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][8]} onClick={() => this.props.hourBools[5][8] = !this.props.hourBools[5][8]}>
                                                            9 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][9]} onClick={() => this.props.hourBools[5][9] = !this.props.hourBools[5][9]}>
                                                            10 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][10]} onClick={() => this.props.hourBools[5][10] = !this.props.hourBools[5][10]}>
                                                            11 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][11]} onClick={() => this.props.hourBools[5][11] = !this.props.hourBools[5][11]}>
                                                            12 AM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                <Table.Row>
                                                    <Table.Cell>PM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][12]} onClick={() => this.props.hourBools[5][12] = !this.props.hourBools[5][12]}>
                                                            1 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][13]} onClick={() => this.props.hourBools[5][13] = !this.props.hourBools[5][13]}>
                                                            2 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][14]} onClick={() => this.props.hourBools[5][14] = !this.props.hourBools[5][14]}>
                                                            3 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][15]} onClick={() => this.props.hourBools[5][15] = !this.props.hourBools[5][15]}>
                                                            4 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][16]} onClick={() => this.props.hourBools[5][16] = !this.props.hourBools[5][16]}>
                                                            5 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][17]} onClick={() => this.props.hourBools[5][17] = !this.props.hourBools[5][17]}>
                                                            6 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][18]} onClick={() => this.props.hourBools[5][18] = !this.props.hourBools[5][18]}>
                                                            7 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][19]} onClick={() => this.props.hourBools[5][19] = !this.props.hourBools[5][19]}>
                                                            8 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][20]} onClick={() => this.props.hourBools[5][20] = !this.props.hourBools[5][20]}>
                                                            9 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][21]} onClick={() => this.props.hourBools[5][21] = !this.props.hourBools[5][21]}>
                                                            10 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][22]} onClick={() => this.props.hourBools[5][22] = !this.props.hourBools[5][22]}>
                                                            11 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[5][23]} onClick={() => this.props.hourBools[5][23] = !this.props.hourBools[5][23]}>
                                                            12 PM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                </Table.Body>
                                            </Table>
                                    </Tab.Pane> },
                                { menuItem: 'Sunday', render: () => 
                                    <Tab.Pane>
                                        <Table sundayhours>
                                                <Table.Body>
                                                <Table.Row>
                                                    <Table.Cell>AM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][0]} onClick={() => this.props.hourBools[6][0] = !this.props.hourBools[6][0]}>
                                                            1 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][1]} onClick={() => this.props.hourBools[6][1] = !this.props.hourBools[6][1]}>
                                                            2 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][2]} onClick={() => this.props.hourBools[6][2] = !this.props.hourBools[6][2]}>
                                                            3 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][3]} onClick={() => this.props.hourBools[6][3] = !this.props.hourBools[6][3]}>
                                                            4 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][4]} onClick={() => this.props.hourBools[6][4] = !this.props.hourBools[6][4]}>
                                                            5 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][5]} onClick={() => this.props.hourBools[6][5] = !this.props.hourBools[6][5]}>
                                                            6 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][6]} onClick={() => this.props.hourBools[6][6] = !this.props.hourBools[6][6]}>
                                                            7 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][7]} onClick={() => this.props.hourBools[6][7] = !this.props.hourBools[6][7]}>
                                                            8 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][8]} onClick={() => this.props.hourBools[6][8] = !this.props.hourBools[6][8]}>
                                                            9 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][9]} onClick={() => this.props.hourBools[6][9] = !this.props.hourBools[6][9]}>
                                                            10 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][10]} onClick={() => this.props.hourBools[6][10] = !this.props.hourBools[6][10]}>
                                                            11 AM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][11]} onClick={() => this.props.hourBools[6][11] = !this.props.hourBools[6][11]}>
                                                            12 AM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                <Table.Row>
                                                    <Table.Cell>PM</Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][12]} onClick={() => this.props.hourBools[6][12] = !this.props.hourBools[6][12]}>
                                                            1 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][13]} onClick={() => this.props.hourBools[6][13] = !this.props.hourBools[6][13]}>
                                                            2 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][14]} onClick={() => this.props.hourBools[6][14] = !this.props.hourBools[6][14]}>
                                                            3 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][15]} onClick={() => this.props.hourBools[6][15] = !this.props.hourBools[6][15]}>
                                                            4 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][16]} onClick={() => this.props.hourBools[6][16] = !this.props.hourBools[6][16]}>
                                                            5 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][17]} onClick={() => this.props.hourBools[6][17] = !this.props.hourBools[6][17]}>
                                                            6 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][18]} onClick={() => this.props.hourBools[6][18] = !this.props.hourBools[6][18]}>
                                                            7 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][19]} onClick={() => this.props.hourBools[6][19] = !this.props.hourBools[6][19]}>
                                                            8 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][20]} onClick={() => this.props.hourBools[6][20] = !this.props.hourBools[6][20]}>
                                                            9 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][21]} onClick={() => this.props.hourBools[6][21] = !this.props.hourBools[6][21]}>
                                                            10 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][22]} onClick={() => this.props.hourBools[6][22] = !this.props.hourBools[6][22]}>
                                                            11 PM
                                                        </Button>
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button toggle active={this.props.hourBools[6][23]} onClick={() => this.props.hourBools[6][23] = !this.props.hourBools[6][23]}>
                                                            12 PM
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                                </Table.Body>
                                            </Table>
                                    </Tab.Pane> }
                            ]
                    }
                />
                </div>
        )
    }
}

HoursOfOperationWidget.proptype =
{
    hourBools: PropTypes.array
};