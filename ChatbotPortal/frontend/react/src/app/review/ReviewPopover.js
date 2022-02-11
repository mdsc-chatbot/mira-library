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
import { Table, Checkbox, Rating, Icon, Modal, Header, Button} from 'semantic-ui-react';
import { SecurityContext } from "../contexts/SecurityContext";
import axios from "axios";


export default class ReviewPopover extends React.Component {
    static contextType = SecurityContext;

    get_reviews_by_id = (resource_id, email_id) => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/api/review/", {
            headers: options 
        }).then(res => {
            //console.log(res.data)
            var entry = res.data.find(o => (o.resource_id === resource_id && o.reviewer_user_email === email_id));
            //console.log(resource_id)
            //console.log(email_id)
            //console.log(entry)
            this.setState({comment: entry.review_comments});
            this.setState({reviewData: JSON.parse(entry.question_answers)}); 
            this.populateAndCalculateScore();
        });
    }

    constructor(props) {
        super(props);

        this.state = {
            negativeCBoxQuestions: [8],
            boolQuestionIsNA: [],
            rateQuestionIsNA: [],
            questionBools: [],
            questionScores: [],
            bScore: 0,
            rScore: 0,
            treshholdScore: 73, //if the score goes beyond the resource is better to be accepted
            maxScore: 86, //max possible score that a resource can get (it can be changed by makinga question Not applicable)
            bHarmful: false,
            bViable: false,
            reviewData: [],
            isGoverment: false,
            isProfitCompanyOrDeveloper: false,
            isNonProfitCompany: false,
            isRegisteredCharity: false,
            isPublicHealthcareProvider: false,
            isAcademicInst: false,
            modals: [],
            comment: ""
        };

        for (var i = 0; i < 9; i++) this.state.questionBools.push(false);
        for (var i = 0; i < 7; i++) this.state.questionScores.push(0);
        for (var i = 0; i < 9; i++) this.state.boolQuestionIsNA.push(false);
        for (var i = 0; i < 7; i++) this.state.rateQuestionIsNA.push(false);
        for (var i = 0; i < 15; i++) this.state.modals.push(false);

        //this.populateAndCalculateScore();
        //console.log(this.props);
    }

    handleCBChange = (event, position) => {
        // const updatedCheckedState = this.state.questionBools.map((item, index) =>
        //     index === position ? !item : item
        // );
        // console.log('updatedCheckedState', updatedCheckedState);
        // this.setState({ questionBools: updatedCheckedState });

        // console.log(updatedCheckedState, this.state.negativeCBoxQuestions, position)
        // const totalScore = updatedCheckedState.reduce(
        //     (sum, currentState) => {
        //         if (currentState === true) {
        //             if (this.state.negativeCBoxQuestions.indexOf(position)!=-1){
        //                 console.log('negative clicked', this.state.negativeCBoxQuestions)
        //                 return sum-1
        //             } 
        //             return sum+1;
        //         }
        //         return sum;
        //     },
        //     0
        // );
        // this.setState({bScore: totalScore});
        // console.log('as',this.state)
    };
    handleCBNAChange = (event, position) => {
        // var isChecked = !event.currentTarget.firstChild.checked;
        // var newBoolQuestionIsNA = this.state.boolQuestionIsNA;
        // newBoolQuestionIsNA[position] = isChecked;
        // this.setState({ boolQuestionIsNA: newBoolQuestionIsNA })
        // var element = document.getElementById(("checkbox" + position));
        // isChecked ? element.parentElement.classList.add("invisiblee") : element.parentElement.classList.remove("invisiblee");
        // this.calculateScore();
    };

    handleRTChange = (event, position, rating, maxRating) => {
        // const updatedRateState = this.state.questionScores.map((item, index) =>
        //     index === position ? rating : this.state.questionScores[index]
        // );
        // this.setState({ questionScores: updatedRateState });

        // const totalScore = updatedRateState.reduce(
        //     (sum, currentState) => {
        //         return sum+currentState;
        //     },
        //     0
        // );
        // this.setState({rScore: totalScore});
    };
    handleRTNAChange = (event, position) => {
        // var isChecked = !event.currentTarget.firstChild.checked;
        // var newRateQuestionIsNA = this.state.rateQuestionIsNA;
        // newRateQuestionIsNA[position] = isChecked;
        // this.setState({ rateQuestionIsNA: newRateQuestionIsNA })
        // var element = document.getElementById(("rating" + position));
        // console.log(isChecked, element, position)
        // isChecked ? element.parentElement.classList.add('invisiblee') : element.parentElement.classList.remove('invisiblee');

        // this.calculateScore();
        // var element = document.getElementById(("rating" + position));
        // element.classList.remove('invisiblee');
    };

    handleOrgCBChange = (checkBoxName) => {
        // checkBoxName == 'isGoverment' ? this.setState({ isGoverment: !this.state.isGoverment }) :
        //     checkBoxName == 'isProfitCompanyOrDeveloper' ? this.setState({ isProfitCompanyOrDeveloper: !this.state.isProfitCompanyOrDeveloper }) :
        //         checkBoxName == 'isNonProfitCompany' ? this.setState({ isNonProfitCompany: !this.state.isNonProfitCompany }) :
        //             checkBoxName == 'isRegisteredCharity' ? this.setState({ isRegisteredCharity: !this.state.isRegisteredCharity }) :
        //                 checkBoxName == 'isPublicHealthcareProvider' ? this.setState({ isPublicHealthcareProvider: !this.state.isPublicHealthcareProvider }) :
        //                     checkBoxName == 'isAcademicInst' ? this.setState({ isAcademicInst: !this.state.isAcademicInst }) : null;
    }

    componentDidUpdate(previousProps, previousState) {
        // console.log('calculating...', this.state.questionScores, previousState.questionScores)
        // if (previousState.questionBools != this.state.questionBools ||
        //     previousState.questionScores != this.state.questionScores ||
        //     previousState.boolQuestionIsNA != this.state.boolQuestionIsNA ||
        //     previousState.rateQuestionIsNA != this.state.rateQuestionIsNA) {
        //     this.calculateScore();
        // }
    }

    populateAndCalculateScore = () => {
        var rScore = 0;
        var bScore = 0;
        var maxScore = 0;
        var questionBools = this.state.questionBools;
        var questionScores = this.state.questionScores;
        var boolQuestionIsNA = this.state.boolQuestionIsNA;

        //console.log(this.state.reviewData);

        //checkboxes
        for (var i = 0; i < questionBools.length; i++) {
            //get bool question by number
            var response = this.state.reviewData["QA_array"][i];
            if (response["answer"]=="NA") {
                // NA
                boolQuestionIsNA[i] = true;
            } else {
                // Assigned
                if (this.state.negativeCBoxQuestions.includes(i)) {
                    // negative impact
                    if (response["answer"]=="-2") {
                        // checked
                        questionBools[i]=true;
                    } else {
                        // not checked
                        questionBools[i]=false;
                    }
                } else {
                    // positive impact
                    if (response["answer"]=="2") {
                        // checked
                        questionBools[i]=true;
                    } else {
                        // not checked
                        questionBools[i]=false;
                    }
                }
            }
        }
        //ratings
        for (var i = 0; i < questionScores.length; i++) {
            var response = this.state.reviewData["QA_array"][i+questionBools.length];
            if (response["answer"]=="NA") {
                // NA
                questionScores[i] = 0;
            } else {
                questionScores[i] = parseInt(response["answer"])/2;
            }
        }

        //set org bools
        this.setState({isGoverment: this.state.reviewData["organizationType"]["isGovernment"]});
        this.setState({isProfitCompanyOrDeveloper: this.state.reviewData["organizationType"]["isProfitCompanyOrDeveloper"]});
        this.setState({isNonProfitCompany: this.state.reviewData["organizationType"]["isNonProfitCompany"]});
        this.setState({isRegisteredCharity: this.state.reviewData["organizationType"]["isRegisteredCharity"]});
        this.setState({isPublicHealthcareProvider: this.state.reviewData["organizationType"]["isPublicHealthcareProvider"]});
        this.setState({isAcademicInst: this.state.reviewData["organizationType"]["isAcademicInst"]});

        //read various scores
        bScore = this.state.reviewData["bScore"] / 2
        rScore = this.state.reviewData["rScore"] / 2
        maxScore = this.state.reviewData["maxScore"]

        //update everything
        this.setState({ bScore });
        this.setState({ rScore });
        this.setState({ maxScore });
        this.setState({ questionBools })
        this.setState({ questionScores })
        this.setState({ boolQuestionIsNA })
        
    }

    toggleHarm = () => {}// this.setState((prevState) => ({ bHarmful: !prevState.bHarmful }))
    toggleViable = () => {}//this.setState((prevState) => ({ bViable: !prevState.bViable }))
    setModalState = (isOpen, index) => {
        var newModals = this.state.modals
        newModals[index] = isOpen
        this.setState({modals:newModals})
    }

    render() {
        return (
            <React.Fragment>
                <Modal
                    onClose={() => {this.setModalState(false,15);}}
                    onOpen={() => 
                        {
                            this.get_reviews_by_id(this.props.resId, this.props.revId);
                            this.setModalState(true,15);
                        }
                    }
                    open={this.state.modals[15]}
                    trigger={<Icon name="columns"/>}
                >
                    <Modal.Header>Review Evaluation Matrix</Modal.Header>
                    <Modal.Content matrix>
                        <h2>Submission Quality</h2>
                        <Table collapsing>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell width={7}>Section 1: Source of Resource</Table.HeaderCell>
                                    <Table.HeaderCell width={7}></Table.HeaderCell>
                                    <Table.HeaderCell width={2}>Not Applicable (NA)</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>

                            <Table.Body>
                                <Table.Row>
                                    <Table.Cell>Where does the resource come from? (Check all that apply)
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,14)}
                                        onOpen={() => this.setModalState(true,14)}
                                        open={this.state.modals[14]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Where does the resource come from? (Check all that apply)
                                        </Header>
                                        <Modal.Content>
                                        <p><span>The difference between a registered charity and a non-profit organization is outlined <a target="_blank" href="https://www.canada.ca/en/revenue-agency/services/charities-giving/giving-charity-information-donors/about-registered-charities/what-difference-between-a-registered-charity-a-non-profit-organization.html">here</a>, organization websites will indicate their registered status. Multiple selections are enabled, this may be used if a resource is the result of a collaborative effort. </span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,14)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled onChange={(e) => this.handleOrgCBChange('isGoverment')} checked={this.state.isGoverment} label='Government' /></div>
                                        <div><Checkbox disabled onChange={(e) => this.handleOrgCBChange('isProfitCompanyOrDeveloper')} checked={this.state.isProfitCompanyOrDeveloper} label='For profit company or developer' /></div>
                                        <div><Checkbox disabled onChange={(e) => this.handleOrgCBChange('isNonProfitCompany')} checked={this.state.isNonProfitCompany} label='Non-profit company' /></div>
                                        <div><Checkbox disabled onChange={(e) => this.handleOrgCBChange('isRegisteredCharity')} checked={this.state.isRegisteredCharity} label='Registered charity' /></div>
                                        <div><Checkbox disabled onChange={(e) => this.handleOrgCBChange('isPublicHealthcareProvider')} checked={this.state.isPublicHealthcareProvider} label='A public healthcare provider' /></div>
                                        <div><Checkbox disabled onChange={(e) => this.handleOrgCBChange('isAcademicInst')} checked={this.state.isAcademicInst} label='Academic institution' /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Could this organization or company have a conflict of interest in providing this resource?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,13)}
                                        onOpen={() => this.setModalState(true,13)}
                                        open={this.state.modals[13]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Could this organization or company have a conflict of interest in providing this resource?
                                        </Header>
                                        <Modal.Content>
                                        <p>Does this organization have a self-serving interest in providing this resource, that could arguably bias the resource and/or information they are providing?</p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,13)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="yes" checked={this.state.questionBools[8]} id='checkbox8' onChange={(e) => this.handleCBChange(e, 8)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[8]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 8)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                            </Table.Body>
                        </Table>
                        <Table collapsing>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell width={7}>Section 2: Readability</Table.HeaderCell>
                                    <Table.HeaderCell width={7}></Table.HeaderCell>
                                    <Table.HeaderCell width={2}>Not Applicable (NA)</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                <Table.Row>
                                    <Table.Cell>The material uses common, everyday language
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,12)}
                                        onOpen={() => this.setModalState(true,12)}
                                        open={this.state.modals[12]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            The material uses common, everyday language
                                        </Header>
                                        <Modal.Content>
                                        <p><span>For further guidance, consult the Plain Language Writing Checklist from <a target="_blank" href="https://www.sickkids.ca/contentassets/92c5abda231e44b6832f5e3effeacdf8/plain-language-checklist_jan2017-sickkids-kt-program.pdf">SickKids</a>.</span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,12)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[0]} id='checkbox0' onChange={(e) => this.handleCBChange(e, 0)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[0]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 0)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Medical terms are used only to familiarize the audience with the terms. When used, medical terms are defined</Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[1]} id='checkbox1' onChange={(e) => this.handleCBChange(e, 1)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[1]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 1)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                {/* <Table.Row>
                                    <Table.Cell>The material uses the active voice</Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox label="If yes, check box. If no, leave blank." checked={this.state.questionBools[2]} id='checkbox2' onChange={(e) => this.handleCBChange(e, 2)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox checked={this.state.boolQuestionIsNA[2]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 2)} /></div>
                                    </Table.Cell>
                                </Table.Row> */}
                            </Table.Body>
                        </Table>
                        <Table collapsing>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell width={7}>Section 3: Accessibility</Table.HeaderCell>
                                    <Table.HeaderCell width={7}></Table.HeaderCell>
                                    <Table.HeaderCell width={2}>Not Applicable (NA)</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>

                            <Table.Body>
                                <Table.Row>
                                    <Table.Cell>Does the resource provide at least one accessibility feature (like adjust text size, text to voice, or colourblind colour scheme)?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,11)}
                                        onOpen={() => this.setModalState(true,11)}
                                        open={this.state.modals[11]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Does the resource provide at least one accessibility feature (like adjust text size, text to voice, or colourblind colour scheme)?
                                        </Header>
                                        <Modal.Content>
                                        <p><span>The </span><a target="_blank" href="https://wave.webaim.org/extension/"><span>WAVE</span></a><span> website (and browser extensions) can assist in contrast checking and other elements of accessibility.</span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,11)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[2]} id='checkbox2' onChange={(e) => this.handleCBChange(e, 2)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[2]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 2)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is the resource available in French?</Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[3]} id='checkbox3' onChange={(e) => this.handleCBChange(e, 3)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[3]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 3)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is the resource available in a language other than English and French?</Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[4]} id='checkbox4' onChange={(e) => this.handleCBChange(e, 4)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[4]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 4)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is the resource free?</Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[5]} id='checkbox5' onChange={(e) => this.handleCBChange(e, 5)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[5]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 5)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                            </Table.Body>
                        </Table>
                        <Table collapsing>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell width={7}>Section 4: Resource Quality</Table.HeaderCell>
                                    <Table.HeaderCell width={7}></Table.HeaderCell>
                                    <Table.HeaderCell width={2}>Not Applicable (NA)</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>

                            <Table.Body>
                                <Table.Row>
                                    <Table.Cell>Are the aims clear? 
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,0)}
                                        onOpen={() => this.setModalState(true,0)}
                                        open={this.state.modals[0]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Are the aims clear?
                                        </Header>
                                        <Modal.Content>
                                            <p><span>Look for clear indication at the beginning of the resource of&nbsp;</span></p>
                                            <ol>
                                            <li aria-level="1"><span>What is it about?&nbsp;</span></li>
                                            <li aria-level="1"><span>What is meant to cover (and what topics are excluded)?</span></li>
                                            <li aria-level="1"><span>Who might find it useful?</span></li>
                                            </ol>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,0)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating disabled id='rating0' icon="star" min={1} maxRating={5} rating={this.state.questionScores[0]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[0]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 0)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Does it achieve its aims?  
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,1)}
                                        onOpen={() => this.setModalState(true,1)}
                                        open={this.state.modals[1]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Does it achieve its aims? 
                                        </Header>
                                        <Modal.Content>
                                            <p>Consider whether the resource provides the information and/or service as outlined above.</p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,1)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating disabled id='rating1' icon="star" min={1} maxRating={5} rating={this.state.questionScores[1]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[1]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 1)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is it relevant? 
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,2)}
                                        onOpen={() => this.setModalState(true,2)}
                                        open={this.state.modals[2]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Is it relevant? 
                                        </Header>
                                        <Modal.Content>
                                            <p><span>Consider whether:&nbsp;</span></p>
                                            <ol>
                                            <li aria-level="1"><span>The resource addresses the question the client may ask. &nbsp;</span></li>
                                            <li aria-level="1"><span>The resource addresses the need the client may have in accessing it.</span></li>
                                            </ol>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,2)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating disabled id='rating2' icon="star" min={1} maxRating={5} rating={this.state.questionScores[2]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[2]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 2)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is it clear what sources of information were used to compile the resource (other than the author or producer)?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,3)}
                                        onOpen={() => this.setModalState(true,3)}
                                        open={this.state.modals[3]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Is it clear what sources of information were used to compile the resource (other than the author or producer)? 
                                        </Header>
                                        <Modal.Content>
                                        <p>Check whether the main claims or statements made about mental health topics are accompanied by a reference to the sources used as evidence, e.g. a research study or expert opinion. Look for a means of checking the sources used such as a bibliography/reference list, or the addresses of the experts or organizations quoted, or external links to the online sources.</p>
                                        <p><strong>In order to score a full 5, the resources should fulfill both of these conditions.</strong> Lists of additional sources of support and information* are not necessarily sources of evidence for the current resource.</p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,3)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating disabled id='rating3' icon="star" min={1} maxRating={5} rating={this.state.questionScores[3]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[3]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 3)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is it clear when the information used or reported in the resource was produced?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,4)}
                                        onOpen={() => this.setModalState(true,4)}
                                        open={this.state.modals[4]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Is it clear when the information used or reported in the resource was produced?
                                        </Header>
                                        <Modal.Content>
                                        <p><span>Look for dates of the main sources of information used to compile the resource, as well as the date of resource publication (or copyright date). </span><strong>In order to score a full 5, these dates must be found.</strong></p>
                                        <p><span>If the resource is a forum, check to ensure responses to client questions are being addressed in a timely manner (less than 24 hours for a response to the initial post). </span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,4)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating disabled id='rating4' icon="star" min={1} maxRating={5} rating={this.state.questionScores[4]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[4]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 4)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is it balanced or unbiased?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,5)}
                                        onOpen={() => this.setModalState(true,5)}
                                        open={this.state.modals[5]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Is it balanced or unbiased?
                                        </Header>
                                        <Modal.Content>
                                        <p><span>Look for a clear indication of whether the resource is written from a personal or objective point of view. Check to see that a range of sources of information was used to compile the resource, e.g. more than one research study or expert (if applicable), or evidence of an external assessment of the resource.&nbsp;</span></p>
                                        <p><strong>Be wary if</strong><span>: the resource relies primarily on evidence from single cases (if applicable), or the information is presented in a sensational, emotive, or alarmist way.</span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,5)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating id='rating5' icon="star" min={1} maxRating={5} rating={this.state.questionScores[5]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[5]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 5)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Does it provide details of additional sources of support and information?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,6)}
                                        onOpen={() => this.setModalState(true,6)}
                                        open={this.state.modals[6]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Does it provide details of additional sources of support and information?
                                        </Header>
                                        <Modal.Content>
                                        <p><span>Look for suggestions of further reading, or for details of other organisations providing advice and information about the mental health topic being addressed.&nbsp;</span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,6)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Rating id='rating6' icon="star" min={1} maxRating={5} rating={this.state.questionScores[6]} /> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.rateQuestionIsNA[6]} label='Not Applicable (NA)' onChange={(e) => this.handleRTNAChange(e, 6)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Is the resource patient facing?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,7)}
                                        onOpen={() => this.setModalState(true,7)}
                                        open={this.state.modals[7]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Is the resource patient facing?
                                        </Header>
                                        <Modal.Content>
                                        <p><span>Is the resource relevant for an individual with the conditions specified? Is it intended for patient use generally?&nbsp;</span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,7)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[6]} id='checkbox6' onChange={(e) => this.handleCBChange(e, 6)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[6]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 6)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Does the resource provide any cautions?
                                    <Modal
                                        basic
                                        onClose={() => this.setModalState(false,8)}
                                        onOpen={() => this.setModalState(true,8)}
                                        open={this.state.modals[8]}
                                        size='small'
                                        trigger={<Icon color="blue" name='info circle'/>}
                                        >
                                        <Header icon>
                                            <Icon name='info circle' />
                                            Does the resource provide any cautions?
                                        </Header>
                                        <Modal.Content>
                                        <p><span>Is there any warning for a user that the resource is not intended to replace medical care? Is there an emergency phone number on the website to help direct someone in significant distress?&nbsp;</span></p>
                                        </Modal.Content>
                                        <Modal.Actions>
                                            <Button disabled basic color='blue' inverted onClick={() => this.setModalState(false,8)}>
                                            <Icon name='checkmark' /> OK
                                            </Button>
                                        </Modal.Actions>
                                    </Modal>    
                                    </Table.Cell>
                                    <Table.Cell>
                                        <div><Checkbox disabled label="If yes, check box. If no, leave blank." checked={this.state.questionBools[7]} id='checkbox7' onChange={(e) => this.handleCBChange(e, 7)} /></div>
                                    </Table.Cell>
                                    <Table.Cell warning>
                                        <div><Checkbox disabled checked={this.state.boolQuestionIsNA[7]} label='Not Applicable (NA)' onChange={(e) => this.handleCBNAChange(e, 7)} /></div>
                                    </Table.Cell>
                                </Table.Row>
                            </Table.Body>
                        </Table>
                        {((this.state.bScore + this.state.rScore) * 2 / this.state.maxScore).toFixed(2) > (this.state.treshholdScore / 100)
                            ? <h3 class="ui green header">Score:{(this.state.bScore + this.state.rScore) * 2}/{this.state.maxScore} </h3>
                            :
                            <h3 class="ui red header">Score:{(this.state.bScore + this.state.rScore) * 2}/{this.state.maxScore}</h3>
                        }
                        <h3>Comments: {this.state.comment}</h3>
                    </Modal.Content>
                    <Modal.Actions>
                        <Button color='black' onClick={() => this.setModalState(false,15)}>
                        Close
                        </Button>
                    </Modal.Actions>
                </Modal>
            </React.Fragment>
        );
    }
}