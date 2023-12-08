from flask import Flask, jsonify, request, abort
import uuid

app = Flask(__name__)

# In-memory data stores for repositories, commits, trees, files, issues, and comments
repositories = {
    #  Sample repositories stored as dictionaries
    1: {'id': 1, 'name': 'Repo 1', 'branches': {'main': ['hash123'], 'dev': ['hash456']}, 'tags': ['v1.0']},

    2: {'id': 2, 'name': 'Repo 2',
        'branches':
            {'main': ['hash789']},
        'tags': ['v2.0']
        }
}

commits = {
    # Sample commits associated with repositories
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
    # Sample issues for tracking in repositories
    1: [{'id': 1, 'description': 'Issue 1 in Repo 1', 'status': 'Open', 'comments': []}],
    2: [{'id': 2, 'description': 'Issue 1 in Repo 2', 'status': 'Open', 'comments': []}]
}

comments = {
    # Sample comments associated with issues

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
    """
    List all repositories.
    Returns:
        JSON response containing a list of repositories.
    """
    return jsonify(list(repositories.values()))


@app.route('/repositories/<int:repo_id>', methods=['GET'])
def view_specific_repository(repo_id):
    """
    View a specific repository by its ID, including the latest commit on the main branch by default.
    Args:
        repo_id (int): The ID of the repository to view.
    Returns:
        JSON response containing the repository details and the latest commit on the main branch, or a 404 error if not found.
    """
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")

    # Retrieve the latest commit hash on the main branch
    latest_commit_hash = repo.get('branches', {}).get('main', [])[-1]
    latest_commit = commits.get(latest_commit_hash, {})

    # Add the latest commit data to the repository information
    repo_info = {**repo, 'latest_commit': latest_commit}

    return jsonify(repo_info)


@app.route('/repositories/<int:repo_id>/branches', methods=['GET'])
def list_branches(repo_id):
    """
    List all branches in a specific repository.
    Args:
        repo_id (int): The ID of the repository.
    Returns:
        JSON response containing a list of branches or a 404 error if the repository is not found.
    """
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    return jsonify(list(repo.get('branches', {}).keys()))


@app.route('/repositories/<int:repo_id>/tags', methods=['GET'])
def list_tags(repo_id):
    """
    List all tags of a specified repository.
    Args:
        repo_id (int): The ID of the repository.
    Returns:
        JSON response containing a list of tags or a 404 error if the repository is not found.
    """
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")
    return jsonify(repo.get('tags', []))


@app.route('/repositories/<int:repo_id>/commits', methods=['GET'])
def list_all_commits(repo_id):
    """
    List all commits in a specific repository with pagination.
    Args:
        repo_id (int): The ID of the repository.
    Returns:
        Paginated JSON response containing commits or a 404 error if the repository is not found.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Retrieve the specified repository's commits; return 404 error if the repository is not found
    repo = repositories.get(repo_id)
    if not repo:
        abort(404, description=f"Repository with ID {repo_id} not found.")

    repo_commits = [commit for commit in commits.values() if commit['repo_id'] == repo_id]
    paginated_commits = paginate(repo_commits, page, per_page)

    return jsonify(paginated_commits)


@app.route('/repositories/<int:repo_id>/branches/<branch_name>/commits', methods=['GET'])
def list_commits_on_branch(repo_id, branch_name):
    """
    List commits on a specific branch of a repository with pagination.
    Args:
        repo_id (int): The ID of the repository.
        branch_name (str): The name of the branch.
    Returns:
        Paginated JSON response containing commits or a 404 error if the branch/repository is not found.
    """
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
    """
    View a specific commit.
    Args:
        repo_id (int): The ID of the repository.
        commit_hash (str): The hash of the commit.
    Returns:
        JSON response containing commit details or a 404 error if the commit/repository is not found.
    """
    commit = commits.get(commit_hash)
    if not commit:
        abort(404, description=f"Commit with hash {commit_hash} not found.")
    if commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {commit_hash} not found in repository {repo_id}.")
    return jsonify(commit)


@app.route('/repositories/<int:repo_id>/commits/<commit_hash>/tree', methods=['GET'])
def view_repository_tree_for_commit(repo_id, commit_hash):
    """
    View the repository tree for a specific commit.
    Args:
        repo_id (int): The ID of the repository.
        commit_hash (str): The hash of the commit.
    Returns:
        JSON response containing the commit tree or a 404 error if the commit/repository is not found.
    """
    commit = commits.get(commit_hash)
    if not commit or commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {commit_hash} not found in repository {repo_id}.")
    tree = trees.get(commit_hash)
    return jsonify(tree)


@app.route('/repositories/<int:repo_id>/tree/<tree_hash>/<path:path>', methods=['GET'])
def retrieve_file_or_directory_content(repo_id, tree_hash, path):
    """
    Retrieve file or directory content from a specific commit.
    Args:
        repo_id (int): The ID of the repository.
        tree_hash (str): The hash of the tree.
        path (str): The file or directory path.
    Returns:
        JSON response containing file or directory content, or a 404 error if the path/commit/repository is not found.
    """
    commit = commits.get(tree_hash)
    if not commit or commit['repo_id'] != repo_id:
        abort(404, description=f"Commit with hash {tree_hash} not found in repository {repo_id}.")

    if path.endswith('/'):
        # Handling directory content request
        tree_entry = trees.get(tree_hash, {}).get(path)
        return jsonify({'type': 'tree', 'content': list(tree_entry['items'].keys())})

    # Check if path is a file in the root directory
    if '/' not in path and path in trees.get(tree_hash, {}).get('/', {}).get('items', {}):
        file_content = files.get(path)
        if file_content:
            return jsonify({'type': 'blob', 'content': file_content})

    # Split path into directory and filename
    directory, _, filename = path.rpartition('/')
    directory += '/' if directory else ''

    # Check if the directory exists in the tree
    tree_entry = trees.get(tree_hash, {}).get(directory)
    if tree_entry and filename in tree_entry['items']:
        # Handle file content for files in subdirectories
        if tree_entry['items'][filename] == 'blob':
            file_content = files.get(filename)
            return jsonify({'type': 'blob', 'content': file_content})
        elif tree_entry['items'][filename] == 'tree':
            # Return directory contents
            return jsonify({'type': 'tree', 'content': list(tree_entry['items'].keys())})
    else:
        # Path does not exist as a file or directory
        abort(404, description=f"Path '{path}' not found in commit {tree_hash}.")


# Issue Endpoints
@app.route('/repositories/<int:repo_id>/issues', methods=['GET', 'POST'])
def issues_operations(repo_id):
    """
    Perform operations (GET, POST) on issues of a repository.
    Args:
        repo_id (int): The ID of the repository.
    Returns:
        For GET: JSON response containing a list of issues or filtered by status.
        For POST: JSON response containing the newly created issue.
    """
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
        if 'description' not in new_issue_data or not isinstance(new_issue_data['description'], str) or len(
                new_issue_data) > 1: abort(400, description="Invalid issue data: only 'description' is required.")

        new_issue_id = str(uuid.uuid4())
        new_issue = {'id': new_issue_id, 'repo_id': repo_id, 'status': 'Open', **new_issue_data}
        issues.setdefault(repo_id, []).append(new_issue)
        return jsonify(new_issue), 201


@app.route('/repositories/<int:repo_id>/issues/<int:issue_id>', methods=['GET', 'PUT'])
def issue_operations(repo_id, issue_id):
    """
    Perform operations (GET, PUT) on a specific issue of a repository.
    Args:
        repo_id (int): The ID of the repository.
        issue_id (int): The ID of the issue.
    Returns:
        For GET: JSON response containing issue details.
        For PUT: JSON response containing the updated issue details.
    """
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
    """
    Perform operations (GET, POST) on comments of a specific issue in a repository.
    Args:
        repo_id (int): The ID of the repository.
        issue_id (int): The ID of the issue.
    Returns:
        For GET: JSON response containing a list of comments.
        For POST: JSON response containing the newly added comment.
    """
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


# Error Handling
@app.errorhandler(404)
def resource_not_found(e):
    """
    Error handler for 404 Not Found.
    Args:
        e (Exception): The exception that was raised.
    Returns:
        JSON response containing the error message.
    """
    return jsonify(error=f"{str(e.description)}"), 404


@app.errorhandler(400)
def bad_request(e):
    """
    Error handler for 400 Bad Request.
    Args:
        e (Exception): The exception that was raised.
    Returns:
        JSON response containing the error message.
    """
    return jsonify(error=str(e)), 400


def paginate(data, page, per_page):
    """
    Paginate a list of data.
    Args:
        data (list): The data to be paginated.
        page (int): The current page number.
        per_page (int): The number of items per page.
    Returns:
        A slice of the data for the specified page.
    """
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]
