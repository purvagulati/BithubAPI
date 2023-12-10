# GraphQL API 
## ER Diagram


## Queries

### 1. pullRequestById

- **Input:** `id: ID`
- **Description:** Retrieves the details of a pull request by its unique ID.
- **Output:** A `PullRequest` object, including fields like `id`, `title`, `createdAt`, `description`, `sourceCommit`, `targetBranch`, `status`, `statusMessage`, `user`, `comments`, and `fileChanges`.

### 2. pullRequests

- **Input:** `filters: PullRequestFilter`
- **Description:** Fetches multiple pull requests based on specified filters, such as status.
- **Output:** An array of `PullRequest` objects.

### 3. commentsByPullRequest

- **Input:** `pullRequestId: ID!`
- **Description:** Retrieves all comments associated with a specific pull request.
- **Output:** An array of `Comment` objects related to the pull request.

## Mutations

### 1. createPullRequest

- **Input:** `CreatePullRequestInput`
- **Description:** Creates a new pull request with specified details.
- **Output:** The newly created `PullRequest` object.

### 2. addCommentToPullRequest

- **Input:** `AddCommentInput`
- **Description:** Adds a comment to a specific pull request.
- **Output:** The updated `PullRequest` object, including the new comment.

### 3. addReactionToComment

- **Input:** `AddReactionInput`
- **Description:** Adds a reaction to a specified comment in a pull request.
- **Output:** The updated `Comment` object with the new reaction.

### 4. removeReactionFromComment

- **Input:** `RemoveReactionInput`
- **Description:** Removes a reaction from a particular comment.
- **Output:** The updated `Comment` object with the reaction removed.

### 5. mergePullRequest

- **Input:** `id: ID!`
- **Description:** Merges a specified pull request if it meets the criteria.
- **Output:** The updated `PullRequest` object with a status indicating the result of the merge operation.

### 6. rejectPullRequest

- **Input:** `id: ID!`
- **Description:** Marks a pull request as rejected.
- **Output:** The updated `PullRequest` object with a status of 'rejected'.

## Code Structure

### Modular and Decoupled Code
The codebase is organized to ensure separation of concerns and ease of maintenance, with distinct modules for different functionalities.

### 1. Schema.graphql

This file defines the GraphQL schema for the API, detailing the structure for queries and mutations.

- **Types**: Includes various types such as `PullRequest`, `Commit`, `FileChange`, `ChangedLine`, `Comment`, `UserReaction`, `ReactionCount`, and `User`.
- **Input Types**: Comprises input types like `PullRequestFilter`, `CreatePullRequestInput`, `AddCommentInput`, `AddReactionInput`, and `RemoveReactionInput`.
- **Query Type**: Outlines the available queries, such as `pullRequestById`, `pullRequests`, and `commentsByPullRequest`.
- **Mutation Type**: Specifies the available mutations, including `createPullRequest`, `addCommentToPullRequest`, `addReactionToComment`, `removeReactionFromComment`, `mergePullRequest`, and `rejectPullRequest`.

[View Schema.graphql](https://github.com/your-repository-link/schema.graphql)

### 2. Resolvers.js

Contains the logic for handling GraphQL queries and mutations.

- **Queries**: Implements functions to fetch data as per the specified queries.
- **Mutations**: Handles data modifications and updates as defined in the mutations.

[View Resolvers.js](https://github.com/your-repository-link/resolvers.js)

### 3. db.js

Acts as a mock database for the system, containing:

- **Mock Data for Pull Requests and Comments**: Arrays storing mock data simulating pull requests and comments.
- **Utility Functions**: Functions that provide and manipulate mock data for the resolvers.

[View Db.js](https://github.com/your-repository-link/db.js)

### 4. pullRequestService.js

This file is the service layer handling database operations related to pull requests and comments.

- It includes functions for finding, creating, and updating pull requests and comments.
- Ensures the business logic is separated from the data fetching logic.

[View pullRequestService.js](https://github.com/your-repository-link/pullRequestService.js)

## Testing

1. **Testcase Identifier:** `Query1-Happy`
   - **Description:** Fetch details of a pullRequest by its unique ID.
   - **Input:**
     ```json
       {
       "pullRequestByIdId": "pr-12345"
       }
      ```
   - **Output:** 
     ```json
     {
     "data": {
     "pullRequestById": {
      "id": "pr-12345",
      "title": "Fix login issue",
      "createdAt": "2023-12-09T09:08:27.997Z",
      "description": "This pull request fixes the login issue reported in issue #54321.",
      "sourceCommit": "123abc",
      "commits": "blackbox tests,whitebox test",
      "targetBranch": "main",
      "status": "pending",
      "statusMessage": "Pull request is open",
      "user": {
        "id": "user-1",
        "name": "Alice",
        "email": "alice@cmu.andrew.edu"
      },
      "comments": [
        {
          "id": "comment-1",
          "userId": "user-1",
          "content": "Looks good to me.",
          "reactions": [
            {
              "userId": "user-1",
              "reaction": "👍"
            },
            {
              "userId": "user-4",
              "reaction": "👍"
            }
          ],
          "reactionCounts": [
            {
              "reaction": "👍",
              "count": 2
            }
          ],
          "pullRequestId": "pr-12345",
          "lineNumber": null
        },
        {
          "id": "comment-3",
          "userId": "user-1",
          "content": "Looks good to me.",
          "reactions": [
            {
              "userId": "user-1",
              "reaction": "👍"
            },
            {
              "userId": "user-2",
              "reaction": "😀"
            }
          ],
          "reactionCounts": [
            {
              "reaction": "👍",
              "count": 1
            },
            {
              "reaction": "😀",
              "count": 1
            }
          ],
          "pullRequestId": "pr-12345",
          "lineNumber": null
        }
      ],
      "fileChanges": [
        {
          "id": "fileChange-1",
          "fileName": "login.js",
          "changes": "Added null check for user credentials and updated login logic",
          "changedLines": [
            {
              "line": 55,
              "code": "if (userCredentials != null) {",
              "type": "+",
              "comments": []
            },
            {
              "line": 56,
              "code": "   performLogin(userCredentials);",
              "type": "+",
              "comments": []
            }
          ]
        },
        {
          "id": "fileChange-2",
          "fileName": "README.md",
          "changes": "Updated installation instructions and contact information",
          "changedLines": [
            {
              "line": 10,
              "code": "Run `npm install` to install all dependencies.",
              "type": "+",
              "comments": [
                {
                  "id": "comment-38",
                  "userId": "user-3",
                  "content": "This line needs refactoring.",
                  "reactions": [
                    {
                      "userId": "user-1",
                      "reaction": "👍"
                    }
                  ],
                  "reactionCounts": [
                    {
                      "reaction": "👍",
                      "count": 1
                    }
                  ],
                  "pullRequestId": "pr-12345",
                  "lineNumber": 10
                }
              ]
            },
            {
              "line": 25,
              "code": "For support, contact xyz@andrew.cmu.edu.",
              "type": "+",
              "comments": [
                {
                  "id": "comment-45",
                  "userId": "user-3",
                  "content": "This line needs refactoring.",
                  "reactions": [
                    {
                      "userId": "user-19",
                      "reaction": "👍"
                    }
                  ],
                  "reactionCounts": [
                    {
                      "reaction": "👍",
                      "count": 1
                    }
                  ],
                  "pullRequestId": "pr-12345",
                  "lineNumber": 25
                }
              ]
            }
          ]
        }
      ]
      }}}
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/q1h.png))
   - **Remarks:** Successful case.

2. **Testcase Identifier:** `Query1-Error`
   - **Description:** Fetch details of a pullRequest that does not exist.
   - **Inputs:** 
     ```json
     {
      "pullRequestByIdId": "pr-0"
     }
     ```
   - **Output:** 
     ```json
     {
      "errors": [
      {
      "message": "Pull request with ID pr-0 not found."
      }
     ],
     "data": {
      "pullRequestById": null
      }
     }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/q1e.png))
   - **Remarks:** Doctor not found.

3. **Testcase Identifier:** `Query2-Happy`
   - **Description:** Fetches multiple pull requests based on specified filter, that is PR status.
   - **Input:** 
     ```json
      {
       "filters": {
                "status": "pending"
                 }
      }
     ```
   - **Output:** 
     ```json
     {
     "data": {
      "pullRequests": [
      {
        "id": "pr-12345",
        "title": "Fix login issue",
        "createdAt": "2023-12-09T09:08:27.997Z",
        "description": "This pull request fixes the login issue reported in issue #54321.",
        "sourceCommit": "123abc",
        "commits": "blackbox tests,whitebox test",
        "targetBranch": "main",
        "status": "pending",
        "statusMessage": "Pull request is open",
        "user": {
          "id": "user-1",
          "name": "Alice",
          "email": "alice@cmu.andrew.edu"
        },
        "comments": [
          {
            "id": "comment-1",
            "userId": "user-1",
            "content": "Looks good to me.",
            "reactions": [
              {
                "userId": "user-1",
                "reaction": "👍"
              },
              {
                "userId": "user-4",
                "reaction": "👍"
              }
            ],
            "reactionCounts": [
              {
                "reaction": "👍",
                "count": 2
              }
            ]
          },
          {
            "id": "comment-3",
            "userId": "user-1",
            "content": "Looks good to me.",
            "reactions": [
              {
                "userId": "user-1",
                "reaction": "👍"
              },
              {
                "userId": "user-2",
                "reaction": "😀"
              }
            ],
            "reactionCounts": [
              {
                "reaction": "👍",
                "count": 1
              },
              {
                "reaction": "😀",
                "count": 1
              }
            ]
          }
        ]
      },
      {
        "id": "pr-67890",
        "title": "Update README",
        "createdAt": "2023-02-09T09:08:20.997Z",
        "description": "Updates the README file with new instructions.",
        "sourceCommit": "0456def",
        "commits": null,
        "targetBranch": "develop",
        "status": "pending",
        "statusMessage": "Pull request is open",
        "user": {
          "id": "user-2",
          "name": "Bob",
          "email": "bob@example.com"
        },
        "comments": [
          {
            "id": "comment2",
            "userId": "user-2",
            "content": "Please add more details to the README changes.",
            "reactions": [
              {
                "userId": "user-1",
                "reaction": "👍"
              },
              {
                "userId": "user-2",
                "reaction": "😭"
              }
            ],
            "reactionCounts": [
              {
                "reaction": "👍",
                "count": 1
              },
              {
                "reaction": "😭",
                "count": 1
              }
            ]
          }
        ]
      }
      ] } }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/q2h.png)
   - **Remarks:** Successful case.

4. **Testcase Identifier:** `Query2-Error`
   - **Description:** Fetches multiple pull requests based on specified filter, that is an inavlid PR status.
   - **Inputs:** 
     ```json
      {
     "filters": {
         "status": "open"
        }
      }
     ```
   - **Output:** 
     ```json
      {
        "errors": [
       {
         "message": "Invalid status filter: open"
       }
                 ],
       "data": {
           "pullRequests": null
        }
     }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/q2e.png))
   - **Remarks:** 'pending', 'merged', 'rejected', 'merge conflict' are the only valid PR statuses available in BitHub. 

5. **Testcase Identifier:** `Query3-Happy`
   - **Description:** Retrieves all comments associated of a valid pull request.
   - **Inputs:** 
     ```json
     {
         "pullRequestId": "pr-12345"
     }
     ```
   - **Output:** 
     ```json
     {
       "data": {
       "commentsByPullRequest": [
      {
        "id": "comment-1",
        "userId": "user-1",
        "content": "Looks good to me.",
        "reactions": [
          {
            "userId": "user-1",
            "reaction": "👍"
          },
          {
            "userId": "user-4",
            "reaction": "👍"
          }
        ],
        "reactionCounts": [
          {
            "reaction": "👍",
            "count": 2
          }
        ],
        "pullRequestId": "pr-12345"
      },
      {
        "id": "comment-3",
        "userId": "user-1",
        "content": "Looks good to me.",
        "reactions": [
          {
            "userId": "user-1",
            "reaction": "👍"
          },
          {
            "userId": "user-2",
            "reaction": "😀"
          }
        ],
        "reactionCounts": [
          {
            "reaction": "👍",
            "count": 1
          },
          {
            "reaction": "😀",
            "count": 1
          }
        ],
        "pullRequestId": "pr-12345"
      }
      ]  } }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/q3h.png))
   - **Remarks:** Successful case.

6. **Testcase Identifier:** `Query3-Error`
   - **Description:** Comments associated of an invalid pull request `id` return null.
   - **Inputs:** 
     ```json
     {
         "pullRequestId": "pr-0"
     }
     ```
   - **Output:** 
     ```json
        {
        "errors": [
       {
         "message": "Pull request with ID pr-0 not found."
       }
              ],
      "data": {
          "commentsByPullRequest": null
            }
       }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/q3e.png)
   - **Remarks:** No comments are displayed as the pull request with specified id does not exist.

7. **Testcase Identifier:** `Mut1-Happy`
   - **Description:** Creates a new pull request with specified details.
   - **Inputs:** 
     ```json
     {
     "input": {
       "title": "Bug Fix: User Authentication Error",
       "description": "Resolves an issue where users were unable to log in under certain conditions.",
      "sourceCommit": "78910ghijkl",
      "targetBranch": "development",
      "user": {
           "id": "user-456",
           "name": "Purva",
          "email": "purva@cmu.andrew.edu"
        }
     }
     ```
   - **Output:** 
     ```json
        {
     "data": {
     "createPullRequest": {
      "id": "pr-1702169036320",
      "title": "Bug Fix: User Authentication Error",
      "createdAt": "2023-12-10T00:43:56.320Z",
      "description": "Resolves an issue where users were unable to log in under certain conditions.",
      "sourceCommit": "78910ghijkl",
      "targetBranch": "development",
      "status": "pending",
      "statusMessage": "Pull request created",
      "user": {
        "id": "user-456",
        "name": "Purva",
        "email": "purva@cmu.andrew.edu"
      } } } }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m1h.png)
   - **Remarks:** New pull request with specified details created

8. **Testcase Identifier:** `Mut1-Error`
   - **Description:** Attemots to creates a new pull request with some missing details.
   - **Inputs:** 
     ```json
     {
     "input": {
       "title": "Bug Fix: User Authentication Error",
       "description": "Resolves an issue where users were unable to log in under certain conditions.",
      "targetBranch": "development",
      "user": {
           "id": "user-456",
           "name": "Purva",
          "email": "purva@cmu.andrew.edu"
        }
     }
     ```
   - **Output:** 
     ```json
        {
      "errors": [
       {
      "message": "Variable \"$input\" got invalid value { title: \"Bug Fix: User Authentication Error\", description: \"Resolves an issue where users were unable to log in under certain conditions.\", targetBranch: \"development\", user: { id: \"user-456\", name: \"Purva\", email: \"purva@cmu.andrew.edu\" } }; Field \"sourceCommit\" of required type \"String!\" was not provided."
      }  ]  }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m1h.png)
   - **Remarks:** GraphQL performs its own validation based on theschema. The mutation's input fields are marked as non-nullable (using !) in the GraphQL schema, is these fields are missing or null in the request, GraphQ throws a validation error before the resolver is executed. 

9. **Testcase Identifier:** `Mut2-Happy`
   - **Description:** Adds a comment to a specific pull request.
   - **Inputs:** 
     ```json
     {
     "input": {
      "pullRequestId": "pr-12345",
     "content": "Add unit tests for each class",
      "userId": "purvag"
     } }
     ```
   - **Output:** 
     ```json
     {
     "data": {
      "addCommentToPullRequest": {
      "id": "comment-1702173626504",
      "userId": "purvag",
      "content": "Add unit tests for each class"
     } } }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m2h.png)
   - **Remarks:** Successful Case. 

10. **Testcase Identifier:** `Mut2-Error`
   - **Description:** Does not add a comment to an invalid pull request.
   - **Input:** 
     ```json
     {
     "input": {
      "pullRequestId": "pr-0",
     "content": "Add unit tests for each class",
      "userId": "purvag"
     } }
     ```
   - **Output:** 
     ```json
      {
     "errors": [
      {
         "message": "Pull request not found"
      }
      ],
        "data": {
       "addCommentToPullRequest": null
     } }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m2e.png)
   - **Remarks:** Comment was not added as PR id is not valid.

11. **Testcase Identifier:** `Mut3-Happy`
   - **Description:** Adds a reaction to a specified comment in a pull request.
   - **Input:** 
   ```json
    {
     "input": { 
      "id": "comment-1",
      "userId": "user-9",
      "reaction": "😀"
    } }
  ```
   - **Output:** 
     ```json
     {
     "data": {
      "addReactionToComment": {
      "id": "comment-1",
      "userId": "user-1",
      "content": "Looks good to me.",
      "reactions": [
        {
          "userId": "user-1",
          "reaction": "👍"
        },
        {
          "userId": "user-4",
          "reaction": "👍"
        },
        {
          "userId": "user-9",
          "reaction": "😀"
        }
      ],
      "reactionCounts": [
        {
          "reaction": "👍",
          "count": 2
        },
        {
          "reaction": "😀",
          "count": 1
        }
      ],
      "pullRequestId": "pr-12345",
      } } }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m3h.png)
   - **Remarks:** Reaction was added to the comment.

12. **Testcase Identifier:** `Mut3-Error1`
   - **Description:** Attempts to add a reaction to an invalid comment.
   - **Input:** 
     ```json
     {
     "input": { 
      "id": "comment-0",
      "userId": "user-9",
      "reaction": "😀"
       }  }
     ```
   - **Output:** 
     ```json
     {
     "errors": [
      {
      "message": "Comment with ID comment-0 not found"
      }
     ],
     "data": {
       "addReactionToComment": null
     }
     }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m3e1.png)
   - **Remarks:** Comment id not found.

13. **Testcase Identifier:** `Mut3-Error2`
   - **Description:** Attempts to add a second reaction to an invalid comment.
   - **Input:** 
     ```json
     {
     "input": { 
      "id": "comment-1",
      "userId": "user-1",
      "reaction": "😀"
       }  }
     ```
   - **Output:** 
     ```json
     {
     "errors": [
      {
      "message": "User user-1 already reacted with 👍."
      }
     ],
     "data": {
       "addReactionToComment": null
     }
     }
     ```
   - **Screenshot:** ![Screenshot](https://github.com/17-625-API-Design-F23/final-team-project-team-mutators/blob/component2-graphql/src/main/component_2/screenshots/m3e2.png)
   - **Remarks:** User already had a reaction to that comment.


