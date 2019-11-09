import React from "react";
import Homepage from "./Homepage";
import { Switch, Route } from "react-router-dom";
import { ProfilePage } from "./profile";
import ResourcePage from "./resource/ResourcePage";
import ResourceDetail from "./resource/ResourceDetail";
import reviewResource from "./review/reviewResource";
import { ReviewPage } from "./review";
import HeaderMenu from "./HeaderMenu";
import LoginPage from "./authentication/LoginPage";
import LogoutPage from "./authentication/LogoutPage";
import { SecurityContextProvider } from "./security/SecurityContext";
import Footer from "./Footer";
import ResourceSubmitForm from "./resource/ResourceSubmitForm";
import PublicResource from "./public/PublicResource";
import SearchPage from "./search/SearchPage";
import FAQ from "./FAQ.js";
import PasswordResetPage from "./password/PasswordResetPage"
import PasswordResetRequestPage from "./password/PasswordResetRequestPage"
import PasswordChangeForm from "./password/PasswordChangeForm"
import UserPage from "./search/UserPage";
import { Divider } from "semantic-ui-react";

export default function App() {
    return (
        <div>
            <SecurityContextProvider>
                <HeaderMenu />
                <Switch>
                    <Route exact path={baseRoute + "/profile"}>
                        <ProfilePage />
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
                    <Route exact path={baseRoute + "/search"}>
                        <SearchPage />
                    </Route>
                    <Route
                        exact
                        path={baseRoute + "/resource/:resourceID"}
                        component={ResourceDetail}
                    ></Route>
                    <Route
                        exact
                        path={baseRoute + "/review/:resourceID"}
                        component={reviewResource}
                    ></Route>
                    <Route exact path={baseRoute + "/resource_submit"}>
                        <ResourceSubmitForm />
                    </Route>
                    <Route exact path={baseRoute + "/public_resource"}>
                        <PublicResource />
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
                <Footer />
            </SecurityContextProvider>
        </div>
    );
}

export const baseRoute = "/chatbotportal/app";
