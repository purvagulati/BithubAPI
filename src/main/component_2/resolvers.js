// Importing the pullRequestService module to use its functions.
const dbService = require('./pullRequestService');

const resolvers = {
   // Query resolvers handle fetching data.
   Query: {
      // Resolver for fetching a single pull request by its ID.
      pullRequestById: (_, {
         id
      }) => {
         const pullRequest = dbService.findPullRequestById(id);
         if (pullRequest) {
            // Augmenting the pull request with its comments.
            pullRequest.comments = dbService.getCommentsByPullRequestId(pullRequest.id).map(comment => ({
               ...comment,
               // Transforming reactions object into an array.
               reactions: comment.reactions ? Object.entries(comment.reactions).map(([userId, reaction]) => ({
                  userId,
                  reaction
               })) : []
            }));
         }
         return pullRequest;
      },
      // Resolver for fetching multiple pull requests with optional filters.
      pullRequests: (_, args) => {
         const pullRequests = dbService.getPullRequests(args.filters);
         pullRequests.forEach(pr => {
            // Augmenting each pull request with its comments.
            pr.comments = dbService.getCommentsByPullRequestId(pr.id).map(comment => ({
               ...comment,
               // Transforming reactions object into an array.
               reactions: comment.reactions ? Object.entries(comment.reactions).map(([userId, reaction]) => ({
                  userId,
                  reaction
               })) : []
            }));
         });
         return pullRequests;
      },
      // Resolver for fetching comments of a specific pull request.
      commentsByPullRequest: (_, {
         pullRequestId
      }) => {
         const comments = dbService.getCommentsByPullRequestId(pullRequestId);
         return comments.map(comment => ({
            ...comment,
            // Transforming reactions object into an array.
            reactions: Object.entries(comment.reactions).map(([userId, reaction]) => ({
               userId,
               reaction
            }))
         }));
      }
   },
   // Mutation resolvers handle data modification.
   Mutation: {
      // Resolver to create a new pull request.
      createPullRequest: (_, {
         input
      }) => dbService.createPullRequest(input),
      // Resolver to add a new comment to a pull request.
      addCommentToPullRequest: (_, {
         input
      }) => {
         const result = dbService.addCommentToPullRequest(input);
         if (result.error) {
            throw new Error(result.error); // Error handling for comment creation failure.
         }
         return result;
      },
      // Resolver to add a reaction to a comment.
      addReactionToComment: (_, {
         input
      }) => {
         try {
            const updatedComment = dbService.addReactionToComment(input.id, input.userId, input.reaction);
            updatedComment.reactions = Object.entries(updatedComment.reactions).map(([userId, reaction]) => ({
               userId,
               reaction
            }));
            return updatedComment;
         } catch (error) {
            throw new Error(error.message); // Error handling for reaction addition failure.
         }
      },
      // Resolver to remove a reaction from a comment.
      removeReactionFromComment: (_, {
         input
      }) => {
         try {
            const {
               commentId,
               userId
            } = input;
            const updatedComment = dbService.removeReactionFromComment(commentId, userId);
            updatedComment.reactions = Object.entries(updatedComment.reactions).map(([userId, reaction]) => ({
               userId,
               reaction
            }));
            return updatedComment;
         } catch (error) {
            throw new Error(error.message); // Error handling for reaction removal failure.
         }
      },
      // Resolver to merge a pull request.
      mergePullRequest: (_, {
         id
      }) => dbService.mergePullRequest(id),
      // Resolver to reject a pull request.
      rejectPullRequest: (_, {
         id
      }) => dbService.rejectPullRequest(id),
   },
};

// Exporting the resolvers for use in the GraphQL server.
module.exports = resolvers;