import React from "react";
import { Route } from "react-router-dom";

import ResourceList from './ResourceList'
import ResourceDetail from './ResourceDetail.js'

const BaseRouter = () => (
  <div>
    <Route exact path="/chatbotportal/" component={ResourceList} />{" "}
    <Route exact path="/chatbotportal/:resourceID/" component={ResourceDetail} />{" "}
  </div>
);

export default BaseRouter;