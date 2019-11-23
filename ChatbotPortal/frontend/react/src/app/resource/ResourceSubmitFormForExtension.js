import React, {Component} from "react";
import axios from "axios";
import validator from "validator";
import {
    Container,
    Form,
    FormInput,
    Header,
    Icon,
    Input,
    Menu,
    MenuItem,
    Message,
    Rating,
    Responsive
} from "semantic-ui-react";
import TagDropdown from "./TagDropdown";
import styles from "./ResourceSubmitForm.css";
import {MenuContext} from "../contexts/MenuContext"
import CategoryDropdown from "./CategoryDropdown";
import UpdateContexts from "./UpdateContexts";

/**
 * This component only handles resouce submission directed from the extension
 */
export default class ResourceSubmitForm extends Component {

    static contextType = MenuContext;

    /**
     * The constructor that initializes the state
     * @param props
     */
    constructor(props) {
        super(props);
        /**
         * The state of this component
         * @type {{
         *      comments: string,
         *      submitted: number,
         *      attachment: null,
         *      currentTags: null,
         *      rating: number,
         *      url_validated: boolean,
         *      title: string,
         *      attachmentPath: string,
         *      url: (null|*),
         *      tags: []}}
         */
        this.state = {
            title: "Unknown title",
            url: decodeURIComponent(this.props.match.params.url),
            rating: 1,
            attachment: null,
            attachmentPath: "", // To clear the file after submitting it
            comments: "",

            category: 1,
            tags: [],
            url_validated: true,
            currentTags: null,
            submitted: 0
        };
        this.baseState = this.state;
    }

    componentDidMount() {
        this.context.set_menu_visibility(false);
    }

    /**
     * This component creates the resource from the form data
     * @returns {FormData}
     */
    create_resource = () => {
        // Creating form data object
        const resourceFormData = new FormData();

        // Inputting data in the object
        resourceFormData.append("created_by_user", this.props.match.params.first_name);
        resourceFormData.append("created_by_user_pk", this.props.match.params.id);
        resourceFormData.append("title", "Unknown title");
        resourceFormData.append("url", this.state.url);
        resourceFormData.append("rating", this.state.rating);
        resourceFormData.append("comments", this.state.comments);
        resourceFormData.append("category", this.state.category);
        // If attachment is not null, then append it to the form data
        this.state.attachment !== null
            ? resourceFormData.append("attachment", this.state.attachment)
            : null;

        // Submission for tags
        // Lists have to be submitted in a certain way in order for the server to recognize it
        if (this.state.tags && this.state.tags.length) {
            this.state.tags.forEach(value => {
                resourceFormData.append(`tags`, value);
            });
        }

        return resourceFormData;
    };

    /**
     * This function post the resources by calling backend APIs
     */
    post_resource = () => {
        /**
         * Extracting the resouce form data
         * @type {FormData}
         */
        const resourceFormData = this.create_resource();

        /**
         * Having a common authorization header for backend queries
         * @type {{Authorization: string}}
         */

        axios
            .post("/chatbotportal/resource/", resourceFormData, {
                headers: {Authorization: `Bearer ${this.props.match.params.token}`}
            })
            .then(() => {
            })
            .catch(error => {
                console.error(error);
                this.set_submitted_state(-1, "POST FAILURE");
            });

        this.set_submitted_state(1, "POST SUCESS");
    };

    /**
     * Set submitted state upon requesting to post a resource.
     * Upon success, set to 1, otherwise -1
     * @param submitted_value
     * @param submitted_message
     */
    set_submitted_state = (submitted_value, submitted_message) => {
        if (submitted_value === 1) {
            this.update_user_submissions();
        }
        this.setState({submitted: submitted_value}, () => {
            setTimeout(() => {
                this.setState(this.baseState);
            }, 1000);
        });
        console.log(submitted_message);
    };

    /**
     * Upon successful submission, update the submission details in the user's instance by calling backend APIs
     */
    update_user_submissions = () => {
        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.props.match.params.token}`
        };
        axios
            .put(`/chatbotportal/authentication/${this.props.match.params.id}/update/submissions/`,
                '',
                {headers: options})
            .then(() => {
            }, error => {
                console.log(error);
            });
    };

    /**
     * This function updates the rating changes in the form
     * @param event
     * @param data
     */
    handleRate = (event, data) => {
        this.setState({rating: data.rating});
    };

    /**
     * This function handles the changes in the resource submission form field
     * @param event
     */
    handleChange = event => {
        this.setState({[event.target.name]: event.target.value});
    };

    /**
     * This function handles the file changes in form field.
     * event.target.value holds the pathname of a file
     * @param event
     */
    handleFileChange = event => {
        this.setState({
            [event.nativeEvent.target.name]: event.nativeEvent.target.files[0],
            attachmentPath: event.nativeEvent.target.value
        });
    };

    /**
     * This function gets executed upon submitting the form
     * @param event
     */
    handleSubmit = event => {
        // Validations
        if (!validator.isURL(this.state.url) || !this.state.url) {
            this.setState({url_validated: false});
        } else {
            this.post_resource();
        }
        event.preventDefault();
    };

    /**
     * This renders the resource submission form
     * @returns {*}
     */
    render() {
        return (
            <div>
                <UpdateContexts token={this.props.match.params.token}/>
                <Menu inverted stackable pointing secondary size="small">
                    <MenuItem>
                        <Header as="h2" style={{color: "#3075c9"}}>
                            <Icon name="qq"/>
                            Chatbot Resources
                        </Header>
                    </MenuItem>
                </Menu>
                <div style={{padding: "2%"}}>
                    <Container vertical>
                        <Responsive as={Header} minWidth={320}>
                            <Header
                                as={"h3"}
                                color="blue"
                                content={"Resource Submission"}
                                size={"small"}
                                textAlign={"center"}
                            />
                        </Responsive>
                        <Form size={"mini"} onSubmit={this.handleSubmit} success error>
                            <div>
                                {this.state.url_validated ? (
                                    <FormInput
                                        fluid
                                        label="Enter URL"
                                        name="url"
                                        onChange={this.handleChange}
                                        placeholder="https://"
                                        required
                                        value={this.state.url}
                                    />) : (
                                    <Form.Input
                                        error={{
                                            content: "Please enter a valid url",
                                            pointing: "below"
                                        }}
                                        fluid
                                        label="Enter URL"
                                        name="url"
                                        onChange={this.handleChange}
                                        placeholder="https://"
                                        required
                                        value={this.state.url}
                                    />
                                )}
                                <Form.Field>
                                    <label>Resource Usefulness Rating</label>
                                    <Rating
                                        defaultRating={this.state.rating}
                                        icon="star"
                                        label="Rating"
                                        maxRating={5}
                                        name="rating"
                                        onChange={this.handleChange}
                                        onRate={this.handleRate}
                                        size="massive"
                                        value={this.state.rating}
                                    />
                                </Form.Field>

                                <Form.Field>
                                    <label>Category</label>
                                    <CategoryDropdown
                                        value={this.state.category}
                                        onChange={category => this.setState({category})}
                                    />
                                </Form.Field>

                                <Form.Field>
                                    <label>Tags</label>
                                    <Form.Group className={styles.dropdownPadding}>
                                        <TagDropdown
                                            value={this.state.tags}
                                            onChange={tags => this.setState({tags})}
                                        />
                                    </Form.Group>
                                </Form.Field>
                                <Form.TextArea
                                    label="Comments"
                                    name="comments"
                                    onChange={this.handleChange}
                                    placeholder="Enter any comments (Optional)"
                                    value={this.state.comments}
                                />
                                <Form.Field>
                                    <label>Upload an attachment</label>
                                    <Input
                                        name="attachment"
                                        onChange={this.handleFileChange}
                                        type="file"
                                        value={this.state.attachmentPath}
                                    />
                                </Form.Field>

                                <div>
                                    {(() => {
                                        if (this.state.submitted === 1)
                                            return (
                                                <Message
                                                    success
                                                    header="Submit success"
                                                    content="Congratulations! You've submitted a resource!"
                                                />
                                            );
                                        else if (this.state.submitted === -1)
                                            return (
                                                <Message
                                                    error
                                                    header="Submit failure"
                                                    content="Something went wrong! Your resource is not submitted."
                                                />
                                            );
                                        else return <div/>;
                                    })()}
                                </div>
                                <Form.Button
                                    name="submit"
                                    content="Submit"
                                    color="green"/>
                            </div>
                        </Form>
                    </Container>
                </div>
            </div>
        );
    }
}
