const db = require('./db.js');

const resolvers = {
    Query: {
        PRDetailsById: (_, { id }) => db.getPRById(id),
        ListPRs: (_, { status }) => db.listPRs(status),
        PRComments: (_, { prId }) => db.getComments(prId),
    },
    Mutation: {
        CreatePR: (_, { description, sourceCommit, branchTarget }) => {
            const newPR = {
                id: generateID(), // Implement a function to generate unique IDs
                description,
                sourceCommit,
                branchTarget,
                status: 'pending',
                comments: []
            };
            return db.createPR(newPR);
        },
        AddPRComment: (_, { prId, content, lineNumber }) => {
            const newComment = {
                id: generateID(), // Implement a function to generate unique IDs
                prId,
                content,
                type: lineNumber ? 'inline' : 'general',
                lineNumber,
                reactions: {}
            };
            return db.addComment(newComment);
        },
        ReactToComment: (_, { commentId, reactionType }) => db.reactToComment(commentId, reactionType),
        UpdatePRStatus: (_, { prId, newStatus }) => db.updatePRStatus(prId, newStatus),
        MergePR: (_, { prId }) => db.mergePR(prId),
    }
};

module.exports = resolvers;
