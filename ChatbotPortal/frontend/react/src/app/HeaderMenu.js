/**
 * @file: HeaderMenu.js
 * @summary: Component for website header, conditionally links to different pages depends on if the user is logged in
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
import React, { Component } from 'react';
import {
  Dropdown,
  Header,
  Icon,
  Menu,
  Responsive,
  Segment,
  Image,
} from 'semantic-ui-react';
import { baseRoute } from './App';
import { Link } from 'react-router-dom';
import { SecurityContext } from './contexts/SecurityContext';
import { MenuContext } from './contexts/MenuContext';
import styles from './App.css';
import ownStyles from './HeaderMenu.css';

/**
 * This class renders the Header Menu of a logged in user
 */
export class HeaderMenu extends Component {
  static contextType = SecurityContext;
  constructor(props) {
    super(props);

    this.state = {};
  }
  handleItemClick = (e, { name }) => this.setState({ activeItem: name });

  /**
   * This class renders the header menu of a logged in user for Web and Tablet
   */
  headerMenuWeb = () => {
    const { activeItem } = this.state;
    var static_url = "{% get_static_prefix %}";
    return (
      <React.Fragment>
        <Menu inverted fluid pointing secondary size='large'>
          {/* 
https://ibb.co/3fG4zSj
https://ibb.co/KsctrDz
https://ibb.co/9wx9pbr */}

          <a
            href={baseRoute}
            active={activeItem === 'Home'}
            onClick={this.handleItemClick}
          >
            <img
              style={{ padding: '-10px', maxWidth: '170px' }}
              src="/static/logo.png"
              alt='logo2x'
              border='0'
            />
          </a>
          

          <Menu.Item
            name='Public Resources'
            as={Link}
            to={baseRoute + '/public_resource'}
            position='right'
            active={activeItem === 'Public Resources'}
            onClick={this.handleItemClick}
          />

          <Menu.Item
            name='FAQ'
            as={Link}
            to={baseRoute + '/faq'}
            active={activeItem === 'FAQ'}
            onClick={this.handleItemClick}
          />

          {this.context.security.is_logged_in && (
            <Menu.Item
              name='My Profile'
              as={Link}
              to={baseRoute + '/profile'}
              active={activeItem === 'My Profile'}
              onClick={this.handleItemClick}
            />
          )}

          {this.context.security.is_logged_in && (
            <Menu.Item
              name='My resources'
              as={Link}
              to={baseRoute + '/resource'}
              active={activeItem === 'My resources'}
              onClick={this.handleItemClick}
            />
          )}

          {this.context.security.is_logged_in &&
            this.context.security.is_reviewer && (
              <Menu.Item
                name='My reviews'
                as={Link}
                to={baseRoute + '/review'}
                active={activeItem === 'My reviews'}
                onClick={this.handleItemClick}
              />
          )}

          {this.context.security.is_logged_in &&
            this.context.security.is_editor && (
              <Menu.Item
                name='Manage reviews'
                as={Link}
                to={baseRoute + '/managereviews'}
                active={activeItem === 'Manage reviews'}
                onClick={this.handleItemClick}
              />
          )}

          {this.context.security.is_logged_in &&
            this.context.security.is_staff && (
              <Menu.Item
                name='Manage users'
                as={Link}
                to={baseRoute + '/search'}
                active={activeItem === 'Search'}
                onClick={this.handleItemClick}
              />
            )}

          {this.context.security.is_logged_in && (
            <Menu.Item
              name='Logout'
              as={Link}
              to={baseRoute + '/logout'}
              active={activeItem === 'Logout'}
              onClick={this.handleItemClick}
            />
          )}

          {!this.context.security.is_logged_in && (
            <Menu.Item
              name='Login'
              as={Link}
              to={baseRoute + '/login'}
              active={activeItem === 'Login'}
              onClick={this.handleItemClick}
            />
          )}
        </Menu>
      </React.Fragment>
    );
  };

  /**
   * This class renders the header menu of a logged in user for Mobile
   */
  headerMenuMobile = () => {
    const { activeItem } = this.state;
    return (
      <React.Fragment>
        <Menu inverted pointing fluid widths={2} size='small'>
          <a
            href={baseRoute}
            active={activeItem === 'Home'}
            onClick={this.handleItemClick}
          >
            <img
              style={{ padding: '-10px', maxWidth: '120px' }}
              src='/static/logo.png'
              alt='logo2x'
              border='0'
            />
          </a>

          <Menu.Menu
            position='right'
            className={`${ownStyles.fullWidthListbox} ${ownStyles.marginRightMenu}`}
          >
            <Dropdown item text='Menu' floating labeled>
              <Dropdown.Menu className={styles.headerMobile}>
                <Dropdown.Item>
                  <Menu.Item
                    name='Public Resources'
                    as={Link}
                    to={baseRoute + '/public_resource'}
                    position='right'
                    active={activeItem === 'Public Resources'}
                    onClick={this.handleItemClick}
                  />
                </Dropdown.Item>

                {this.context.security.is_logged_in && (
                  <Dropdown.Item>
                    <Menu.Item
                      name='My Profile'
                      as={Link}
                      to={baseRoute + '/profile'}
                      active={activeItem === 'My Profile'}
                      onClick={this.handleItemClick}
                    />
                  </Dropdown.Item>
                )}

                {this.context.security.is_logged_in && (
                  <Dropdown.Item>
                    <Menu.Item
                      name='My resources'
                      as={Link}
                      to={baseRoute + '/resource'}
                      active={activeItem === 'My resources'}
                      onClick={this.handleItemClick}
                    />
                  </Dropdown.Item>
                )}

                {this.context.security.is_logged_in &&
                  this.context.security.is_reviewer && (
                    <Dropdown.Item>
                      <Menu.Item
                        name='My reviews'
                        as={Link}
                        to={baseRoute + '/review'}
                        active={activeItem === 'My reviews'}
                        onClick={this.handleItemClick}
                      />
                    </Dropdown.Item>
                )}

                {this.context.security.is_logged_in &&
                  this.context.security.is_editor && (
                    <Menu.Item
                      name='Manage reviews'
                      as={Link}
                      to={baseRoute + '/managereviews'}
                      active={activeItem === 'Manage reviews'}
                      onClick={this.handleItemClick}
                    />
                )}

                {this.context.security.is_logged_in &&
                  this.context.security.is_staff && (
                    <Dropdown.Item>
                      <Menu.Item
                        name='Manage users'
                        as={Link}
                        to={baseRoute + '/search'}
                        active={activeItem === 'Search'}
                        onClick={this.handleItemClick}
                      />
                    </Dropdown.Item>
                  )}

                {this.context.security.is_logged_in && (
                  <Dropdown.Item>
                    <Menu.Item
                      name='Logout'
                      as={Link}
                      to={baseRoute + '/logout'}
                      active={activeItem === 'Logout'}
                      onClick={this.handleItemClick}
                    />
                  </Dropdown.Item>
                )}

                {!this.context.security.is_logged_in && (
                  <Dropdown.Item>
                    <Menu.Item
                      name='Login'
                      as={Link}
                      to={baseRoute + '/login'}
                      active={activeItem === 'Login'}
                      onClick={this.handleItemClick}
                    />
                  </Dropdown.Item>
                )}

                <Dropdown.Item>
                  <Menu.Item
                    name='FAQ'
                    as={Link}
                    to={baseRoute + '/faq'}
                    active={activeItem === 'FAQ'}
                    onClick={this.handleItemClick}
                  />
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Menu.Menu>
        </Menu>
      </React.Fragment>
    );
  };

  /**
   * This renders the HeaderMenu
   * @returns {React.Fragment}
   */
  render() {
    return (
      <MenuContext.Consumer>
        {(MenuContext) => (
          <React.Fragment>
            {MenuContext.menu_visibility ? (
              <Segment.Group>
                <Responsive maxWidth={1009}>
                  {this.headerMenuMobile()}
                </Responsive>

                <Responsive minWidth={1010}>
                  <React.Fragment>{this.headerMenuWeb()}</React.Fragment>
                </Responsive>
              </Segment.Group>
            ) : (
              <Menu inverted fluid pointing secondary size='large'>
                <Header as='h2' style={{ color: '#3075c9', paddingLeft: 50 }}>
                  <img
                    src={require('./logo/logo_transparent.ico')}
                    alt={'NDD Portal'}
                    size='medium'
                    ui
                    wrapped
                  />
                </Header>
              </Menu>
            )}
          </React.Fragment>
        )}
      </MenuContext.Consumer>
    );
  }
}
export default HeaderMenu;
