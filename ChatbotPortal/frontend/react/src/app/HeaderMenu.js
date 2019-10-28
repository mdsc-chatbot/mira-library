import React, { Component } from "react";
import { Menu, Header, Icon, Segment } from "semantic-ui-react";
import { baseRoute } from "./App";
import { Link } from "react-router-dom";

export class HeaderMenu extends Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    handleItemClick = (e, { name }) => this.setState({ activeItem: name });

    render() {
        const { activeItem } = this.state;

        return (
            <div>
                <Segment style={{ padding: "2em 0em" }} vertical inverted>
                    <Menu inverted pointing secondary size="large">
                        <Menu.Item as="a" style={{ paddingLeft: 50 }}>
                            <Link to={baseRoute}>
                                <Header as="h2" style={{ color: "#3075c9" }}>
                                    <Icon name="qq" />
                                    Chatbot Portal
                                </Header>
                            </Link>
                        </Menu.Item>

                        {/* <Menu.Item
                            name="Resources"
                            as={Link}
                            to={baseRoute + "/resource"}
                            position="right"
                            active={activeItem === "Resources"}
                            onClick={this.handleItemClick}
                        />
                        <Menu.Item
                            name="Login"
                            as={Link}
                            to={baseRoute + "/login"}
                            active={activeItem === "Login"}
                            onClick={this.handleItemClick}
                        /> */}

                        <Menu.Item
                            name="Profile"
                            as={Link}
                            to={baseRoute + "/profile"}
                            position="right"
                            active={activeItem === "Profile"}
                            onClick={this.handleItemClick}
                        />
                        <Menu.Item
                            name="My resources"
                            as={Link}
                            to={baseRoute + "/resource"}
                            active={activeItem === "My resources"}
                            onClick={this.handleItemClick}
                        />
                        <Menu.Item
                            name="My reviews"
                            as={Link}
                            to={baseRoute + "/review"}
                            active={activeItem === "My reviews"}
                            onClick={this.handleItemClick}
                        />
                        <Menu.Item
                            name="Logout"
                            as={Link}
                            to={baseRoute + "/login"}
                            active={activeItem === "Logout"}
                            onClick={this.handleItemClick}
                        />
                         <Menu.Item
                            name="Search"
                            as={Link}
                            to={baseRoute + "/search"}
                            active={activeItem === "Search"}
                            onClick={this.handleItemClick}
                        />
                    </Menu>
                </Segment>
            </div>
        );
    }
}

export default HeaderMenu;
