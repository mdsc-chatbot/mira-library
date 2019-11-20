import React from 'react';
import PropTypes from 'prop-types';
import axios, {CancelToken} from 'axios';
import {Dropdown} from 'semantic-ui-react';
import TagPopup from "./TagPopup";
import { SecurityContext } from "../security/SecurityContext";


export default class TagDropdown extends React.Component {
	static contextType = SecurityContext;

	static mapResponseToDropdownOption = tag => ({
		key : tag.id,
		text : tag.name,
		value : tag.id
	});

	constructor(props) {
		super(props);

		this.state = {
			searchQuery : '',
			tagOptions : [], // options to show to user (to click)
			selectedOptions : [], // selected options so that the current values don't 'disappear' in the UI
			searchRequestCancelToken : null,
		};
	}

	handleChange = (event, data) => {
		// Change value
		this.props.onChange(data.value);

		this.setState({
			searchQuery: ''
		});

		// Find out if the newest value was selected/unselected
		// If selected, add the selected option to selectedOptions
		// If unselected, remove the selected option in selectedOptions
		// This is to make sure the UI is consistent.
		// First, find the selected option using the text of the dropdown
		const selectedText = event.target.textContent;
		const selectedOption = data.options.find(option => option.text === selectedText);

		if (selectedOption !== undefined) {
			// Selected
			const newSelectedOptions = this.state.selectedOptions.slice();
			newSelectedOptions.push(selectedOption);
			this.setState({ selectedOptions : newSelectedOptions })
		} else {
			// Unselected
			const indexOfSelectedOption = this.state.selectedOptions.find(option => option.text === selectedText);
			const newSelectedOptions = this.state.selectedOptions.slice();
			newSelectedOptions.splice(indexOfSelectedOption, 1);
			this.setState({ selectedOptions : newSelectedOptions })
		}
	};

	handleSearchChange = (event, {searchQuery}) => {
		// Cancel previous search requests if possible
		if (this.state.searchRequestCancelToken) {
			this.state.searchRequestCancelToken.cancel()
		}

		// Prepare for promise cancellation
		const source = CancelToken.source();

		// Fetch search results
		axios
            .get(
                "/chatbotportal/resource/fetch-tags",
                {
                    params: {
                        name: searchQuery
                    },
                    cancelToken: source.token
                },
                {
                    headers: { Authorization: `Bearer ${this.context.security.token}` }
                }
            )
            .then(response => {
                // Transform JSON tag into tag that semantic ui's dropdown can read
                let tagOptions = [];
                if (response.data) {
                    tagOptions = response.data.map(TagDropdown.mapResponseToDropdownOption);
                }

                // Add any options that didn't come back from the server, but is selected in the dropdown
                // This makes sure that the value is rendered properly in the UI
                if (this.state.selectedOptions) {
                    for (const selectedOption of this.state.selectedOptions) {
                        if (
                            tagOptions.find(
                                tagOption => tagOption.value === selectedOption.value
                            ) === undefined
                        ) {
                            tagOptions.push(selectedOption);
                        }
                    }
                }

                this.setState({
                    tagOptions
                });
            });

		this.setState({
			searchQuery : searchQuery,
			searchRequestCancelToken : source
		})
	};

	handleNewTagAdded = (tag) => {
		// Adding new tag to values
		const value = this.props.value.slice();
		value.push(tag.id);
		this.props.onChange(value);

		// Adding tag to selected options
		this.setState((prevState) => {
			const selectedOptions = prevState.selectedOptions.slice();
			selectedOptions.push(TagDropdown.mapResponseToDropdownOption(tag));
			const tagOptions = prevState.tagOptions.slice();
			tagOptions.push(TagDropdown.mapResponseToDropdownOption(tag));

			return {
				selectedOptions,
				tagOptions
			};
		});
	};

	render() {
		return (
			<React.Fragment>
				<Dropdown
					fluid
					selection
					multiple
					placeholder='Enter tags'
					search
					options={this.state.tagOptions}
					onChange={this.handleChange}
					onSearchChange={this.handleSearchChange}
					searchQuery={this.state.searchQuery}
					value={this.props.value}
				/>
				<TagPopup onNewTag={this.handleNewTagAdded} />
			</React.Fragment>
		);
	}
}

TagDropdown.propTypes = {
	value : PropTypes.array,
	onChange : PropTypes.func,
};