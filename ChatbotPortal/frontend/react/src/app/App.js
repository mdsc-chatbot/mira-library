/**
 * @file: App.js
 * @summary: main react app, routing to different components
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
import React from "react";
import Homepage from "./Homepage";
import {Route, Switch} from "react-router-dom";
import ProfilePage from "./profile/ProfilePage";
import ResourcePage from "./resource/ResourcePage";
import ResourceDetail from "./resource/ResourceDetail";
import reviewResource from "./review/reviewResource";
import {ReviewPage} from "./review";
import HeaderMenu from "./HeaderMenu";
import LoginPage from "./authentication/LoginPage";
import LogoutPage from "./authentication/LogoutPage";
import {SecurityContextProvider} from "./contexts/SecurityContext";
import Footer from "./Footer";
import ResourceSubmitForm from "./resource/ResourceSubmitForm";
import PublicResourcePage from "./public/PublicResourcePage";
import SearchPage from "./search/SearchPage";
import ManageReviews from "./managereviews/ManageReviews"
import FAQ from "./FAQ.js";
import PasswordResetPage from "./password/PasswordResetPage"
import PasswordResetRequestPage from "./password/PasswordResetRequestPage"
import PasswordChangeForm from "./password/PasswordChangeForm"
import {Segment} from "semantic-ui-react";
import EmailValidationRequestPage from "./authentication/EmailValidationRequestPage";
import ResourceSubmitFormForExtension from "./resource/ResourceSubmitFormForExtension";
import {MenuContextProvider} from './contexts/MenuContext';
import styles from "./App.css";

/**
 * This class renders the re-direction of the links, and menu, according
 * to whether the user is logged in or not
 */

export default function App() {
    const mainPage = () => {
        return(
            <SecurityContextProvider>
                <MenuContextProvider>
                    <Segment  className={styles.headerMenu} inverted attached = 'top'>
                        <HeaderMenu/>
                    </Segment>
                    <Segment className={`${styles.segmentWeb} ${styles.segmentResponsive}`} attached>
                        <Switch>
                            <Route exact path={baseRoute + "/profile"}>
                                <ProfilePage/>
                            </Route>
                            <Route exact path={baseRoute + "/resource"}>
                                <ResourcePage />
                            </Route>
                            <Route exact path={baseRoute + "/review"}>
                                <ReviewPage />
                            </Route>
                            <Route exact path={baseRoute + "/managereviews"}>
                                <ManageReviews />
                            </Route>
                            <Route exact path={baseRoute + "/login"}>
                                <LoginPage />
                            </Route>
                            <Route exact path={baseRoute + "/logout"}>
                                <LogoutPage />
                            </Route>
                            <Route
                                exact path={baseRoute + "/validate/email"}
                                component={EmailValidationRequestPage}
                            />
                            <Route exact path={baseRoute + "/search"}>
                                <SearchPage />
                            </Route>
                            <Route
                                exact
                                path={baseRoute + "/resource/:resourceID"}
                                component={ResourceDetail}
                            />
                            <Route
                                exact
                                path={baseRoute + "/review/:resourceID"}
                                component={reviewResource}
                            />

                            <Route
                                exact path={baseRoute + "/resource_submit"}
                                component={ResourceSubmitForm}
                            />

                            <Route
                                exact path={baseRoute + "/resource_submit/extension/:id/:first_name/:token/:url"}
                                component={ResourceSubmitFormForExtension}
                            />

                            <Route exact path={baseRoute + "/public_resource*"}>
                                {({match}) => (
                                    <PublicResourcePage match={match}/>
                                )}
                            </Route>
                            <Route exact path={baseRoute + "/faq"}>
                                <FAQ />
                            </Route>

                            <Route
                                exact path={baseRoute + "/password"}
                                component={PasswordChangeForm}
                            />
                            <Route
                                exact path={baseRoute + "/password/reset"}
                                component={PasswordResetRequestPage}
                            />
                            <Route
                                exact path={baseRoute + "/password/reset/:uid/:token"}
                                component={PasswordResetPage}
                            />
                            <Route>
                                <Homepage />
                            </Route>

                        </Switch>
                    </Segment>
                </MenuContextProvider>
                <Segment attached = 'bottom' inverted><Footer /></Segment>
            </SecurityContextProvider>);
    };

    /**
     * This renders the Page according to the user and link
     * @returns {React.Fragment}
     */
    return (
        <React.Fragment>
            {mainPage()}
        </React.Fragment>

    );
}

export const baseRoute = "/chatbotportal/app";
