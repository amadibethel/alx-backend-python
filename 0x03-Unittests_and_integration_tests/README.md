## Python Testing Project
This project demonstrates unit testing and integration testing in Python using the `unittest` framework, `unittest.mock`, and `parameterized`.
We test different components of a mock GitHub client (`GithubOrgClient`) and utility functions with mocks, fixtures, and parametrized tests.

### Objectives

**Apply common testing patterns such as:**

- Mocking

- Parametrization

- Fixtures

**Write Python tests that:**

- Cover standard inputs and corner cases.

- Avoid real HTTP or database calls by using mocks.

- Validate end-to-end behavior with integration tests.

## Project Structure

```
├── client.py        # Contains GithubOrgClient implementation
├── utils.py         # Utility functions (e.g., memoization, get_json)
├── fixtures.py      # Test fixtures with sample payloads
├── test_utils.py    # Unit tests for utils.py
├── test_client.py   # Unit tests for client.py
├── test_integration.py # Integration tests for GithubOrgClient
└── README.md        # This documentation
```

Types of Tests
**Unit Tests**

- Validate individual functions or methods in isolation.

- Example:

    - `utils.get_json`: Mock requests.get so no actual HTTP call is made.
    - `utils.memoize`: Ensure repeated calls return cached values.
    - `GithubOrgClient.has_license`: Confirm license filtering logic.

- Goal: Verify the function works if everything else works.

### Integration Tests

- Validate a workflow end-to-end.

- Example:

    - `GithubOrgClient.public_repos`: Ensures repository fetching and filtering works correctly.

    - Uses fixtures (`org_payload`, `repos_payload`) instead of real API calls.

- Only external requests (requests.get) are mocked.

- Goal: Verify that all pieces of the system interact correctly.

### Requirements
- All files must be:
- Follow pycodestyle 2.5
  - Executable
  - End with a new line
  - Properly documented with full sentences
  - Type-annotated

### Resources

- unittest: [Unit testing framework](https://docs.python.org/3/library/unittest.html)

- unittest.moc: [Mock object library](https://docs.python.org/3/library/unittest.mock.html)

- parameterized:[parameterized](https://github.com/wolever/parameterized) and [parameterized Doc](https://pypi.org/project/parameterized/)

- Memoization in Python:[Memoization ](https://en.wikipedia.org/wiki/Memoization)

## Running Tests

Run any test file with
```
$ python3 -m unittest path/to/test_file.py
```
Example:
```
$ python3 -m unittest test_utils.py
$ python3 -m unittest test_client.py
```
To run all tests at once:
```
$ python3 -m unittest discover
```
### Key Idea:

- Unit tests check correctness of small isolated parts.

- Integration tests check correctness of the whole system working together.