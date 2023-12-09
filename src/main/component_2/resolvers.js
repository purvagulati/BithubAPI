// Importing the pullRequestService module to use its functions.
const dbService = require('./pullRequestService');

// Helper function to transform comments
function transformInlineComments(comments) {
   return comments.map(comment => ({
      ...comment,
      // Transforming reactions object into an array.
      reactions: comment.reactions ? Object.entries(comment.reactions).map(([userId, reaction]) => ({
         userId,
         reaction
      })) : []
   }));
}

function transformComments(comments) {
  return comments
     .filter(comment => comment.lineNumber == null) // Filter out comments with a line number
     .map(comment => ({
        ...comment,
        reactions: comment.reactions ? Object.entries(comment.reactions).map(([userId, reaction]) => ({
           userId,
           reaction
        })) : []
     }));
}

const resolvers = {
   // Queries
   Query: {
      // Resolver for fetching a single pull request by its ID.
      pullRequestById: (_, {
         id
      }) => {
         const pullRequest = dbService.findPullRequestById(id);
         if (!pullRequest) {
          throw new Error(`Pull request with ID ${id} not found.`);
         }
         if (pullRequest) {
            // Augmenting the pull request with its comments using transformComments function.
            pullRequest.comments = transformComments(dbService.getCommentsByPullRequestId(pullRequest.id));

            pullRequest.fileChanges.forEach(fileChange => {
              fileChange.changedLines.forEach(changedLine => {
                 changedLine.comments = transformInlineComments(dbService.getCommentsBychangedLines(changedLine.line));
              });
           });
           
         }
         return pullRequest;
      },
      // Resolver for fetching multiple pull requests with optional filters.
      pullRequests: (_, args) => {
         const pullRequests = dbService.getPullRequests(args.filters);
         pullRequests.forEach(pr => {
            // Augmenting each pull request with its comments using transformComments function.
            pr.comments = transformComments(dbService.getCommentsByPullRequestId(pr.id));

            
         });
         return pullRequests;
      },
      // Resolver for fetching comments of a specific pull request.
      commentsByPullRequest: (_, {
         pullRequestId
      }) => {
         const comments = dbService.getCommentsByPullRequestId(pullRequestId);
         return transformComments(comments);
      }
   },

   // Mutations
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
         // Transform the added comment's reactions
         result.comments = transformComments(result.comments);
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
      mergePullRequest: (_, { id }) => {
        const pullRequest = dbService.mergePullRequest(id);
        if (!pullRequest || pullRequest.error) {
           throw new Error(pullRequest.error || `Pull request with ID ${id} not found.`);
        }
     
        // Augmenting the pull request with its comments using transformComments function.
        pullRequest.comments = transformComments(dbService.getCommentsByPullRequestId(pullRequest.id));
        return pullRequest;
     },

      // Resolver to reject a pull request.
      rejectPullRequest: (_, {
         id
      }) => dbService.rejectPullRequest(id),
   },
};

module.exports = resolvers;