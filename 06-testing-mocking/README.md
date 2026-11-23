# Exercise 6 (slide 93): testing and mocking with pytest

**Statement:** [courses.dallard.tech/ci_cd/testing_python_intro](https://courses.dallard.tech/ci_cd/testing_python_intro/)
**Result:** 33 tests pass, 1 is skipped on purpose (it needs a real API key), **coverage 100%**.

```bash
cd 06-testing-mocking
pip install -r requirements.txt
pytest                                        # run everything
pytest --cov=src --cov-report=term-missing    # + coverage report
pytest -m "not slow"                          # skip the tests marked slow
pytest -m slow                                # only the slow tests
pytest --markers                              # list the available markers
```

> The course page writes `pytest --markers=slow` to run only slow tests. `--markers` only **lists** the markers; `-m slow` is what **runs** the marked tests.

## Project structure (the "solid project structure" from the course)

```
06-testing-mocking/
├── src/
│   ├── app.py                  # e-commerce example: 3 functions + 2 classes
│   └── groq_chat.py            # a function calling an LLM API
├── tests/
│   ├── conftest.py             # shared fixtures: repo, order_service, fake_groq_client
│   ├── test_unit_app.py        # unit tests
│   ├── test_integration_app.py # integration tests
│   └── test_groq_chat.py       # mocking tests
├── pyproject.toml              # pytest settings + the "slow" marker
└── requirements.txt
```

## The test pyramid

| Level | Tests what | Speed | Amount | Here |
| --- | --- | --- | --- | --- |
| **Unit** | one function or class, alone | very fast | the most | `calculate_discount`, `calculate_tax`, `calculate_total`, `ProductRepository` |
| **Integration** | several parts working together | slower | fewer | `OrderService` + `ProductRepository` + the calculations |
| **End-to-end** | the whole app like a real user | slowest | the fewest | not in pytest: Playwright or Selenium |

## Concepts used

| Concept | Where | In one line |
| --- | --- | --- |
| `assert` | every test | the check: if false, the test fails and pytest shows both values |
| `pytest.raises` | `test_unit_negative_price_raises_error` | checks that the code raises the right error |
| `@pytest.mark.parametrize` | `test_unit_out_of_range_discounts_rejected` | runs the same test once per value |
| **Fixture** | `conftest.py` | a function that prepares test data; a test asks for it by naming it as a parameter |
| **AAA** (Arrange, Act, Assert) | `test_unit_custom_tax_rate_total` | every test has 3 clear parts |
| **Mock** | `fake_groq_client` | a fake object replacing the real API client |
| `return_value` | `conftest.py` | what the fake method returns |
| `side_effect` | `test_ask_groq_raises_error_when_api_fails` | makes the fake raise an error, to **simulate a failure** |
| `assert_called_once_with` | `test_ask_groq_calls_api_correctly` | checks **our code sent the right request** |
| `mocker.patch` | `test_default_client_is_created_when_none_given` | replaces the `Groq` class itself during one test |
| **Marker** | `@pytest.mark.slow` | labels a test so it can be selected or skipped with `-m` |
| **Coverage** | `pytest --cov=src` | which lines the tests execute (100% here) |

## Why mock the LLM API?

Calling the real Groq API in tests would need an API key (which must never be in a public repo), an internet connection and tokens (money). It would also be slow, fail whenever the API is down, and return a different answer every time. With a mock, the test is instant, free and predictable.

**What we test:** that **our code sends the right request** and handles the answer and the failures. Whether the LLM gives a good answer is the API provider's job, not ours.
