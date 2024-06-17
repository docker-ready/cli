# Docker Ready CLI

Docker Ready CLI is a tool for lazy DevOps(and other) engineers.

This tool is definitely for you if:

- you don't like to write configs from scratch;
- you don't have time to review the deployment project documentation;
- you need a ready-to-use project;
- you are lazy and just want everything to work after one command.

## Installation

```shell
$ pipx install docker-ready-cli
```

## Documentation

### Run command

```
$ docker-ready run PROJECT_NAME
```

### Show command

Show all available projects:

```shell
$ docker-ready show
```

Show information about the project by name:

```shell
$ docker-ready show PROJECT_NAME
```

### Ps command

A list of running projects with brief information about their containers.

```shell
$ docker-ready ps
```

A list of running containers for a specific project with detailed information.

```shell
$ docker-ready ps PROJECT_NAME
```
