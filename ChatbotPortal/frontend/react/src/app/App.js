import React from "react";
import Homepage from "./Homepage";
import {Route, Switch} from "react-router-dom";
import {ProfilePage} from "./profile";
import ResourcePage from "./resource/ResourcePage";
import ResourceDetail from "./resource/ResourceDetail";
import reviewResource from "./review/reviewResource";
import {ReviewPage} from "./review";
import HeaderMenu from "./HeaderMenu";
import LoginPage from "./authentication/LoginPage";
import LogoutPage from "./authentication/LogoutPage";
import {SecurityContextProvider} from "./security/SecurityContext";
import Footer from "./Footer";
import ResourceSubmitForm from "./resource/ResourceSubmitForm";
import PublicResourcePage from "./public/PublicResourcePage";
import SearchPage from "./search/SearchPage";
import FAQ from "./FAQ.js";
import PasswordResetPage from "./password/PasswordResetPage"
import PasswordResetRequestPage from "./password/PasswordResetRequestPage"
import PasswordChangeForm from "./password/PasswordChangeForm"
import {Responsive, Segment} from "semantic-ui-react";
import EmailValidationRequestPage from "./authentication/EmailValidationRequestPage";
import ResourceSubmitFormForExtension from "./resource/ResourceSubmitFormForExtension";
import styles from "./App.css";

export default function App() {
    const mainPage = () => {
        return(<SecurityContextProvider>
            <Segment inverted attached = 'top'> <HeaderMenu /></Segment>
            <Segment attached>
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
            <div></div>

            <Segment inverted><Footer /></Segment>
        </SecurityContextProvider>);
    };
    return (

        <Segment.Group>

            <Responsive minWidth={768}>
                <div>
                    {mainPage()}
                </div>
            </Responsive>

            <Responsive maxWidth={767}>
                    {mainPage()}
            </Responsive>

        </Segment.Group>

    );
}

export const baseRoute = "/chatbotportal/app";
