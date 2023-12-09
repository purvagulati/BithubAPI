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
    const { pullRequestId, userId, content, lineNumber } = input;
    
    // Check if the pull request exists
    const pullRequest = findPullRequestById(pullRequestId);
    if (!pullRequest) {
       return { error: 'Pull request not found' };
    }
    // Create a new comment with the userId
    const newComment = {
       id: `comment-${Date.now()}`,
       userId, // include the userId in the comment
       content,
       lineNumber,
    };
    comments.push(newComment);
    return newComment;
 }
 
 function addReactionToComment(commentId, userId, reaction) {
    console.log(`addReactionToComment called with commentId: ${commentId}, userId: ${userId}, reaction: ${reaction}`);

    // Find the comment by its ID
    const comment = comments.find(c => c.id === commentId);
    if (!comment) {
        console.error(`Comment with ID ${commentId} not found`);
        throw new Error(`Comment with ID ${commentId} not found`);
    }
    console.log(`Found comment: ${JSON.stringify(comment)}`);

    // Initialize the reactions object if it doesn't exist
    if (!comment.reactions) {
        comment.reactions = {};
        console.log(`Initialized reactions object for commentId: ${commentId}`);
    }

    // Check for existing reaction from the same user
    if (comment.reactions[userId]) {
        throw new Error(`User ${userId} already reacted with ${comment.reactions[userId]}. Updating reaction.`);
    }

    // Add or update the user's reaction to the comment
    comment.reactions[userId] = reaction;
    console.log(`Updated reactions for commentId: ${commentId}: ${JSON.stringify(comment.reactions)}`);

    // Calculate the updated reaction counts
    comment.reactionCounts = calculateReactionCounts(comment.reactions);
    console.log(`Updated reaction counts for commentId: ${commentId}: ${JSON.stringify(comment.reactionCounts)}`);

    // Return the updated comment
    console.log(`Returning updated comment for commentId: ${commentId}`);
    return comment;
}

function removeReactionFromComment(commentId, userId) {
    // Find the comment by its ID
    const comment = comments.find(c => c.id === commentId);
    if (!comment) {
        console.error(`Comment with ID ${commentId} not found`);
        throw new Error(`Comment with ID ${commentId} not found`);
    }

    // Check if the user has reacted to the comment
    if (!comment.reactions || !comment.reactions[userId]) {
        console.error(`No reaction from user ${userId} on comment ${commentId}`);
        throw new Error(`No reaction from user ${userId} on comment ${commentId}`);
    }

    // Remove the user's reaction
    delete comment.reactions[userId];
    console.log(`Removed reaction from user ${userId} on comment ${commentId}`);

    // Recalculate the reaction counts
    comment.reactionCounts = calculateReactionCounts(comment.reactions);
    console.log(`Updated reaction counts for commentId: ${commentId}: ${JSON.stringify(comment.reactionCounts)}`);

    // Return the updated comment
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
    removeReactionFromComment,
    mergePullRequest,
    rejectPullRequest,
 };