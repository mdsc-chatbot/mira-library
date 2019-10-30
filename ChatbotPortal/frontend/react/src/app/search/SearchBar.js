// import _ from 'lodash'
// import faker from 'faker'
// import axios from "axios";
// import React, {Component} from 'react'
// import {Grid, Search, Segment, Header} from 'semantic-ui-react'
// import {SecurityContext} from "../security/SecurityContext";
//
// const initialState = {isLoading: false, results: [], value: ''};
//
// const source = _.times(5, () => ({
//     title: faker.company.companyName(),
//     description: faker.company.catchPhrase(),
//     image: faker.internet.avatar(),
//     price: faker.finance.amount(0, 100, 2, '$'),
// }));
//
// export default class SearchBar extends Component {
//     state = initialState;
//     static contextType = SecurityContext;
//     handleResultSelect = (e, {result}) => this.setState({value: result.title});
//
//     handleSearchChange = (e, {value}) => {
//         this.setState({isLoading: true, value});
//
//         setTimeout(() => {
//             if (this.state.value.length < 1) return this.setState(initialState);
//
//             const re = new RegExp(_.escapeRegExp(this.state.value), 'i');
//             const isMatch = (result) => re.test(result.title);
//
//             this.setState({
//                 isLoading: false,
//                 results: _.filter(source, isMatch),
//             })
//         }, 300)
//     };
//
//     BASE_SEARCH_URL = 'http://127.0.0.1:8000/authentication/';
//
//     componentDidMount() {
//         axios.get(this.BASE_SEARCH_URL)
//     }
//
//     render() {
//         const {isLoading, value, results} = this.state;
//
//         return (
//             <Grid>
//                 <Grid.Column width={6}>
//                     <Search
//                         loading={isLoading}
//                         onResultSelect={this.handleResultSelect}
//                         onSearchChange={_.debounce(this.handleSearchChange, 500, {
//                             leading: true,
//                         })}
//                         results={results}
//                         value={value}
//                         {...this.props}
//                     />
//                 </Grid.Column>
//                 <Grid.Column width={10}>
//                   <Segment>
//                     <Header>State</Header>
//                     <pre style={{ overflowX: 'auto' }}>
//                       {JSON.stringify(this.state, null, 2)}
//                     </pre>
//                     <Header>Options</Header>
//                     <pre style={{ overflowX: 'auto' }}>
//                       {JSON.stringify(source, null, 2)}
//                     </pre>
//                   </Segment>
//                 </Grid.Column>
//             </Grid>
//         )
//     }
// }
