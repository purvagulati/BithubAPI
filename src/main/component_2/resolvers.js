const dbService = require('./pullRequestService');

const resolvers = {
  Query: {
    pullRequestById: (_, { id }) => {
      const pullRequest = dbService.findPullRequestById(id);
      if (pullRequest) {
        pullRequest.comments = dbService.getCommentsByPullRequestId(pullRequest.id).map(comment => ({
          ...comment,
          reactions: comment.reactions ? Object.entries(comment.reactions).map(([userId, reaction]) => ({ userId, reaction })) : []
        }));
      }
      return pullRequest;
    },
    pullRequests: (_, args) => {
      const pullRequests = dbService.getPullRequests(args.filters);
      pullRequests.forEach(pr => {
        pr.comments = dbService.getCommentsByPullRequestId(pr.id).map(comment => ({
          ...comment,
          reactions: comment.reactions ? Object.entries(comment.reactions).map(([userId, reaction]) => ({ userId, reaction })) : []
        }));
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
    addCommentToPullRequest: (_, { input }) => {
      const result = dbService.addCommentToPullRequest(input);
      if (result.error) {
        throw new Error(result.error);
      }
      return result;
    },
    addReactionToComment: (_, { input }) => {
      try {
        const updatedComment = dbService.addReactionToComment(input.id, input.userId, input.reaction);
        updatedComment.reactions = Object.entries(updatedComment.reactions).map(([userId, reaction]) => ({
          userId,
          reaction
         }));
         return updatedComment;
      } catch (error) {
        throw new Error(error.message);
      }
    },
    mergePullRequest: (_, { id }) => dbService.mergePullRequest(id),
    rejectPullRequest: (_, { id }) => dbService.rejectPullRequest(id),
  },
};

module.exports = resolvers;