
''' 
TEST CASES:

1 Resource submission basic: only url and resource rating
INPUT
- url: https://www.google.com/
- resource rating: 1


2 Resource submission basic: invalid url and resource rating
INPUT
- url: this_is_an_invalid_url
- resource usefulness rating: 2


3 Resource submission basic: not found url and resource rating
INPUT
- url: http://127.0.0.1:8000/notfoundurl
- resource usefulness rating: 3


4 Resource submission with tag and comment: url, resource rating, tag, comment
INPUT
- url: https://www.ualberta.ca/
- resource usefulness rating: 4
- tags: university, alberta, test (will need to add these tags to database before searching)
- comments: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa strong. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede link mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi.


5 Resource submission with tag, comment and attachment: url, resource rating, tag, comment, attachement
INPUT
- url: https://reactjs.org/
- resource usefulness rating: 5
- tags: react, web development, test (will need to add these tags to database before searching)
- comments: React makes it painless to create interactive UIs. Design simple views for each state in your application, and React will efficiently update and render just the right components when your data changes.

'''
