# Object-Oriented Programming & Design Patterns in Python

Exercises for the **OOP & design patterns** course (CentraleSupélec, Bachelor AIDAMS 2A, Benjamin Dallard).

| Slide | Exercise | Contents | Tests |
| --- | --- | --- | --- |
| 18 | [Bash script](01-bash-script/) | `env_install.sh`: installs Python, pip and Jupyter on macOS / Linux, with colours, logging, strict mode, `--dry-run` and `--uninstall` | — |
| 26 | [Git workflow](02-git-workflow/) | commands and answers for the 11 parts + reflection questions, `install.sh`, `bash-installer/` | — |
| 67 | [OOP problems](03-oop-problems/) | operator overloading (6 problems) and inheritance (3 problems) | 28 ✅ |
| 68 | [UML practice](04-uml/) | Hospital (3 tasks) and ABCD Records (3 levels): class, use case and sequence diagrams | — |
| 84 | [Design patterns](05-design-patterns/) | Factory Method, Builder, Singleton, Adapter, Decorator, Strategy, Template Method | 56 ✅ |
| 93 | [Testing & mocking](06-testing-mocking/) | unit / integration tests, fixtures, mocking an LLM API, markers, coverage 100% | 33 ✅ |

## Run all the tests

```bash
pip install pytest pytest-mock pytest-cov groq
(cd 03-oop-problems && pytest)
(cd 05-design-patterns && pytest)
(cd 06-testing-mocking && pytest)
```

Each folder has its own README explaining the exercise, the choices made and what to remember for the exam. UML diagrams are written in [Mermaid](https://mermaid.js.org/), so GitHub draws them directly.
