# GraphQL API for Pull Request Management

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


