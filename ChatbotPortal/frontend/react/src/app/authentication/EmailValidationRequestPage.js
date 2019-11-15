import React, {Component} from "react";
import {Grid, Message} from "semantic-ui-react";

class EmailValidationRequestPage extends Component {

    render() {
        return (
            <Grid
                onSubmit={e => this.props.handle_login(e, this.state)}
                textAlign="center"
                style={{height: "100vh"}}
                verticalAlign="middle"
            >
                <Grid.Column style={{maxWidth: 450}}>
                    <Message
                        success
                        header='Activate Your Portal'
                        content={this.props.location.state.message}
                    />
                </Grid.Column>
            </Grid>
        )
    }
}

export default EmailValidationRequestPage;