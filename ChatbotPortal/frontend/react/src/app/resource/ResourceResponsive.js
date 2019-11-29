/**
 * @file: ResourceResponsive.js
 * @summary: Component that adjust all resources components paddings responsively to mobile or desktop
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

import React, { Component } from "react";
import { Responsive } from "semantic-ui-react";

export class ResourceResponsive extends Component {
    render() {
        return (
            <div>
                <Responsive {...Responsive.onlyMobile}>
                    <div style={{ paddingTop: 30, paddingLeft: 15, paddingRight: 15, paddingBottom: 30 }}>
                        {this.props.resource_component}
                    </div>
                </Responsive>
                <Responsive minWidth={768}>
                    <div style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30 }}>
                        {this.props.resource_component}
                    </div>
                </Responsive>
            </div>
        );
    }
}

export default ResourceResponsive;
