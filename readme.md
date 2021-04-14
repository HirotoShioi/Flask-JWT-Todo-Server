# TODO server

Implement a REST server using Flask to manage todos

- User can login
- User can logout
- Logged in user can add TODO
- Logged in user can get their TODOs
- Logged in user can delete their TODOs
- Logged in user can change TODO's status from incomplete to complete

## Data structure

User:
- userId : Int Or uuid
- username : String
- password : String

Todo:
- body : String
- isComplete : Boolean
- createdAt : UTCTime