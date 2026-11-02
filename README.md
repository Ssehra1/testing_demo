# GitHub Actions testing demo (no server required)

This teaching example includes a small item service, a SQLite repository, and an injectable notifier.

- `Tests/test_integration.py` integrates `ItemService` with a real SQLite database held in memory; an external notification dependency is mocked.
- `Tests/test_doubles.py` demonstrates dummy, stub, fake, spy, and mock test doubles. These are isolated unit tests, not database integration tests.
- `.github/workflows/tests.yml` runs both suites on pushes and pull requests.

## Run locally

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m pytest -v Tests/test_integration.py
python -m pytest -v Tests/test_doubles.py
```

## Push to GitHub

Copy all the files and folders (including `.github`) into your GitHub repository and commit them. The Actions tab will show the `Automated Testing Demo` workflow.

## Why this fixes the missing `client` fixture

The original test required a Flask-specific pytest fixture (`client`) that had never been declared. This demo calls Python classes directly and creates the SQLite database within each test. Therefore no pytest application fixture, external server, or Docker configuration is needed.

## Concepts

- Integration test: real service + real SQLite repository, verify SQL persistence.
- Mock: verifies that `item_created(...)` was called correctly.
- Fake: a small in-memory repository with functional behavior.
- Stub: returns a canned item.
- Spy: records calls into a list.
- Dummy: placeholder dependency that isn't used in the tested path.
