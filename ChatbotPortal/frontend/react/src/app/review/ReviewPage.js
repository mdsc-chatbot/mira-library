import React from 'react';

export default function ReviewPage() {
	return (
		<container>
			<table class="ui celled table">
				<thead>
					<tr>
					<th>URL</th>
					<th>Type</th>
					<th>Tags</th>
					<th></th>
					</tr>
				</thead>
				<tbody>
					<tr>
					<td>test1</td>
					<td>Disability</td>
					<td>ADHD, ADD</td>
					<td>
						<button class="positive ui button">Approve</button><button class="negative ui button">Reject</button> <label></label>
					</td>
					</tr>
				</tbody>
			</table>
		</container>
	);
}