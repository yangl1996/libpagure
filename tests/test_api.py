import pytest

from libpagure import Pagure


@pytest.fixture(scope='module')
def simple_pg():
    """ Create a simple Pagure object
    to be used in test
    """
    pg = Pagure(pagure_repository="testrepo")
    return pg


def test_pagure_object():
    """ Test the pagure object creation """

    pg = Pagure(pagure_token="a token",
                pagure_repository="test_repo")
    assert pg.token == "a token"
    assert pg.repo == "test_repo"
    assert pg.namespace is None
    assert pg.username is None
    assert pg.instance == "https://pagure.io"
    assert pg.insecure is False
    assert pg.header == {"Authorization": "token a token"}


basic_url_data = [
    (None, None, 'testrepo', 'https://pagure.io/api/0/testrepo/'),
    (None, 'testnamespace', 'testrepo',
     'https://pagure.io/api/0/testnamespace/testrepo/'),
    ('testfork', None, 'testrepo',
     'https://pagure.io/api/0/fork/testfork/testrepo/'),
    ('testfork', 'testnamespace', 'testrepo',
     'https://pagure.io/api/0/fork/testfork/testnamespace/testrepo/'),
]


@pytest.mark.parametrize("user, namespace, repo, expected",
                         basic_url_data)
def test_create_basic_url(user, namespace, repo, expected):
    """ Test creation of url in function of argument
    passed to the Pagure class.
    """
    pg = Pagure(pagure_repository=repo,
                fork_username=user,
                namespace=namespace)
    url = pg.create_basic_url()
    assert url == expected


def test_api_version(mocker, simple_pg):
    """ Test the call to the version API """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.api_version()
    Pagure._call_api.assert_called_once_with('https://pagure.io/api/0/version')


def test_list_users(mocker, simple_pg):
    """ Test the call to the users API """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.list_users(pattern='c')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/users', params={'pattern': 'c'})


def test_list_tags(mocker, simple_pg):
    """ Test the call to the tags API """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.list_tags(pattern='easy')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/tags', params={'pattern': 'easy'})


def test_list_groups(mocker, simple_pg):
    """ Test the call to the groups API """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.list_groups()
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/groups', params=None)


def test_error_codes(mocker, simple_pg):
    """ Test the call to the error codes API """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.error_codes()
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/error_codes')


pr_data = [
    ('teststatus', 'testassignee', 'testauthor',
        {'status': 'teststatus', 'assignee': 'testassignee', 'author': 'testauthor'}),
    (None, None, None, {})
]


@pytest.mark.parametrize("status, assignee, author, expected", pr_data)
def test_list_requests(mocker, simple_pg, status, assignee, author, expected):
    """ Test the API call to the pull-requests endpoint """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.list_requests(status, assignee, author)
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/pull-requests', params=expected)


def test_request_info(mocker, simple_pg):
    """ Test the API call to get pull-request info """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.request_info('123')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/pull-request/123')


def test_merge_request(mocker, simple_pg):
    """ Test the API call to merge a pull-request """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.merge_request('123')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/pull-request/123/merge', method='POST')


def test_close_request(mocker, simple_pg):
    """ Test the API call to close a pull-request """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.close_request('123')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/pull-request/123/close', method='POST')


comment_data = [
    ("test body", None, None, None, {'comment': 'test body'}),
    ("test body", "testcommit", "testfilename", "testrow",
     {'comment': 'test body', 'commit': 'testcommit', 'filename': 'testfilename',
      'row': 'testrow'})
]


@pytest.mark.parametrize("body, commit, filename, row, expected", comment_data)
def test_comment_request(mocker, simple_pg, body, commit, filename, row, expected):
    """ Test the API call to comment on a pull-request """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.comment_request('123', body, commit, filename, row)
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/pull-request/123/comment', method='POST',
        data=expected)


flag_data = [
    ('testuser', 'testpercent', 'testcomment', 'testurl', None, None,
     {'username': 'testuser', 'percent': 'testpercent', 'comment': 'testcomment',
      'url': 'testurl'}),
    ('testuser', 'testpercent', 'testcomment', 'testurl', 'testuid', 'testcommit',
     {'username': 'testuser', 'percent': 'testpercent', 'comment': 'testcomment',
      'url': 'testurl', 'uid': 'testuid', 'commit': 'testcommit'})
]


@pytest.mark.parametrize("username, percent, comment, url, uid, commit, expected",
                         flag_data)
def test_flag_request(mocker, simple_pg, username, percent, comment, url, uid,
                      commit, expected):
    """ Test the API call to flag a pull-request """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.flag_request('123', username, percent, comment, url, uid, commit)
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/pull-request/123/flag', method='POST',
        data=expected)


def test_create_issue(mocker, simple_pg):
    """ Test the API call to create an issue """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.create_issue('A test issue', 'Some issue content', True)
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/new_issue', method='POST',
        data={'title': 'A test issue', 'issue_content': 'Some issue content',
              'priority': True})


def test_list_issues(mocker, simple_pg):
    """ Test the API call to list all issues of a project """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.list_issues('status', 'tags', 'assignee', 'author',
                          'milestones', 'priority', 'no_stones', 'since')
    expected = {'status': 'status', 'tags': 'tags', 'assignee': 'assignee',
                'author': 'author', 'milestones': 'milestones', 'priority': 'priority',
                'no_stones': 'no_stones', 'since': 'since'}
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/issues', params=expected)


def test_issue_info(mocker, simple_pg):
    """ Test the API call to info about a project issue """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.issue_info('123')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/issue/123')


def test_list_comment(mocker, simple_pg):
    """ Test the API call to info about a project issue """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.get_list_comment('123', '001')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/issue/123/comment/001')


def test_change_issue_status(mocker, simple_pg):
    """ Test the API call to change the status of a project issue """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.change_issue_status('123', 'Closed', 'wontfix')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/issue/123/status', method='POST',
        data={'status': 'Closed', 'close_status': 'wontfix'})


def test_change_issue_milestone(mocker, simple_pg):
    """ Test the API call to change the milestone of a project issue """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.change_issue_milestone('123', 'Tomorrow')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/issue/123/milestone', method='POST',
        data={'milestone': 'Tomorrow'})


def test_comment_issue(mocker, simple_pg):
    """ Test the API call to change the milestone of a project issue """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.comment_issue('123', 'A comment')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/issue/123/comment', method='POST',
        data={'comment': 'A comment'})


def test_project_tags(mocker, simple_pg):
    """ Test the API call to get a project tags """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.project_tags()
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/git/tags')


def test_list_projects(mocker, simple_pg):
    """ Test the API call to list all projects on a pagure instance """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.list_projects('tags', 'pattern', 'username', 'owner',
                            'namespace', 'fork', 'short', 1, 100)
    expected = {'tags': 'tags', 'pattern': 'pattern', 'username': 'username',
                'owner': 'owner', 'namespace': 'namespace', 'fork': 'fork',
                'short': 'short', 'page': '1', 'per_page': '100'}
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/projects', params=expected)


def test_user_info(mocker, simple_pg):
    """ Test the API call to get info about a user """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.user_info('auser')
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/user/auser')


def test_new_project(mocker, simple_pg):
    """ Test the API call to list all projects on a pagure instance """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.new_project('name', 'description', 'namespace', 'url',
                            'avatar_email', True, True)
    expected = {'name': 'name', 'description': 'description', 'namespace': 'namespace',
                'url': 'url', 'avatar_email': 'avatar_email',
                'create_readme': True, 'private': True}
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/new', data=expected, method='POST')


def test_project_branches(mocker, simple_pg):
    """ Test the API call to get info about a user """
    mocker.patch('libpagure.Pagure._call_api')
    simple_pg.project_branches()
    Pagure._call_api.assert_called_once_with(
        'https://pagure.io/api/0/testrepo/git/branches')
