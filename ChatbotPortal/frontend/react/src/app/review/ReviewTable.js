import React, { Component } from "react";
import axios from "axios";
import { Table } from "semantic-ui-react";

export default class ReviewTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      resources: {}
    };
  }

  get_resources = () => {
    axios.get("http://127.0.0.1:8000/api/resource").then(res => {
      this.setState({
        resources: res.data
      });
    });
  };

  componentDidMount() {
    this.get_resources();
  }

  render() {
    return (
        <div>
            <div style={{paddingTop:30, paddingLeft:100, paddingRight:100}}>
                You have N pending reviews
				<button class="ui right floated button" >Completed Reviews</button>
                <Table class="ui celled table">
                    <thead>
                        <tr>
                        <th>URL</th>
                        <th>Comments</th>
                        <th>Tags</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                        {/*placeholder resource references until i figure out the actual response
                        I think the use is like {resources.JSON KEY HERE} ex. {resources.url}*/}
                        <td>test</td>
                        <td>great for kids</td>
                        <td>kids, ADHD</td>
                        <td>
                            <button class="positive ui button">Approve</button>
                            <button class="negative ui button">Reject</button>
                        </td>
                        </tr>
                    </tbody>
                </Table>
            </div>
        </div>
    );
  }
}