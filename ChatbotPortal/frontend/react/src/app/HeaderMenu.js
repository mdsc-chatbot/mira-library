import React from "react";
import { Link } from "react-router-dom";
import { Menu, Header, Icon, Segment } from "semantic-ui-react";
import { baseRoute } from "./App";

export default function HeaderMenu() {
    return (
        <div>
            <Segment style={{ padding: "3em 0em" }} vertical>
                <Menu pointing secondary size="large">
                    <Menu.Item as="a" style={{ paddingLeft: 50 }}>
                        <Link to={baseRoute}>
                            <Header as="h2" style={{ color: "#3075c9" }}>
                                <Icon name="qq" />
                                Chatbot Portal
                            </Header>
                        </Link>
                    </Menu.Item>
                    <Menu.Item position="right">
                        <Link to={baseRoute + "/resource"}>Resources</Link>
                    </Menu.Item>
                    <Menu.Item style={{ paddingRight: 100 }}>
                        <Link to={baseRoute + "/login"}>Login</Link>
                    </Menu.Item>
                </Menu>
            </Segment>
        </div>
    );
}
