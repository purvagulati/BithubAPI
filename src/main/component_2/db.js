// db.js
// Mock database for demonstration purposes

const pullRequests = []; // Array to store pull requests
const comments = []; // Array to store comments

// Function to find a pull request by ID
function findPullRequestById(id) {
  return pullRequests.find(pr => pr.id === id);
}

// Function to get a list of pull requests
function getPullRequests(filters = {}) {
  return pullRequests.filter(pr => {
    return Object.entries(filters).every(([key, value]) => pr[key] === value);
  });
}

// Function to get comments by pull request ID
function getCommentsByPullRequestId(prId) {
  return comments.filter(comment => comment.pullRequestId === prId);
}

// Function to create a new pull request
function createPullRequest(input) {
  const newPullRequest = { id: `pr-${Date.now()}`, ...input, status: 'open' };
  pullRequests.push(newPullRequest);
  return newPullRequest;
}

// Function to add a comment to a pull request
function addCommentToPullRequest(input) {
  const newComment = { id: `comment-${Date.now()}`, ...input };
  comments.push(newComment);
  return newComment;
}

// Function to add a reaction to a comment
function addReactionToComment(commentId, reaction) {
  const comment = comments.find(c => c.id === commentId);
  if (!comment) return null;

  comment.reactions = comment.reactions || [];
  comment.reactions.push(reaction);
  return comment;
}

// Functions to change the status of a pull request
function mergePullRequest(id) {
  const pullRequest = findPullRequestById(id);
  if (pullRequest) pullRequest.status = 'merged';
  return pullRequest;
}

function rejectPullRequest(id) {
  const pullRequest = findPullRequestById(id);
  if (pullRequest) pullRequest.status = 'rejected';
  return pullRequest;
}

module.exports = {
  findPullRequestById,
  getPullRequests,
  getCommentsByPullRequestId,
  createPullRequest,
  addCommentToPullRequest,
  addReactionToComment,
  mergePullRequest,
  rejectPullRequest,
};
