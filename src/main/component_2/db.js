// Mock database interface 

const PRs = []; // Array to store PRs
const Comments = []; // Array to store comments

module.exports = {
    // Fetch a PR by ID
    getPRById: (id) => PRs.find(pr => pr.id === id),

    // List PRs by status
    listPRs: (status) => PRs.filter(pr => pr.status === status),

    // Get comments for a PR
    getComments: (prId) => Comments.filter(comment => comment.prId === prId),

    // Create a PR
    createPR: (pr) => {
        PRs.push(pr);
        return pr;
    },

    // Add a comment
    addComment: (comment) => {
        Comments.push(comment);
        return comment;
    },

    // Update a PR's status
    updatePRStatus: (id, newStatus) => {
        const pr = PRs.find(pr => pr.id === id);
        if (pr) {
            pr.status = newStatus;
        }
        return pr;
    },

    // Merge a PR
    mergePR: (id) => {
        const pr = PRs.find(pr => pr.id === id);
        if (pr && pr.status === 'pending') {
            pr.status = 'merged';
        }
        return pr;
    },

    // React to a comment
    reactToComment: (commentId, reaction) => {
        const comment = Comments.find(c => c.id === commentId);
        if (comment) {
            // Add or update reaction count
            comment.reactions[reaction] = (comment.reactions[reaction] || 0) + 1;
        }
        return comment;
    }
};
