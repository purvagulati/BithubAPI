from flask import Flask, jsonify, request, abort
import uuid

app = Flask(__name__)

# In-Memory Data Stores
repositories = {
    1: {'id': 1, 'name': 'Repo 1', 'branches': {'main': 'hash123', 'dev': 'hash456'}, 'tags': ['v1.0']},
    2: {'id': 2, 'name': 'Repo 2', 'branches': {'main': 'hash789'}, 'tags': ['v2.0']}
}
commits = {
    'hash123': {'hash': 'hash123', 'message': 'Initial commit', 'repo_id': 1},
    'hash456': {'hash': 'hash456', 'message': 'Dev commit', 'repo_id': 1},
    'hash789': {'hash': 'hash789', 'message': 'Initial commit', 'repo_id': 2}
}
trees = {
    'hash123': {'/': ['file1.txt', 'dir1/']},
    'hash456': {'/': ['file2.txt', 'dir2/']},
    'hash789': {'/': ['file3.txt', 'dir3/']}
}
files = {
    'file1.txt': 'Content of file1',
    'file2.txt': 'Content of file2',
    'file3.txt': 'Content of file3'
}
issues = {
    1: [{'id': 1, 'description': 'Issue 1 in Repo 1', 'status': 'Open', 'comments': []}],
    2: [{'id': 2, 'description': 'Issue 1 in Repo 2', 'status': 'Open', 'comments': []}]
}

comments = {
    1: [  # Comments for issue with ID 1
        {
            'id': 101,
            'issue_id': 1,
            'text': 'This is the first comment on issue 1.',
            'submitter_id': 'user123',
            'date': '2023-01-01'
        },
        {
            'id': 102,
            'issue_id': 1,
            'text': 'This is the second comment on issue 1.',
            'submitter_id': 'user456',
            'date': '2023-01-02'
        }
    ],
    2: [  # Comments for issue with ID 2
        {
            'id': 201,
            'issue_id': 2,
            'text': 'This is the first comment on issue 2.',
            'submitter_id': 'user789',
            'date': '2023-01-03'
        }
    ]
    # ... more comments for other issues ...
}


# Error Handling
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error"), 500


# Repository Endpoints
@app.route('/repositories', methods=['GET'])
def list_repositories():
    return jsonify(list(repositories.values()))


@app.route('/repositories/<int:repo_id>', methods=['GET'])
def view_specific_repository(repo_id):
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    return jsonify(repo)


@app.route('/repositories/<int:repo_id>/branches', methods=['GET'])
def list_branches(repo_id):
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    return jsonify(list(repo.get('branches', {}).keys()))


@app.route('/repositories/<int:repo_id>/tags', methods=['GET'])
def list_tags(repo_id):
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    return jsonify(repo.get('tags', []))


@app.route('/repositories/<int:repo_id>/branches/<branch_name>/commits', methods=['GET'])
def list_commits_on_branch(repo_id, branch_name):
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    if branch_name not in repo.get('branches', {}):
        abort(404, description=f"Branch {branch_name} not found in repository {repo_id}.")
    branch_commit_hash = repo['branches'][branch_name]
    commit = commits.get(branch_commit_hash)
    return jsonify([commit] if commit else [])


@app.route('/repositories/<int:repo_id>/commits/<commit_hash>', methods=['GET'])
def view_specific_commit(repo_id, commit_hash):
    commit = commits.get(commit_hash)
    if not commit:
        abort(404, description=f"Commit with hash {commit_hash} not found.")
    if commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {commit_hash} not found in repository {repo_id}.")
    return jsonify(commit)


@app.route('/repositories/<int:repo_id>/commits/<commit_hash>/tree', methods=['GET'])
def view_repository_tree_for_commit(repo_id, commit_hash):
    commit = commits.get(commit_hash)
    if not commit or commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {commit_hash} not found in repository {repo_id}.")
    tree = trees.get(commit_hash)
    return jsonify(tree)


@app.route('/repositories/<int:repo_id>/tree/<tree_hash>/<path>', methods=['GET'])
def retrieve_file_or_directory_content(repo_id, tree_hash, path):
    commit = commits.get(tree_hash)
    if not commit or commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {tree_hash} not found in repository {repo_id}.")
    if path not in files:
        abort(404, description=f"File or directory {path} not found in the tree with hash {tree_hash}.")
    return jsonify(files[path])


@app.route('/repos/<int:repo_id>/branches/main/latest-commit', methods=['GET'])
def view_latest_commit_on_main_branch(repo_id):
    repo = repositories.get(repo_id)
    if not repo or 'main' not in repo.get('branches', {}):
        abort(404, description=f"Repository with ID {repo_id} does not have a 'main' branch.")
    latest_commit_hash = repo['branches']['main']
    latest_commit = commits.get(latest_commit_hash)
    return jsonify(latest_commit)


# Issue Endpoints
@app.route('/repos/<int:repo_id>/issues', methods=['GET', 'POST'])
def issues_operations(repo_id):
    if request.method == 'GET':
        return jsonify(issues.get(repo_id, []))
    elif request.method == 'POST':
        new_issue_data = request.json
        new_issue_id = str(uuid.uuid4())
        new_issue = {'id': new_issue_id, 'repo_id': repo_id, 'status': 'Open', **new_issue_data}
        issues.setdefault(repo_id, []).append(new_issue)
        return jsonify(new_issue), 201


@app.route('/repos/<int:repo_id>/issues/<int:issue_id>', methods=['GET', 'PUT'])
def issue_operations(repo_id, issue_id):
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    if request.method == 'GET':
        return jsonify(issue)
    elif request.method == 'PUT':
        issue_data = request.json
        issue['status'] = issue_data.get('status', issue['status'])
        return jsonify(issue)


@app.route('/repos/<int:repo_id>/issues/<int:issue_id>/comments', methods=['GET', 'POST'])
def issue_comments(repo_id, issue_id):
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    if request.method == 'GET':
        return jsonify(issue.get('comments', []))
    elif request.method == 'POST':
        new_comment = request.json
        issue.setdefault('comments', []).append(new_comment)
        return jsonify(new_comment), 201


@app.route('/repos/<int:repo_id>/issues/<int:issue_id>', methods=['PUT'])
def update_issue_status(repo_id, issue_id):
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    if 'status' not in request.json or request.json['status'] not in ['Open', 'Closed']:
        abort(400, description="Invalid status provided.")

    issue['status'] = request.json['status']
    return jsonify(issue)




@app.route('/repos/<int:repo_id>/issues/<int:issue_id>/add-comment', methods=['POST'])
def add_comment_to_issue(repo_id, issue_id):
    # Add a new comment to an issue
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    new_comment = request.json
    new_comment_id = str(uuid.uuid4())
    new_comment['id'] = new_comment_id
    issue.setdefault('comments', []).append(new_comment)
    return jsonify(new_comment), 201

@app.route('/repos/<int:repo_id>/issues', methods=['POST'])
def report_issue(repo_id):
    data = request.json
    if not data or 'description' not in data or any(key not in ['description'] for key in data.keys()):
        abort(400, description="Invalid issue data provided.")
    new_issue_id = str(uuid.uuid4())
    new_issue = {'id': new_issue_id, 'repo_id': repo_id, 'status': 'Open', 'description': data['description']}
    issues.setdefault(repo_id, []).append(new_issue)
    return jsonify(new_issue), 201



if __name__ == '__main__':
    app.run(debug=True)
