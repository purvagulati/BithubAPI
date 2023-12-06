import pytest
from api import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test for listing repositories
def test_list_repositories(client):
    response = client.get('/repositories')
    assert response.status_code == 200
    assert 'Repo 1' in response.data.decode()


# Test for viewing a specific repository
def test_view_specific_repository(client):
    response = client.get('/repositories/1')
    assert response.status_code == 200
    assert 'Repo 1' in response.data.decode()


# Test for 404 on viewing non-existent repository
def test_view_specific_repository_not_found(client):
    response = client.get('/repositories/999')
    assert response.status_code == 404


# Test for listing branches in a repository
def test_list_branches(client):
    response = client.get('/repositories/1/branches')
    assert response.status_code == 200
    assert 'main' in response.data.decode()


# Test for listing tags in a repository
def test_list_tags(client):
    response = client.get('/repositories/1/tags')
    assert response.status_code == 200
    assert 'v1.0' in response.data.decode()


# Test for listing commits on a branch
def test_list_commits_on_branch(client):
    response = client.get('/repositories/1/branches/main/commits')
    assert response.status_code == 200
    assert 'hash123' in response.data.decode()


# Test for viewing a specific commit
def test_view_specific_commit(client):
    response = client.get('/repositories/1/commits/hash123')
    assert response.status_code == 200
    assert 'hash123' in response.data.decode()


# Test for viewing the repository tree for a commit
def test_view_repository_tree_for_commit(client):
    response = client.get('/repositories/1/commits/hash123/tree')
    assert response.status_code == 200


# Test for retrieving file content or subdirectories
def test_retrieve_file_or_directory_content(client):
    response = client.get('/repositories/1/tree/hash123/file1.txt')
    assert response.status_code == 200
    assert 'Content of file1' in response.data.decode()


# Test for viewing the latest commit on main branch
def test_view_latest_commit_on_main_branch(client):
    response = client.get('/repos/1/branches/main/latest-commit')
    assert response.status_code == 200
    assert 'hash123' in response.data.decode()


# Test for listing issues for a repository
def test_list_issues(client):
    response = client.get('/repos/1/issues')
    assert response.status_code == 200


# Test for reporting a new issue
def test_report_issue(client):
    new_issue = {'description': 'New issue test'}
    response = client.post('/repos/1/issues', json=new_issue)
    assert response.status_code == 201


# Test for viewing an issue
def test_view_issue(client):
    response = client.get('/repos/1/issues/1')
    assert response.status_code == 200
    assert 'Issue 1 in Repo 1' in response.data.decode()


# Test for updating an issue status
def test_update_issue_status(client):
    update_data = {'status': 'Closed'}
    response = client.put('/repos/1/issues/1', json=update_data)
    assert response.status_code == 200
    assert 'Closed' in response.data.decode()


# Test for listing comments on an issue
def test_list_comments_on_issue(client):
    response = client.get('/repos/1/issues/1/comments')
    assert response.status_code == 200


# Test for adding a comment to an issue
def test_add_comment_to_issue(client):
    new_comment = {'text': 'New comment'}
    response = client.post('/repos/1/issues/1/comments', json=new_comment)
    assert response.status_code == 201


# Test for retrieving a non-existent file or directory
def test_retrieve_nonexistent_file_or_directory_content(client):
    response = client.get('/repositories/1/tree/hash123/nonexistent.txt')
    assert response.status_code == 404


# Test for viewing a non-existent commit
def test_view_nonexistent_commit(client):
    response = client.get('/repositories/1/commits/nonexistent')
    assert response.status_code == 404


# Test for viewing the tree of a non-existent commit
def test_view_tree_for_nonexistent_commit(client):
    response = client.get('/repositories/1/commits/nonexistent/tree')
    assert response.status_code == 404


# Test for viewing the latest commit on a non-existent branch
def test_view_latest_commit_on_nonexistent_branch(client):
    response = client.get('/repos/1/branches/nonexistent/latest-commit')
    assert response.status_code == 404


# Test for viewing a non-existent issue
def test_view_nonexistent_issue(client):
    response = client.get('/repos/1/issues/999')
    assert response.status_code == 404


# Test for updating a non-existent issue
def test_update_nonexistent_issue_status(client):
    update_data = {'status': 'Closed'}
    response = client.put('/repos/1/issues/999', json=update_data)
    assert response.status_code == 404


# Test for adding a comment to a non-existent issue
def test_add_comment_to_nonexistent_issue(client):
    new_comment = {'text': 'New comment'}
    response = client.post('/repos/1/issues/999/comments', json=new_comment)
    assert response.status_code == 404


# Test for listing comments on a non-existent issue
def test_list_comments_on_nonexistent_issue(client):
    response = client.get('/repos/1/issues/999/comments')
    assert response.status_code == 404


# Test for invalid method on a repository endpoint
def test_invalid_method_on_repositories(client):
    response = client.post('/repositories')
    assert response.status_code == 405


# Test for invalid repository ID format
def test_invalid_repository_id_format(client):
    response = client.get('/repositories/abc')
    assert response.status_code == 404


# Test for retrieving file content with invalid path
def test_retrieve_file_with_invalid_path(client):
    response = client.get('/repositories/1/tree/hash123/invalidpath.txt')
    assert response.status_code == 404

def test_update_nonexistent_issue(client):
    update_data = {'status': 'Closed'}
    response = client.put('/repos/1/issues/9999', json=update_data)
    assert response.status_code == 404

def test_nonexistent_branch(client):
    response = client.get('/repositories/1/branches/nonexistent')
    assert response.status_code == 404

def test_nonexistent_commit(client):
    response = client.get('/repositories/1/commits/nonexistent')
    assert response.status_code == 404

def test_nonexistent_tree_in_commit(client):
    response = client.get('/repositories/1/commits/nonexistent/tree')
    assert response.status_code == 404


def test_nonexistent_file_in_tree(client):
    response = client.get('/repositories/1/tree/hash123/nonexistent.txt')
    assert response.status_code == 404

def test_report_issue_with_missing_fields(client):
    new_issue = {}  # Missing 'description'
    response = client.post('/repos/1/issues', json=new_issue)
    assert response.status_code == 400

def test_report_issue_with_extra_fields(client):
    new_issue = {'description': 'New issue', 'extra_field': 'extra'}
    response = client.post('/repos/1/issues', json=new_issue)
    assert response.status_code == 400

def test_update_issue_invalid_status(client):
    update_data = {'status': 'InvalidStatus'}
    response = client.put('/repos/1/issues/1', json=update_data)
    assert response.status_code == 400
