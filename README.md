# pytest_zebrunner


The official Zebrunner Pytest agent provides reporting functionality. It can automatically track selenium sessions
and send info about session details to Zebrunner backend. It can be ease integrated in project just by installing library
and adding configuration file.

## Installation
---------------

    pip install pytest_zebrunner

## Configuration
----------------
Library don't ready for usage just after installation. It won't send data to
zebrunner service without additional configuration. To configure app you need to
specify environment variables. It can be done by specifying variables in `.env`
file.

```dosini
SERVICE_URL=<zebrunner url>
ACCESS_TOKEN=<access_token>
ZEBRUNNER_PROJECT=ProjectName
ZEBRUNNER_ENABLED=true
BUILD=1.25.16
ENV=stage
```

You can configure agent only with environment variables. Another formats would
be added in future. Planed formats are `yaml`, `ini` and program arguments.

### Configuration description
`SERVICE_URL` - [required] Base URL of Zebrunner service.
Example: `https://pytesttest.qaprosoft.farm`

`ACCESS_TOKEN` - [required] Authorization token. You can find it in Account & profile section.

`ZEBRUNNER_PROJECT` - [required] Name of project.

`ZEBRUNNER_ENABLED` - You can disable agent if it makes side effects in you project or doesn't work.

`BUILD` - Version of product on which tests are running.

`ENV` - Testing environment name.

If required configurations not provided there is a warning in logs with problem description and names of options,
which need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.

## Additional functionality
---------------------------
