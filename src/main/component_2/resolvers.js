// resolver.js
const db = require('./db');

const resolvers = {
  Query: {
    pullRequestById: (_, { id }) => db.findPullRequestById(id),
    pullRequests: (_, args) => db.getPullRequests(args.filters),
    commentsByPullRequest: (_, { pullRequestId }) => db.getCommentsByPullRequestId(pullRequestId),
  },
  Mutation: {
    createPullRequest: (_, { input }) => db.createPullRequest(input),
    addCommentToPullRequest: (_, { input }) => db.addCommentToPullRequest(input),
    addReactionToComment: (_, { input }) => db.addReactionToComment(input.commentId, input.reaction),
    mergePullRequest: (_, { id }) => db.mergePullRequest(id),
    rejectPullRequest: (_, { id }) => db.rejectPullRequest(id),
  },
};

module.exports = resolvers;
