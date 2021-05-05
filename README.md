# Zebrunner PyTest agent


The official Zebrunner PyTest agent provides the reporting functionality. It can automatically track Selenium sessions
and send the info about session details to Zebrunner backend. It can be easily integrated into a project by just installing the library
and adding the configuration file.

Including reporting into your project is easy - just install the agent and provide minimal valid configuration for reporting.


## Installation

    pip install pytest-zebrunner

## Configuration
After the installation, reporting is disabled by default. It won't send any data to the Zebrunner service without a valid configuration.
To configure the app, you need to specify environment variables. It can also be done by specifying variables in the `.env` file in the root path of your project.
You can configure the agent **only** with environment variables. Other formats like `yaml`, `ini` and program arguments will be added in future.

<!-- groups:start -->
### Environment variables
```dosini
REPORTING_SERVICE_URL=<zebrunner url>
ACCESS_TOKEN=<access_token>
ZEBRUNNER_PROJECT=ProjectName
ZEBRUNNER_ENABLED=true
TEST_RUN_NAME=Testing new features
BUILD=1.25.16
ENV=stage
SEND_LOGS=true
```

- `SERVICE_URL` - [required] It is the Zebrunner server hostname. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Service URL' section;

- `ACCESS_TOKEN` - [required] Access token must be used to perform API calls. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Token' section;

- `ZEBRUNNER_PROJECT` - [required] It is the project that the test run belongs to. The default value is `UNKNOWN`. You can manage projects in Zebrunner in the appropriate section;

- `REPORTING_ENABLED` - You can disable the agent if it has side effects on you project or doesn't work. *Default*: `true`

- `TEST_RUN_NAME` - It is the display name of the test run. *Default*: `Unnamed-%time`

- `BUILD` -  It is the build number that is associated with the test run. It can depict either the test build number or the application build number;

- `ENV` - It is the environment where the tests will run.

- `SEND_LOGS` - Sends test logs to Zebrunner. *Default*: `false`
<!-- groups:end -->

If the required configurations are not provided, there is a warning displayed in logs with the problem description and the names of options
which need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.

## Collecting logs
It is also possible to enable the log collection for your tests. All you have to do to enable logging is to enable it in the configuration.
The agent connects to pythons root logger and collects the logs from there. In future, more options are expected to be available for configuring logs sending.


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
