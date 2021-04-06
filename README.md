# Zebrunner PyTest agent


The official Zebrunner Pytest agent provides reporting functionality. It can automatically track selenium sessions
and send info about session details to Zebrunner backend. It can be ease integrated in project just by installing library
and adding configuration file.

To include reporting into your project is pretty easy - just install agent and provide minimal valid configuration for reporting.


## Installation

    pip install pytest-zebrunner

## Configuration
After installation reporting is disabled by default. It won't send data to zebrunner service without valid configuration.
To configure app you need to specify environment variables. It also can be done by specifying variables in `.env` file in root path of your project.
You can configure agent **only** with environment variables. Another formats would be added in future.
Planed formats are `yaml`, `ini` and program arguments.

<!-- groups:start -->
### Environment variables
```dosini
SERVICE_URL=<zebrunner url>
ACCESS_TOKEN=<access_token>
ZEBRUNNER_PROJECT=ProjectName
ZEBRUNNER_ENABLED=true
TEST_RUN_NAME=Testing new features
BUILD=1.25.16
ENV=stage
SEND_LOGS=true
```

- `SERVICE_URL` - [required] It is Zebrunner server hostname. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Service URL' section;

- `ACCESS_TOKEN` - [required] Access token must be used to perform API calls. It can be obtained in Zebrunner on the 'Account & profile' page under the 'Token' section;

- `ZEBRUNNER_PROJECT` - [required] It is the project that the test run belongs to. The default value is `UNKNOWN`. You can manage projects in Zebrunner in the appropriate section;

- `REPORTING_ENABLED` - You can disable agent if it makes side effects in you project or doesn't work. *Default*: `true`

- `TEST_RUN_NAME` - It is the display name of the test run. *Default*: `Unnamed-%time`

- `BUILD` -  It is the build number that is associated with the test run. It can depict either the test build number or the application build number;

- `ENV` - It is the environment where the tests will run.

- `SEND_LOGS` - Send test logs to zebrunner. *Default*: `false`
<!-- groups:end -->

If required configurations not provided there is a warning in logs with problem description and names of options,
which need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.

## Collecting logs
It is also possible to enable the log collection for your tests.  All you have to do to enable logging is to enable it in configuration.
Agent connects to pythons root logger and collect logs from there. Possible, in future would be more options to configure logs sending.


## Additional functionality

**IMPORTANT**: All attachments to tests can be done only while some test is running.
All attachments to test-run can be done only while pytest test-session is active.
---------------------------

### Collecting captured screenshot
Sometimes it may be useful to have an ability to track captured screenshots in scope of zebrunner reporting. The agent comes
with API allowing you to send your screenshots to Zebrunner, so they will be attached to the test.

```python
from pytest_zebrunner.attachments import attach_test_screenshot


def test_something():
    ...
    driver.save_screenshot("path_to_screenshot.png) # Capture screenshot with selenium driver
    attach_test_screenshot("path_to_screenshot.png")
    ...
```

### Collecting additional artifacts
In case your tests or entire test run produce some artifacts, it may be useful to track them in Zebrunner.
The agent comes with a few convenient methods for uploading artifacts in Zebrunner and linking them to the currently running test or the test run.
Artifacts and artifact-references can be attached using functions from `attachments` module. Together with an artifact
or artifact reference, you must provide the display name. For the file, this name must contain the file extension that
reflects the actual content of the file. If the file extension does not match the file content, this file will not be
saved in Zebrunner. Artifact reference can have an arbitrary name.

#### Attach artifact to test
```python
from pytest_zebrunner.attachments import attach_test_artifact


def test_something():
    ...
    attach_test_artifact("path_to_artifact")
    ...
```

### Attach artifact-reference to test
```python
from pytest_zebrunner.attachments import attach_test_artifact_reference


def test_something():
    ...
    attach_test_artifact_reference("name", "reference")
    ...
```

### Attach artifact to test-run
```python
from pytest_zebrunner.attachments import attach_test_run_artifact


attach_test_run_artifact("path_to_artifact")
```

### Attach artifact-reference to test-run
```python
from pytest_zebrunner.attachments import attach_test_run_artifact_reference


attach_test_run_artifact_reference("name", "reference")
```

Artifact upload process is performed in the foreground now, sow it will block execution thread while sending.
In future release background uploading would be realized.


### Attaching test labels
In some cases, it may be useful to attach some meta information related to a test. The agent comes with a concept of a label.
Label is a key-value pair associated with a test. The key and value are represented by a `str`. Labels can be attached to
tests and test-runs.

```python
@pytest.mark.label("name", "value")
def test_something():
    ...
```
or
```python
from pytest_zebrunner.attachments import attach_test_label


def test_something():
    ...
    attach_test_label("name", "value")
    ...
```
**Note:** These two methods can be combined.

For test-run:
```python
from pytest_zebrunner.attachments import attach_test_run_label

attach_test_run_label("name", "value")
```


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

### Tracking of web driver sessions
The Zebrunner test agent has a great ability to track tests along with remote driver sessions. You have nothing to do :)
The agent automatically injects tracking functionality to selenium driver if selenium library is installed. Agent sends
driver capabilities to zebrunner when the driver starts and finish time when the driver stops.
