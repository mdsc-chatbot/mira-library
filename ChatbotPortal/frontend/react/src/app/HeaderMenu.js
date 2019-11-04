import React, { Component } from "react";
import { Menu, Header, Icon, Segment } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";
import { SecurityContext } from "./security/SecurityContext";

export class HeaderMenu extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {};
    }

    handleItemClick = (e, { name }) => this.setState({ activeItem: name });

    render() {
        const { activeItem } = this.state;

        return (
            <div>
                <Segment inverted>
                    <Menu inverted pointing secondary size="small">
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

                        {this.context.security.is_logged_in && this.context.security.is_staff && (
                            <Menu.Item
                                name="Search"
                                as={Link}
                                to={baseRoute + "/search"}
                                active={activeItem === "Search"}
                                onClick={this.handleItemClick}
                            />
                        )}
                    </Menu>
                </Segment>
            </div>
        );
    }
}

export default HeaderMenu;
