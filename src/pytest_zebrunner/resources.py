refresh_token = {"refreshToken": "REFRESH_TOKEN"}

test_run_v1 = {
    "name": "Test NG run",
    "startedAt": "2019-12-03T10:15:30+01:00",
    "framework": "testng",
    "config": {"env": "value", "appVersion": "value", "platform": "value"},
}


test_v1 = {
    "uuid": "1512351235-3215-3125-3215531",
    "name": "Test ABC",
    "className": "com.test.MyTests",
    "methodName": "featureTest()",
    "startedAt": "2007-12-03T10:15:30Z",
    "maintainer": "johndoe@zebrunner.com",
}


test_result_v1 = {"result": "failed", "endedAt": "2007-12-03T10:15:30Z"}


test_log = []

test_artifact = {
    "name": "jenkins-log-20200604.tar.gz",
    "url": "https://ci.organization.org/pipelines/jenkins-log- 20200604.tar.gz",
}
