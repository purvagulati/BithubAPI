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




