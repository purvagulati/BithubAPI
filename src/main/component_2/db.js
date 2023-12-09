// db.js
// Mock database for GraphQL Manual Testing

const pullRequests = [
  {
    id: 'pr-12345',
    title: 'Fix login issue',
    description: 'This pull request fixes the login issue reported in issue #54321.',
    sourceCommit: '123abc',
    createdAt: '2023-12-09T09:08:27.997Z',
    targetBranch: 'main',
    status: 'pending',
    statusMessage: 'Pull request is open',
    user: { id: 'user-1', name: 'Alice', email: 'alice@example.com' },
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
          { line: 10, code: "Run `npm install` to install all dependencies.", type: '+', comments: [] },
          { line: 25, code: "For support, contact support@example.com.", type: '+', comments: [] }
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
          { line: 55, code: "if (userCredentials != null) {", type: '+', comments: [] },
          { line: 56, code: "   performLogin(userCredentials);", type: '+', comments: [] }
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
  }
];

module.exports = { pullRequests, comments };
