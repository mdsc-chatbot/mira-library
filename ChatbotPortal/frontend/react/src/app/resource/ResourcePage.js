import React from "react";
import ResourceList from "./ResourceList";
import ResourceSubmitForm from "./ResourceSubmitForm";
import { Container } from "semantic-ui-react";

export default class ResourcePage extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Container fluid>
        <ResourceSubmitForm />
        <ResourceList />
      </Container>
    );
  }
}
