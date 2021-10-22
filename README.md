# Zebrunner PyTest agent


The official Zebrunner PyTest agent provides the reporting functionality. It can automatically track Selenium sessions
and send the info about session details to Zebrunner backend. It can be easily integrated into a project by just installing the library
and adding the configuration file.

Including reporting into your project is easy - just install the agent and provide minimal valid configuration for reporting.


## Installation

    pip install pytest-zebrunner


## Configuration
After the installation, reporting is disabled by default. It won't send any data to the Zebrunner service without a valid configuration.

It is currently possible to provide the configuration via:
1. Environment variables
2. YAML file

`pyproject.toml`, `command arguments` are in plans for future releases.



<!-- groups:start -->
### Environment variables
The following configuration parameters are recognized by the agent:

- `REPORTING_ENABLED` - enables or disables reporting. The default value is `true`.
- `REPORTING_SERVER_HOSTNAME` - mandatory if reporting is enabled. It is Zebrunner server hostname. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Service URL' section;
- `REPORTING_SERVER_ACCESS_TOKEN` - mandatory if reporting is enabled. Access token must be used to perform API calls. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Token' section;
- `REPORTING_PROJECT_KEY` - optional value. It is the project that the test run belongs to. The default value is `DEF`. You can manage projects in Zebrunner in the appropriate section;
- `REPORTING_RUN_DISPLAY_NAME` - optional value. It is the display name of the test run. The default value is `Default Suite`;
- `REPORTING_RUN_BUILD` - optional value. It is the build number that is associated with the test run. It can depict either the test build number or the application build number;
- `REPORTING_RUN_ENVIRONMENT` - optional value. It is the environment where the tests will run;
- `REPORTING_SEND_LOGS` - Sends test logs to Zebrunner. Default: `true`;

Agent also recognizes `.env` file in the resources root folder.
<!-- groups:end -->

<!-- groups:start -->
### Yaml file
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
  run:
    display-name: Nightly Regression Suite
    build: 1.12.1.96-SNAPSHOT
    environment: TEST-1
```
<!-- groups:end -->

- `reporting.enabled` - enables or disables reporting. The default value is `true`;
- `reporting.server.hostname` - mandatory if reporting is enabled. Zebrunner server hostname. Can be obtained in Zebrunner on the 'Account & profile' page under the 'Service URL' section;
- `reporting.server.access-token` - mandatory if reporting is enabled. Access token must be used to perform API calls. Can be obtained in Zebrunner on the 'Account & profile' page under the 'Token' section;
- `reporting.project-key` - optional value. The project that the test run belongs to. The default value is `DEF`. You can manage projects in Zebrunner in the appropriate section;
- `reporting.send-logs` - Sends test logs to Zebrunner. Default: `true`
- `reporting.run.display-name` - optional value. The display name of the test run. The default value is Default Suite;
- `reporting.run.build` - optional value. The build number that is associated with the test run. It can depict either the test build number or the application build number;
- `reporting.run.environment` - optional value. The environment in which the tests will run.

If the required configurations are not provided, there is a warning displayed in logs with the problem description and the names of options
which need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.

## Collecting logs
For sending logs to zebrunner you need to add ZebrunnerHandler to yours logger.
Example:
```python
import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

logger = logging.getLogger(__name__)
logger.addHandler(ZebrunnerHandler())
```

To send all logs to zebrunner you can add `ZebrunnerHandler` to root logger.
```python
import logging

from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

logging.root.addHandler(ZebrunnerHandler())
```


## Additional functionality

**IMPORTANT**: All attachments to tests can only be done while some test is running.
All attachments to a test run can only be done while a pytest test session is active.
---------------------------

### Collecting captured screenshot
Sometimes it may be useful to have the ability to track captured screenshots in scope of Zebrunner Reporting. The agent comes
with the API allowing you to send your screenshots to Zebrunner, so that they could be attached to the test.

```python
from pytest_zebrunner import attach_test_screenshot


def test_something():
    ...
    driver.save_screenshot("path_to_screenshot.png) # Capture screenshot with selenium driver
    attach_test_screenshot("path_to_screenshot.png")
    ...
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

### Attaching artifact reference to test
```python
from pytest_zebrunner import attach_test_artifact_reference


def test_something():
    ...
    attach_test_artifact_reference("name", "reference")
    ...
```

### Attaching artifact to test run
```python
from pytest_zebrunner import attach_test_run_artifact


attach_test_run_artifact("path_to_artifact")
```

### Attaching artifact reference to test run
```python
from pytest_zebrunner import attach_test_run_artifact_reference


attach_test_run_artifact_reference("name", "reference")
```

Artifact uploading process is performed in the foreground now, so it will block the execution thread while sending.
The background uploading will be available in upcoming releases.


### Attaching test labels
In some cases, it may be useful to attach some meta information related to a test. The agent comes with a concept of a label.
Label is a key-value pair associated with a test. The key and value are represented by a `str`. Labels can be attached to
tests and test runs.

```python
@pytest.mark.label("name", "value")
def test_something():
    ...
```
or
```python
from pytest_zebrunner import attach_test_label


def test_something():
    ...
    attach_test_label("name", "value")
    ...
```
**Note:** These two methods can be combined.

For test run:
```python
from pytest_zebrunner import attach_test_run_label

attach_test_run_label("name", "value")
```


### Tracking of test maintainer
You may want to add transparency to the process of automation maintenance by having an engineer responsible for
evolution of specific tests or test classes. Zebrunner comes with a concept of a maintainer - a person that can be
assigned to maintain tests. In order to keep track of those, the agent comes with the `@pytest.mark.maintainer` annotation.

See a sample test bellow:

```python
@pytest.mark.maintainer("username_of_maintainer")
def test_something():
    ...
```

### Tracking web driver sessions
The Zebrunner test agent has a great ability to track tests along with remote driver sessions. You don't have to do anything.
The agent automatically injects the tracking functionality to the Selenium driver if the Selenium library is installed. The agent sends
driver capabilities to Zebrunner when the driver starts and the finish time when the driver stops.

Zebrunner can automatically collect your test artifacts like videos or selenium session logs if you are using
test running providers like ZebrunnerHub, BrowserStack, Lambdatest, etc. To enable this you need to enable integration in your project in Zebrunner
and also specify the `provider` capability.

#### Zebrunner
Example:
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

### BrowserStack
BrowserStack saves video and logs by default so you need just to specify capability.
Example:
```python
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
