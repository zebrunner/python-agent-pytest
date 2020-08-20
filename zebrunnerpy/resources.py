job = {
  "id": None,
  "jenkinsHost": "http://127.0.0.1:8080",
  "jobURL": "http://localhost:8080/job/Job_Selenoid/",
  "name": "NAME",
  "userId": "USER_ID_INT"
}


project = {
    "description": "DESCRIPTION",
    "id": None,
    "name": "NAME"
}


refresh_token = {
  "refreshToken": "REFRESH_TOKEN"
}


artifact = {
      "expiresIn": None,
      "id": None,
      "link": "LINK",
      "name": "NAME",
      "testId": "TEST_ID_INT"
}


test_case = {
  "id": None,
  "info": None,
  "primaryOwnerId": "OWNER_ID_INT",
  "project": None,
  "secondaryOwnerId": None,
  "testClass": "TEST_CLASS",
  "testMethod": "TEST_METHOD",
  "testSuiteId": "TEST_SUITE_ID_INT"
}


test = {
  "artifacts": [],
  "blocker": None,
  "ciTestId": None,
  "configXML": None,
  "dependsOnMethods": None,
  "finishTime": None,
  "id": None,
  "knownIssue": None,
  "message": None,
  "messageHashCode": None,
  "name": "NAME",
  "needRerun": None,
  "retry": None,
  "startTime": None,
  "status": None,
  "testArgs": None,
  "testCaseId": "TEST_CASE_ID_INT",
  "testClass": None,
  "testGroup": None,
  "testMetrics": None,
  "testRunId": "TEST_RUN_ID_INT",
  "workItems": []
}


test_run = {
  "blocker": None,
  "buildNumber": "BUILD_NUMBER_INT",
  "ciRunId": None,
  "configXML": None,
  "driverMode": "DRIVER_MODE",
  "id": None,
  "jobId": "JOB_ID_INT",
  "knownIssue": None,
  "project": None,
  "reviewed": None,
  "scmBranch": None,
  "scmCommit": None,
  "scmURL": None,
  "startedBy": "STARTED_BY",
  "status": None,
  "testSuiteId": "TEST_SUITE_ID_INT",
  "upstreamJobBuildNumber": None,
  "upstreamJobId": None,
  "userId": None,
  "workItem": None
}


test_suite = {
  "description": None,
  "fileName": "FILE_NAME",
  "name": "NAME",
  "userId": "USER_ID"
}


user_cred = {
  "password": "PASSWORD",
  "username": "USERNAME"
}


user = {
  "email": None,
  "firstName": "FIRST_NAME",
  "id": None,
  "lastLogin": None,
  "lastName": "LAST_NAME",
  "password": "PASSWORD",
  "permissions": [],
  "photoURL": None,
  "preferences": [],
  "roles": [],
  "source": None,
  "status": None,
  "username": "USERNAME"
}
