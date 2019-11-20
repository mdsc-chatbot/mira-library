import React, { Component } from "react";
import {Menu, Header, Icon, Segment, Responsive, Dropdown, Container} from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import { SecurityContext } from "./security/SecurityContext";
import styles from "./App.css";

export class HeaderMenu extends Component {
    static contextType = SecurityContext;
    constructor(props) {
        super(props);

        this.state = {};
    }
    handleItemClick = (e, { name }) => this.setState({ activeItem: name });



    headerMenuWeb = () => {
        const { activeItem } = this.state;
        return(
            //<div>
            <Menu inverted stackable pointing secondary size="large">
                <Menu.Item
                    as="a"
                    style={{ paddingLeft: 50 }}
                    active={activeItem === "Home"}
                    onClick={this.handleItemClick}
                >
                    <Link to={baseRoute}>
                        <Header as="h2" style={{ color: "#3075c9" }}>
                            <Icon name="qq" />
                            Chatbot Resources
                        </Header>
                    </Link>
                </Menu.Item>

                <Menu.Item
                    name="Public Resources"
                    as={Link}
                    to={baseRoute + "/public_resource"}
                    position="right"
                    active={activeItem === "Public Resources"}
                    onClick={this.handleItemClick}
                />

                <Menu.Item
                    name="FAQ"
                    as={Link}
                    to={baseRoute + "/faq"}
                    active={activeItem === "FAQ"}
                    onClick={this.handleItemClick}
                />

                <Menu.Item
                    name="Passchange"
                    as={Link}
                    to={baseRoute + "/password"}
                    active={activeItem === "Passchange"}
                    onClick={this.handleItemClick}
                />
                {this.context.security.is_logged_in && (
                    <Menu.Item
                        name="My Profile"
                        as={Link}
                        to={baseRoute + "/profile"}
                        active={activeItem === "My Profile"}
                        onClick={this.handleItemClick}
                    />
                )}

                {this.context.security.is_logged_in && (
                    <Menu.Item
                        name="My resources"
                        as={Link}
                        to={baseRoute + "/resource"}
                        active={activeItem === "My resources"}
                        onClick={this.handleItemClick}
                    />
                )}

                {this.context.security.is_logged_in && (
                    <Menu.Item
                        name="My reviews"
                        as={Link}
                        to={baseRoute + "/review"}
                        active={activeItem === "My reviews"}
                        onClick={this.handleItemClick}
                    />
                )}

                {this.context.security.is_logged_in && this.context.security.is_staff && (
                    <Menu.Item
                        name="Search"
                        as={Link}
                        to={baseRoute + "/search"}
                        active={activeItem === "Search"}
                        onClick={this.handleItemClick}
                    />
                )}

                {this.context.security.is_logged_in && (
                    <Menu.Item
                        name="Logout"
                        as={Link}
                        to={baseRoute + "/logout"}
                        active={activeItem === "Logout"}
                        onClick={this.handleItemClick}
                    />
                )}

                {!this.context.security.is_logged_in && (
                    <Menu.Item
                        name="Login"
                        as={Link}
                        to={baseRoute + "/login"}
                        active={activeItem === "Login"}
                        onClick={this.handleItemClick}
                    />
                )}
            </Menu>
            //</div>

        );
    };

    headerMenuMobile = () => {
        const { activeItem } = this.state;
        return(
            //<div>
            <Menu inverted pointing fluid widths = {2} size="small">
                <Menu.Item
                    as="a"
                    style={{ paddingLeft: 50 }}
                    active={activeItem === "Home"}
                    onClick={this.handleItemClick}
                >
                    <Link to={baseRoute}>
                        <Header as="h4" style={{ color: "#3075c9" }}>
                            <Icon name="qq" />
                            Chatbot Resources
                        </Header>
                    </Link>
                </Menu.Item>
                <Menu.Menu position = 'right'>

                    <Dropdown item text='Menu' floating labeled>

                        <Dropdown.Menu className={styles.headerMobile}>

                            <Dropdown.Item>
                                <Menu.Item
                                    name="Public Resources"
                                    as={Link}
                                    to={baseRoute + "/public_resource"}
                                    position="right"
                                    active={activeItem === "Public Resources"}
                                    onClick={this.handleItemClick}
                                />
                            </Dropdown.Item>

                            {this.context.security.is_logged_in && (
                                <Dropdown.Item><Menu.Item
                                    name="My Profile"
                                    as={Link}
                                    to={baseRoute + "/profile"}
                                    active={activeItem === "My Profile"}
                                    onClick={this.handleItemClick}
                                /></Dropdown.Item>
                            )}

                            {this.context.security.is_logged_in && (
                                <Dropdown.Item><Menu.Item
                                    name="My resources"
                                    as={Link}
                                    to={baseRoute + "/resource"}
                                    active={activeItem === "My resources"}
                                    onClick={this.handleItemClick}
                                /></Dropdown.Item>
                            )}

                            {this.context.security.is_logged_in && (
                                <Dropdown.Item><Menu.Item
                                    name="My reviews"
                                    as={Link}
                                    to={baseRoute + "/review"}
                                    active={activeItem === "My reviews"}
                                    onClick={this.handleItemClick}
                                /></Dropdown.Item>
                            )}

                            {this.context.security.is_logged_in && this.context.security.is_staff && (
                                <Dropdown.Item><Menu.Item
                                    name="Search"
                                    as={Link}
                                    to={baseRoute + "/search"}
                                    active={activeItem === "Search"}
                                    onClick={this.handleItemClick}
                                /></Dropdown.Item>
                            )}

                            {this.context.security.is_logged_in && (
                                <Dropdown.Item><Menu.Item
                                    name="Logout"
                                    as={Link}
                                    to={baseRoute + "/logout"}
                                    active={activeItem === "Logout"}
                                    onClick={this.handleItemClick}
                                /></Dropdown.Item>
                            )}

                            {!this.context.security.is_logged_in && (
                                <Dropdown.Item><Menu.Item
                                    name="Login"
                                    as={Link}
                                    to={baseRoute + "/login"}
                                    active={activeItem === "Login"}
                                    onClick={this.handleItemClick}
                                /></Dropdown.Item>
                            )}

                            <Dropdown.Item>
                                <Menu.Item
                                    name="FAQ"
                                    as={Link}
                                    to={baseRoute + "/faq"}
                                    active={activeItem === "FAQ"}
                                    onClick={this.handleItemClick}
                                />
                            </Dropdown.Item>
                        </Dropdown.Menu>

                    </Dropdown>

                </Menu.Menu>
            </Menu>
            //</div>

        );
    };

    headerMenu = () => {
        return(
            <Segment.Group className={styles.segmentWeb}>

                <Responsive minWidth={768}>
                    {this.headerMenuWeb()}
                </Responsive>

                <Responsive maxWidth={767}>
                    {this.headerMenuMobile()}
                </Responsive>

            </Segment.Group>
        );
    };

    render() {
        return (
            <React.Fragment>
                <Segment.Group className={styles.segmentWeb}>
                    <Responsive maxWidth={767}>
                        {this.headerMenu()}
                    </Responsive>

                    <Responsive minWidth={768}>
                        <React.Fragment>
                            {this.headerMenu()}
                        </React.Fragment>
                    </Responsive>
                </Segment.Group>
            </React.Fragment>

        );
    }
}

export default HeaderMenu;
