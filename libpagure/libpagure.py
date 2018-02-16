# -*- coding: utf-8 -*-

import requests
import logging

from .exceptions import APIError


class NullHandler(logging.Handler):
    # Null logger to avoid spurious messages
    def emit(self, record):
        pass


LOG = logging.getLogger("libpagure")

# Add the null handler to top-level logger used by the library
hand = NullHandler()
LOG.addHandler(hand)


class Pagure(object):

    # TODO: add error handling
    # TODO: write some unit tests
    def __init__(
            self,
            pagure_token=None,
            pagure_repository=None,
            fork_username=None,
            namespace=None,
            instance_url="https://pagure.io",
            insecure=False):
        """
        Create an instance.
        :param pagure_token: pagure API token
        :param pagure_repository: pagure project name
        :param fork_username: if this is a fork, it's the username
             of the fork creator
        :param instance_url: the URL of pagure instance name
        :return:
        """
        self.token = pagure_token
        self.repo = pagure_repository
        self.username = fork_username
        self.namespace = namespace
        self.instance = instance_url
        self.session = requests.session()
        self.insecure = insecure
        if self.token:
            self.header = {"Authorization": "token " + self.token}
        else:
            self.header = None

    def _call_api(self, url, method='GET', params=None, data=None):
        """ Method used to call the API.
        It returns the raw JSON returned by the API or raises an exception
        if something goes wrong.

        :arg url: the URL to call
        :kwarg method: the HTTP method to use when calling the specified
            URL, can be GET, POST, DELETE, UPDATE...
            Defaults to GET
        :kwarg params: the params to specify to a GET request
        :kwarg data: the data to send to a POST request

        """

        req = self.session.request(
            method=method,
            url=url,
            params=params,
            headers=self.header,
            data=data,
            verify=not self.insecure,
        )

        output = None
        try:
            output = req.json()
        except Exception as err:
            LOG.debug(req.text)
            # TODO: use a dedicated error class
            raise Exception('Error while decoding JSON: {0}'.format(err))

        if req.status_code != 200:
            LOG.error(output)
            if 'error_code' in output:
                raise APIError(output['error'])
        return output

    def create_basic_url(self):
        """ Create URL prefix for API calls based on type of repo.

        Repo may be forked and may be in namespace. That makes total 4
        different types of URL.

        :return:
        """
        if self.username is None:
            if self.namespace is None:
                request_url = "{}/api/0/{}/".format(
                    self.instance, self.repo)
            else:
                request_url = "{}/api/0/{}/{}/".format(
                    self.instance, self.namespace, self.repo)
        else:
            if self.namespace is None:
                request_url = "{}/api/0/fork/{}/{}/".format(
                    self.instance, self.username, self.repo)
            else:
                request_url = "{}/api/0/fork/{}/{}/{}/".format(
                    self.instance, self.username, self.namespace, self.repo)
        return request_url

    def api_version(self):
        """
        Get Pagure API version.
        :return:
        """
        request_url = "{}/api/0/version".format(self.instance)
        return_value = self._call_api(request_url)
        return return_value['version']

    def list_users(self, pattern=None):
        """
        List all users registered on this Pagure instance.
        :param pattern: filters the starting letters of the return value
        :return:
        """
        request_url = "{}/api/0/users".format(self.instance)
        params = None
        if pattern:
            params = {'pattern': pattern}
        return_value = self._call_api(request_url, params=params)
        return return_value['users']

    def list_tags(self, pattern=None):
        """
        List all tags made on this project.
        :param pattern: filters the starting letters of the return value
        :return:
        """
        request_url = "{}tags".format(self.create_basic_url())

        params = None
        if pattern:
            params = {'pattern': pattern}

        return_value = self._call_api(request_url, params=params)
        return return_value['tags']

    def list_groups(self, pattern=None):
        """
        List all groups on this Pagure instance.
        :param pattern: filters the starting letters of the return value
        :return:
        """
        request_url = "{}/api/0/groups".format(self.instance)
        params = None
        if pattern:
            params = {'pattern': pattern}

        return_value = self._call_api(request_url, params=params)
        return return_value['groups']

    def error_codes(self):
        """
        Get a dictionary of all error codes.
        :return:
        """
        request_url = "{}/api/0/error_codes".format(self.instance)
        return_value = self._call_api(request_url)
        return return_value

    def list_requests(self, status=None, assignee=None, author=None):
        """
        Get all pull requests of a project.
        :param status: filters the status of the requests
        :param assignee: filters the assignee of the requests
        :param author: filters the author of the requests
        :return:
        """
        request_url = "{}pull-requests".format(self.create_basic_url())

        payload = {}
        if status is not None:
            payload['status'] = status
        if assignee is not None:
            payload['assignee'] = assignee
        if author is not None:
            payload['author'] = author

        return_value = self._call_api(request_url, params=payload)
        return return_value['requests']

    def request_info(self, request_id):
        """
        Get information of a single pull request.
        :param request_id: the id of the request
        :return:
        """
        request_url = "{}pull-request/{}".format(self.create_basic_url(),
                                                 request_id)

        return_value = self._call_api(request_url)
        return return_value

    def merge_request(self, request_id):
        """
        Merge a pull request.
        :param request_id: the id of the request
        :return:
        """
        request_url = "{}pull-request/{}/merge".format(self.create_basic_url(),
                                                       request_id)

        return_value = self._call_api(request_url, method='POST')

        LOG.debug(return_value)

    def close_request(self, request_id):
        """
        Close a pull request.
        :param request_id: the id of the request
        :return:
        """
        request_url = "{}pull-request/{}/close".format(self.create_basic_url(),
                                                       request_id)

        return_value = self._call_api(request_url, method='POST')

        LOG.debug(return_value)

    def comment_request(self, request_id, body, commit=None,
                        filename=None, row=None):
        """
        Create a comment on the request.
        :param request_id: the id of the request
        :param body: the comment body
        :param commit: which commit to comment on
        :param filename: which file to comment on
        :param row: which line of code to comment on
        :return:
        """
        request_url = ("{}pull-request/{}/comment"
                       .format(self.create_basic_url(), request_id))

        payload = {'comment': body}
        if commit is not None:
            payload['commit'] = commit
        if filename is not None:
            payload['filename'] = filename
        if row is not None:
            payload['row'] = row

        return_value = self._call_api(request_url,
                                      method='POST', data=payload)

        LOG.debug(return_value)

    def flag_request(self, request_id, username, percent, comment, url,
                     uid=None, commit=None):
        """
        Add or edit a flag of the request.
        :param request_id: the id of the request
        :param username: the name of the application to be displayed
        :param percent: the percentage of completion to be displayed
        :param comment: a short message summarizing the flag
        :param url: a relevant URL
        :param uid: a unique id used to identify the flag.
            If not provided, pagure will generate one
        :param commit: which commit to flag on
        :return:
        """
        request_url = "{}pull-request/{}/flag".format(self.create_basic_url(),
                                                      request_id)

        payload = {'username': username, 'percent': percent,
                   'comment': comment, 'url': url}
        if commit is not None:
            payload['commit'] = commit
        if uid is not None:
            payload['uid'] = uid

        return_value = self._call_api(request_url,
                                      method='POST', data=payload)

        LOG.debug(return_value)

    def create_issue(self, title, content, priority=None,
                     milestone=None, tags=None, assignee=None,
                     private=None):
        """
        Create a new issue.
        :param title: the title of the issue
        :param content: the description of the issue
        :param priority: the priority of the ticket
        :param milestone: the milestone of the ticket
        :param tags: comma sperated list of tag for the ticket
        :param assignee: the assignee of the ticket
        :param private: whether create this issue as private
        :return:
        """
        request_url = "{}new_issue".format(self.create_basic_url())

        payload = {'title': title, 'issue_content': content}

        if priority is not None:
            payload['priority'] = priority
        if milestone is not None:
            payload['milestone'] = milestone
        if tags is not None:
            payload['tag'] = tags
        if assignee is not None:
            payload['assignee'] = assignee
        if private is not None:
            payload['private'] = private

        return_value = self._call_api(request_url,
                                      method='POST', data=payload)

        LOG.debug(return_value)

    def list_issues(
            self, status=None, tags=None, assignee=None, author=None,
            milestones=None, priority=None, no_stones=None, since=None,
            order=None
    ):
        """
        List all issues of a project.
        :param status: filters the status of the issues
        :param tags: filers the tags of the issues
        :param assignee: filters the assignee of the issues
        :param author: filters the author of the issues
        :param milestones: filters the milestones of the issues (list of
            strings)
        :param priority: filters the priority of the issues
        :param no_stones: If True returns only the issues having no milestone,
            if False returns only the issues having a milestone
        :param since: Filters the issues updated after this date.
            The date can either be provided as an unix date or in the format
            Y-M-D
        :param order: Set the ordering of the issues. This can be asc or desc.
            Default: desc
        :return:
        """
        request_url = "{}issues".format(self.create_basic_url())

        payload = {}
        if status is not None:
            payload['status'] = status
        if tags is not None:
            payload['tags'] = tags
        if assignee is not None:
            payload['assignee'] = assignee
        if author is not None:
            payload['author'] = author
        if milestones is not None:
            payload['milestones'] = milestones
        if priority is not None:
            payload['priority'] = priority
        if no_stones is not None:
            payload['no_stones'] = no_stones
        if since is not None:
            payload['since'] = since
        if order is not None:
            payload['order'] = order

        return_value = self._call_api(request_url, params=payload)

        return return_value['issues']

    def issue_info(self, issue_id):
        """
        Get info about a single issue.
        :param issue_id: the id of the issue
        :return:
        """
        request_url = "{}issue/{}".format(self.create_basic_url(), issue_id)

        return_value = self._call_api(request_url)

        return return_value

    def get_list_comment(self, issue_id, comment_id):
        """
        Get a specific comment of an issue.
        :param issue_id: the id of the issue
        :param comment_id: the id of the comment
        :return:
        """
        request_url = "{}issue/{}/comment/{}".format(self.create_basic_url(),
                                                     issue_id, comment_id)

        return_value = self._call_api(request_url)

        return return_value

    def change_issue_status(self, issue_id, new_status, close_status=None):
        """
        Change the status of an issue.
        :param issue_id: the id of the issue
        :param new_status: the new status fo the issue
        :param close_status: optional param to add reason why issue
            has been closed (like wontfix, fixed, duplicate, ...)
        :return:
        """
        request_url = "{}issue/{}/status".format(self.create_basic_url(),
                                                 issue_id)

        payload = {'status': new_status}
        if close_status is not None:
            payload['close_status'] = close_status

        return_value = self._call_api(request_url,
                                      method='POST', data=payload)

        LOG.debug(return_value)

    def change_issue_milestone(self, issue_id, milestone):
        """
        Change the milestone of an issue.
        :param issue_id: the id of the issue
        :param milestone: the new milestone for the issue
            (set None to remove milestone)
        :return:
        """
        request_url = "{}issue/{}/milestone".format(self.create_basic_url(),
                                                    issue_id)

        payload = {} if milestone is None else {'milestone': milestone}

        return_value = self._call_api(request_url,
                                      method='POST', data=payload)

        LOG.debug(return_value)

    def comment_issue(self, issue_id, body):
        """
        Comment to an issue.
        :param issue_id: the id of the comment
        :param body: the comment body
        :return:
        """
        request_url = "{}issue/{}/comment".format(self.create_basic_url(),
                                                  issue_id)

        payload = {'comment': body}

        return_value = self._call_api(request_url,
                                      method='POST', data=payload)

        LOG.debug(return_value)

    def project_tags(self):
        """
        List all git tags made to the project.
        :return:
        """
        request_url = "{}git/tags".format(self.create_basic_url())

        return_value = self._call_api(request_url)

        return return_value['tags']

    def list_projects(self, tags=None, pattern=None, username=None, owner=None,
                      namespace=None, fork=None, short=None, page=None,
                      per_page=None):
        """
        Lisk all projects on this Pagure instance.
        :param tags: filters the tags of the project
        :param pattern: filters the projects by the pattern string
        :param username: filters the username of the project administrators
        :param owner: filters the projects by ownership
        :param namespace: filters the projects by namespace
        :param fork: filters whether it is a fork (True) or not (False)
        :param short: whether to return the entrie JSON or just a sub-set
        :param page: specifies that pagination should be turned on and that
            this specific page should be displayed
        :param per_page: the number of projects to return per page.
            The maximum is 100
        :return:
        """
        request_url = "{}/api/0/projects".format(self.instance)

        payload = {}
        if tags is not None:
            payload['tags'] = tags
        if pattern is not None:
            payload['pattern'] = pattern
        if username is not None:
            payload['username'] = username
        if owner is not None:
            payload['owner'] = owner
        if namespace is not None:
            payload['namespace'] = namespace
        if fork is not None:
            payload['fork'] = fork
        if short is not None:
            payload['short'] = short
        if page is not None:
            payload['page'] = str(page)
        if per_page is not None:
            payload['per_page'] = str(per_page)

        return_value = self._call_api(request_url, params=payload)

        return return_value['projects']

    def user_info(self, username):
        """
        Get info of a specific user.
        :param username: the username of the user to get info about
        :return:
        """
        request_url = "{}/api/0/user/{}".format(self.instance, username)

        return_value = self._call_api(request_url)

        return return_value

    def new_project(self, name, description, namespace=None, url=None,
                    avatar_email=None, create_readme=False, private=False):
        """
        Create a new project on the pagure instance
        :param name: the name of the new project.
        :param description: A short description of the new project.
        :param namespace: The namespace of the project to fork
        :param url: A url providing more information about the project.
        :param avatar_email: An email address for the avatar of the project.
        :param create_readme: Boolean to specify if there should be a
            readme added to the project on creation.
        :param private: boolean to specify if the project is private
        :return:
        """
        request_url = "{}/api/0/new".format(self.instance)

        payload = {'name': name, 'description': description}
        if namespace is not None:
            payload['namespace'] = namespace
        if url is not None:
            payload['url'] = url
        if avatar_email is not None:
            payload['avatar_email'] = avatar_email
        payload['create_readme'] = create_readme
        payload['private'] = private

        return_value = self._call_api(request_url, data=payload,
                                      method='POST')

        return return_value['message']

    def project_branches(self):
        """
        List all branches associated with a repository.
        :return:
        """
        request_url = "{}git/branches".format(self.create_basic_url())

        return_value = self._call_api(request_url)

        return return_value['branches']
