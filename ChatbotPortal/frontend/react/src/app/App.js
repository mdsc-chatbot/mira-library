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
          <Route
            exact
            path={baseRoute + "/resource/:resourceID"}
            component={ResourceDetail}
          ></Route>
          <Route>
            <Homepage />
          </Route>
        </Switch>
      </SecurityContextProvider>
    </div>
  );
}

export const baseRoute = "/chatbotportal/app";
