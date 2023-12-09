// db.js
// Mock database for GraphQL Manual Testing

const pullRequests = [
  {
    id: 'pr-12345',
    title: 'Fix login issue',
    description: 'This pull request fixes the login issue reported in issue #54321.',
    sourceCommit: '123abc',
    commits: 'blackbox tests,whitebox test',
    createdAt: '2023-12-09T09:08:27.997Z',
    targetBranch: 'main',
    status: 'pending',
    statusMessage: 'Pull request is open',
    user: { id: 'user-1', name: 'Alice', email: 'alice@cmu.andrew.edu' },
    comments: [],
    fileChanges: [
      { 
        id: 'fileChange-1', 
        fileName: 'login.js', 
        changes: 'Added null check for user credentials and updated login logic',
        changedLines: [
          { line: 55, code: "if (userCredentials != null) {", type: '+', comments: [] },
          { line: 56, code: "   performLogin(userCredentials);", type: '+', comments: [] }
        ]
      },
      { 
        id: 'fileChange-2', 
        fileName: 'README.md', 
        changes: 'Updated installation instructions and contact information',
        changedLines: [
          { line: 10, code: "Run `npm install` to install all dependencies.", type: '+', comments: [{
            id: 'comment-38', 
            userId: 'user-3', 
            content: 'This line needs refactoring.', 
            lineNumber: 10,
            reactions: {'user-1': '👍'}, 
            pullRequestId: 'pr-12345', 
          }] },
          { line: 25, code: "For support, contact xyz@andrew.cmu.edu.", type: '+' }
        ]
      },
    ],
  },
  {
    id: 'pr-67890',
    title: 'Update README',
    description: 'Updates the README file with new instructions.',
    sourceCommit: '0456def',
    targetBranch: 'develop',
    createdAt: '2023-02-09T09:08:20.997Z',
    status: 'pending',
    statusMessage: 'Pull request is open',
    user: { id: 'user-2', name: 'Bob', email: 'bob@example.com' },
    comments: [],
    fileChanges: [
      { 
        id: 'fileChange-1', 
        fileName: 'login.js', 
        changes: 'Added null check for user credentials and updated login logic',
        changedLines: [
          { line: 55, code: "if (userCredentials != incorrect) {", type: '+', comments: [{
            id: 'comment-33', 
            userId: 'user-3', 
            content: 'This line needs refactoring.', 
            lineNumber: 55,
            reactions: {}, 
            pullRequestId: 'pr-12345', 
          }]  },
          { line: 56, code: "performLogin(userCredentials);", type: '+' }
        ]
      },
    ]
  }
];

const comments = [
  {
    id: 'comment-1',
    userId: 'user-1',
    content: 'Looks good to me.',
    lineNumber: null,
    reactions: { 'user-1': '👍', 'user-4': '👍' },
    pullRequestId: 'pr-12345',
  },
  {
    id: 'comment-3',
    userId: 'user-1',
    content: 'Looks good to me.',
    lineNumber: null,
    reactions: { 'user-1': '👍', 'user-2': '😀' },
    pullRequestId: 'pr-12345',
  },
  {
    id: 'comment2',
    userId: 'user-2',
    content: 'Please add more details to the README changes.',
    lineNumber: null,
    reactions: { 'user-1': '👍', 'user-2': '😭' },
    pullRequestId: 'pr-67890',
  },
  {
    id: 'comment-38', 
    userId: 'user-3', 
    content: 'This line needs refactoring.', 
    lineNumber: 10,
    reactions: {'user-1': '👍'}, 
    pullRequestId: 'pr-12345', 
  },
  {
    id: 'comment-45', 
    userId: 'user-3', 
    content: 'This line needs refactoring.', 
    lineNumber: 25,
    reactions: {'user-19': '👍'}, 
    pullRequestId: 'pr-12345', 
  }
];

module.exports = { pullRequests, comments };
