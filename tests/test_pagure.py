import unittest
import libpagure
import requests_mock
import json

@requests_mock.Mocker()
class TestApiVersion(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)
        
    def test_version(self, m):
        mock_resp = """
        {
          "version": "0.14"
        }
        """
        m.get('https://mockpagure.io/api/0/version', text=mock_resp)
        res = self.pagure.api_version()
        self.assertEqual(res, json.loads(mock_resp)['version'])

@requests_mock.Mocker()
class TestListUsers(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)

    def test_listall(self, m):
        mock_resp = """        
        {
          "mention": [
            {
              "image": "https://avatarcdn/user1",
              "name": "Random User",
              "username": "rdmusr"
            },
            {
              "image": "https://avatarcdn/user2",
              "name": "randomuser",
              "username": "another"
            },
            {
              "image": "https://avatarcdn/user3",
              "name": "User Chan",
              "username": "u_chan"
            },
            {
              "image": "https://avatarcdn/user4",
              "name": "aabbcc",
              "username": "aabbcc"
            }
          ],
          "total_users": 4,
          "users": [
            "rdmusr",
            "another",
            "u_chan",
            "aabbcc"
          ]
        }
        """
        m.get('https://mockpagure.io/api/0/users', text=mock_resp)
        res = self.pagure.list_users()
        self.assertEqual(res, json.loads(mock_resp)['users'])
    
    def test_filtered(self, m):
        mock_resp = """        
        {
          "mention": [
            {
              "image": "https://avatarcdn/user3",
              "name": "User Chan",
              "username": "u_chan"
            }
          ],
          "total_users": 1,
          "users": [
            "u_chan"
          ]
        }
        """
        m.get('https://mockpagure.io/api/0/users?pattern=u', text=mock_resp)
        res = self.pagure.list_users(pattern="u")
        self.assertEqual(res, json.loads(mock_resp)['users'])

@requests_mock.Mocker()
class TestListGroups(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)

    def test_listall(self, m):
        mock_resp = """        
        {
          "groups": [
            "first_group",
            "SecondGroup"
          ],
          "total_groups": 2
        }
        """
        m.get('https://mockpagure.io/api/0/groups', text=mock_resp)
        res = self.pagure.list_groups()
        self.assertEqual(res, json.loads(mock_resp)['groups'])
    
    def test_filtered(self, m):
        mock_resp = """        
        {
          "groups": [
            "SecondGroup"
          ],
          "total_groups": 1
        }
        """
        m.get('https://mockpagure.io/api/0/groups?pattern=Sec', text=mock_resp)
        res = self.pagure.list_groups(pattern="Sec")
        self.assertEqual(res, json.loads(mock_resp)['groups'])

@requests_mock.Mocker()
class TestListErrorCode(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)

    def test_list(self, m):
        mock_resp = """        
        {
          "ETIMESTAMP": "Invalid timestamp format",
          "ETRACKERDISABLED": "Issue tracker disabled for this project"
        }
        """
        m.get('https://mockpagure.io/api/0/error_codes', text=mock_resp)
        res = self.pagure.error_codes()
        self.assertEqual(res, json.loads(mock_resp))

@requests_mock.Mocker()
class TestListProjects(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)

    def test_filter_username(self, m):
        mock_resp = """        
        {
          "args": {
            "fork": null,
            "namespace": null,
            "owner": null,
            "pattern": null,
            "tags": [],
            "username": "yangl1996"
          },
          "projects": [
            {
              "access_groups": {
                "admin": [],
                "commit": [],
                "ticket": []
              },
              "access_users": {
                "admin": [],
                "commit": [],
                "owner": [
                  "yangl1996"
                ],
                "ticket": []
              },
              "close_status": [],
              "custom_keys": [],
              "date_created": "1497467693",
              "description": "Testground for libpagure",
              "fullname": "libpagure-test",
              "id": 2469,
              "milestones": {},
              "name": "libpagure-test",
              "namespace": null,
              "parent": null,
              "priorities": {},
              "tags": [],
              "user": {
                "fullname": "Lei Yang",
                "name": "yangl1996"
              }
            },
            {
              "access_groups": {
                "admin": [],
                "commit": [],
                "ticket": []
              },
              "access_users": {
                "admin": [],
                "commit": [],
                "owner": [
                  "yangl1996"
                ],
                "ticket": []
              },
              "close_status": [
                "Invalid",
                "Insufficient data",
                "Fixed",
                "Duplicate"
              ],
              "custom_keys": [],
              "date_created": "1435592462",
              "description": "A git centered forge",
              "fullname": "forks/yangl1996/pagure",
              "id": 90,
              "milestones": {},
              "name": "pagure",
              "namespace": null,
              "parent": {
                "access_groups": {
                  "admin": [],
                  "commit": [],
                  "ticket": []
                },
                "access_users": {
                  "admin": [
                    "ryanlerch"
                  ],
                  "commit": [
                    "puiterwijk"
                  ],
                  "owner": [
                    "pingou"
                  ],
                  "ticket": [
                    "cverna",
                    "mprahl",
                    "jcline",
                    "vivekanand1101",
                    "lslebodn",
                    "farhaan"
                  ]
                },
                "close_status": [
                  "Invalid",
                  "Insufficient data",
                  "Fixed",
                  "Duplicate"
                ],
                "custom_keys": [],
                "date_created": "1431549490",
                "description": "A git centered forge",
                "fullname": "pagure",
                "id": 10,
                "milestones": {},
                "name": "pagure",
                "namespace": null,
                "parent": null,
                "priorities": {},
                "tags": [
                  "pagure",
                  "fedmsg"
                ],
                "user": {
                  "fullname": "Pierre-YvesChibon",
                  "name": "pingou"
                }
              },
              "priorities": {},
              "tags": [],
              "user": {
                "fullname": "Lei Yang",
                "name": "yangl1996"
              }
            }
          ],
          "total_projects": 2
        }
        """
        m.get('https://mockpagure.io/api/0/projects?username=yangl1996', text=mock_resp)
        res = self.pagure.list_projects(username='yangl1996')
        self.assertEqual(res, json.loads(mock_resp)['projects'])
        
    def test_filter_username_and_fork(self, m):
        mock_resp = """        
        {
          "args": {
            "fork": null,
            "namespace": null,
            "owner": null,
            "pattern": null,
            "tags": [],
            "username": "yangl1996"
          },
          "projects": [
            {
              "access_groups": {
                "admin": [],
                "commit": [],
                "ticket": []
              },
              "access_users": {
                "admin": [],
                "commit": [],
                "owner": [
                  "yangl1996"
                ],
                "ticket": []
              },
              "close_status": [
                "Invalid",
                "Insufficient data",
                "Fixed",
                "Duplicate"
              ],
              "custom_keys": [],
              "date_created": "1435592462",
              "description": "A git centered forge",
              "fullname": "forks/yangl1996/pagure",
              "id": 90,
              "milestones": {},
              "name": "pagure",
              "namespace": null,
              "parent": {
                "access_groups": {
                  "admin": [],
                  "commit": [],
                  "ticket": []
                },
                "access_users": {
                  "admin": [
                    "ryanlerch"
                  ],
                  "commit": [
                    "puiterwijk"
                  ],
                  "owner": [
                    "pingou"
                  ],
                  "ticket": [
                    "cverna",
                    "mprahl",
                    "jcline",
                    "vivekanand1101",
                    "lslebodn",
                    "farhaan"
                  ]
                },
                "close_status": [
                  "Invalid",
                  "Insufficient data",
                  "Fixed",
                  "Duplicate"
                ],
                "custom_keys": [],
                "date_created": "1431549490",
                "description": "A git centered forge",
                "fullname": "pagure",
                "id": 10,
                "milestones": {},
                "name": "pagure",
                "namespace": null,
                "parent": null,
                "priorities": {},
                "tags": [
                  "pagure",
                  "fedmsg"
                ],
                "user": {
                  "fullname": "Pierre-YvesChibon",
                  "name": "pingou"
                }
              },
              "priorities": {},
              "tags": [],
              "user": {
                "fullname": "Lei Yang",
                "name": "yangl1996"
              }
            }
          ],
          "total_projects": 1
        }
        """
        m.get('https://mockpagure.io/api/0/projects?username=yangl1996&fork=True', text=mock_resp)
        res = self.pagure.list_projects(username='yangl1996', fork=True)
        self.assertEqual(res, json.loads(mock_resp)['projects'])
        
@requests_mock.Mocker()
class TestGetUserInfo(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)

    def test_list(self, m):
        mock_resp = """        
        {
          "forks": [
            {
              "access_groups": {
                "admin": [],
                "commit": [],
                "ticket": []
              },
              "access_users": {
                "admin": [],
                "commit": [],
                "owner": [
                  "yangl1996"
                ],
                "ticket": []
              },
              "close_status": [
                "Invalid",
                "Insufficient data",
                "Fixed",
                "Duplicate"
              ],
              "custom_keys": [],
              "date_created": "1435592462",
              "description": "A git centered forge",
              "fullname": "forks/yangl1996/pagure",
              "id": 90,
              "milestones": {},
              "name": "pagure",
              "namespace": null,
              "parent": {
                "access_groups": {
                  "admin": [],
                  "commit": [],
                  "ticket": []
                },
                "access_users": {
                  "admin": [
                    "ryanlerch"
                  ],
                  "commit": [
                    "puiterwijk"
                  ],
                  "owner": [
                    "pingou"
                  ],
                  "ticket": [
                    "farhaan",
                    "lslebodn",
                    "vivekanand1101",
                    "mprahl",
                    "jcline",
                    "cverna"
                  ]
                },
                "close_status": [
                  "Invalid",
                  "Insufficient data",
                  "Fixed",
                  "Duplicate"
                ],
                "custom_keys": [],
                "date_created": "1431549490",
                "description": "A git centered forge",
                "fullname": "pagure",
                "id": 10,
                "milestones": {},
                "name": "pagure",
                "namespace": null,
                "parent": null,
                "priorities": {},
                "settings": {
                  "Enforce_signed-off_commits_in_pull-request": false,
                  "Minimum_score_to_merge_pull-request": -1,
                  "Only_assignee_can_merge_pull-request": false,
                  "Web-hooks": null,
                  "always_merge": false,
                  "fedmsg_notifications": true,
                  "issue_tracker": true,
                  "issues_default_to_private": false,
                  "project_documentation": true,
                  "pull_request_access_only": false,
                  "pull_requests": true
                },
                "tags": [
                  "pagure",
                  "fedmsg"
                ],
                "user": {
                  "fullname": "Pierre-YvesChibon",
                  "name": "pingou"
                }
              },
              "priorities": {},
              "settings": {
                "Enforce_signed-off_commits_in_pull-request": false,
                "Minimum_score_to_merge_pull-request": -1,
                "Only_assignee_can_merge_pull-request": false,
                "Web-hooks": null,
                "always_merge": false,
                "fedmsg_notifications": true,
                "issue_tracker": true,
                "issues_default_to_private": false,
                "project_documentation": false,
                "pull_request_access_only": false,
                "pull_requests": true
              },
              "tags": [],
              "user": {
                "fullname": "Lei Yang",
                "name": "yangl1996"
              }
            }
          ],
          "repos": [
            {
              "access_groups": {
                "admin": [],
                "commit": [],
                "ticket": []
              },
              "access_users": {
                "admin": [
                  "pingou",
                  "sayanchowdhury"
                ],
                "commit": [],
                "owner": [
                  "yangl1996"
                ],
                "ticket": []
              },
              "close_status": [
                "Invalid",
                "Insufficient data",
                "Fixed",
                "Duplicate"
              ],
              "custom_keys": [],
              "date_created": "1437130074",
              "description": "A Python library for Pagure APIs",
              "fullname": "libpagure",
              "id": 107,
              "milestones": {},
              "name": "libpagure",
              "namespace": null,
              "parent": null,
              "priorities": {},
              "settings": {
                "Enforce_signed-off_commits_in_pull-request": false,
                "Minimum_score_to_merge_pull-request": -1,
                "Only_assignee_can_merge_pull-request": false,
                "Web-hooks": null,
                "always_merge": false,
                "fedmsg_notifications": true,
                "issue_tracker": true,
                "issues_default_to_private": false,
                "project_documentation": false,
                "pull_request_access_only": false,
                "pull_requests": true
              },
              "tags": [
                "pagure",
                "fedora-infra",
                "fedmsg"
              ],
              "user": {
                "fullname": "Lei Yang",
                "name": "yangl1996"
              }
            },
            {
              "access_groups": {
                "admin": [],
                "commit": [],
                "ticket": []
              },
              "access_users": {
                "admin": [],
                "commit": [],
                "owner": [
                  "yangl1996"
                ],
                "ticket": []
              },
              "close_status": [],
              "custom_keys": [],
              "date_created": "1497467693",
              "description": "Testground for libpagure",
              "fullname": "libpagure-test",
              "id": 2469,
              "milestones": {},
              "name": "libpagure-test",
              "namespace": null,
              "parent": null,
              "priorities": {},
              "settings": {
                "Enforce_signed-off_commits_in_pull-request": false,
                "Minimum_score_to_merge_pull-request": -1,
                "Only_assignee_can_merge_pull-request": false,
                "Web-hooks": null,
                "always_merge": false,
                "fedmsg_notifications": true,
                "issue_tracker": true,
                "issues_default_to_private": false,
                "project_documentation": false,
                "pull_request_access_only": false,
                "pull_requests": true
              },
              "tags": [],
              "user": {
                "fullname": "Lei Yang",
                "name": "yangl1996"
              }
            }
          ],
          "user": {
            "fullname": "Lei Yang",
            "name": "yangl1996"
          }
        }
        """
        m.get('https://mockpagure.io/api/0/user/yangl1996', text=mock_resp)
        res = self.pagure.user_info('yangl1996')
        self.assertEqual(res, json.loads(mock_resp))
        
@requests_mock.Mocker()
class TestCreateNewProject(unittest.TestCase):
    
    def setUp(self):
        self.pagure = libpagure.Pagure(
            user_token='1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ',
            instance_url='https://mockpagure.io',
            insecure=False)
    
    def test_list(self, m):
        expt_body = 'name=testnewproject&description=for+test+purposes&url=http%3A%2F%2Fexample.org&create_readme=True'
        mock_resp = """
        {
          "message": "Project \\"testnewproject\\" created"
        }
        """
        m.post(
            'https://mockpagure.io/api/0/new',
            headers={'Authorization': 
            'token 1KLLJ74RFM3C8349L3P2VFOD3NC58ATE7B5IG31PSTP10KYHDJ1F6NRHSSGS91EQ'},
            additional_matcher=lambda req: (req.text == expt_body),
            text=mock_resp)
        res = self.pagure.new_project(
            'testnewproject',
            'for test purposes',
            url='http://example.org',
            create_readme=True)
        self.assertEqual(res, json.loads(mock_resp)['message'])

if __name__ == '__main__':
    unittest.main()