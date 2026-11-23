# Exercise 1 (slide 18): configure a development environment with Bash

**Statement:** [courses.dallard.tech/linux/bash_exo](https://courses.dallard.tech/linux/bash_exo/)
**Deliverable:** [`env_install.sh`](env_install.sh)

```bash
chmod +x env_install.sh     # make it executable
./env_install.sh --dry-run  # see what it would do
./env_install.sh            # really install
```

## Part 1: shell setup (done by hand)

| Step | Command |
| --- | --- |
| Which shell is running | `ps -p $$` (current shell), `echo "$SHELL"` (login shell) |
| Shell framework | Oh My Zsh (macOS) or Oh My Bash (Linux), theme set in `~/.zshrc` / `~/.bashrc` |
| Git plugin | `plugins=(git)` in the config file, then `source ~/.zshrc` |
| Check | `gst` behaves like `git status` |

**What is the purpose of `source`?** It runs a file's commands *inside the current shell* instead of in a new one. After editing `~/.zshrc`, `source ~/.zshrc` applies the changes to the terminal you're in, without opening a new one.

## Part 2: Python check

`python3 --version`. Always call `python3` explicitly: some systems still have Python 2 behind `python`.

## Part 3: the script

| Feature | Where in the script |
| --- | --- |
| Shebang + executable | `#!/usr/bin/env bash`, `chmod +x` |
| 1. Pretty printing with `printf` | `pretty_print()` |
| 2. OS detection with `$OSTYPE` | `detect_os()` |
| 3. Install python3 if missing, else show the version | `install_python()` |
| 4. pip version | `check_pip()` |
| 5. Jupyter installation (different per OS) | `install_jupyter()` |
| 6. `brew doctor` on macOS | `macos_health_check()` |

### Bonus challenges

| Bonus | How |
| --- | --- |
| Colours | ANSI codes: green = success, yellow = warning, red = error |
| Logging | every action written with a timestamp to `~/env_install.log` |
| Strict mode | `set -euo pipefail` |
| Command-line arguments | `--dry-run`, `--verbose`, `--quiet`, `--help` |
| Uninstall option | `--uninstall` removes Jupyter |

## Verification checklist

- [x] Shell prompt shows the framework theme
- [x] `gst` works like `git status`
- [x] `python3 --version` returns 3.x
- [x] `python3 -m pip --version` works
- [x] `jupyter notebook` launches
- [x] macOS: `brew doctor` reports no serious issue
