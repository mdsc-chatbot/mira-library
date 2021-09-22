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
 import {Table, Checkbox, Rating, Popup, Icon} from 'semantic-ui-react';
 import {SecurityContext} from "../contexts/SecurityContext";
 
 
 export default class ReviewMatrix extends React.Component {
     static contextType = SecurityContext;

 
     constructor(props) {
         super(props);
 
         this.state = {
             negativeCBoxQuestions: [9],
             boolQuestionIsNA: [],
             rateQuestionIsNA: [],
             questionBools: [],
             questionScores: [],
             bScore: 0,
             rScore: 0,
             treshholdScore: 73, //if the score goes beyond the resource is better to be accepted
             maxScore: 90, //max possible score that a resource can get (it can be changed by makinga question Not applicable)
             bHarmful: false,
             bViable: false,
             reviewData: {},
             isGoverment: false,
             isProfitCompanyOrDeveloper: false,
             isNonProfitCompany: false,
             isRegisteredCharity: false,
             isPublicHealthcareProvider: false,
             isAcademicInst: false,
         };

         for(var i = 0; i < 10; i++) this.state.questionBools.push(false);
         for(var i = 0; i < 7; i++) this.state.questionScores.push(0);
         for(var i = 0; i < 10; i++) this.state.boolQuestionIsNA.push(false);
         for(var i = 0; i < 7; i++) this.state.rateQuestionIsNA.push(false);
    }
 
    handleCBChange = (event, position) => {
        const updatedCheckedState = this.state.questionBools.map((item, index) =>
            index === position ? !item : item
        );
        console.log('updatedCheckedState', updatedCheckedState);
        this.setState({questionBools: updatedCheckedState});

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
        var isChecked = !event.currentTarget.firstChild.checked;
        var newBoolQuestionIsNA = this.state.boolQuestionIsNA;
        newBoolQuestionIsNA[position] = isChecked;
        this.setState({boolQuestionIsNA:newBoolQuestionIsNA})
        var element = document.getElementById(("checkbox"+position));
        isChecked ? element.parentElement.classList.add("invisiblee") : element.parentElement.classList.remove("invisiblee");
        this.calculateScore();

        
        // if(isChecked){
            // const updatedCheckedState = this.state.questionBools.map((item, index) =>
            //     index === position ? false : item
            // );
            // this.setState({questionBools: updatedCheckedState});
            // var element = document.getElementById(("checkbox"+position));
            // element.parentElement.classList.add("invisiblee");
            // element.parentElement.classList.remove("checked");

        //     const totalScore = this.state.questionBools.reduce(
        //         (sum, currentState, currentIndex) => {
        //             if(currentIndex === position) return sum;
        //             if (currentState === true) {
        //                 if (this.state.negativeCBoxQuestions.indexOf(position)!=-1) return sum
        //                 return sum + 1;
        //             }
        //             return sum;
        //         },
        //         0
        //     );
        //     this.setState({bScore: totalScore});
        // }else{
        //     var element = document.getElementById(("checkbox"+position));
        //     element.parentElement.classList.remove("invisiblee");
        //     const wasChecked = element.parentElement.className.includes('checked');
        //     wasChecked? element.parentElement.classList.add("checked"):element.parentElement.classList.add("checked");
        //     const updatedCheckedState = this.state.questionBools.map((item, index) =>
        //         index === position ? wasChecked : item
        //     );
        //     this.setState({questionBools: updatedCheckedState});
        //     const totalScore = updatedCheckedState.reduce(
        //         (sum, currentState) => {
        //             if (currentState === true) {
        //                 if (this.state.negativeCBoxQuestions.indexOf(position)!=-1){
        //                     return sum-1
        //                 } 
        //                 return sum + 1;
        //             }
        //             return sum;
        //         },
        //         0
        //     );
        //     this.setState({bScore: totalScore});
        // }

        // if(this.state.negativeCBoxQuestions.indexOf(position)==-1){
        //     isChecked ? this.setState({maxScore: this.state.maxScore - 2}) : this.setState({maxScore: this.state.maxScore + 2});
        // }else{
        //     isChecked ? this.setState({maxScore: this.state.maxScore - 2}) : this.setState({maxScore: this.state.maxScore + 2});
        // }
    };

    handleRTChange = (event, position, rating, maxRating ) => {
        const updatedRateState = this.state.questionScores.map((item, index) =>
            index === position ? rating : this.state.questionScores[index]
        );
        this.setState({questionScores: updatedRateState});
    
        // const totalScore = updatedRateState.reduce(
        //     (sum, currentState) => {
        //         return sum+currentState;
        //     },
        //     0
        // );
        // this.setState({rScore: totalScore});
    };
    handleRTNAChange = (event, position) => {
        var isChecked = !event.currentTarget.firstChild.checked;
        var newRateQuestionIsNA = this.state.rateQuestionIsNA;
        newRateQuestionIsNA[position] = isChecked;
        this.setState({rateQuestionIsNA:newRateQuestionIsNA})
        var element = document.getElementById(("rating"+position));
        console.log(isChecked, element, position)
        isChecked ? element.parentElement.classList.add('invisiblee') : element.parentElement.classList.remove('invisiblee');

        this.calculateScore();

        // if(isChecked){
        //     const updatedRateState = this.state.questionScores.map((item, index) =>
        //         index === position ? 0 : this.state.questionScores[index]
        //     );
        //     this.setState({questionScores: updatedRateState});
        //     var element = document.getElementById(("rating"+position));

        //     element.classList.add('invisiblee');
        //     const totalScore = this.state.questionScores.reduce(
        //         (sum, currentState, currentIndex) => {
        //             if(currentIndex === position) return sum;
        //             return sum+currentState;
        //         },
        //         0
        //     );
        //     this.setState({rScore: totalScore});
        // }else{
            var element = document.getElementById(("rating"+position));
            element.classList.remove('invisiblee');
        //     const innnn = Array.from(element.childNodes).filter(element => element.getAttribute('aria-checked')=='true' );
        //     if(innnn.length > 0){
        //         const r = innnn[0].getAttribute('aria-posinset');
        //         const updatedRateState = this.state.questionScores.map((item, index) =>
        //             index === position ? parseInt(r) : item
        //         );
        //         this.setState({questionScores: updatedRateState});
        //         const totalScore = updatedRateState.reduce(
        //             (sum, currentState) => {
        //                 return sum+currentState;
        //             },
        //             0
        //         );
        //         this.setState({rScore: totalScore});
        //     }
        // }
        // isChecked ? this.setState({maxScore: this.state.maxScore - 10}) : this.setState({maxScore: this.state.maxScore + 10});
    };

    handleOrgCBChange = (checkBoxName) => {
        checkBoxName=='isGoverment' ? this.setState({isGoverment:!this.state.isGoverment}) :
        checkBoxName=='isProfitCompanyOrDeveloper' ? this.setState({isProfitCompanyOrDeveloper:!this.state.isProfitCompanyOrDeveloper}) :
        checkBoxName=='isNonProfitCompany' ? this.setState({isNonProfitCompany:!this.state.isNonProfitCompany}) :
        checkBoxName=='isRegisteredCharity' ? this.setState({isRegisteredCharity:!this.state.isRegisteredCharity}) :
        checkBoxName=='isPublicHealthcareProvider' ? this.setState({isPublicHealthcareProvider:!this.state.isPublicHealthcareProvider}) :
        checkBoxName=='isAcademicInst' ? this.setState({isAcademicInst:!this.state.isAcademicInst}) : null;
    }

    componentDidUpdate(previousProps, previousState){
        console.log('calculating...', this.state.questionScores, previousState.questionScores)
        if(previousState.questionBools != this.state.questionBools ||
             previousState.questionScores != this.state.questionScores ||
             previousState.boolQuestionIsNA != this.state.boolQuestionIsNA ||
             previousState.rateQuestionIsNA != this.state.rateQuestionIsNA ){
                this.calculateScore();
            }
    }

    calculateScore = () => {
        var rScore = 0;
        var bScore = 0;
        var maxScore = 0;
        var questionBools = this.state.questionBools;
        var questionScores = this.state.questionScores;
        var reviewData = {};
        var reviewAnswers = new Array();

        //checkboxes
        for(var i=0; i<questionBools.length; i++){
            const isNA = this.state.boolQuestionIsNA[i];
            if(isNA){
                // NA
                reviewAnswers.push({question:'bool question '+i, answer:'NA'})
            }else{
                // Assigned
                if (this.state.negativeCBoxQuestions.includes(i)){
                    // negative impact
                    if(questionBools[i]){
                        // checked
                        reviewAnswers.push({question:'bool question '+i, answer:'-2'})
                        bScore=parseInt(bScore)-1
                    }else{
                        // not checked
                        reviewAnswers.push({question:'bool question '+i, answer:'0'})
                    }
                }else{
                    // positive impact
                    if(questionBools[i]) {
                        // checked
                        bScore=parseInt(bScore)+1
                        reviewAnswers.push({question:'bool question '+i, answer:'2'})
                    }else{
                        // not checked
                        reviewAnswers.push({question:'bool question '+i, answer:'0'})
                    }
                    maxScore=parseInt(maxScore)+2;
                }
            }
        }
        //ratings
        for(var i=0; i<questionScores.length; i++){
            const isNA = this.state.rateQuestionIsNA[i];
            if(isNA){
                // NA
                reviewAnswers.push({question:'rating question '+i, answer:'NA'})
            }else{
                // ratings - A
                rScore=parseInt(questionScores[i])+rScore;
                maxScore=parseInt(maxScore)+10;
                reviewAnswers.push({question:'rating question '+i, answer:questionScores[i]*2})
            }
        }
        this.setState({bScore});
        this.setState({rScore});
        this.setState({maxScore});
        this.setState({bViable: this.state.bViable});
        this.setState({bHarmful: this.state.bHarmful});

        reviewData = {
            maxScore:maxScore,
            bScore:(bScore*4),
            rScore:(rScore*2),
            QA_array: reviewAnswers,
            organizationType: {
                isGoverment: this.state.isGoverment,
                isProfitCompanyOrDeveloper: this.state.isProfitCompanyOrDeveloper,
                isNonProfitCompany: this.state.isNonProfitCompany,
                isRegisteredCharity: this.state.isRegisteredCharity,
                isPublicHealthcareProvider: this.state.isPublicHealthcareProvider,
                isAcademicInst: this.state.isAcademicInst,
            }
        };
        console.log('reviewData',reviewData)
        this.props.onChange(reviewData);
    }

    toggleHarm = () => this.setState((prevState) => ({ bHarmful: !prevState.bHarmful }))
    toggleViable = () => this.setState((prevState) => ({ bViable: !prevState.bViable }))
 
     render() {
         return (
             <React.Fragment>
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
                            <Table.Cell >Where does the resource come from? (Check all that apply)</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={(e)=>this.handleOrgCBChange('isGoverment')} checked={this.state.isGoverment} label='Government' /></div>
                                <div><Checkbox onChange={(e)=>this.handleOrgCBChange('isProfitCompanyOrDeveloper')} checked={this.state.isProfitCompanyOrDeveloper} label='For profit company or developer' /></div>
                                <div><Checkbox onChange={(e)=>this.handleOrgCBChange('isNonProfitCompany')} checked={this.state.isNonProfitCompany} label='Non-profit company' /></div>
                                <div><Checkbox onChange={(e)=>this.handleOrgCBChange('isRegisteredCharity')} checked={this.state.isRegisteredCharity} label='Registered charity' /></div>
                                <div><Checkbox onChange={(e)=>this.handleOrgCBChange('isPublicHealthcareProvider')} checked={this.state.isPublicHealthcareProvider} label='A public healthcare provider' /></div>
                                <div><Checkbox onChange={(e)=>this.handleOrgCBChange('isAcademicInst')} checked={this.state.isAcademicInst} label='Academic institution' /></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Could this organization or company have a conflict of interest in providing this resource?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[9]} id='checkbox9' onChange={(e)=>this.handleCBChange(e, 9)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[9]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 9)}/></div>
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
                            <Table.Cell>The material uses common, everyday language</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[0]} id='checkbox0' onChange={(e)=>this.handleCBChange(e, 0)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[0]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 0)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Medical terms are used only to familiarize the audience with the terms. When used, medical terms are defined</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[1]} id='checkbox1' onChange={(e)=>this.handleCBChange(e, 1)} /></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[1]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 1)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>The material uses the active voice</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[2]} id='checkbox2' onChange={(e)=>this.handleCBChange(e, 2)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[2]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 2)}/></div>
                            </Table.Cell>
                        </Table.Row>
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
                            <Table.Cell>Does it have at least one accessibility feature (like adjust text size, text to voice, or colourblind colour scheme)?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[3]} id='checkbox3' onChange={(e)=>this.handleCBChange(e, 3)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[3]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 3)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it work with French?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[4]} id='checkbox4' onChange={(e)=>this.handleCBChange(e, 4)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[4]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 4)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it work with a language other than English and French?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[5]} id='checkbox5' onChange={(e)=>this.handleCBChange(e, 5)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[5]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 5)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is the resource free?</Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[6]} id='checkbox6' onChange={(e)=>this.handleCBChange(e, 6)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[6]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 6)}/></div>
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
                            <Table.Cell>Are the aims clear? <Popup content='look for a clear indication at the begining of the resource of: 1)what is it about?  2)what it is meant to cover(and what topics are meant to be excluded) 3)who might find it useful' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating0' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 0, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[0]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 0)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it achieve it's aims? <Popup content='Consider whether the resource provides the information and/or service it amed to as outlined in previous question.' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating1' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 1, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[1]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 1)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it relevant? <Popup content='Consider whether: 1)the resource addresses the questions that client might ask. 2)The resource addresses the need the client may have in accessing it.' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating2' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 2, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[2]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 2)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it clear what sources of information were used to compile the resource (other than the author or producer)? <Popup content='HINT
                                Check whether the main claims or statements made about mental health topics are accompanied by a reference to the sources used as evidence, e.g. a research study or expert opinion.
                                Look for a means of checking the sources used such as a bibliography/reference list or the addresses of the experts or organisations quoted, or external links to the online sources.
                                Rating note: In order to score a full "5" the resources should fulfill both hints. Lists of additional sources of support and information (Question 4.7) are not necessarily sources of evidence for the current resource.' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating3' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 3, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[3]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 3)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it clear when the information used or reported in the resource was produced?<Popup content='HINT: Look for:
                                dates of the main sources of information used to compile the resource
                                date of any revisions of the resource 
                                date of resource (copyright date).
                                If the resource is a forum, check to ensure responses to client questions are being addressed in a timely manner (less than 24 hours for a response to an initial post). 
                                Rating note: The hints are placed in order of importance - in order to score a full "5" the dates relating to the first hint should be found.
                                ' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating4' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 4, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[4]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 4)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is it balanced or unbiased?<Popup content='HINT: Look for:
                                a clear indication of whether the resource is written from a personal or objective point of view
                                evidence that a range of sources of information was used to compile the resource, e.g. more than one research study or expert (if applicable)
                                evidence of an external assessment of the resource.
                                Be wary if:
                                the resource relies primarily on evidence from single cases (if applicable) 
                                the information is presented in a sensational, emotive or alarmist way.
                                ' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating5' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 5, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[5]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 5)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does it provide details of additional sources of support and information?<Popup content='HINT Look for suggestions for further reading or for details of other organisations providing advice and information about the mental health topic.
                                ' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Rating id='rating6' min={1} maxRating={5} onRate={(e, {rating, maxRating})=>this.handleRTChange(e, 6, rating, maxRating)}/> &nbsp;&nbsp;&nbsp;1)No&nbsp;&nbsp;3)Partially&nbsp;&nbsp;5)Yes</div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.rateQuestionIsNA[6]} label='Not Applicable (NA)' onChange={(e)=>this.handleRTNAChange(e, 6)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Is the resource patient facing?<Popup content='Is the resource relevant for an individual with the condition specified? Is it intended for patient use generally?' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[7]} id='checkbox7' onChange={(e)=>this.handleCBChange(e, 7)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[7]} label='Not Applicable (NA)' onChange={(e)=>this.handleCBNAChange(e, 7)}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Does the resource provide any cautions?<Popup content='Is there any warning for a user that the resource is not intended to replace medical care?
                                    Is there an emergency phone number on the website to help direct someone in significant distress?
                                ' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Checkbox checked={this.state.questionBools[8]} id='checkbox8' onChange={(e)=>this.handleCBChange(e, 8)}/></div>
                            </Table.Cell>
                            <Table.Cell warning>
                                <div><Checkbox checked={this.state.boolQuestionIsNA[8]} label='Not Applicable (NA)'  onChange={(e)=>this.handleCBNAChange(e, 8)}/></div>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                <Table collapsing>
                    <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={5}>Section 5: Overall</Table.HeaderCell>
                        <Table.HeaderCell width={5}></Table.HeaderCell>
                    </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        <Table.Row positive>
                            <Table.Cell>Is the resource still viable/functional? <Popup content='Do the links to access the resource still work (please test them)
                                If appropriate, is the phone number still in service? (other than 911, please phone numbers provided)
                                *If the answer to this question is no, then the resource will be noted as rejected and flagged for follow-up by the Resource Portal Editor.
                                ' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={this.toggleViable} checked={this.state.bViable}/></div>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row negative>
                            <Table.Cell>Can the resource cause harm?<Popup content='Does the resource make recommendations or suggestions that directly defy clinical guidance? Does it include false information, like a suicide hotline number that doesn’t actually work?
                                *If the answer to this question is yes, then the resource will be noted as rejected and flagged for follow-up by the Resource Portal Editor. 
                                ' trigger={<Icon name='question circle'/>}/></Table.Cell>
                            <Table.Cell>
                                <div><Checkbox onChange={this.toggleHarm} checked={this.state.bHarmful}/></div>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
                { this.state.bHarmful ? <h3 class="ui red header">Score:{(this.state.bScore+this.state.rScore)*2}/{this.state.maxScore} &nbsp;&nbsp; Harmful resource is not accepted</h3> :
                    !this.state.bViable ? <h3 class="ui red header">Score:{(this.state.bScore+this.state.rScore)*2}/{this.state.maxScore} &nbsp;&nbsp; Resources should be functional/viable</h3> :
                    (this.state.bScore+this.state.rScore*2/this.state.maxScore).toFixed(2) > (this.state.treshholdScore/100) && !this.state.bHarmful && this.state.bViable
                    ? <h3 class="ui green header">Score:{(this.state.bScore+this.state.rScore)*2}/{this.state.maxScore} &nbsp;&nbsp; This resource passes all given criteria. Approval is recommended. If you feel it necessary to reject this resource, please explain why in the review comments.</h3>
                    :                    
                    <h3 class="ui red header">Score:{(this.state.bScore+this.state.rScore)*2}/{this.state.maxScore} &nbsp;&nbsp;This resource does not meet the minimum standards for approval. If you feel it necessary to approve this resource, please explain why in the review comments.</h3>
                }
                
             </React.Fragment>
         );
     }
 }
 
 //ReviewMatrix.propTypes = {
 //    value: PropTypes.array,
 //    onChange: PropTypes.func
 //};