import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";
import {AutoSizer, Column, InfiniteLoader, Table} from 'react-virtualized';
import 'react-virtualized/styles.css';

// const {Table, Column} = ReactVirtualized;

class SearchBar extends Component {
    static contextType = SecurityContext;

    BASE_URL = 'http://127.0.0.1:8000/authentication/';

    constructor(props) {
        super(props);
        this.state = {
            // users: '',
            rowHeight:0,
            loadedData: []
        }
    }

    componentDidMount() {
        // this.get_users();
        // this.getRowsFromServer(1, 1);
        this.loadMoreRows({startIndex: 0,stopIndex: 1})
    }

    // get_users = () => {
    //     // Defining header and content-type for accessing authenticated information
    //     const options = {
    //         'Content-Type': 'application/json',
    //         'Authorization': `Bearer ${this.context.security.token}`
    //     };
    //     axios
    //         .get(this.BASE_URL + 'super/search/alluser/', {headers : options})
    //         .then(
    //             response => {
    //                 // console.log(response.data);
    //                 this.setState({
    //                     users : response.data
    //                 });
    //                 this.setState({
    //                     loadedData: this.state.loadedData.concat(this.state.users)
    //                 });
    //                 console.log(this.state.loadedData)
    //             },
    //             error => {
    //                 console.log(error);
    //             }
    //         );
    // };

    // loadMoreRows = ({startIndex, stopIndex}) => {
    //     console.log("I am inside loadmorerows");
    //     // simulate a request
    //     setTimeout(() => {this.actualLoadMore({startIndex, stopIndex})}, 500);
    //     // we need to return a promise
    //     return new Promise((resolve, reject) => {
    //         this.promiseResolve = resolve;
    //     })
    // };
    //
    // actualLoadMore = ({startIndex, stopIndex}) => {
    //     this.getRowsFromServer(startIndex, stopIndex);
    //     this.promiseResolve();
    // }

    loadMoreRows = ({startIndex, stopIndex}) => {
        this.props.getDataFromServer({startIndex, stopIndex}).then( (result) => {
            var tempData = this.state.loadedData
            result.forEach(returnItem => {
                tempData.push(returnItem)
            })
            this.setState({loadedData:tempData})
        })
    }

    getRowsFromServer = ({startIndex, stopIndex }) => {
        return new Promise((resolve, reject) => {
            fetch(`http://127.0.0.1:8000/authentication/super/search/id_range/${startIndex}/${stopIndex}/`)
                .then(response => response.json())
                .then(result => {
                    resolve(result)
                })
        })
    }
    // getRowsFromServer = (startIndex, stopIndex) => {
    //     console.log("I am inside getRows");
    //
    //     const url = `http://127.0.0.1:8000/authentication/super/search/id_range/${startIndex}/${stopIndex}/`;
    //
    //     // Having the permission header loaded
    //     const options = {
    //         'Content-Type': 'application/json',
    //         'Authorization': `Bearer ${this.context.security.token}`
    //     };
    //
    //     /**
    //      * Calling the backend API
    //      */
    //     axios
    //         .get(url, {headers: options})
    //         .then(
    //             response => {
    //                 console.log(response.data)
    //                 this.setState({
    //                     loadedData: this.state.loadedData.concat(response.data)
    //                 });
    //                 console.log(this.state.loadedData)
    //             },
    //             error => {
    //                 console.log(error);
    //             }
    //         )
    // };

    isRowLoaded = ({index}) => {
        console.log(index);
        return !!this.state.loadedData[index];
    };



    render() {
        return(
            <div className="container">
                <h1>Users</h1>
                <InfiniteLoader
                    // This function gets the row index and must say if the row data are already loaded or not
                    isRowLoaded={this.isRowLoaded}
                    // A function that receives a start index and a stop index and should return a promise that
                    // should be resolved once the new data area loaded
                    loadMoreRows={this.loadMoreRows}
                    // The number of rows in the original data base
                    rowCount={10000000}
                >
                    {/*onRowsRender: This function should be passed as the child's onRowsRender property,
                    it informs loader when the user is scrolling*/}
                    {/*registerChild: This function should be set as the child's ref property. It enables a set
                    of rows to be refreshed once their data has finished loading*/}
                    {({onRowsRendered, registerChild}) => (
                        <AutoSizer>
                            {({width}) =>
                                <Table
                                    ref={registerChild}
                                    onRowsRendered={onRowsRendered}
                                    rowClassName='table-row'
                                    // The height of the table header
                                    headerHeight={40}
                                    // The width of the table
                                    width={width}
                                    // The height of the table
                                    height={400}
                                    // The height of the rows
                                    rowHeight={40}
                                    // The number of rows (real time is expensive operation)
                                    rowCount={this.state.loadedData.length}
                                    // A function that given the row index returns the rwo object
                                    rowGetter={({index}) => this.state.loadedData[index]}
                                >
                                    <Column
                                        label='Id'
                                        // The key name of the row object used to retrieve the value inserted in the cell
                                        dataKey='id'
                                        // The width of the column
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Email'
                                        dataKey='email'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='First Name'
                                        dataKey='first_name'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Last Name'
                                        dataKey='last_name'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Joined on'
                                        dataKey='date_joined'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Last Login'
                                        dataKey='last_login'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Activated'
                                        dataKey='is_active'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Reviewer'
                                        dataKey='is_reviewer'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Staff'
                                        dataKey='is_staff'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Admin'
                                        dataKey='is_superuser'
                                        width={width * 0.1}
                                    />
                                    <Column
                                        label='Affiliation'
                                        dataKey='affiliation'
                                        width={width * 0.1}
                                    />
                                </Table>}
                        </AutoSizer>)}
                </InfiniteLoader>
            </div>
        );
    }
}

export default SearchBar;
