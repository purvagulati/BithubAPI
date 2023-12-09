// pullRequestService.js
// Service layer for handling database operations

const {
    pullRequests,
    comments
 } = require('./db');
 
 function findPullRequestById(id) {
    return pullRequests.find(pr => pr.id === id);
 }
 
 function getPullRequests(filters = {}) {
    return pullRequests.filter(pr => {
       return Object.entries(filters).every(([key, value]) => pr[key] === value);
    });
 }
 
 function getCommentsByPullRequestId(prId) {
    return comments
      .filter(comment => comment.pullRequestId === prId)
      .map(comment => ({
        ...comment,
        reactionCounts: calculateReactionCounts(comment.reactions)
      }));
  }

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
 
 function addCommentToPullRequest(input) {
    const newComment = {
       id: `comment-${Date.now()}`,
       ...input
    };
    comments.push(newComment);
    return newComment;
 }
 
 function addReactionToComment(commentId, userId, reaction) {
    const comment = comments.find(c => c.id === commentId);
    if (!comment) return null;
    comment.reactions[userId] = reaction;
    return comment;
  }

 
  function calculateReactionCounts(reactions) {
    const reactionCounts = {};
  
    // Iterate over the object of reactions
    for (const userId in reactions) {
      const reaction = reactions[userId];
      reactionCounts[reaction] = (reactionCounts[reaction] || 0) + 1;
    }
  
    return Object.entries(reactionCounts).map(([reaction, count]) => ({ reaction, count }));
  }
  
  
 
 function mergePullRequest(id) {
    const pullRequest = findPullRequestById(id);
    if (!pullRequest) return {
       error: 'Pull request not found',
       pullRequest: null
    };
 
    // Check if the sourceCommit starts with zero
    if (pullRequest.sourceCommit.startsWith('0')) {
       pullRequest.status = 'merge conflict';
       pullRequest.statusMessage = 'This branch has conflicts that must be resolved';
       // Returning the pullRequest object with a conflict message
       return pullRequest;
    }
 
    pullRequest.status = 'merged';
    pullRequest.statusMessage = 'Pull request successfully merged';
    return pullRequest;
 
 }
 
 function rejectPullRequest(id) {
    const pullRequest = findPullRequestById(id);
    if (!pullRequest) return {
       error: 'Pull request not found',
       pullRequest: null
    };
 
    pullRequest.status = 'rejected';
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