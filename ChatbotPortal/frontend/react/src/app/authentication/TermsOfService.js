/**
 * @file: TermsOfServices.js
 * @summary: Terms of Service usage agreement information
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

import React, {Component} from 'react'
import {Header, Modal} from "semantic-ui-react";
import styles from "../shared/Link.css";

export class TermsOfService extends Component {
    render() {
        return (
            <div>
                <Modal trigger={<Header as="h5" color="blue" className={styles.link}>Terms of Service</Header>}
                       closeIcon>
                    <Modal.Header>ONLINE CONSENT AND PRIVACY NOTICE – Neurodevelopmental Disability Portal </Modal.Header>
                    <Modal.Content scrolling>
                    <b>Study Title:</b>  <i>Canadian Network for Personalized Interventions in Intellectual Disability</i>
                    
                    <b>Principal Investigator:</b>  <i>Dr. Francois Bolduc, MD, PhD FRCPC</i>       Ph: 780-492-9616 <br/><br/>
                    Thank you for choosing to register at Neurodevelopmental Disability (NDD) Resource Portal. 
                    You are being asked to use a novel tool for providing and storing resources related to neurodevelopmental disability (NDD). 
                    Before you agree to participate in this project, please take the time to read the following consent form and make sure you understand its contents. <br/><br/>
                    
                    If you have any questions or concerns about this privacy notice,
                    or our practices with regards to your personal information, please contact the research coordinator at <b>780-492-7034</b> or <a>nddopen@ualberta.ca</a>. <br/>
                    
                    In this privacy notice, we seek to explain to you in the clearest way possible what information we collect, how we use it and what rights you have in relation to it. We hope you take some time to read through it carefully, 
                    as it is important. If there are any terms in this privacy notice that you do not agree with, please discontinue use of our Services immediately. 

                    <b>Please read this privacy notice carefully as it will help you understand your participation in the project. </b><br/><br/>

                    <b>1. WHAT IS THE PURPOSE AND BACKGROUND OF THIS STUDY? </b><br/>
                    The main purpose of the study is to find new ways to improve access to services and information for individuals with intellectual disability and their families. 
                    This research study is sponsored by the Canadian Institutes of Health Research (CIHR) and the Natural Sciences and Engineering Research Council of Canada (NSERC).<br/>
                    The NDD Portal is a website dedicated to providing and gathering information regarding autism, intellectual disability, and learning disability. 
                    The information is gathered from a variety of sources such as health professionals, educators, parents, and resource submissions need to be approved.<br/>
                    <br/>

                    <b>2. WHAT WILL I BE ASKED TO DO? </b><br/>
                    You will be asked to provide your name and email and create a password in order to login to the portal where 
                    you will then be able to submit resources related to NDD. Optionally, we would like to indicate the type of neurodevelopmental disorder 
                    (for instance autism, intellectual disability and learning disability). This information helps us better tailor our website. After you
                    fill out the sign-up form, we will send you and email for verification. <br/>
                    To submit a resource, you are required to input a website URL and rate how useful it was to you. The rating on each resource shows how 
                    useful it is. Your submitted resource is rated first by you, then manually adjusted by us or Reviewers. Each resource is rated from 0-5 stars. 
                    You can also search for and select a tag to categorize your resource (ex. Autism, ADHD, age, etc.). If you cannot find a tag that accurately
                    categorizes your resource, you can submit a new tag for us to review. We then may add it to our database so that you can search for and select it later. 
                    You can also upload a file attachment related to the resource. We will also ask you to indicate the location most relevant for this resource (city, province, country) if applicable.<br/>
                    As a logged-in user of the site, you can view My Profile which shows your profile and the number of resource submission.  You can also view My Resources, 
                    which shows your submitted resources and their details. Reviewer status may be given you. A Reviewer can approve or reject a submitted resource. They are 
                    also required to give a review comment. If you are approved as a Reviewer, you can also see My Reviews, which shows the pending resources waiting for you to review. <br/><br/>

                    <b>3. WHAT INFORMATION DO WE COLLECT? </b><br/>
                    We collect personal information that you voluntarily provide to us when you register which will be your name, email and a password for logging in and 
                    using the portal. Optionally, we would like to indicate the type of neurodevelopmental disorder (for instance autism, intellectual disability and learning disability). 
                    This information helps us better tailor our website. After you fill out the sign-up form, we will send you and email for verification. <br/>
                    All personal information that you provide to us must be true, complete and accurate, and you must notify us of any changes to such personal information.<br/>
                    <br/>

                    <b>4. WILL YOUR INFORMATION BE SHARED WITH ANYONE?  </b><br/>
                    We will potentially share the websites and other types of resources you provide through the NDD portal with other researchers, other organizations or partners. 
                    We may process or share your data that we hold based on the following legal basis: <br/>
                    More specifically, we may need to process your data or share your personal information in the following situations: <br/>
                    <b><i>Affiliates.</i></b> We may share your information with our affiliates, in which case we will require those affiliates to honor this privacy notice. Affiliates include the University of Alberta and any subsidiaries of it. <br/>
                    <br/>

                    <b>5. HOW LONG DO WE KEEP YOUR INFORMATION? </b><br/>
                    We will only keep your personal information for as long as it is necessary for the purpose of the study mentioned in the purpose and background. 
                    You have full control over your account and you can withdraw your consent for the privacy at any time and your account will be permanently deleted. 
                    This action is irreversible so you will have to register with us again. 
                    In order to withdraw your consent at any time you can reach the research coordinator at 780-492-7034.<br/>
                    <br/>

                    <b>6. DO WE COLLECT INFORMATION FROM MINORS?  </b><br/>
                    We do not knowingly collect or market to children under 18 years of age. By agreeing to this privacy form, you agree you are over the age of 18. <br/>
                    <br/>

                    <b>7. WHAT ARE THE POSSIBLE BENEFITS AND RISKS? </b><br/>
                    You may not get any benefit from your participation in this study. In the long term, this study may help families, 
                    healthcare providers, or educators by providing better resources to those who are affected by an NDD. <br />
                    It is not possible to know all of the risks that may happen in a study, but the researchers have taken all reasonable safeguards to minimize any k
                    nown risks to a study participant. You can decide to withdraw from the study and 
                    request your information to be deleted at any time by calling or emailing the study team. <br/>
                    <br/>

                    <b>8. WHAT ARE YOUR PRIVACY RIGHTS? </b><br/>
                    You can review, change or delete your information at any time you wish. <br/>
                    <br/>

                    <b>Account Information</b><br/><br/>
                    If you would at any time like to terminate your account, you can: <br />
                    Upon your request to terminate your account, we will delete your account and information from our databases. However, we may retain some information
                    in our files to prevent fraud, troubleshoot problems, assist with any investigations, enforce our Terms of Use and/or comply with applicable legal
                    requirements. <br/><br/><br/>

                    <b>9. IS THERE ANY CONFIDENTIALITY NOTICE?</b><br/>
                    During the study we will be collecting information about you (your name, email address, and type of NDD). The information will be stored in an
                    encrypted database. We will do everything we can to make sure that this data is kept private. We cannot guarantee absolute privacy. However, 
                    we will make every effort to make sure that the information is kept private.
                    The information will be available to our study team only and will not be visible to other participants.  <br />
                    You will have the possibility to communicate any questions by contacting the study coordinator either by phone or email.<br/>
                    During research studies it is important that the data we get are accurate. For this reason, the information collected about the user may be looked at by 
                    the University of Alberta auditors or the University of Alberta Health Research Ethics Board. 
                    The sponsors (CIHR and NSERC) will not have access to personal information that could identify you. <br/>
                    After the study is done, we will still need to securely store the data collected as part of the study. At the University of Alberta, we keep data stored for 
                    a minimum of 5 years after the end of the study.<br/><br/>
                    <br/>

                    <b>10. WILL I BE REIMBURSED FOR PARTICIPATING IN ANY CAPACITY IN THIS STUDY?</b><br/>
                    Participation is voluntary and should you choose to participate, you can withdraw at any time. If you leave the study, we will not collect new information 
                    and you can request us to remove the information already collected.  <br/><br/>
                    <br/>

                    <b>11. HOW CAN YOU CONTACT US ABOUT THIS NOTICE OR ANY OTHER QUESTIONS?      </b><br/>
                    If you have any questions or would like to participate in this study, please contact the study coordinator by contacting <i>780-492-7034</i> or <a>nddopen@ualberta.ca</a>.  <br/>
                    If you have any questions regarding your rights as a research participant, you may contact the Health Research Ethics Board at 780-492-2615. This office is independent of the study investigators.
                    <br/>
                    <br/>

                    <h3>DISCLAIMER - NDD RESOURCE PORTAL SUBMISSION </h3>
                    <br/><br/><br/>
                    <b>WEBSITE DISCLAIMER </b><br/>
                    The information provided is for general informational purposes only. We make no representation or warranty of any kind, express or implied,
                     regarding the accuracy, adequacy, validity, reliability, availability or completeness of any information on this site. UNDER NO CIRCUMSTANCE 
                     SHALL WE HAVE ANY LIABILITY TO YOU FOR ANY LOSS OR DAMAGE OF ANY KIND INCURRED AS A RESULT OF THE USE OF THE SITE OR OUR MOBILE APPLICATION OR 
                     RELIANCE ON ANY INFORMATION PROVIDED ON THE SITE AND OUR MOBILE APPLICATION. YOUR USE OF THE SITE AND OUR MOBILE APPLICATION AND YOUR RELIANCE ON 
                     ANY INFORMATION ON THE SITE AND OUR MOBILE APPLICATION IS SOLELY AT YOUR OWN RISK. <br/><br/>

 
                    <b>EXTERNAL LINKS DISCLAIMER  </b><br/>
                    The Site may contain links to other websites or content belonging to or originating from third parties. Such external links are not investigated,
                    monitored, or checked for accuracy, adequacy, validity, reliability, availability or completeness by us. WE DO NOT WARRANT, ENDORSE, GUARANTEE, OR
                    ASSUME RESPONSIBILITY FOR THE ACCURACY OR RELIABILITY OF ANY INFORMATION OFFERED BY THIRD-PARTY WEBSITES LINKED THROUGH THE SITE OR ANY WEBSITE. 
                    WE WILL NOT BE A PARTY TO OR IN ANY WAY BE RESPONSIBLE FOR MONITORING ANY TRANSACTION BETWEEN YOU AND THIRD-PARTY PROVIDERS OF PRODUCTS OR SERVICES. <br/><br/>


                    <b>PROFESSIONAL DISCLAIMER </b><br/>
                    The Site cannot and does not contain medical/health advice. The medical/health information is provided for general informational and educational 
                    purposes only and is not a substitute for professional advice. Accordingly, before taking any actions based upon such information, we encourage you to 
                    consult with the appropriate professionals. We do not provide any kind of medical/health advice. THE USE OR RELIANCE OF ANY INFORMATION 
                    CONTAINED ON THIS SITE OR OUR MOBILE APPLICATION IS SOLELY AT YOUR OWN RISK.  <br/><br/>

                    <b>TESTIMONIALS DISCLAIMER </b><br/>
                    The Site may contain ratings on website links by other users. The rating reflects the personal experience to the users and may not necessarily represent the 
                    rating of all users. We do not claim, and you should not assume that the experience will be same for every user. YOUR INDIVIDUAL RESULTS MAY VARY.  
                    The views and opinions contained in the testimonials belong solely to the individual user and do not reflect our views and opinions. We are not 
                    affiliated with users who provide rating on the resources. <br/><br/>

                    <b>Please read the following statements: </b><br/>
                    <ol>
                        <li>You understand that you have been asked to be in a research study. </li>

                        <li>You read the information about the study above. </li>

                        <li>You understand the benefits and risks involved in taking part in this research study. </li>

                        <li>You understand that you are free to leave the study at any time without having to give a reason. </li>

                        <li>You understand you can contact the study coordinator for any questions. </li>

                        <li>You understand the issue of confidentiality. </li>

                        <li>You understand who will have access to the information you provide. </li>

                        <li>You agree to be contacted by the study team if more information is needed or for potential participation in another study. </li>
                    </ol>
                    <br/><br/>
                    <b>Do you understand all the above-mentioned statements and do you agree to participate in this study? </b><br/>
                    Yes or No


                    </Modal.Content>
                </Modal>
            </div>
        )
    }
}

export default TermsOfService
