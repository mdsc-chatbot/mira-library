import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";
import {AutoSizer, Column, SortDirection, Table, InfiniteLoader} from 'react-virtualized';
import 'react-virtualized/styles.css';
import {render} from "react-dom";
import SearchPage from "./SearchPage";
import LoginPage from "../authentication/LoginPage";
import {Redirect} from "react-router";
import {baseRoute} from "../App";
import {Header, Icon, Image} from "semantic-ui-react";
import {Link} from "react-router-dom";
import UserPage from "./UserPage";
import { Modal } from 'semantic-ui-react'


/**
 * This component has a regular view for showing all the users by repeatedly loading data
 * from the server. Instead of loading everything at once, the view uses virtualized
 * react table library to fetch the data in a promise resolve manner to ensure the
 * maximum performance through providing infinite scroll to the user (admin).
 */
class SearchTable extends Component {

    // The security context
    static contextType = SecurityContext;

    BASE_URL = 'http://127.0.0.1:8000/authentication/';


    constructor(props) {
        super(props);

        /**
         * The state of the component
         */
        this.state = {
            rowHeight: 0,
            loadedData: [],
            // loadedData: this.props.loadedData
            redirectToUserProfile: false,
            rowData: '',
            modal_open: true,
        }
    }

    /**
     * Upon mounting the component, the first row from the database is called,
     * and stored in the state
     */
    componentDidMount() {
        this.loadMoreRows({startIndex: 0, stopIndex: 1});
    }

    /**
     * This function loads more rows upon scrolling down
     * @param startIndex = the starting row to be fetched from the database
     * @param stopIndex = the ending row to be fetched from the database
     */
    loadMoreRows = ({startIndex, stopIndex}) => {
        // Getting rows from server; upon successful completion, every items in the
        // result is pushed in a temporary variable which in turn is stored in the
        // loadedData state.
        this.getRowsFromServer({startIndex, stopIndex}).then((result) => {
            let tempData = this.state.loadedData.slice();
            result.forEach(returnItem => {
                tempData.push(returnItem)
            });
            this.setState({loadedData: tempData})
        })
    };

    /**
     * This function calls the backend API to fetch a range of rows asynchronously
     * @param startIndex = the starting row to be fetched from the database
     * @param stopIndex = the ending row to be fetched from the database
     */
    getRowsFromServer = ({startIndex, stopIndex}) => {
        /**
         * Creating a promise
         */
        return new Promise((resolve, reject) => {
            const url = `http://127.0.0.1:8000/authentication/super/rows/${startIndex}/${stopIndex}/`;

            // Having the permission header loaded
            const options = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.context.security.token}`
            };

            axios
                .get(url, {headers: options})
                .then(response => {
                    // Resolving the promise
                    resolve(response.data)
                }, error => {
                    // Rejecting the promise
                    reject(error)
                })
        })
    };

    /**
     * This function checks if a row is already loaded in the view
     * @param index = Index of the row that needs to be loaded
     */
    isRowLoaded = ({index}) => {
        if (this.props.is_advance_used) {
            return !!this.props.loadedData[index]
        } else {
            return !!this.state.loadedData[index]
        }
    };

    rowCount = () => {
        return this.props.is_advance_used ?
            this.props.loadedData.length:
            this.state.loadedData.length
    };

    rowGetter = ({index}) => {
        if (this.props.is_advance_used) {
            return this.props.loadedData[index]
        } else {
            return this.state.loadedData[index]
        }
    };

    handleRowClick = ({index, rowData}) => {
        console.log(rowData);
        this.setState({
            redirectToUserProfile: true,
            rowData: rowData
        });

    };


    // sortDirection = () => {
    // }
    // sortBy = () => {
    // }

    close_modal = ()=> this.setState({modal_open:false})
    render() {
        return (
            <div className="container">
                <h1>Users</h1>
                <InfiniteLoader
                    // This function gets the row index and must say if the row data are already loaded or not
                    isRowLoaded={this.isRowLoaded}
                    // A function that receives a start index and a stop index and should return a promise that
                    // should be resolved once the new data area loaded
                    loadMoreRows={this.props.is_advance_used ? () => null : this.loadMoreRows}
                    // loadMoreRows={this.loadMoreRows}
                    // The number of rows in the original data base
                    rowCount={1000000}
                >
                    {/*onRowsRender: This function should be passed as the child's onRowsRender property,
                    it informs loader when the user is scrolling*/}
                    {/*registerChild: This function should be set as the child's ref property. It enables a set
                    of rows to be refreshed once their data has finished loading*/}

                    {
                        ({onRowsRendered, registerChild}) => (
                            <AutoSizer>
                                {({width}) =>
                                    <Table
                                        ref={registerChild}
                                        onRowsRendered={onRowsRendered}
                                        //sortBy={'first_name'}
                                        //sortDirection={SortDirection.ASC}
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
                                        // rowCount={this.props.loadedData.length}
                                        rowCount={this.rowCount()}
                                        // A function that given the row index returns the rwo object
                                        // rowGetter={({index}) => this.props.loadedData[index]}
                                        rowGetter={this.rowGetter}
                                        onRowClick={this.handleRowClick}
                                    >
                                        <Column
                                            label='Id'
                                            // The key name of the row object used to retrieve the value inserted in the cell
                                            dataKey='id'
                                            // The width of the column
                                            width={width * 0.02}
                                        />
                                        <Column
                                            label='Photo'
                                            // The key name of the row object used to retrieve the value inserted in the cell
                                            dataKey='profile_picture'
                                            // The width of the column
                                            width={width * 0.05}
                                            cellRenderer={({cellData}) => (cellData ?
                                                (<img
                                                    src={`/static/${cellData.split('/')[cellData.split('/').length - 1]}`}
                                                    // style='height: 100%; width: 100%; object-fit: contain'
                                                    width={'100%'}
                                                    height={'100%'}
                                                    alt={'Profile Picture'}
                                                />)
                                                : cellData)}
                                        />
                                        <Column
                                            label='Email'
                                            dataKey='email'
                                            width={width * 0.3}
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
                                            width={width * 0.05}
                                        />
                                        <Column
                                            label='Reviewer'
                                            dataKey='is_reviewer'
                                            width={width * 0.05}
                                        />
                                        <Column
                                            label='Staff'
                                            dataKey='is_staff'
                                            width={0}
                                        />
                                        <Column
                                            label='Admin'
                                            dataKey='is_superuser'
                                            width={0}
                                        />
                                        <Column
                                            label='Affiliation'
                                            dataKey='affiliation'
                                            width={width * 0.5}
                                        />
                                        <Column
                                            label='Submissions'
                                            dataKey='submissions'
                                            width={0}
                                        />
                                        <Column
                                            label='Points'
                                            dataKey='points'
                                            width={0}
                                        />
                                    </Table>}
                            </AutoSizer>)
                    }
                </InfiniteLoader>

                {this.state.redirectToUserProfile ? (
                    <Modal open={this.state.modal_open} onClose={this.close_modal}>
                        <Modal.Content>
                    <UserPage rowData={this.state.rowData}/>
                        </Modal.Content>
                    </Modal>
                ) : null}
            </div>
        );
    }
}

export default SearchTable;

//https://medium.com/@joedister/using-react-virtualized-infiniteloader-autosizer-and-table-with-material-ui-styles-react-76d3596b6c93
//https://www.abidibo.net/blog/2019/01/11/react-virtualized-infinite-scrolling-table-how/