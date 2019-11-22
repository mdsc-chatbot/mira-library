import React, {Component} from 'react';
import axios from "axios";
import {AutoSizer, Column, InfiniteLoader, Table} from 'react-virtualized';
import 'react-virtualized/styles.css';
import {Modal} from "semantic-ui-react";
import UserPage from "./UserPage";
import {SecurityContext} from "../contexts/SecurityContext";


/**
 * This component has a regular view for showing all the users by repeatedly loading data
 * from the server. Instead of loading everything at once, the view uses virtualized
 * react table library to fetch the data in a promise resolve manner to ensure the
 * maximum performance through providing infinite scroll to the user (admin).
 */
class SearchTable extends Component {

    /**
     * The security context that has the permission token and other user credential details.
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    /**
     * This is the constructor that initializes the state
     * @param props : properties passed from the parent component
     */
    constructor(props) {
        super(props);

        /**
         * This is the state of the component
         * @type {{redirectToUserProfile: boolean, totalPage: number, nextPage: *, rowData: string, loadedData: []}}
         */
        this.state = {
            totalPage: 1,
            nextPage: this.props.url,
            loadedData: [],
            rowData: '',
            redirectToUserProfile: false,
        }
    }

    /**
     * Upon mounting the component, the first row from the database is called,
     * and stored in the state
     */
    componentDidMount() {
        this.loadMoreRows({startIndex: 0});
    }

    /**
     * As the state changes, this function is called.
     * It only gets executed upon clicking the search button.
     * @param prevProps
     * @param prevState
     * @param snapshot
     */
    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.search_clicked) {
            /**
             * Since state change is asynchronous,
             * the callback function assures that load more row is performed
             * after the asynchronous operation is over.
             */
            this.setState({
                totalPage: 1,
                nextPage: this.props.url,
                loadedData: [],
                rowData: '',
            }, () => {
                this.loadMoreRows({startIndex: 0});
            });
        }
    }

    /**
     * This function loads more rows upon scrolling down
     * @param startIndex = the starting row to be fetched from the database
     * @param stopIndex = the ending row to be fetched from the database
     */
    loadMoreRows = ({startIndex, stopIndex}) => {
        console.log({startIndex, stopIndex});
        // Getting rows from server; upon successful completion, every items in the
        // result is pushed in a temporary variable which in turn is stored in the
        // loadedData state.
        console.log(this.state.nextPage)
        if (!!this.state.nextPage) {
            this.getRowsFromServer(this.state.nextPage)
                .then((result) => {
                    // state and props should be immutable in react principles,
                    // the slice function just creates a copy of the state loadedData
                    // instead of passing it by reference, so that we can alter the
                    // variable without violating the react principles
                    let tempData = this.state.loadedData.slice();
                    result['results'].forEach(returnItem => {
                        tempData.push(returnItem)
                    });
                    // Now change the state properly using react principle of setState
                    this.setState({
                        totalPage: result['count'],
                        nextPage: result['next'],
                        loadedData: tempData,
                    })
                })
        }

    };

    /**
     * This function calls the backend API to fetch a range of rows asynchronously
     * @param nextPage = the page to fetched from the backend
     */
    getRowsFromServer = (nextPage) => {
        /**
         * Creating a promise to perform asynchronous operation
         */
        return new Promise((resolve, reject) => {

            // Having the permission header loaded
            const options = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.context.security.token}`
            };

            axios
                .get(nextPage, {headers: options})
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
        return !!this.state.loadedData[index]
    };

    /**
     * This function count the number of rows by getting the length of the loadedData
     */
    rowCount = () => {
        return this.state.loadedData.length
    };

    /**
     * This function gets the row from the loadedData
     * @param index = The position of row to be fetched
     */
    rowGetter = ({index}) => {
        return this.state.loadedData[index]
    };

    /**
     * This function handles the events after clicking a row on the table
     * @param index = The position of row on the table
     * @param rowData = The data that is stored in the row by key:value pair
     */
    handleRowClick = ({rowData}) => {
        this.setState({
            redirectToUserProfile: true,
            rowData: rowData
        });
    };

    /**
     * This function gets back to the table from the modal after clicking the dimmed region.
     */
    modalClose = () => {
        this.setState({
            redirectToUserProfile: false
        });
        // Reloading the page after modal closes
        // window.location.reload();
    };

    /**
     * This function renders the infinite loader containing table.
     */
    render() {
        return (
            <div className="container">
                <InfiniteLoader
                    // This function gets the row index and must say if the row data are already loaded or not
                    isRowLoaded={this.isRowLoaded}
                    // A function that receives a start index and a stop index and should return a promise that
                    // should be resolved once the new data area loaded
                    loadMoreRows={this.loadMoreRows}
                    // The number of rows in the original data base
                    rowCount={1000000}
                    threshold={2}
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
                                        rowClassName='table-row'
                                        // The height of the table header
                                        headerHeight={40}
                                        // The width of the table
                                        width={width}
                                        // The height of the table
                                        height={650}
                                        // The height of the rows
                                        rowHeight={40}
                                        // The number of rows (real time is expensive operation)
                                        rowCount={this.rowCount()}
                                        // A function that given the row index returns the rwo object
                                        rowGetter={this.rowGetter}
                                        // Triggers the modal after clicking the a row
                                        onRowClick={this.handleRowClick}
                                    >
                                        <Column
                                            label='Id'
                                            // The key name of the row object used to retrieve the value inserted in the cell
                                            dataKey='id'
                                            // The width of the column
                                            width={width * 0.01}
                                        />
                                        <Column
                                            label='Email'
                                            dataKey='email'
                                            width={width * 0.125}
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
                                            label='Activate'
                                            dataKey='is_active'
                                            width={width * 0.07}
                                        />
                                        <Column
                                            label='Reviewer'
                                            dataKey='is_reviewer'
                                            width={width * 0.07}
                                        />
                                        <Column
                                            label='Staff'
                                            dataKey='is_staff'
                                            width={width * 0.07}
                                        />
                                        <Column
                                            label='Submissions'
                                            dataKey='submissions'
                                            width={width * 0.05}
                                        />
                                        <Column
                                            label='Pending'
                                            dataKey='pending_submissions'
                                            width={width * 0.05}
                                        />
                                        <Column
                                            label='Approved'
                                            dataKey='approved_submissions'
                                            width={width * 0.05}
                                        />
                                        <Column
                                            label='Photo'
                                            // The key name of the row object used to retrieve the value inserted in the cell
                                            dataKey='profile_picture'
                                            // The width of the column
                                            width={width * 0.0}
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
                                            label='Joined on'
                                            dataKey='date_joined'
                                            width={width * 0.0}
                                        />
                                        <Column
                                            label='Last Login'
                                            dataKey='last_login'
                                            width={width * 0.0}
                                        />

                                        <Column
                                            label='Admin'
                                            dataKey='is_superuser'
                                            width={width * 0.0}
                                        />
                                        <Column
                                            label='Affiliation'
                                            dataKey='affiliation'
                                            width={width * 0.0}
                                        />
                                        <Column
                                            label='Points'
                                            dataKey='points'
                                            width={width * 0.0}
                                        />
                                    </Table>}
                            </AutoSizer>)
                    }
                </InfiniteLoader>
                {/* The modal to be shown for user profile */}
                <Modal
                    open={this.state.redirectToUserProfile}
                    onClose={this.modalClose}
                >
                    <Modal.Content>
                        <UserPage rowData={this.state.rowData}/>
                    </Modal.Content>
                </Modal>
            </div>
        );
    }
}

export default SearchTable;

//https://medium.com/@joedister/using-react-virtualized-infiniteloader-autosizer-and-table-with-material-ui-styles-react-76d3596b6c93
//https://www.abidibo.net/blog/2019/01/11/react-virtualized-infinite-scrolling-table-how/