
# GraphQL Schema Design

## Queries

### pullRequestById
- **Input:** `id: ID`
- **Description:** Retrieves details of a specific pull request by its unique ID.
- **Output:** `PullRequest` object with fields `id: ID!`, `title: String!`, `description: String!`, `sourceCommit: String!`, `targetBranch: String!`, `status: String!`, `user: User!`, `comments: [Comment]`, `fileChanges: [FileChange]`.

### pullRequests
- **Input:** `filters: PullRequestFilter`
- **Description:** Fetches a list of pull requests based on given filters such as status.
- **Output:** Array of `PullRequest` objects matching the filter criteria.

### commentsByPullRequest
- **Input:** `pullRequestId: ID`
- **Description:** Lists all comments associated with a specific pull request.
- **Output:** Array of `Comment` objects linked to the given pull request ID.

## Mutations

### createPullRequest
- **Input:** `input: CreatePullRequestInput`
- **Description:** Creates a new pull request with provided details like title, description, source commit, and target branch.
- **Output:** Newly created `PullRequest` object.

### addCommentToPullRequest
- **Input:** `input: AddCommentInput`
- **Description:** Adds a comment to an existing pull request, specifying the pull request ID and content of the comment.
- **Output:** Newly added `Comment` object to the pull request.

### addReactionToComment
- **Input:** `input: AddReactionInput`
- **Description:** Adds a reaction to a specific comment on a pull request.
- **Output:** Updated `Comment` object with the new reaction added.

### mergePullRequest
- **Input:** `id: ID`
- **Description:** Merges an open pull request identified by the given ID.
- **Output:** Updated `PullRequest` object with a status changed to 'merged'.

### rejectPullRequest
- **Input:** `id: ID`
- **Description:** Rejects an open pull request identified by the given ID.
- **Output:** Updated `PullRequest` object with a status changed to 'rejected'.