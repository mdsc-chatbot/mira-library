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
import Footer from "./Footer";
import ResourceSubmitForm from "./resource/ResourceSubmitForm";
import PublicResource from "./public/PublicResource";

export default function App() {
    return (
        <div style={{ display:"flex", minHeight:"100vh", flexDirection:"column" }}>
            <SecurityContextProvider>
                <HeaderMenu />
                <div style={{ flex:1 }}>
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
                </div>
                <Footer />
            </SecurityContextProvider>
        </div>
    );
}

export const baseRoute = "/chatbotportal/app";
