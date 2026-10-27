# platform-lab

A small Flask to-do API, used as a learning project for Platform Engineering: rebuilding, layer by layer, a mini version of a production setup (OpenShift, Argo CD, Kafka, AWS, monitoring).

## Layer 1: Container and CI

**What I built**

- A Dockerfile for the API, built and run locally with Podman. Dependencies are installed before the app code is copied, so code changes reuse the cached `pip install` layer. The container runs as a non-root user (UID 1001).
- A GitHub Actions workflow (`.github/workflows/ci.yml`) that runs `pytest` on every pull request to `main` and on every push to `main`.
- A ruleset on `main`: no direct pushes, changes go through a PR, and the `test` check must pass before merging. Tested with a PR that broke a test on purpose: the merge was blocked.
- On push to `main` only, the workflow builds the image for `linux/amd64` and `linux/arm64` and pushes it to GHCR as `ghcr.io/tunwan/todo-api`, tagged `latest` and with the commit SHA. The package is public, so it can be pulled without credentials.

**What broke and how I fixed it**

- `ModuleNotFoundError: No module named 'app'` in CI. Plain `pytest` adds the test file's folder (`tests/`) to `sys.path`, not the repo root; it only worked locally with `python -m pytest`. Fixed with `pytest.ini` (`pythonpath = .`), so plain `pytest` works everywhere.
- The ruleset was created with enforcement set to `disabled`, so `main` was not actually protected. Caught by checking the ruleset before the test PR; switched it to `Active`.
- The workflow YAML would not parse because of misaligned indentation in the `build` job. Checked locally with `ruby -ryaml -e 'YAML.load_file(".github/workflows/ci.yml")'`.
- Node.js 20 deprecation warning from `actions/checkout@v4` and `actions/setup-python@v5`. Bumped both to `@v7`.

## Run locally

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
python -m app.main   # http://localhost:8080/health
```

Or from the published image:

```sh
podman run -p 8080:8080 ghcr.io/tunwan/todo-api:latest
```
