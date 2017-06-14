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
            user_token=None,
            instance_url="https://pagure.io",
            insecure=False):
        """
        Create an instance.
        :param pagure_token: pagure API token
        :param instance_url: the URL of pagure instance name
        :param insecure: currently not implemented
        :return:
        """
        self.token = user_token
        self.instance = instance_url
        self.session = requests.session()
        self.insecure = insecure
        if self.token:
            self.session.headers.update({"Authorization": "token " + self.token})

    def _call_api(self, endpoint, method='GET', params=None, data=None):
        """ Method used to call the API.
        It returns the raw JSON returned by the API or raises an exception
        if something goes wrong.

        :arg endpoint: the endpoint to call, based on /api/0
        :kwarg method: the HTTP method to use when calling the specified
            URL, can be GET, POST, DELETE, UPDATE...
            Defaults to GET
        :kwarg params: the params to specify to a GET request
        :kwarg data: the data to send to a POST request

        """
        base_url = "{}/api/0".format(self.instance)
        req = self.session.request(
            method=method,
            url=base_url+endpoint,
            params=params,
            data=data,
            verify=not self.insecure
        )

        output = None
        try:
            output = req.json()
        except Exception as err:
            LOG.debug(req.text)
            # TODO: use a dedicated error class
            raise Exception('Error while decoding JSON: {0}'.format(err))

        if req.status_code != 200:
            LOG.debug('full output: {0}'.format(output))
            if output is None:
                # TODO: use a dedicated error class
                raise Exception('No output returned by %s' % req.url)
            if 'error_code' in output:
                raise APIError(output['error'])

        return output

    def api_version(self):
        """
        Get Pagure API version.
        :return:
        """
        endpoint = "/version"
        
        return_value = self._call_api(endpoint)
        return return_value['version']

    def list_users(self, pattern=None):
        """
        List all users registered on this Pagure instance.
        :param pattern: filters the starting letters of the return value
        :return:
        """
        endpoint = "/users"
        
        params = None
        if pattern:
            params = {'pattern': pattern}
        return_value = self._call_api(endpoint, params=params)
        return return_value['users']

    def list_groups(self, pattern=None):
        """
        List all groups on this Pagure instance.
        :param pattern: filters the starting letters of the return value
        :return:
        """
        endpoint = "/groups"
        
        params = None
        if pattern:
            params = {'pattern': pattern}
        return_value = self._call_api(endpoint, params=params)
        return return_value['groups']

    def error_codes(self):
        """
        Get a dictionary of all error codes.
        :return:
        """
        endpoint = "/error_codes"
        
        return_value = self._call_api(endpoint)
        return return_value

    def list_projects(self, tags=None, username=None, fork=None):
        """
        Lisk all projects on this Pagure instance.
        :param tags: filters the tags of the project
        :param username: filters the username of the project administrators
        :param fork: filters whether it is a fork (True) or not (False)
        :return:
        """
        endpoint = "/projects"
        
        payload = {}
        if tags is not None:
            payload['tags'] = tags
        if username is not None:
            payload['username'] = username
        if fork is not None:
            payload['fork'] = fork
        return_value = self._call_api(endpoint, params=payload)
        return return_value['projects']

    def user_info(self, username):
        """
        Get info of a specific user.
        :param username: the username of the user to get info about
        :return:
        """
        endpoint = "/user/{}".format(username)
        
        return_value = self._call_api(endpoint)
        return return_value

    def new_project(self, name, description, namespace=None, url=None,
                    avatar_email=None, create_readme=False):
        """
        Create a new project on the pagure instance
        :param name: the name of the new project.
        :param description: A short description of the new project.
        :param namespace: The namespace of the project to fork
        :param url: A url providing more information about the project.
        :param avatar_email: An email address for the avatar of the project.
        :param create_readme: Boolean to specify if there should be a
            readme added to the project on creation.
        :return:
        """
        endpoint = "/new"

        payload = {'name': name, 'description': description}
        if namespace is not None:
            payload['namespace'] = namespace
        if url is not None:
            payload['url'] = url
        if avatar_email is not None:
            payload['avatar_email'] = avatar_email
        if create_readme is not None:
            payload['create_readme'] = create_readme

        return_value = self._call_api(endpoint, data=payload, method='POST')
        return return_value['message']
        
class Project(object):
    
    def __init__(
            self,
            pagure,
            project_token=None,
            project_name=None,
            namespace=None):
        """
        Create an instance.
        :param pagure_instance: an instance of Pagure class
        :param pagure_token: pagure API token
        :param pagure_repository: pagure project name
        :param fork_username: if this is a fork, it's the username
             of the fork creator
        :param instance_url: the URL of pagure instance name
        :return:
        """
        self.pagure = pagure;
        self.token = project_token
        self.repo = project_name
        self.namespace = namespace
        self.instance = instance_url
        if self.token:
            self.header = {"Authorization": "token " + self.token}
        else:
            self.header = None
            
    def _call_api(self, endpoint, method='GET', params=None, data=None):
        """ Method used to call the API.
        It returns the raw JSON returned by the API or raises an exception
        if something goes wrong.

        :arg endpoint: the endpoint to call, based on /api/0/<project name>
        :kwarg method: the HTTP method to use when calling the specified
            URL, can be GET, POST, DELETE, UPDATE...
            Defaults to GET
        :kwarg params: the params to specify to a GET request
        :kwarg data: the data to send to a POST request

        """
        if self.namespace is None:
            base_url = "{}/api/0/{}".format(
                self.pagure.instance, self.repo)
        else:
            base_url = "{}/api/0/fork/{}/{}".format(
                self.pagure.instance, self.namespace, self.repo)
                
        req = self.session.request(
            method=method,
            url=base_url+endpoint,
            params=params,
            data=data,
            verify=not self.pagure.insecure
        )

        output = None
        try:
            output = req.json()
        except Exception as err:
            LOG.debug(req.text)
            # TODO: use a dedicated error class
            raise Exception('Error while decoding JSON: {0}'.format(err))

        if req.status_code != 200:
            LOG.debug('full output: {0}'.format(output))
            if output is None:
                # TODO: use a dedicated error class
                raise Exception('No output returned by %s' % req.url)
            if 'error_code' in output:
                raise APIError(output['error'])

        return output
    
    def list_tags(self, pattern=None):
        """
        List all tags made on this project.
        :param pattern: filters the starting letters of the return value
        :return:
        """
        endpoint = "/tags"
        params = None
        if pattern:
            params = {'pattern': pattern}

        return_value = self._call_api(endpoint, params=params)
        return return_value['tags']
        
    def list_requests(self, status=None, assignee=None, author=None):
        """
        Get all pull requests of a project.
        :param status: filters the status of the requests
        :param assignee: filters the assignee of the requests
        :param author: filters the author of the requests
        :return:
        """
        endpoint = "/pull-requests"
        payload = {}
        if status is not None:
            payload['status'] = status
        if assignee is not None:
            payload['assignee'] = assignee
        if author is not None:
            payload['author'] = author

        return_value = self._call_api(endpoint, params=payload)
        return return_value['requests']

    def request_info(self, request_id):
        """
        Get information of a single pull request.
        :param request_id: the id of the request
        :return:
        """
        endpoint = "/pull-request/{}".format(request_id)

        return_value = self._call_api(endpoint)
        return return_value

    def merge_request(self, request_id):
        """
        Merge a pull request.
        :param request_id: the id of the request
        :return:
        """
        endpoint = "/pull-request/{}/merge".format(request_id)
 
        return_value = self._call_api(endpoint, method='POST')
        if return_value['message'] != "Changes merged!":
            raise Exception(return_value['message'])

    def close_request(self, request_id):
        """
        Close a pull request.
        :param request_id: the id of the request
        :return:
        """
        endpoint = "/pull-request/{}/close".format(request_id)
        
        return_value = self._call_api(endpoint, method='POST')
        if return_value['message'] != "Pull-request closed!":
            raise Exception(return_value['message'])

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
        endpoint = "/pull-request/{}/comment".format(request_id)

        payload = {'comment': body}
        if commit is not None:
            payload['commit'] = commit
        if filename is not None:
            payload['filename'] = filename
        if row is not None:
            payload['row'] = row

        return_value = self._call_api(endpoint,
                                      method='POST', data=payload)
        if return_value['message'] != "Comment added":
            raise Exception(return_value['message'])

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
        endpoint = "/pull-request/{}/flag".format(request_id)

        payload = {'username': username, 'percent': percent,
                   'comment': comment, 'url': url}
        if commit is not None:
            payload['commit'] = commit
        if uid is not None:
            payload['uid'] = uid

        return_value = self._call_api(endpoint,
                                      method='POST', data=payload)

        if return_value['message'] != "Flag added" and return_value['message'] != "Flag updated":
            raise Exception(return_value['message'])

    def create_issue(self, title, content, private=None):
        """
        Create a new issue.
        :param title: the title of the issue
        :param content: the description of the issue
        :param private: whether create this issue as private
        :return:
        """
        endpoint = "/new_issue"

        payload = {'title': title, 'issue_content': content}
        if private:
            payload['private'] = private

        return_value = self._call_api(endpoint,
                                      method='POST', data=payload)

        if return_value['message'] != "Issue created":
            raise Exception(return_value['message'])

    def list_issues(
            self, status=None, tags=None, assignee=None, author=None,
            milestones=None, priority=None, no_stones=None, since=None
    ):
        """
        List all issues of a project.
        :param status: filters the status of the issues
        :param tags: filers the tags of the issues
        :param assignee: filters the assignee of the issues
        :param author: filters the author of the issues
        :param milestones: filters the milestones of the issues (list of strings)
        :param priority: filters the priority of the issues
        :param no_stones: If True returns only the issues having no milestone,
            if False returns only the issues having a milestone
        :param since: Filters the issues updated after this date.
            The date can either be provided as an unix date or in the format Y-M-D
        :return:
        """
        endpoint = "/issues"

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

        return_value = self._call_api(endpoint, params=payload)

        return return_value['issues']

    def issue_info(self, issue_id):
        """
        Get info about a single issue.
        :param issue_id: the id of the issue
        :return:
        """
        endpoint = "/issue/{}".format(issue_id)

        return_value = self._call_api(endpoint)
        return return_value

    def get_list_comment(self, issue_id, comment_id):
        """
        Get a specific comment of an issue.
        :param issue_id: the id of the issue
        :param comment_id: the id of the comment
        :return:
        """
        endpoint = "/issue/{}/comment/{}".format(issue_id, comment_id)

        return_value = self._call_api(endpoint)
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
        endpoint = "/issue/{}/status".format(issue_id)

        payload = {'status': new_status}
        if close_status is not None:
            payload['close_status'] = close_status

        return_value = self._call_api(endpoint,
                                      method='POST', data=payload)

        if not return_value['message'].startswith("Successfully"):
            raise Exception(return_value['message'])

    def change_issue_milestone(self, issue_id, milestone):
        """
        Change the milestone of an issue.
        :param issue_id: the id of the issue
        :param milestone: the new milestone for the issue
            (set None to remove milestone)
        :return:
        """
        endpoint = "/issue/{}/milestone".format(issue_id)

        payload = {} if milestone is None else {'milestone': milestone}

        return_value = self._call_api(endpoint,
                                      method='POST', data=payload)

        if not return_value['message'].startswith("Successfully"):
            raise Exception(return_value['message'])

    def comment_issue(self, issue_id, body):
        """
        Comment to an issue.
        :param issue_id: the id of the comment
        :param body: the comment body
        :return:
        """
        endpoint = "/issue/{}/comment".format(issue_id)

        payload = {'comment': body}

        return_value = self._call_api(endpoint,
                                      method='POST', data=payload)

        if return_value['message'] != 'Comment added':
            raise Exception(return_value['message'])

    def project_tags(self):
        """
        List all git tags made to the project.
        :return:
        """
        endpoint = "/git/tags"
        
        return_value = self._call_api(endpoint)

        return return_value['tags']
