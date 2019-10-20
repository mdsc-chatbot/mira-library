import React from "react";
import { Link } from "react-router-dom";
import { Menu, Header, Icon, Button, Label, Image } from "semantic-ui-react";
import { baseRoute } from "./App";

export default function HeaderMenu() {
  return (
    <Menu size="large">
      <Link to={baseRoute}>
        <Menu.Item as="a">
          <Header as="h2" style={{ color: "#3075c9" }}>
            <Icon name="qq" />
            Chatbot Portal
          </Header>
        </Menu.Item>
      </Link>
      <Menu.Item name="home" as="a">
        <Link to={baseRoute}>Home</Link>
      </Menu.Item>
      <Menu.Item name="profile" as="a">
        <Link to={baseRoute + "/profile"}>Profile</Link>
      </Menu.Item>
      <Menu.Item name="resource" as="a">
        <Link to={baseRoute + "/resource"}>Resource</Link>
      </Menu.Item>
      <Menu.Item name="review" as="a">
        <Link to={baseRoute + "/review"}>Review</Link>
      </Menu.Item>
      <Menu.Item position="right">
        <Button as="a">
          <Link to={baseRoute + "/login"}>Login</Link>
        </Button>
        <Button as="a" style={{ marginLeft: "0.5em" }}>
          Sign Up
        </Button>
      </Menu.Item>
      <Menu.Menu position="right">
        <Menu.Item>
          <Label as="a" color="blue" image>
            <Image
              size="tiny"
              src="https://www.iconsdb.com/icons/download/color/4AFFFF/checked-user-24.png"
            />
            My Self
          </Label>
          <Link to={baseRoute + "/profile"} />
        </Menu.Item>
      </Menu.Menu>
    </Menu>
  );
}
