# Zebrunner PyTest reporting agent

The official Zebrunner PyTest agent provides the reporting functionality. It can automatically track Selenium sessions
and send the info about session details to Zebrunner backend. It can be easily integrated into a project by just installing the library
and adding the configuration file.

Including reporting into your project is easy - just install the agent and provide minimal valid configuration for reporting.

## Inclusion into your project

    pip install pytest-zebrunner


## Configuring reporting of test executions

After the installation, reporting is disabled by default. It won't send any data to the Zebrunner service without a valid configuration.

It is currently possible to provide the configuration via:
1. Environment variables
2. YAML file

`pyproject.toml`, `command arguments` are in plans for future releases.

### via environment variables

The following configuration parameters are recognized by the agent:

- `REPORTING_ENABLED` - enables or disables reporting. The default value is `true`.
- `REPORTING_SERVER_HOSTNAME` - mandatory if reporting is enabled. It is Zebrunner server hostname. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Service URL' section;
- `REPORTING_SERVER_ACCESS_TOKEN` - mandatory if reporting is enabled. Access token must be used to perform API calls. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Token' section;
- `REPORTING_PROJECT_KEY` - optional value. It is the project that the test run belongs to. The default value is `DEF`. You can manage projects in Zebrunner in the appropriate section;
- `REPORTING_RUN_DISPLAY_NAME` - optional value. It is the display name of the test run. The default value is `Default Suite`;
- `REPORTING_RUN_BUILD` - optional value. It is the build number that is associated with the test run. It can depict either the test build number or the application build number;
- `REPORTING_RUN_ENVIRONMENT` - optional value. It is the environment where the tests will run;
- `REPORTING_SEND_LOGS` - Sends test logs to Zebrunner. Default: `true`;
- `REPORTING_NOTIFICATION_NOTIFY_ON_EACH_FAILURE` - optional value. Specifies whether Zebrunner should send notification to Slack/Teams on each test failure. The notifications will be sent even if the suite is still running. The default value is `false`;
- `REPORTING_NOTIFICATION_SLACK_CHANNELS` - optional value. The list of comma-separated Slack channels to send notifications to. Notification will be sent only if Slack integration is properly configured in Zebrunner with valid credentials for the project the tests are reported to. Zebrunner can send two type of notifications: on each test failure (if appropriate property is enabled) and on suite finish;
- `REPORTING_NOTIFICATION_MS_TEAMS_CHANNELS` - optional value. The list of comma-separated Microsoft Teams channels to send notifications to. Notification will be sent only if Teams integration is configured in Zebrunner project with valid webhooks for the channels. Zebrunner can send two type of notifications: on each test failure (if appropriate property is enabled) and on suite finish;
- `REPORTING_NOTIFICATION_EMAILS` - optional value. The list of comma-separated emails to send notifications to. This type of notification does not require further configuration on Zebrunner side. Unlike other notification mechanisms, Zebrunner can send emails only on suite finish;
 - `REPORTING_RUN_TREAT_SKIPS_AS_FAILURES` - optional value. If value is false all test-runs with skipped & passed tests
 would be marked as passed.

Agent also recognizes `.env` file in the resources root folder.

### via YAML file

Agent recognizes agent.yaml or agent.yml file in the resources root folder. It is currently not possible to configure an alternative file location.

Below is a sample configuration file:

```yaml
reporting:
  enabled: true
  project-key: DEF
  send-logs: true
  server:
    hostname: localhost:8080
    access-token: <token>
  notification:
    notify-on-each-failure: true
    slack-channels: automation, dev-team
    ms-teams-channels: automation, qa-team
    emails: example@example.com
  run:
    treat_skips_as_failures: false
    display-name: Nightly Regression Suite
    build: 1.12.1.96-SNAPSHOT
    environment: TEST-1
```

- `reporting.enabled` - enables or disables reporting. The default value is `true`;
- `reporting.server.hostname` - mandatory if reporting is enabled. Zebrunner server hostname. Can be obtained in Zebrunner on the 'Account & profile' page under the 'Service URL' section;
- `reporting.server.access-token` - mandatory if reporting is enabled. Access token must be used to perform API calls. Can be obtained in Zebrunner on the 'Account & profile' page under the 'Token' section;
- `reporting.project-key` - optional value. The project that the test run belongs to. The default value is `DEF`. You can manage projects in Zebrunner in the appropriate section;
- `reporting.send-logs` - Sends test logs to Zebrunner. Default: `true`
- `reporting.run.display-name` - optional value. The display name of the test run. The default value is Default Suite;
- `reporting.run.build` - optional value. The build number that is associated with the test run. It can depict either the test build number or the application build number;
- `reporting.run.environment` - optional value. The environment in which the tests will run.
- `reporting.notification.notify-on-each-failure` - optional value. Specifies whether Zebrunner should send notification to Slack/Teams on each test failure. The notifications will be sent even if the suite is still running. The default value is `false`;
- `reporting.notification.slack-channels` - optional value. The list of comma-separated Slack channels to send notifications to. Notification will be sent only if Slack integration is properly configured in Zebrunner with valid credentials for the project the tests are reported to. Zebrunner can send two type of notifications: on each test failure (if appropriate property is enabled) and on suite finish;
- `reporting.notification.ms-teams-channels` - optional value. The list of comma-separated Microsoft Teams channels to send notifications to. Notification will be sent only if Teams integration is configured in Zebrunner project with valid webhooks for the channels. Zebrunner can send two type of notifications: on each test failure (if appropriate property is enabled) and on suite finish;
- `reporting.notification.emails` - optional value. The list of comma-separated emails to send notifications to. This type of notification does not require further configuration on Zebrunner side. Unlike other notification mechanisms, Zebrunner can send emails only on suite finish;
 - `reporting.run.treat-skips-as-failures` - optional value. If value is false all test-runs with skipped & passed tests
 would be marked as passed.

If the required configurations are not provided, there is a warning displayed in logs with the problem description and the names of options
which need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.

### Advanced configuration example

Sometimes there is need to change configuration from run to run. This can be done with changing environment variables
before each run.

```python
import os
from datetime import datetime
import random

import dotenv
import pytest


# Generate your run name here
def get_run_name():
    return f"Regression [{datetime.now()}] [Other helpull stuff]"

# Generate your build number here
def get_build_number():
    return f"{random.randint(1, 10)}.{random.randint(1, 10)}.{random.randint(1, 10)}"

def load_access_token():
    return dotenv.dotenv_values("secrets/secrets.txt")["REPORTING_SERVER_ACCESS_TOKEN"]


def run_tests():
    os.environ["REPORTING_RUN_DISPLAY_NAME"] = get_run_name()
    os.environ["REPORTING_RUN_BUILD"] = get_build_number()

    # If you store your secrets seperately you can load it here
    dotenv.load_dotenv("secrets/secrets.env")
    # or you can set directly
    os.environ["REPORTING_SERVER_ACCESS_TOKEN"] = load_access_token()

    # Here you can pass arguments to pytest
    pytest.main(["-n", "-2"])


if __name__ == "__main__":
    run_tests()
```

## Collecting test logs

For sending logs to zebrunner you need to add ZebrunnerHandler to yours logger.
Example:

```python
import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

logger = logging.getLogger(__name__) # It might any logger that you created earlier
logger.addHandler(ZebrunnerHandler())
```

## Collecting captured screenshot
Sometimes it may be useful to have the ability to track captured screenshots in scope of Zebrunner Reporting. The agent comes
with the API allowing you to send your screenshots to Zebrunner, so that they could be attached to the test.

```python
from pytest_zebrunner import attach_test_screenshot


def test_something():
    ...
    driver.save_screenshot("path_to_screenshot.png") # Capture screenshot with selenium driver
    attach_test_screenshot("path_to_screenshot.png")
    ...
```

## Additional reporting capabilities

**IMPORTANT**: All attachments to tests can only be done while some test is running.
All attachments to a test run can only be done while a pytest test session is active.

### Tracking test maintainer

You may want to add transparency to the process of automation maintenance by having an engineer responsible for
evolution of specific tests or test classes. Zebrunner comes with a concept of a maintainer - a person that can be
assigned to maintain tests. In order to keep track of those, the agent comes with the `@pytest.mark.maintainer` annotation.

See a sample test bellow:

```python
@pytest.mark.maintainer("username_of_maintainer")
def test_something():
    ...
```

### Attaching labels

In some cases, it may be useful to attach some meta information related to a test. The agent comes with a concept of a label.
Label is a key-value pair associated with a test. The key and value are represented by a `str`. Labels can be attached to
tests and test runs.

There is a repeatable label mark that can be used to attach labels to a test. There is also a API to attach labels during test or execution.
The agent has functions that can be used to attach labels.
```python
from pytest_zebrunner import attach_test_label, attach_test_run_label


@pytest.mark.label("name", "value")
def test_something():
    ...
    attach_test_label("test-label", "some value")
    attach_test_run_label("test-run-label", "value")
    ...
```
The test from the sample above attaches 3 test-level labels.

### Reverting test registration
In some cases it might be handy not to register test execution in Zebrunner. This may be caused by very special circumstances of test environment or execution conditions.


Zebrunner agent comes with a convenient method revert_registration() from CurrentTest class for reverting test registration at runtime. The following code snippet shows a case where test is not reported on Monday.
```python
from datetime import date

from pytest_zebrunner import CurrentTest


def test_something() -> None:
    ...
    if date.today().weekday() == 0:
        CurrentTest.revert_registration()
    ...
```

### Overriding run attributes
This section contains information on agent APIs allowing to manipulate test run attributes during runtime.

#### Setting build at runtime
All the configuration mechanisms listed above provide possibility to declaratively set test run build. But there might be cases when actual build becomes available only at runtime.

For such cases Zebrunner agent has a special method that can be used at any moment of the suite execution:
```python
# conftest.py

from pytest_zebrunner import CurrentTestRun


@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session: Session) -> None:
    CurrentTestRun.set_build("1.0.0")
```
In the above example, the `pytest_sessionstart` hook resolves and sets the test run build.

#### Setting locale
If you want to get full reporting experience and collect as much information in Zebrunner as its possible, you may want to report the test run locale.

For this, Zebrunner agent has a special method that can be used at any moment of the suite execution:
```python
# conftest.py

from pytest_zebrunner import CurrentTestRun


@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session: Session) -> None:
    CurrentTestRun.set_locale("<your-locale>")
```
In the above example, the `pytest_sessionstart` hook resolves and sets the test run locale.

#### Overriding platform
A test run in Zebrunner may have platform associated with the run. If there is at least one initiated `Remote` driver session within the test run, then its platform will be displayed as a platform of the whole test run. Even if subsequent `Remote` drivers are initiated on another platform, the very first one will be displayed as the run platform.

In some cases you may want to override the platform of the first `Remote` driver session. Another problem is that it is not possible to specify `API` as a platform.

Zebrunner provides two special methods to solve both of these problems: `CurrentTestRun.set_platform(name)` and `CurrentTestRun.set_platform_version(name, version)`.
In the example below, the hook sets the API as a platform associated with the current test run.

```python
# conftest.py

from pytest_zebrunner import CurrentTestRun


@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session: Session) -> None:
    CurrentTestRun.set_platform("API")
```

### Collecting additional artifacts
In case your tests or an entire test run produce some artifacts, it may be useful to track them in Zebrunner.
The agent comes with a few convenient methods for uploading artifacts in Zebrunner and linking them to the currently running test or test run.
Artifacts and artifact references can be attached using functions from `attachments` module. Together with an artifact
or artifact reference, you must provide the display name. For the file, this name must contain the file extension that
reflects the actual content of the file. If the file extension does not match the file content, this file will not be
saved in Zebrunner. Artifact reference can have an arbitrary name.

#### Attaching artifact to test
```python
from pytest_zebrunner import attach_test_artifact


def test_something():
    ...
    attach_test_artifact("path_to_artifact")
    ...
```

or with mark:

```python
@pytest.mark.artifact("path_to_artifact")
def test_something():
    ...
```

#### Attaching artifact reference to test

```python
from pytest_zebrunner import attach_test_artifact_reference


def test_something():
    ...
    attach_test_artifact_reference("name", "reference")
    ...
```

or with mark:

```python
@pytest.mark.artifact_reference("name", "reference")
def test_something():
    ...
```

#### Attaching artifact to test run

```python
from pytest_zebrunner import attach_test_run_artifact


attach_test_run_artifact("path_to_artifact")
```

#### Attaching artifact reference to test run

```python
from pytest_zebrunner import attach_test_run_artifact_reference


attach_test_run_artifact_reference("name", "reference")
```

Artifact uploading process is performed in the foreground now, so it will block the execution thread while sending.
The background uploading will be available in upcoming releases.

## Syncing test executions with external TCM systems

Zebrunner provides an ability to upload test results to external test case management systems (TCMs) on test run finish. For some TCMs it is possible to upload results in real-time during the test run execution.

This functionality is currently supported for TestRail, Xray, Zephyr Squad and Zephyr Scale.

### TestRail

For successful upload of test run results in TestRail, two steps must be performed:

1. Integration with TestRail is configured and enabled for Zebrunner project
2. Configuration is performed on the tests side


#### Configuration

Zebrunner agent has a special `TestRail` class with a bunch of methods to control results upload:

`#set_suite_id(str)`
:   Mandatory. The method sets TestRail suite id for current test run. This method must be invoked before all tests. Thus, it should be invoked from `pytest_sessionstart` hook.

`#set_case_id(str)` or `@pytest.mark.test_rail_case_id(str)`
:   Mandatory. Using these mechanisms you can set TestRail's case associated with specific automated test. It is highly recommended using the `@pytest.mark.test_rail_case_id` annotation instead of static method invocation. Use the static method only for special cases

`#disable_sync()`
:   Optional. Disables result upload. Same as `#set_suite_id(str)`, this method must be invoked before all tests

`#include_all_test_cases_in_new_run()`
:   Optional. Includes all cases from suite into newly created run in TestRail. Same as `#set_suite_id(str)`, this method must be invoked before all tests

`#enable_real_time_sync()`
:   Optional. Enables real-time results upload. In this mode, result of test execution will be uploaded immediately after test finish. This method also automatically invokes `#include_all_test_cases_in_new_run()`. Same as `#set_suite_id(str)`, this method must be invoked before all tests

`#set_run_id(str)`
:   Optional. Adds result into existing TestRail run. If not provided, test run is treated as new. Same as `#set_suite_id(str)`, this method must be invoked before all tests

`#set_run_name(str)`
:   Optional. Sets custom name for new TestRail run. By default, Zebrunner test run name is used. Same as `#set_suite_id(str)`, this method must be invoked before all tests

`#set_milestone(str)`
:   Optional. Adds result in TestRail milestone with the given name. Same as `#set_suite_id(str)`, this method must be invoked before all tests

`#set_assignee(str)`
:   Optional. Sets TestRail run assignee. Same as `#set_suite_id(str)`, this method must be invoked before all tests

By default, a new run containing only cases assigned to the tests will be created in TestRail on test run finish.

#### Example

In the example below, a new run with name "Best run ever" will be created in TestRail on test run finish. Suite id is `321` and assignee is "Deve Loper". Results of the `awesome_test1` will be uploaded as result of cases with id `10000`, `10001`, `10002`. Results of the `awesome_test2` will be uploaded as result of case with id `20000`.
```python
#conftest.py
from pytest_zebrunner.tcm import TestRail

@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session: Session) -> None:
    TestRail.set_suite_id("321");
    TestRail.set_run_name("Best run ever");
    TestRail.set_assignee("Deve Loper");

```
```python
# test_file.py
import pytest

from pytest_zebrunner.tcm import TestRail


@pytest.mark.test_rail_case_id("10000")
@pytest.mark.test_rail_case_id("10001", "10002")
def awesome_test1():
    ...


def awesome_test2():
    ...
    TestRail.set_case_id("20000")
    ...
```

### Xray

For successful upload of test run results in Xray two steps must be performed:

1. Xray integration is configured and enabled in Zebrunner project
2. Xray configuration is performed on the tests side

#### Configuration

Zebrunner agent has a special `Xray` class with a bunch of methods to control results upload:

`#set_execution_key(str)`
:   Mandatory. The method sets Xray execution key. This method must be invoked before all tests. Thus, it should be invoked from `pytest_sessionstart` hook.

`#set_test_key(str)` or `@pytest.mark.xray_test_key(str)`
:   Mandatory. Using these mechanisms you can set test keys associated with specific automated test. It is highly recommended using the `@pytest.mark.xray_test_key(str)` mark instead of static method invocation. Use the static method only for special cases

`#disable_sync()`
:   Optional. Disables result upload. Same as `#set_execution_key(str)`, this method must be invoked before all tests

`#enable_real_time_sync()`
:   Optional. Enables real-time results upload. In this mode, result of test execution will be uploaded immediately after test finish. Same as `#set_execution_key(str)`, this method must be invoked before all tests

By default, results will be uploaded to Xray on test run finish.

#### Example

In the example below, results will be uploaded to execution with key `ZBR-42`. Results of the `awesome_test1` will be uploaded as result of tests with key `ZBR-10000`, `ZBR-10001`, `ZBR-10002`. Results of the `awesome_test2` will be uploaded as result of test with key `ZBR-20000`.

```python
#conftest.py
from pytest_zebrunner.tcm import Xray

@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session: Session) -> None:
    Xray.set_execution_key("ZBR-42")

```
```python
# test_file.py
import pytest

from pytest_zebrunner.tcm import Xray


@pytest.mark.xray_test_key("ZBR-10000")
@pytest.mark.xray_test_key("ZBR-10001", "ZBR-10002")
def awesome_test1():
    ...


def awesome_test2():
    ...
    Xray.set_case_id("ZBR-20000")
    ...
```

### Zephyr

For successful upload of test run results in Zephyr two steps must be performed:

1. Zephyr integration is configured and enabled in Zebrunner project
2. Zephyr configuration is performed on the tests side

Described steps work for both Zephyr Squad and Zephyr Scale.

#### Configuration

Zebrunner agent has a special `Zephyr` class with a bunch of methods to control results upload:

`#set_test_cycle_key(str)`
:   Mandatory. The method sets Zephyr test cycle key. This method must be invoked before all tests. Thus, it should be invoked from `pytest_sessionstart` hook.

`#set_jira_project_key(str)`
:   Mandatory. Sets Zephyr Jira project key. Same as `#set_test_cycle_key(str)`, this method must be invoked before all tests

`#set_test_case_key(str)` or `@pytest.mark.zephyr_test_case_key(str)`
:   Mandatory. Using these mechanisms you can set test case keys associated with specific automated test. It is highly recommended using the `@pytest.mark.zephyr_test_case_key(str)` mark instead of static method invocation. Use the static method only for special cases

`#disable_sync()`
:   Optional. Disables result upload. Same as `#set_test_cycle_key(str)`, this method must be invoked before all tests

`#enable_real_time_sync()`
:   Optional. Enables real-time results upload. In this mode, result of test execution will be uploaded immediately after test finish. Same as `#set_test_cycle_key(str)`, this method must be invoked before all tests

By default, results will be uploaded to Zephyr on test run finish.

#### Example

In the example below, results will be uploaded to test cycle with key `ZBR-R42` from project with key `ZBR`. Results of the `awesome_test1` will be uploaded as result of tests with key `ZBR-T10000`, `ZBR-T10001`, `ZBR-T10002`. Results of the `awesome_test2` will be uploaded as result of test with key `ZBR-T20000`.

```python
#conftest.py
from pytest_zebrunner.tcm import Zephyr

@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session: Session) -> None:
    Zephyr.set_test_cycle_key("ZBR-R42");
    Zephyr.set_jira_project_key("ZBR");

```
```python
# test_file.py
import pytest

from pytest_zebrunner.tcm import Zephyr


@pytest.mark.zephyr_test_key("ZBR-T10000")
@pytest.mark.zephyr_test_key("ZBR-T10001", "ZBR-T10002")
def awesome_test1():
    ...


def awesome_test2():
    ...
    Zephyr.set_test_case_key("ZBR-T20000")
    ...
```

## Selenium WebDriver support

The Zebrunner test agent is capable of tracking tests along with remote Selenium WebDriver sessions.

### Capturing session artifacts

Zebrunner supports 3 types of test session artifacts:

- Video recording
- Session log
- VNC streaming

Test agent itself does not capture those artifacts since it has no control over underlying Selenium Grid implementation, however, it is possible to attach appropriate artifact references by providing specially designed set of driver session capabilities (**enabling capabilities**) - see the table below for more details. Only the `True` value is considered as trigger to save the link.

| Artifact        | Display name | Enabling capability | Default reference                                  | Reference overriding capability |
| --------------- | ------------ | ------------------- | -------------------------------------------------- | ------------------------------- |
| Video recording | Video        | enableVideo         | `artifacts/test-sessions/<session-id>/video.mp4`   | videoLink                       |
| Session log     | Log          | enableLog           | `artifacts/test-sessions/<session-id>/session.log` | logLink                         |
| VNC streaming   |              | enableVNC           | `<provider-integration-host>/ws/vnc/<session-id>`  | vncLink                         |

The **display name** is the name of the artifact that will be displayed on Zebrunner UI. This value is predefined and unfortunately can not be changed at the moment.

The **default reference** is a reference to a location, where artifact is **expected to reside** in S3-compatible storage once created by test environment - it is important that it stays in sync with test environment configuration. It is possible to override references if needed by providing **reference overriding capabilities**. Note, that special `<session-id>` placeholder is supported and can be used as part of the value of those capabilities allowing runtime session id (generated by WebDriver) to be included into actual reference value.

#### VNC streaming

VNC is an artifact of a special type. They don't have a name and are not displayed among other artifacts. They are displayed in the video section on Zebrunner UI during session execution and are dropped off on session close.

Default reference to the VNC streaming is based on `provider` capability. Value of this capability will be converted to preconfigured integration from **Test Environment Provider** group. The resolved integration must have a filled in URL property and be enabled in order to save the link to VNC streaming. The `<provider-integration-host>` placeholder of the default link will be replaced by the host of the obtained integration URL. Also, the `http` protocol in the VNC streaming url will be automatically replaced by `ws`, and `https` protocol will be replaced by `wss`. Currently, we only support Selenium, Zebrunner and MCloud integrations.

### Examples

The following code snippet shows the creation of `Remote` web driver with enabled VNC streaming, video recording and session log artifacts, but overrides the link to VNC streaming. The `<session-id>` placeholder of `vncLink` capability will be replaced by the actual session id.
```python
def init_driver() -> Remote:
    options = ChromeOptions();
    options.set_capability("enableVNC", "true");
    options.set_capability("vncLink", "wss://example.com/vnc/<session-id>");
    options.set_capability("enableVideo", "true");
    options.set_capability("enableLog", "true");

    return Remote(..., options=options, ...)

```

=== "Zebrunner Selenium Grid"
    ```python
    def test_something():
        hub_url = 'https://username:password@engine.zebrunner.com/wd/hub'
        capabilities = {
            'browserName': 'firefox',
            'enableVideo': True,
            'enableLog': True,
            'enableVNC': True,
            'provider': 'zebrunner',
            ...
        }
        driver = Remote(command_executor=hub_url, desired_capabilities=capabilities)
        ...
    ```

=== "BrowserStack"
    ```python title="BrowserStack"
    def test_something():
        hub_url = 'https://username:password@hub-cloud.browserstack.com/wd/hub'
        capabilities = {
            'browser': 'firefox',
            'provider': 'BROWSERSTACK',
            ...
        }
        driver = Remote(command_executor=hub_url, desired_capabilities=capabilities)
        ...
    ```

## Contribution

To check out the project and build from the source, do the following:
```
git clone git://github.com/zebrunner/python-agent-pytest.git
cd python-agent-pytest
```

## License

Zebrunner reporting agent for PyTest is released under version 2.0 of the [Apache License](https://www.apache.org/licenses/LICENSE-2.0).
