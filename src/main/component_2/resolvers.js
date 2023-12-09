// resolver.js
const dbService = require('./pullRequestService');

const resolvers = {
  Query: {
    pullRequestById: (_, { id }) => {
      const pullRequest = dbService.findPullRequestById(id);
      if (pullRequest) {
        pullRequest.comments = dbService.getCommentsByPullRequestId(pullRequest.id);
      }
      return pullRequest;
    },
    pullRequests: (_, args) => {
      const pullRequests = dbService.getPullRequests(args.filters);
      pullRequests.forEach(pr => {
        pr.comments = dbService.getCommentsByPullRequestId(pr.id);
      });
      return pullRequests;
    },
    commentsByPullRequest: (_, { pullRequestId }) => {
      const comments = dbService.getCommentsByPullRequestId(pullRequestId);
      return comments.map(comment => ({
        ...comment,
        reactions: Object.entries(comment.reactions).map(([userId, reaction]) => ({ userId, reaction }))
      }));
    }    
  },
  Mutation: {
    createPullRequest: (_, { input }) => dbService.createPullRequest(input),
    addCommentToPullRequest: (_, { input }) => dbService.addCommentToPullRequest(input),
    addReactionToComment: (_, { input }) => dbService.addReactionToComment(input.commentId, input.reaction),
    mergePullRequest: (_, { id }) => dbService.mergePullRequest(id),
    rejectPullRequest: (_, { id }) => dbService.rejectPullRequest(id),
    addReactionToComment: (_, { input }) => {
      // input should contain commentId, userId, and reaction
      const comment = dbService.addReactionToComment(input.commentId, input.userId, input.reaction);
      return comment;
    },
  },
};

module.exports = resolvers;
