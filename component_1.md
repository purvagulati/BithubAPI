## Component 1 - Basic website display capabilities (REST API)



Link: [Component_1](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/tree/main/src/main/component_1)

#### 1. List All Repositories

-   Capability: Retrieve a list of all repositories.
    
-   Endpoint: /repositories
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns a list of all repositories in the system.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: None
    
-   Output: List of repositories
    
-   Response Codes: 200 OK
    

#### 2. View Specific Repository

-   Capability: View details of a specific repository.
    
-   Endpoint: /repositories/<int:repo_id>
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns details of a specified repository, including its latest commit on the main branch.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer)
    
-   Output: Repository details and latest commit
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 3. List Branches in a Repository

-   Capability: Retrieve a list of all branches in a specific repository.
    
-   Endpoint: /repositories/<int:repo_id>/branches
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns a list of all branches for the specified repository.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer)
    
-   Output: List of branches
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 4. List Tags in a Repository

-   Capability: Retrieve a list of all tags in a specific repository.
    
-   Endpoint: /repositories/<int:repo_id>/tags
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns a list of all tags for the specified repository.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer)
    
-   Output: List of tags
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 5. List All Commits in a Repository

-   Capability: Retrieve all commits in a specific repository with pagination.
    
-   Endpoint: /repositories/<int:repo_id>/commits
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns a paginated list of all commits in the specified repository.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer), Pagination parameters (optional)
    
-   Output: Paginated list of commits
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 6. List Commits on a Specific Branch

-   Capability: Retrieve commits on a specific branch of a repository with pagination.
    
-   Endpoint: /repositories/<int:repo_id>/branches/<branch_name>/commits
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns a paginated list of commits on a specified branch in a repository.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer), Branch name (string), Pagination parameters (optional)
    
-   Output: Paginated list of commits on a branch
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 7. View a Specific Commit

-   Capability: View details of a specific commit in a repository.
    
-   Endpoint: /repositories/<int:repo_id>/commits/<commit_hash>
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns details of a specified commit in a repository.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer), Commit hash (string)
    
-   Output: Commit details
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 8. View Repository Tree for a Commit

-   Capability: View the repository tree for a specific commit.
    
-   Endpoint: /repositories/<int:repo_id>/commits/<commit_hash>/tree
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns the repository tree associated with a specified commit.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer), Commit hash (string)
    
-   Output: Repository tree for the commit
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 9. Retrieve File or Directory Content from a Commit

-   Capability: Retrieve the content of a file or directory from a specific commit.
    
-   Endpoint: /repositories/<int:repo_id>/tree/<tree_hash>/<path:path>
    
-   HTTP Verb: GET
    
-   Endpoint Description: Returns the content of a file or directory for a given path in a commit's tree.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input: Repository ID (integer), Tree hash (string), File/Directory path (string)
    
-   Output: Content of file or directory
    
-   Response Codes: 200 OK, 404 Not Found
    

#### 10. Issues Operations (GET, POST)

-   Capability: Perform operations on issues of a repository.
    
-   Endpoint: /repositories/<int:repo_id>/issues
    
-   HTTP Verb: GET (list issues), POST (create new issue)
    
-   Endpoint Description: For GET, returns a list of issues or filtered by status; for POST, creates a new issue.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input GET: Repository ID (integer), Optional status filter
    
-   Output GET: List of issues or filtered issues
    
-   Input POST: Repository ID (integer), Issue data (JSON)
    
-   Output POST: Newly created issue
    
-   Response Codes: 200 OK, 400 Bad Request, 404 Not Found
    

#### 11. Issue Operations (GET, PUT)

-   Capability: Perform operations on a specific issue of a repository.
    
-   Endpoint: /repositories/<int:repo_id>/issues/<int:issue_id>
    
-   HTTP Verb: GET (view issue), PUT (update issue)
    
-   Endpoint Description: For GET, returns details of a specific issue; for PUT, updates the issue.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input GET: Repository ID (integer), Issue ID (integer)
    
-   Output GET: Issue details
    
-   Input PUT: Repository ID (integer), Issue ID (integer), Update data (JSON)
    
-   Output PUT: Updated issue
    
-   Response Codes: 200 OK, 400 Bad Request, 404 Not Found
    

#### 12. Issue Comments Operations (GET, POST)

-   Capability: Perform operations on comments of a specific issue in a repository.
    
-   Endpoint: /repositories/<int:repo_id>/issues/<int:issue_id>/comments
    
-   HTTP Verb: GET (list comments), POST (add new comment)
    
-   Endpoint Description: For GET, returns a list of comments on an issue; for POST, adds a new comment to the issue.
    
-   Participants/Stakeholders: Users, External services
    
-   Codified Input & Output with Response Codes:
    

-   Input GET: Repository ID (integer), Issue ID (integer)
    
-   Output GET: List of comments
    
-   Input POST: Repository ID (integer), Issue ID (integer), Comment data (JSON)
    
-   Output POST: Newly added comment
    
-   Response Codes: 200 OK, 400 Bad Request, 404 Not Found
    

  

### Error Handling

----------

-   404 Not Found: Returned when a requested resource (repository, branch, commit, issue, etc.) cannot be found.
    
-   400 Bad Request: Returned when the request cannot be processed due to client error (invalid input data, missing fields, etc.).
