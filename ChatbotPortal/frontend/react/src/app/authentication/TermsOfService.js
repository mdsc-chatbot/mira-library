import React, {Component} from 'react'
import {Header, Modal} from "semantic-ui-react";
import styles from "../shared/Link.css";

export class TermsOfService extends Component {
    render() {
        return (
            <div>
                <Modal trigger={<Header as="h5" color="blue" className={styles.link}>Terms of Service</Header>}
                       closeIcon>
                    <Modal.Header>Terms of Service</Modal.Header>
                    <Modal.Content scrolling>
                        Welcome to the ChatbotResources Portal. <br/>In order to proceed, we would like you to look at
                        our consent form. The assent form can be accessed <a href="/static/public/assent.pdf"
                                                                             target="_blank">here</a>.<br/><br/>
                        <b>ONLINE CONSENT AND INFORMATION LETTER-PERSONAL ASSISTANT</b><br/><br/>
                        <b>Study Title</b>: Canadian Network for Personalized Interventions in Intellectual
                        Disability<br/><br/>
                        <b>Principal Investigator</b>: <i>Dr. Francois Bolduc, MD, PhD FRCPC Ph: 780-492-9616</i><br/>
                        <b>Coordinator</b>:<i> Ph: 780-492-9461</i><br/>
                        Department of Pediatrics<br/>
                        University of Alberta<br/><br/>
                        You are asked to help develop a novel tool for providing information about neurodevelopmental
                        disability (NDD) to help improve access to personalized information and coaching for NDD.
                        Before you agree to participate in this project, please take the time to read the following
                        consent form
                        and make sure you understand its contents.<br/><br/>
                        <b>Purpose and Background</b><br/><br/>
                        The main purpose of the study is to find new ways to improve access to services and information
                        for individuals with intellectual disability and their families. This research study is
                        sponsored by the Kids
                        Brain Health Network (KBHN).<br/><br/>
                        <b>What will I be asked to do?</b><br/><br/>
                        You will be asked to provide your email and create a password if you want. You will be able to
                        provide resources that we may use to add to our database of helpful resources aimed towards
                        helping parents, educators and health workers manage children with neurodevelopmental diagnoses.
                        These resources may be provided publicly in our portal. <br/><br/>
                        <b>Possible Benefits and Risk.</b><br/><br/>
                        You may not get any benefit from your participation in this study. In the long term, this study
                        may
                        help families with NDD, healthcare providers or educators in the future, by providing a better
                        understanding of the factors implicated in NDD, and better interventions may be discovered.
                        It is not possible to know all of the risks that may happen in a study, but the researchers have
                        taken all
                        reasonable safeguards to minimize any known risks to a study participant. You can decide to
                        withdraw from the study and request your information to be deleted at any time by emailing the
                        study
                        team.<br/><br/>
                        <b>Confidentiality</b><br/><br/>
                        During the study we will be collecting information about you and the resources you are
                        submitting.<br/><br/>
                        The information we gather will be stored in an encrypted database. We will
                        do everything we can to make sure that this data is kept private. We cannot guarantee absolute
                        privacy. However, we will make every effort to make sure that the information is kept private.
                        The
                        information will be available to our study team only and will not be visible to other
                        participants.
                        You will have the possibility to communicate any question by contacting the study coordinator
                        either
                        by phone or email (without including confidential information). In some cases, we may obtain or
                        already have your name for other aspect of our study. This will be stored on our password
                        protected
                        computers.<br/><br/>
                        During research studies it is important that the data we get are accurate. For this reason the
                        information collected about the user and the individual for whom they are using the
                        ChatbotResources Portal, may be
                        looked at by the University of Alberta auditors or the University of Alberta Health Research
                        Ethics
                        Board. The sponsor (Kids Brain Health Network) will not have access to personal information that
                        could identify you or your child directly.<br/><br/>
                        After the study is done, we will still need to securely store the data collected as part of the
                        study. At
                        the University of Alberta, we keep data stored for a minimum of 5 years after the end of the
                        study.<br/><br/>
                        <b>Reimbursement</b>: You will not be paid to participate to this component of the study. The
                        rights to the
                        commercial products will belong to the sponsor, collaborators or future unknown
                        researchers.<br/><br/>
                        <b>Participating</b>: Participation is voluntary and should you choose to participate, you can
                        withdraw at
                        any time. If you leave the study, we will not collect new information and you can request us to
                        remove the information already collected.<br/><br/>
                        <b>Questions</b>: If you have any questions or would like to participate in this study please
                        contact the
                        study coordinator by contacting 780-492-9461.<br/><br/>
                        If you have any questions regarding your rights as a research participant, you may contact the
                        Health
                        Research Ethics Board at 780-492-2615. This office is independent of the study
                        investigators.<br/><br/>
                        <b>DISCLAIMER : The medical information on this site is provided as an information resource
                            only, and is not to be used or relied on for any diagnostic or treatment purposes. This
                            information does not create any patient-physician relationship, and should not be used as a
                            substitute for professional diagnosis and treatment. By visiting this site you agree to the
                            these terms and conditions.</b><br/><br/>
                    </Modal.Content>
                </Modal>
            </div>
        )
    }
}

export default TermsOfService
