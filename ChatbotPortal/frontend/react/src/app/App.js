import React from "react";
import Homepage from "./Homepage";
import { Switch, Route } from "react-router-dom";
import { ProfilePage } from "./profile";
import ResourcePage from "./resource/ResourcePage";
import ResourceDetail from "./resource/ResourceDetail";
import { ReviewPage } from "./review";
import HeaderMenu from "./HeaderMenu";
import LoginPage from "./authentication/LoginPage";
import { SecurityContextProvider } from "./security/SecurityContext";
import { Divider } from "semantic-ui-react";
import Footer from "./Footer";
import ResourceSubmitForm from "./resource/ResourceSubmitForm";
import PublicResource from "./public/PublicResource";
import SearchPage from "./search/SearchPage"

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
                    <Route exact path={baseRoute + "/search"}>
                        <SearchPage />
                    </Route>
                    <Route
                        exact
                        path={baseRoute + "/resource/:resourceID"}
                        component={ResourceDetail}
                    >
                    </Route>
                    <Route exact path={baseRoute + "/resource_submit"}>
                        <ResourceSubmitForm />
                    </Route>
                    <Route exact path={baseRoute + "/public_resource"}>
                        <PublicResource />
                    </Route>
                    <Route>
                        <Homepage />
                    </Route>
                </Switch>
                <Divider />
                <Footer />
            </SecurityContextProvider>
        </div>
    );
}

export const baseRoute = "/chatbotportal/app";
