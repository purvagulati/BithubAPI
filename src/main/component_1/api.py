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
    'hash123': {
        '/': {'type': 'tree', 'items': {'file1.txt': 'blob', 'dir1': 'tree'}},
        'dir1/': {'type': 'tree', 'items': {'file2.txt': 'blob', 'subdir': 'tree'}},
        'dir1/subdir/': {'type': 'tree', 'items': {'file3.txt': 'blob'}}
    },
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

}

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

@app.route('/repositories/<int:repo_id>/commits', methods=['GET'])
def list_all_commits(repo_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")

    repo_commits = [commit for commit in commits.values() if commit['repo_id'] == repo_id]
    paginated_commits = paginate(repo_commits, page, per_page)

    return jsonify(paginated_commits)

@app.route('/repositories/<int:repo_id>/branches/<branch_name>/commits', methods=['GET'])
def list_commits_on_branch(repo_id, branch_name):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    if branch_name not in repo.get('branches', {}):
        abort(404, description=f"Branch {branch_name} not found in repository {repo_id}.")

    branch_commit_hashes = repo['branches'].get(branch_name, [])
    branch_commits = [commits[hash] for hash in branch_commit_hashes if hash in commits]
    paginated_commits = paginate(branch_commits, page, per_page)

    return jsonify(paginated_commits)


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


@app.route('/repositories/<int:repo_id>/tree/<tree_hash>/<path:path>', methods=['GET'])
def retrieve_file_or_directory_content(repo_id, tree_hash, path):
    commit = commits.get(tree_hash)
    if not commit or commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {tree_hash} not found in repository {repo_id}.")

    # Normalize path
    if not path.endswith('/'):
        path += '/'

    tree_entry = trees.get(tree_hash, {}).get(path)

    if not tree_entry:
        abort(404, description=f"Path '{path}' not found in commit {tree_hash}.")

    if tree_entry['type'] == 'tree':
        # Return directory contents
        return jsonify({'type': 'tree', 'content': list(tree_entry['items'].keys())})
    elif tree_entry['type'] == 'blob':
        # Return file content
        file_content = files.get(path.strip('/'))
        if file_content is None:
            abort(404, description=f"File '{path}' not found.")
        return jsonify({'type': 'blob', 'content': file_content})
    else:
        abort(500, description="Unexpected content type.")


@app.route('/repositories/<int:repo_id>/branches/main/latest-commit', methods=['GET'])
def view_latest_commit_on_main_branch(repo_id):
    repo = repositories.get(repo_id)
    if not repo or 'main' not in repo.get('branches', {}):
        abort(404, description=f"Repository with ID {repo_id} does not have a 'main' branch.")
    latest_commit_hash = repo['branches']['main']
    latest_commit = commits.get(latest_commit_hash)
    return jsonify(latest_commit)


# Issue Endpoints

@app.route('/repositories/<int:repo_id>/issues', methods=['GET', 'POST'])
def issues_operations(repo_id):
    if request.method == 'GET':
        # Retrieve the optional status query parameter
        status_filter = request.args.get('status')

        repo_issues = issues.get(repo_id, [])

        # Filter issues by status if the status parameter is provided
        if status_filter:
            filtered_issues = [issue for issue in repo_issues if issue['status'] == status_filter]
        else:
            filtered_issues = repo_issues

        return jsonify(filtered_issues)

    elif request.method == 'POST':
        new_issue_data = request.json
        # Validate new issue data
        if 'description' not in new_issue_data or not isinstance(new_issue_data['description'], str):
            abort(400, description="Invalid issue data: 'description' is required.")

        new_issue_id = str(uuid.uuid4())
        new_issue = {'id': new_issue_id, 'repo_id': repo_id, 'status': 'Open', **new_issue_data}
        issues.setdefault(repo_id, []).append(new_issue)
        return jsonify(new_issue), 201


@app.route('/repositories/<int:repo_id>/issues/<int:issue_id>', methods=['GET', 'PUT'])
def issue_operations(repo_id, issue_id):
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    if request.method == 'GET':
        return jsonify(issue)
    elif request.method == 'PUT':
        issue_data = request.json

        # Validate status update
        if 'status' not in issue_data or issue_data['status'] not in ['Open', 'Closed']:
            abort(400, description="Invalid status provided.")

        issue = next((issue for issue in issues.get(repo_id, []) if issue['id'] == issue_id), None)
        if not issue:
            abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

        issue['status'] = issue_data['status']
        return jsonify(issue)


@app.route('/repositories/<int:repo_id>/issues/<int:issue_id>/comments', methods=['GET', 'POST'])
def issue_comments(repo_id, issue_id):
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    if request.method == 'GET':
        return jsonify(issue.get('comments', []))
    elif request.method == 'POST':
        new_comment = request.json

        # Validate new comment
        if 'text' not in new_comment or not isinstance(new_comment['text'], str):
            abort(400, description="Invalid comment data: 'text' is required.")

        new_comment_id = str(uuid.uuid4())
        new_comment['id'] = new_comment_id
        issue = next((issue for issue in issues.get(repo_id, []) if issue['id'] == issue_id), None)
        if not issue:
            abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

        issue.setdefault('comments', []).append(new_comment)
        return jsonify(new_comment), 201

@app.route('/repositories/<int:repo_id>/issues/<int:issue_id>', methods=['PUT'])
def update_issue_status(repo_id, issue_id):
    repo_issues = issues.get(repo_id, [])
    issue = next((issue for issue in repo_issues if issue['id'] == issue_id), None)
    if not issue:
        abort(404, description=f"Issue with ID {issue_id} not found in repository {repo_id}.")

    issue_data = request.json
    if 'status' not in issue_data or issue_data['status'] not in ['Open', 'Closed']:
        abort(400, description="Invalid status provided.")

    issue['status'] = issue_data['status']
    return jsonify(issue)

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

def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

if __name__ == '__main__':
    app.run(debug=True)
