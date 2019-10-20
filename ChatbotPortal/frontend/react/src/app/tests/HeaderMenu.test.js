import React from 'react';
import {MemoryRouter} from 'react-router';
import { render } from '@testing-library/react'
import HeaderMenu from '../HeaderMenu'

test('sees if it renders all header elements', () => {
	const { getByText } = render(
		<MemoryRouter
			initialEntries={["/chatbotportal/app"]}
			initialIndex={0}
		>
			<HeaderMenu />
		</MemoryRouter>
	);

	expect(getByText('Home')).toBeDefined();
	expect(getByText('Profile')).toBeDefined();
	expect(getByText('Resource')).toBeDefined();
	expect(getByText('Review')).toBeDefined();
});