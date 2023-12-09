// pullRequestService.js
// Service layer for handling database operations related to pull requests and comments.

const {
    pullRequests,
    comments
 } = require('./db');
 
 // Finds a pull request by its unique ID.
 function findPullRequestById(id) {
    return pullRequests.find(pr => pr.id === id);
 }
 
 // Retrieves pull requests based on provided filters.
 function getPullRequests(filters = {}) {
    return pullRequests.filter(pr => {
       return Object.entries(filters).every(([key, value]) => pr[key] === value);
    });
 }
 
 // Fetches comments associated with a specific pull request.
 function getCommentsByPullRequestId(prId) {
    return comments
       .filter(comment => comment.pullRequestId === prId)
       .map(comment => ({
          ...comment,
          reactionCounts: calculateReactionCounts(comment.reactions)
       }));
 }

 function getCommentsBychangedLines(lineNumber) {
    return comments
       .filter(comment => comment.lineNumber === lineNumber)
       .map(comment => ({
          ...comment,
          reactionCounts: calculateReactionCounts(comment.reactions)
       }));
 }

 
 // Creates a new pull request and adds it to the database.
 function createPullRequest(input) {
    const newPullRequest = {
       id: `pr-${Date.now()}`,
       ...input,
       status: 'pending',
       statusMessage: 'Pull request created',
       createdAt: new Date().toISOString() // Add a creation timestamp
    };
    pullRequests.push(newPullRequest);
    return newPullRequest;
 }
 
 // Adds a new comment to a specific pull request.
 function addCommentToPullRequest(input) {
    const {
       pullRequestId,
       userId,
       content,
       lineNumber
    } = input;
 
    const pullRequest = findPullRequestById(pullRequestId);
    if (!pullRequest) {
       return {
          error: 'Pull request not found'
       };
    }
 
    const newComment = {
       id: `comment-${Date.now()}`,
       userId,
       content,
       lineNumber,
    };
    comments.push(newComment);
    return newComment;
 }
 
 // Adds a reaction to a specific comment.
 function addReactionToComment(commentId, userId, reaction) {
    const comment = comments.find(c => c.id === commentId);
    if (!comment) {
       throw new Error(`Comment with ID ${commentId} not found`);
    }
 
    if (!comment.reactions) {
       comment.reactions = {};
    }
 
    if (comment.reactions[userId]) {
       throw new Error(`User ${userId} already reacted with ${comment.reactions[userId]}.`);
    }
 
    comment.reactions[userId] = reaction;
 
    comment.reactionCounts = calculateReactionCounts(comment.reactions);
 
    return comment;
 }
 
 // Removes a reaction from a comment.
 function removeReactionFromComment(commentId, userId) {
    const comment = comments.find(c => c.id === commentId);
    if (!comment) {
       throw new Error(`Comment with ID ${commentId} not found`);
    }
 
    if (!comment.reactions || !comment.reactions[userId]) {
       throw new Error(`No reaction from user ${userId} on comment ${commentId}`);
    }
 
    delete comment.reactions[userId];
 
    comment.reactionCounts = calculateReactionCounts(comment.reactions);
 
    return comment;
 }
 
 // Calculates the counts of different types of reactions for a comment.
 function calculateReactionCounts(reactions) {
    const reactionCounts = {};
    for (const userId in reactions) {
       const reaction = reactions[userId];
       reactionCounts[reaction] = (reactionCounts[reaction] || 0) + 1;
    }
    return Object.entries(reactionCounts).map(([reaction, count]) => ({
       reaction,
       count
    }));
 }
 
 // Merges a specified pull request if it meets the criteria.
 function mergePullRequest(id) {
    const pullRequest = findPullRequestById(id);
    if (!pullRequest) return {
       error: 'Pull request not found',
       pullRequest: null
    };
 
    if (pullRequest.sourceCommit.startsWith('0')) {
       pullRequest.status = 'merge conflict';
       pullRequest.statusMessage = 'This branch has conflicts that must be resolved';
       return pullRequest;
    }
 
    pullRequest.status = 'merged';
    pullRequest.statusMessage = 'Pull request successfully merged';
    return pullRequest;
 }
 
 // Marks a pull request as rejected.
 function rejectPullRequest(id) {
    const pullRequest = findPullRequestById(id);
    if (!pullRequest) return {
       error: 'Pull request not found',
       pullRequest: null
    };
 
    pullRequest.status = 'rejected';
    return pullRequest;
 }

 
 // Exporting the functions to make them available for other modules.
 module.exports = {
    findPullRequestById,
    getPullRequests,
    getCommentsByPullRequestId,
    createPullRequest,
    addCommentToPullRequest,
    addReactionToComment,
    removeReactionFromComment,
    mergePullRequest,
    rejectPullRequest,
    getCommentsBychangedLines,
 };