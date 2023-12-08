import json
import pytest
from api import app


@pytest.fixture
def client1():
    """
    A pytest fixture that sets up and provides a test client for the Flask application.
    This client can be used to make requests to the application for testing purposes.
    Yields:
        Flask test client.
    """
    with app.test_client() as client:
        yield client


# Test for listing repositories
def test_list_repositories(client1):
    """
    Tests if the endpoint to list all repositories works correctly.
    Verifies that the response status code is 200 and the expected repository is in the response.
    """
    response = client1.get('/repositories')
    assert response.status_code == 200
    assert 'Repo 1' in response.data.decode()


# Test for listing branches in a repository
def test_list_branches(client1):
    """
    Tests the endpoint for listing all branches of a specific repository.
    Checks if the response contains the expected branch and returns a status code of 200.
    """
    response = client1.get('/repositories/1/branches')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'main' in data and 'dev' in data


# Test for listing tags in a repository
def test_list_tags(client1):
    """
    Tests the endpoint for listing all tags of a repository.
    Ensures that the response includes the expected tag and the status code is 200.
    """
    response = client1.get('/repositories/1/tags')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'v1.0' in data


# Test for listing commits on a branch
def test_list_commits_on_branch(client1):
    """
    Test to ensure the endpoint for listing all commits on a specific branch
    of a repository works correctly. It checks for status code 200 and
    the presence of 'hash123' in the response.
    """
    response = client1.get('/repositories/1/branches/main/commits')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert any(commit['hash'] == 'hash123' for commit in data)


# Test for viewing a specific commit
def test_view_specific_commit(client1):
    """
    Test to ensure the endpoint for viewing a specific commit works correctly.
    It checks for status code 200 and the presence of the commit 'hash123' in the response.
    """
    response = client1.get('/repositories/1')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['name'] == 'Repo 1'
    assert 'latest_commit' in data
    assert data['latest_commit']['hash'] == 'hash123'


# Test for viewing the repository tree for a commit
def test_view_repository_tree_for_commit(client1):
    """
    Test to ensure the endpoint for viewing a specific commit works correctly.
    It checks for status code 200 and the presence of dir1 in response.
    """
    response = client1.get('/repositories/1/commits/hash123/tree')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert '/' in data
    assert 'dir1' in data['/']['items']


# Test for retrieving file content or subdirectories
def test_retrieve_file_or_directory_content(client1):
    """
    Test to ensure the endpoint for retrieving the content of a file or subdirectory
    within a commit's tree works correctly. It checks for status code 200 and
    the presence of 'Content of file1' in the response.
    """
    response = client1.get('/repositories/1/tree/hash123/file1.txt')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['content'] == 'Content of file1'


# Test for listing issues for a repository
def test_list_issues(client1):
    """
    Test to ensure the endpoint for listing all issues of a repository
    works correctly, returning status code 200.
    """
    response = client1.get('/repositories/1/issues')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert any(issue['description'] == 'Issue 1 in Repo 1' for issue in data)


# Test for reporting a new issue
def test_report_issue(client1):
    """
    Test to verify that the endpoint for reporting a new issue in a repository
    works correctly. It checks for status code 201 and the correct creation
    of the issue in the response.
    """
    new_issue = {'description': 'New issue test'}
    response = client1.post('/repositories/1/issues', json=new_issue)
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['description'] == 'New issue test'


# Test for viewing an issue
def test_view_issue(client1):
    """
    Tests the endpoint for viewing a specific issue in a repository.
    Verifies that the response status code is 200 and checks if the expected issue description is in the response.
    """
    response = client1.get('/repositories/1/issues/1')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['description'] == 'Issue 1 in Repo 1'


# Test for updating an issue status
def test_update_issue_status(client1):
    """
    Tests the functionality of updating the status of a specific issue in a repository.
    Checks if the issue status is correctly updated in the response and the status code is 200.
    """
    update_data = {'status': 'Closed'}
    response = client1.put('/repositories/1/issues/1', json=update_data)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'Closed'


# Test for listing comments on an issue
def test_list_comments_on_issue(client1):
    """
    Tests the endpoint for listing all comments on a specific issue in a repository.
    Verifies that the response status code is 200 and confirms the presence of comments.
    """
    response = client1.get('/repositories/1/issues/1/comments')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) > 0  # Assuming there are comments
    assert 'This is the first comment on issue 1.' in [comment['text'] for comment in data]


# Test for adding a comment to an issue
def test_add_comment_to_issue(client1):
    """
    Tests adding a comment to a specific issue in a repository.
    Verifies that the response status code is 201 and the comment is correctly added.
    """
    new_comment = {'text': 'New comment'}
    response = client1.post('/repositories/1/issues/1/comments', json=new_comment)
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['text'] == 'New comment'


# Test for retrieving a non-existent file or directory
def test_retrieve_nonexistent_file_or_directory_content(client1):
    """
    Tests accessing a file or directory within a commit's tree that does not exist.
    Checks that the response status code is 404 for a non-existent file or directory.
    """
    response = client1.get('/repositories/1/tree/hash123/nonexistent.txt')
    assert response.status_code == 404
    assert "Path 'nonexistent.txt' not found in commit hash123" in response.data.decode()


# Test for viewing the tree of a non-existent commit
def test_view_tree_for_nonexistent_commit(client1):
    """
    Tests viewing the tree for a commit that does not exist in a repository.
    Verifies that the response status code is 404 for a non-existent commit.
    """
    response = client1.get('/repositories/1/commits/nonexistent/tree')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found in repository 1." in response.data.decode()


# Test for viewing a non-existent issue
def test_view_nonexistent_issue(client1):
    """
    Tests the response when trying to view an issue that does not exist in a repository.
    Verifies that a 404 status code is returned for a non-existent issue.
    """
    response = client1.get('/repositories/1/issues/999')
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


# Test for updating a non-existent issue
def test_update_nonexistent_issue_status(client1):
    """
    Tests updating the status of an issue that does not exist in a repository.
    Checks that the response status code is 404 for a non-existent issue.
    """
    update_data = {'status': 'Closed'}
    response = client1.put('/repositories/1/issues/999', json=update_data)
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


# Test for adding a comment to a non-existent issue
def test_add_comment_to_nonexistent_issue(client1):
    """
    Tests adding a comment to an issue that does not exist in a repository.
    Verifies that a 404 status code is returned for a non-existent issue.
    """
    new_comment = {'text': 'New comment'}
    response = client1.post('/repositories/1/issues/999/comments', json=new_comment)
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


# Test for listing comments on a non-existent issue
def test_list_comments_on_nonexistent_issue(client1):
    """
    Tests listing comments on an issue that does not exist in a repository.
    Checks that the response status code is 404 for a non-existent issue.
    """
    response = client1.get('/repositories/1/issues/999/comments')
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


# Test for invalid method on a repository endpoint
def test_invalid_method_on_repositories(client1):
    """
    Tests using an invalid HTTP method (like POST) on a GET-only endpoint.
    Verifies that the response status code is 405 (Method Not Allowed).
    """
    response = client1.post('/repositories')
    assert response.status_code == 405
    assert 'Method Not Allowed' in response.data.decode()


# Test for invalid repository ID format
def test_invalid_repository_id_format(client1):
    """
    Tests accessing a repository with an invalid ID format (non-integer).
    Checks that the response status code is 404 for an invalid repository ID.
    """
    response = client1.get('/repositories/abc')
    assert response.status_code == 404
    assert 'The requested URL was not found on the server' in response.data.decode()


# Test for retrieving file content with invalid path
def test_retrieve_file_with_invalid_path(client1):
    """
    Tests retrieving file content from a commit with an invalid path.
    Verifies that a 404 status code is returned for an invalid file path.
    """
    response = client1.get('/repositories/1/tree/hash123/invalidpath.txt')
    assert response.status_code == 404
    assert "Path 'invalidpath.txt' not found in commit hash123" in response.data.decode()


def test_update_nonexistent_issue(client1):
    """
    Tests updating an issue that does not exist in the repository.
    This test verifies that the correct status code (404) is returned
    for an attempt to update a non-existent issue.
    """
    update_data = {'status': 'Closed'}
    response = client1.put('/repositories/1/issues/9999', json=update_data)
    assert response.status_code == 404
    assert "Issue with ID 9999 not found in repository 1" in response.data.decode()


def test_nonexistent_commit(client1):
    """
    Tests the response when requesting a non-existent commit in a repository.
    Verifies that the response status code is 404, indicating the commit does not exist.
    """

    response = client1.get('/repositories/1/commits/nonexistent')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found" in response.data.decode()


def test_nonexistent_tree_in_commit(client1):
    """
    Tests accessing the tree of a commit that does not exist.
    Checks that the response status code is 404 for a request to a non-existent commit's tree.
    """
    response = client1.get('/repositories/1/commits/nonexistent/tree')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found in repository 1." in response.data.decode()


def test_nonexistent_file_in_tree(client1):
    """
    Tests retrieving a non-existent file from a commit's tree.
    Verifies that the response status code is 404, indicating the file is not found.
    """
    response = client1.get('/repositories/1/tree/hash123/nonexistent.txt')
    assert response.status_code == 404
    assert "Path 'nonexistent.txt' not found in commit hash123." in response.data.decode()


def test_report_issue_with_missing_fields(client1):
    """
    Tests creating an issue with missing required fields.
    Ensures that the response status code is 400 (Bad Request) when required issue fields are missing.
    """

    new_issue = {}
    response = client1.post('/repositories/1/issues', json=new_issue)
    assert response.status_code == 400
    assert "Invalid issue data: only 'description' is required." in response.data.decode()


def test_report_issue_with_extra_fields(client1):
    """
    Tests the creation of an issue with additional, unexpected fields.
    Verifies that the response status code is 400, indicating invalid issue data.
    """
    new_issue = {'description': 'New issue', 'extra_field': 'extra'}
    response = client1.post('/repositories/1/issues', json=new_issue)
    assert response.status_code == 400
    assert "Invalid issue data: only 'description' is required." in response.data.decode()


def test_update_issue_invalid_status(client1):
    """
    Tests updating an issue with an invalid status.
    Checks that the response status code is 400 (Bad Request) for invalid status data.
    """
    update_data = {'status': 'InvalidStatus'}
    response = client1.put('/repositories/1/issues/1', json=update_data)
    assert response.status_code == 400
    assert "Invalid status provided." in response.data.decode()


# Test for pagination in list_all_commits
def test_pagination_list_all_commits(client1):
    """
    Tests the pagination functionality in listing all commits.
    Verifies correct response status codes and that pagination limits the number of results.
    """
    response = client1.get('/repositories/1/commits?page=1&per_page=1')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) == 1

    # Invalid page
    response = client1.get('/repositories/1/commits?page=999&per_page=1')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) == 0

    # Invalid per_page
    response = client1.get('/repositories/1/commits?page=1&per_page=999')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) <= 999


# Test for repository not found in list_all_commits
def test_list_all_commits_repository_not_found(client1):
    """
    Tests listing all commits for a repository that does not exist.
    Checks that the response status code is 404 for a non-existent repository.
    """
    response = client1.get('/repositories/999/commits')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


# Test for branch not found in list_commits_on_branch
def test_list_commits_on_branch_not_found(client1):
    """
    Tests the response when listing commits on a branch that does not exist in a repository.
    Verifies that the response status code is 404, indicating the branch is not found.
    """
    response = client1.get('/repositories/1/branches/nonexistent/commits')
    assert response.status_code == 404
    assert "Branch nonexistent not found in repository 1." in response.data.decode()


# Test for commit not in specified repository
def test_view_specific_commit_in_wrong_repository(client1):
    """
    Tests viewing a specific commit that does not belong to the specified repository.
    Verifies that a 404 status code is returned for a commit not found in the given repository.
    """
    response = client1.get('/repositories/2/commits/hash123')
    assert response.status_code == 404
    assert "Commit with hash hash123 not found in repository 2." in response.data.decode()


# Test for viewing non-existent commit's tree
def test_view_nonexistent_commit_tree(client1):
    """
    Tests viewing the tree of a commit that does not exist in the repository.
    Checks that the response status code is 404 for a non-existent commit.
    """
    response = client1.get('/repositories/1/commits/nonexistent/tree')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found in repository 1." in response.data.decode()


# Test for posting an issue with invalid data
def test_post_issue_with_invalid_data(client1):
    """
    Tests creating an issue with invalid data fields.
    Verifies that the response status code is 400 (Bad Request) when the issue data contains invalid fields.
    """
    new_issue = {'wrong_field': 'New issue'}
    response = client1.post('/repositories/1/issues', json=new_issue)
    assert response.status_code == 400
    assert "Invalid issue data: only 'description' is required." in response.data.decode()


# Test for adding a comment to an issue with invalid data
def test_add_comment_with_invalid_data(client1):
    """
    Tests adding a comment to an issue using invalid data fields.
    Checks that the response status code is 400, indicating the submitted comment data is invalid.
    """
    new_comment = {'wrong_field': 'New comment'}
    response = client1.post('/repositories/1/issues/1/comments', json=new_comment)
    assert response.status_code == 400
    assert "Invalid comment data: 'text' is required." in response.data.decode()

def test_list_all_commits_with_nonexistent_repository(client1):
    """
    Tests the scenario where commits are listed for a repository that does not exist.
    Ensures that the response status code is 404, indicating the repository is not found.
    """
    response = client1.get('/repositories/999/commits')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


def test_list_branches_with_nonexistent_repository(client1):
    """
    Tests listing branches for a repository that does not exist.
    Verifies that the response status code is 404, indicating the repository is not found.
    """
    response = client1.get('/repositories/999/branches')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


def test_list_commits_on_branch_with_nonexistent_repository(client1):
    """
    Tests listing commits on a branch for a non-existent repository.
    Checks for a 404 response status code, indicating the repository does not exist.
    """
    response = client1.get('/repositories/999/branches/main/commits')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


def test_view_specific_commit_nonexistent(client1):
    """
    Tests viewing a specific commit that does not exist.
    Ensures that a 404 status code is returned, indicating the commit is not found.
    """
    response = client1.get('/repositories/1/commits/nonexistent')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found." in response.data.decode()


def test_retrieve_file_or_directory_content_with_nonexistent_commit(client1):
    """
    Tests retrieving file or directory content from a commit that does not exist.
    Verifies that the response status code is 404, indicating the commit is not found.
    """
    response = client1.get('/repositories/1/tree/nonexistent/file1.txt')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found in repository 1." in response.data.decode()


def test_post_issue_with_missing_fields(client1):
    """
    Tests posting an issue with missing required fields.
    Checks that the response status code is 400, indicating a bad request due to missing fields.
    """
    new_issue = {}
    response = client1.post('/repositories/1/issues', json=new_issue)
    assert response.status_code == 400
    assert "Invalid issue data: only 'description' is required." in response.data.decode()


def test_add_comment_with_missing_fields(client1):
    """
    Tests adding a comment to an issue with missing required fields.
    Ensures that the response status code is 400 for missing required comment fields.
    """
    new_comment = {}
    response = client1.post('/repositories/1/issues/1/comments', json=new_comment)
    assert response.status_code == 400
    assert "Invalid comment data: 'text' is required." in response.data.decode()


def test_retrieve_content_from_nonexistent_commit(client1):
    """
    Tests retrieving content from a commit that does not exist.
    Verifies that the response status code is 404, indicating the commit is not found.
    """
    response = client1.get('/repositories/1/tree/nonexistent/file.txt')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found in repository 1." in response.data.decode()


def test_post_invalid_issue(client1):
    """
    Tests creating an issue with completely invalid data.
    Checks that the response status code is 400, indicating the issue data is invalid.
    """
    new_issue = {'invalid_field': 'test'}
    response = client1.post('/repositories/1/issues', json=new_issue)
    assert response.status_code == 400
    assert "Invalid issue data: only 'description' is required." in response.data.decode()


def test_update_issue_with_invalid_status(client1):
    """
    Tests updating an issue with an invalid status value.
    Ensures that the response status code is 400, indicating invalid data for issue status.
    """
    update_data = {'status': 'UnknownStatus'}
    response = client1.put('/repositories/1/issues/1', json=update_data)
    assert response.status_code == 400
    assert "Invalid status provided." in response.data.decode()


def test_add_invalid_comment_to_issue(client1):
    """
    Tests adding a comment to an issue with invalid data.
    Verifies that the response status code is 400, indicating invalid comment data.
    """
    new_comment = {'invalid_field': 'test'}
    response = client1.post('/repositories/1/issues/1/comments', json=new_comment)
    assert response.status_code == 400
    assert "Invalid comment data: 'text' is required." in response.data.decode()


def test_list_branches_nonexistent_repo(client1):
    """
    Tests listing branches for a repository that does not exist.
    Checks for a 404 response status code, indicating the repository is not found.
    """
    response = client1.get('/repositories/999/branches')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


def test_list_commits_on_branch_nonexistent_repo(client1):
    """
    Tests listing commits on a non-existent branch of a repository.
    Verifies that the response status code is 404, indicating the branch does not exist.
    """
    response = client1.get('/repositories/999/branches/main/commits')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


def test_view_specific_commit_not_in_repo(client1):
    """
    Tests viewing a commit that exists but not in the specified repository.
    Ensures a 404 status code is returned, indicating the commit is not part of the repository.
    """
    # Assuming 'hash123' exists but is not in repository '2'
    response = client1.get('/repositories/2/commits/hash123')
    assert response.status_code == 404
    assert "Commit with hash hash123 not found in repository 2." in response.data.decode()


def test_retrieve_file_from_nonexistent_commit(client1):
    """
    Tests retrieving a file from a commit that does not exist in the repository.
    Verifies that a 404 status code is returned for a non-existent commit.
    """
    response = client1.get('/repositories/1/tree/nonexistent/nonexistent_file.txt')
    assert response.status_code == 404
    assert "Commit with hash nonexistent not found in repository 1." in response.data.decode()


def test_post_issue_with_no_description(client1):
    """
    Tests creating an issue without providing a description.
    Checks that the response status code is 400, indicating a required field is missing.
    """
    new_issue = {'title': 'Test Issue'}
    response = client1.post('/repositories/1/issues', json=new_issue)
    assert response.status_code == 400
    assert "Invalid issue data: only 'description' is required." in response.data.decode()


def test_update_issue_with_no_status(client1):
    """
    Tests updating an issue without providing a new status.
    Verifies that the response status code is 400, indicating missing required data for issue update.
    """
    update_data = {'title': 'Updated Title'}
    response = client1.put('/repositories/1/issues/1', json=update_data)
    assert response.status_code == 400
    assert "Invalid status provided." in response.data.decode()

def test_add_comment_to_issue_with_no_text(client1):
    """
    Tests adding a comment to an issue without including comment text.
    Ensures that the response status code is 400, indicating a required field is missing.
    """

    new_comment = {'author': 'user'}
    response = client1.post('/repositories/1/issues/1/comments', json=new_comment)
    assert response.status_code == 400
    assert "Invalid comment data: 'text' is required." in response.data.decode()

def test_nonexistent_repository(client1):
    """
    Tests accessing a non-existent repository.
    Checks for a 404 response status code, indicating the repository does not exist.
    """
    response = client1.get('/repositories/999')
    assert response.status_code == 404
    assert "Repository with ID 999 not found" in response.data.decode()


def test_nonexistent_tag(client1):
    """
    Tests accessing a non-existent tag in a repository.
    Ensures that a 404 status code is returned, indicating the tag is not found.
    """
    response = client1.get('/repositories/1/tags/nonexistent')
    assert response.status_code == 404
    assert "The requested URL was not found on the server" in response.data.decode()


def test_nonexistent_file_in_commit(client1):
    """
    Tests accessing a non-existent file in a commit's tree.
    Verifies that a 404 status code is returned, indicating the file is not found in the commit.
    """
    response = client1.get('/repositories/1/tree/hash123/nonexistent.txt')
    assert response.status_code == 404
    assert "Path 'nonexistent.txt' not found in commit hash123" in response.data.decode()


def test_invalid_repo_for_commit(client1):
    """
    Tests accessing a commit from a non-existent or incorrect repository.
    Checks for a 404 response status code, indicating the repository or commit is not found.
    """
    response = client1.get('/repositories/999/commits/hash123')
    assert response.status_code == 404
    assert "Commit with hash hash123 not found in repository 999" in response.data.decode()


def test_view_specific_commit_not_found(client1):
    """
    Tests the scenario where a specific commit is requested but not found.
    Verifies that the response status code is 404, indicating the commit does not exist.
    """
    # Test when a commit is not found
    response = client1.get('/repositories/1/commits/nonexistent')
    assert response.status_code == 404
    assert 'Commit with hash nonexistent not found.' in response.json['error']


def test_view_specific_repository(client1):
    """
    Tests the functionality to view a specific repository.
    Ensures that the response status code is 200 and the repository details are correctly returned.
    """
    # Test when viewing an existing repository
    response = client1.get('/repositories/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Repo 1'


def test_view_specific_repository_not_found(client1):
    """
    Tests accessing a non-existent repository.
    Verifies that a 404 status code is returned, indicating that the repository is not found.
    """
    # Test when viewing a non-existing repository
    response = client1.get('/repositories/3')
    assert response.status_code == 404
    assert 'Repository with ID 3 not found.' in response.json['error']


def test_list_tags_nonexistent_repository(client1):
    """
    Tests listing tags for a repository that does not exist.
    Checks for a 404 response status code, confirming that the repository is not found.
    """
    response = client1.get('/repositories/999/tags')
    assert response.status_code == 404
    assert "Repository with ID 999 not found." in response.data.decode()


def test_update_issue_with_invalid_data(client1):
    """
    Tests updating an issue with invalid data (e.g., incorrect status).
    Ensures that the response status code is 400, indicating a bad request due to invalid data.
    """

    invalid_update_data = {'status': 'InvalidStatus'}
    response = client1.put('/repositories/1/issues/1', json=invalid_update_data)
    assert response.status_code == 400
    assert "Invalid status provided." in response.data.decode()


# Test for non-existent commit
def test_retrieve_from_nonexistent_commit(client1):
    """
    Tests retrieving data (file or directory content) from a non-existent commit.
    Checks for a 404 response status code, indicating that the specified commit does not exist.
    """
    response = client1.get('/repositories/1/tree/nonexistent_commit/somepath')
    assert response.status_code == 404
    assert "Commit with hash nonexistent_commit not found in repository 1." in response.data.decode()


# Test for path not found in tree
def test_retrieve_nonexistent_path_in_commit(client1):
    """
    Tests accessing a path that does not exist within a commit's tree.
    Verifies that a 404 status code is returned, indicating the path is not found in the commit.
    """
    response = client1.get('/repositories/1/tree/hash123/nonexistent_path')
    assert response.status_code == 404
    assert "Path 'nonexistent_path' not found in commit hash123" in response.data.decode()


# Test for directory content retrieval
def test_retrieve_directory_content(client1):
    """
    Tests retrieving content for a directory within a commit's tree.
    Ensures that the response status code is 200 and the directory content is correctly returned.
    """
    response = client1.get('/repositories/1/tree/hash123/dir1/')
    assert response.status_code == 200
    assert 'type' in response.json and response.json['type'] == 'tree'
    assert 'file2.txt' in response.json['content']


# Test for file content retrieval with path processing
def test_retrieve_file_content_with_path_processing(client1):
    """
    Tests retrieving file content from a commit's tree, ensuring correct path processing.
    Verifies that the response status code is 200 and the correct file content is returned.
    """
    response = client1.get('/repositories/1/tree/hash123/dir1/file2.txt')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['type'] == 'blob'
    assert data['content'] == 'Content of file2'

def test_retrieve_subdirectory_content(client1):
    """
    Tests retrieving content of a subdirectory within a commit's tree.
    Checks for a 200 response status code and validates the contents of the subdirectory.
    """
    # Assuming 'dir1/' is a directory in the 'hash123' commit tree
    response = client1.get('/repositories/1/tree/hash123/dir1/')
    assert response.status_code == 200
    # Check if the response correctly lists the contents of 'dir1/'
    assert 'file2.txt' in response.json['content']
    assert 'subdir' in response.json['content']


def test_filter_issues_by_status(client1):
    """
    Tests filtering issues in a repository based on their status.
    Verifies that all returned issues match the requested status and response status code is 200.
    """
    response = client1.get('/repositories/1/issues?status=Open')
    assert response.status_code == 200
    # Assert that all returned issues have 'Open' status
    for issue in response.json:
        assert issue['status'] == 'Open'


def test_issue_not_found(client1):
    """
    Tests accessing an issue that does not exist in a repository.
    Ensures that a 404 status code is returned, indicating the issue is not found.
    """
    response = client1.get('/repositories/1/issues/999')
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


def test_nonexistent_issue_in_comments(client1):
    """
    Tests listing comments for a non-existent issue in a repository.
    Checks for a 404 response status code, confirming that the issue does not exist.
    """
    response = client1.get('/repositories/1/issues/999/comments')
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


def test_nonexistent_issue_update(client1):
    """
    Tests updating a non-existent issue in a repository.
    Verifies that a 404 status code is returned, indicating
    the issue is not found.
    """
    response = client1.put('/repositories/1/issues/999', json={'status': 'Closed'})
    assert response.status_code == 404
    assert "Issue with ID 999 not found in repository 1." in response.data.decode()


def test_retrieve_nested_directory_content(client1):
    """
    Tests retrieving content of a nested directory within a commit's tree.
    Ensures that the response status code is 200 and the directory content is accurately listed.
    """
    response = client1.get('/repositories/1/tree/hash123/dir1/subdir/')
    assert response.status_code == 200
    assert 'file3.txt' in response.json['content']
