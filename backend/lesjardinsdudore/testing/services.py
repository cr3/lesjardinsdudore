"""Service fixtures."""

import sys
from functools import partial
from pathlib import Path

import pytest

from lesjardinsdudore.http import HTTPSession
from lesjardinsdudore.testing.compose import ComposeServer


@pytest.fixture(scope="session")
def project():
    return "test"


@pytest.fixture(scope="session")
def env_vars(project):
    """Environment variables for the services."""
    v = sys.version_info
    python_version = f"{v.major}.{v.minor}.{v.micro}"

    return {
        "COMPOSE_PROJECT_NAME": project,
        "NC_PASSWORD": "test",
        "PYTHON_VERSION": python_version,
    }


@pytest.fixture(scope="session")
def env_file(env_vars, request):
    """Environment file containing `env_vars`.

    Cached for troubleshooting purposes.
    """
    env_file = request.config.cache.makedir("compose") / "env"
    with env_file.open("w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

    return env_file


@pytest.fixture(scope="session")
def compose_files(request):
    directory = Path(request.config.rootdir)
    filenames = ["docker-compose.yml", "compose.yaml", "compose.yml"]
    while True:
        for filename in filenames:
            path = directory / filename
            if path.exists():
                all_files = directory.glob(f"{path.stem}.*")
                ordered_files = sorted(all_files, key=lambda p: len(p.name))
                return list(ordered_files)

        if directory == directory.parent:
            raise FileNotFoundError("Docker compose file not found")

        directory = directory.parent


@pytest.fixture(scope="session")
def compose_server(project, env_file, compose_files, process):
    return partial(
        ComposeServer,
        project=project,
        env_file=env_file,
        compose_files=compose_files,
        process=process,
    )


@pytest.fixture(scope="session")
def api_service(compose_server):
    """API service fixture."""
    server = compose_server("Application startup complete")
    with server.run("api") as service:
        yield service


@pytest.fixture(scope="session")
def api_session(api_service):
    """API HTTP session to the service fixture."""
    return HTTPSession(f"http://{api_service.ip}/")
