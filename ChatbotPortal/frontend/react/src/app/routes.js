import React from "react";
import { Route } from "react-router-dom";

import ResourceLayout from './ResourceLayout.js'
import ResourceDetail from './ResourceDetail.js'

const BaseRouter = () => (
  <div>
    <Route exact path="/chatbotportal/" component={ResourceLayout} />{" "}
    <Route exact path="/chatbotportal/:resourceID/" component={ResourceDetail} />{" "}
  </div>
);

export default BaseRouter;