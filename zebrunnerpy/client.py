from .resource_constants import Initiator, TestStatus, DriverMode
from .api_request import APIRequest
from .resources.user_cred_payload import user_cred
from .resources.test_suite_payload import test_suite
from .resources.test_case_payload import test_case
from .resources.job_payload import job
from .resources.test_run_payload import test_run
from .resources.test_payload import test
from .resources.test_artifact_payload import artifact
from .resources.user_payload import user
from .resources.refresh_token_payload import refresh_token


class ZafiraClient:
    DEFAULT_USER = "anonymous"
    STATUS_PATH = "/api/status"
    REFRESH_TOKEN_PATH = "/api/iam/v1/auth/refresh"
    LOGIN_PATH = "/api/auth/login"
    PROFILE_PATH = "/api/users/profile"
    TEST_SUITES_PATH = "/api/tests/suites"
    TEST_CASES_PATH = "/api/tests/cases"
    JOBS_PATH = "/api/jobs"
    TEST_RUNS_PATH = "/api/tests/runs"
    TESTS_PATH = "/api/tests"
    TEST_FINISH_PATH = "/api/tests/{}/finish"
    TEST_RUNS_FINISH_PATH = "/api/tests/runs/{}/finish"
    TEST_RUNS_ABORT_PATH = "/api/tests/runs/abort?id={}"
    TEST_BY_ID_PATH = "/api/tests/{}"
    ADD_TEST_ARTIFACT = "/api/tests/{}/artifacts"
    TEST_WORK_ITEMS_PATH =  "/api/tests/{}/workitems"
    TEST_RUNS_RESULTS_PATH = "/api/tests/runs/{}/results"
    USERS_PATH = "/api/users"
    PROJECT_PATH = "/api/projects"
    GET_SETTING_TOOL_PATH = "/api/settings/tool/{}"

    INSTANCE = None

    def __new__(cls, service_url):
        if not cls.INSTANCE:
            cls.INSTANCE = super(ZafiraClient, cls).__new__(cls)
        return cls.INSTANCE

    def __init__(self, service_url):
        self.api = APIRequest(service_url)
        self.auth_token = ''

    def get_setting_tool(self, tool):
        return self.api.send_get(ZafiraClient.GET_SETTING_TOOL_PATH.format(tool),
                                 headers=self.init_auth_headers(), default_err_msg="Unable to get settings by tool")

    def is_zafira_available(self):
        is_available = False
        if self.api.send_get(ZafiraClient.STATUS_PATH, default_err_msg="Unable to send ping").status_code == 200:
            is_available = True
        return is_available

    def login(self, username, password):
        user_cred['username'] = username
        user_cred['password'] = password
        return self.api.send_post_without_authorization(ZafiraClient.LOGIN_PATH, user_cred, 'Unable to login')

    def create_test_suite(self, user_id, suite_name, file_name, description=None):
        test_suite['userId'] = user_id
        test_suite['description'] = description
        test_suite['fileName'] = file_name
        test_suite['name'] = suite_name
        return self.api.send_post(ZafiraClient.TEST_SUITES_PATH, test_suite, headers=self.init_auth_headers(),
                                  default_err_msg="Unable to create test suite")

    def create_test_case(self, test_class, test_method, test_suite_id, user_id, info=None, project=None):
        test_case['testClass'] = test_class
        test_case['testMethod'] = test_method
        test_case['testSuiteId'] = test_suite_id
        test_case['primaryOwnerId'] = user_id
        test_case['info'] = info
        test_case['project'] = project
        return self.api.send_post(ZafiraClient.TEST_CASES_PATH, test_case, headers=self.init_headers_with_project(),
                                  default_err_msg="Unable to create test case")

    def create_job(self, user_id, job_name, job_url, jenkins_host):
        job["userId"] = user_id
        job["jobURL"] = job_url
        job["name"] = job_name
        job["jenkinsHost"] = jenkins_host
        return self.api.send_post(ZafiraClient.JOBS_PATH, job, headers=self.init_auth_headers(),
                                  default_err_msg="Unable to create job")

    def start_test_run(self, job_id, test_suite_id, build_number, started_by=Initiator.SCHEDULER.value,  # noqa F405
                       driver_mode=DriverMode.METHOD_MODE.value, config=None, blocker=None,  # noqa F405
                       work_item=None, status=None, project=None, known_issue=None):
        test_run["jobId"] = job_id
        test_run["testSuiteId"] = test_suite_id
        test_run["buildNumber"] = build_number
        test_run["startedBy"] = started_by
        test_run["driverMode"] = driver_mode
        test_run["blocker"] = blocker
        test_run["workItem"] = work_item
        test_run["status"] = status
        test_run["project"] = project
        test_run["knownIssue"] = known_issue
        test_run["configXML"] = config
        return self.api.send_post(ZafiraClient.TEST_RUNS_PATH, test_run, headers=self.init_auth_headers(),
                                  default_err_msg="Unable to start test run")

    def update_test_run(self, test_run):
        return self.api.send_put(ZafiraClient.TEST_RUNS_PATH, test_run, headers=self.init_auth_headers(),
                                 default_err_msg="Unable to start test run")

    def finish_test_run(self, test_run_id):
        return self.api.send_post(ZafiraClient.TEST_RUNS_FINISH_PATH.format(test_run_id),
                                  headers=self.init_auth_headers(), default_err_msg="Unable to finish test run")

    def abort_test_run(self, test_run_id):
        return self.api.send_post(ZafiraClient.TEST_RUNS_ABORT_PATH.format(test_run_id),
                                  headers=self.init_auth_headers(), default_err_msg="Unable to find test run by id")

    def start_test(self, test_run_id, test_case_id, test_name, start_time, ci_test_id,
                   status=TestStatus.IN_PROGRESS.value, test_class=None,  # noqa F405
                   test_group=None, work_items=None):
        test["testRunId"] = test_run_id
        test["testCaseId"] = test_case_id
        test["name"] = test_name
        test["ciTestId"] = ci_test_id
        test["startTime"] = start_time
        test["testClass"] = test_class
        test["status"] = status
        test["workItems"] = work_items
        test["testGroup"] = test_group
        return self.api.send_post(ZafiraClient.TESTS_PATH, test, headers=self.init_auth_headers(),
                                  default_err_msg="Unable to start test")

    def finish_test(self, test):
        return self.api.send_post(ZafiraClient.TEST_FINISH_PATH.format(test["id"]), test,
                                  headers=self.init_auth_headers(), default_err_msg="Unable to finish test")

    def delete_test_by_id(self, test_id):
        return self.api.send_delete(ZafiraClient.TEST_BY_ID_PATH.format(test_id), headers=self.init_auth_headers(),
                                    default_err_msg="Unable to finish test")

    def update_test(self, test):
        return self.api.send_put(ZafiraClient.TESTS_PATH, test, headers=self.init_auth_headers(),
                                 default_err_msg="Unable to update test")

    def add_test_artifact_to_test(self, test_id, link, artifact_name, expires_in=None):
        artifact["testId"] = test_id
        artifact["link"] = link
        artifact["name"] = artifact_name
        artifact["expiresIn"] = expires_in
        return self.api.send_post(ZafiraClient.ADD_TEST_ARTIFACT.format(test_id), artifact,
                                  headers=self.init_auth_headers(), default_err_msg="Unable to add test artifact")

    def refresh_token(self, token):
        refresh_token["refreshToken"] = token
        return self.api.send_post_without_authorization(ZafiraClient.REFRESH_TOKEN_PATH, refresh_token,
                                                        default_err_msg="Unable to refresh token")

    def create_test_work_items(self, test_id, list_work_items):
        return self.api.send_post(ZafiraClient.TEST_WORK_ITEMS_PATH.format(test_id), list_work_items,
                                  headers=self.init_auth_headers(), default_err_msg="Unable to create workitems")

    def get_test_run_results(self, test_run_id):
        return self.api.send_get(ZafiraClient.TEST_RUNS_RESULTS_PATH.format(test_run_id),
                                 headers=self.init_auth_headers(), default_err_msg="Unable to find test run results")

    def create_user(self, first_name, last_name, email, password):
        user["firstName"] = first_name
        user["lastName"] = last_name
        user["email"] = email
        user["password"] = password
        return self.api.send_put(ZafiraClient.USERS_PATH, user, headers=self.init_auth_headers(),
                                 default_err_msg="Unable to create user")

    def get_user_profile(self, username=None):
        endpoint = ZafiraClient.PROFILE_PATH
        if username:
            endpoint += "?username=" + username
        return self.api.send_get(endpoint, headers=self.init_auth_headers(),
                                 default_err_msg="Unable to authorize user")

    def get_user_or_anonymous_if_not_found(self, username):
        try:
            return self.get_user_profile(username)
        except Exception:
            return self.get_user_profile(self.DEFAULT_USER)

    def create_project(self, project):
        return self.api.send_post(ZafiraClient.PROJECT_PATH, project, headers=self.init_auth_headers(),
                                  default_err_msg="Unable to create project")

    def init_auth_headers(self):
        return {"Authorization": "Bearer " + self.auth_token}

    def init_headers_with_project(self):
        return {"Authorization": "Bearer " + self.auth_token, "project": "UNKNOWN"}
