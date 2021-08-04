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
 import {Table, Checkbox, Rating} from 'semantic-ui-react';
 import {SecurityContext} from "../contexts/SecurityContext";
 
 
 export default class ReviewMatrix extends React.Component {
     static contextType = SecurityContext;

 
     constructor(props) {
         super(props);
 
         this.state = {
             questionBools: [],
             questionScores: [],
             bScore: 0,
             rScore: 0,
             bHarmful: false,
             bViable: false
         };

         for(var i = 0; i < 9; i++) this.state.questionBools.push(false);
         for(var i = 0; i < 7; i++) this.state.questionScores.push(0);
     }
 
    handleCBChange = (event, position) => {
        const updatedCheckedState = this.state.questionBools.map((item, index) =>
            index === position ? !item : item
        );
    
        this.setState({questionBools: updatedCheckedState});
        const totalScore = updatedCheckedState.reduce(
            (sum, currentState) => {
                if (currentState === true) {
                    return sum + 1;
                }
                return sum;
            },
            0
        );
        this.setState({bScore: totalScore});
    };

    handleRTChange = (event, position, rating, maxRating ) => {
        console.log(rating)
        const updatedRateState = this.state.questionScores.map((item, index) =>
            index === position ? rating : this.state.questionScores[index]
        );
        console.log(updatedRateState)
        this.setState({questionScores: updatedRateState});
    
        const totalScore = updatedRateState.reduce(
            (sum, currentState) => {
                return sum+currentState;
            },
            0
        );
        console.log(totalScore)
        this.setState({rScore: totalScore});
    };

    toggleHarm = () => this.setState((prevState) => ({ bHarmful: !prevState.bHarmful }))
    toggleViable = () => this.setState((prevState) => ({ bViable: !prevState.bViable }))
 
     render() {
         return (
             <React.Fragment>
                 <h2>Submission Quality</h2>
                <Table collapsing>
                    <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={20}>Section 1: Source of Resource</Table.HeaderCell>
                        <Table.HeaderCell width={10}></Table.HeaderCell>
                    </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        <Table.Row>
                            <Table.Cell >Where does the resource come from? (Check all that apply)</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox label='Government' /></div>
                                <div><Checkbox label='For profit company or developer' /></div>
                                <div><Checkbox label='Non-profit company' /></div>
                                <div><Checkbox label='A public healthcare provider' /></div>
                                <div><Checkbox label='Academic institution' /></div>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                <Table collapsing>
                    <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={20}>Section 2: Readability</Table.HeaderCell>
                        <Table.HeaderCell width={10}></Table.HeaderCell>
                    </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        <Table.Row>
                            <Table.Cell>The material uses common, everyday language</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 0)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Medical terms are used only to familiarize the audience with the terms. When used, medical terms are defined</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 1)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>The material uses the active voice</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 2)}/></div>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                <Table collapsing>
                    <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={20}>Section 3: Accessibility</Table.HeaderCell>
                        <Table.HeaderCell width={10}></Table.HeaderCell>
                    </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        <Table.Row>
                            <Table.Cell>Does it have at least one accessibility feature (like adjust text size, text to voice, or colourblind colour scheme)?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 3)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it work with French?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 4)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it work with a language other than English and French?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 5)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is the resource free?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 6)}/></div>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                <Table collapsing>
                    <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={20}>Section 4: Resource Quality</Table.HeaderCell>
                        <Table.HeaderCell width={10}></Table.HeaderCell>
                    </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        <Table.Row>
                            <Table.Cell>Are the aims clear?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 0, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it achieve it's aims?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 1, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it relevent?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 2, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it clear what sources of information were used to compile the resource (other than the author or producer)?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 3, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it clear when the information used or reported in the resource was produced?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 4, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it balanced or unbiased?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 5, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it provide details of additional sources of support and information?</Table.Cell>
                            <Table.Cell>
                                <div><Rating min={0} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 6, rating, maxRating)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is the resource patient facing?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 7)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does the resource provide any cautions?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleCBChange(e, 8)}/></div>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                <Table collapsing>
                    <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={20}>Section 5: Overall</Table.HeaderCell>
                        <Table.HeaderCell width={10}></Table.HeaderCell>
                    </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        <Table.Row>
                            <Table.Cell>Is the resource still viable/functional?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={this.toggleViable} checked={this.state.bViable}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Can the resource cause harm?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={this.toggleHarm} checked={this.state.bHarmful}/></div>
                            </Table.Cell>
                        </Table.Row>
                        {/*<Table.Row>
                            <Table.Cell>Quality based on the supplied answers.</Table.Cell>
                            <Table.Cell>
                                <div><Rating rating={(((this.state.bScore+this.state.rScore)*5)/49).toFixed(0)} maxRating={5} disabled/></div>
                            </Table.Cell>
                        </Table.Row>*/}
                    </Table.Body>
                </Table>
                <h3> {(((this.state.bScore+this.state.rScore)*100)/49).toFixed(0) > 75 && !this.state.bHarmful && this.state.bViable
                    ? 'This resource passes all given criteria. Approval is recommended. If you feel it necessary to reject this resource, please explain why in the review comments.'
                    : 'This resource does not meet the minimum standards for approval. If you feel it necessary to approve this resource, please explain why in the review comments.'
                }
                </h3>
             </React.Fragment>
         );
     }
 }
 
 //ReviewMatrix.propTypes = {
 //    value: PropTypes.array,
 //    onChange: PropTypes.func
 //};