#!/usr/bin/env bash
# env_install.sh — set up a Python development environment (Python 3, pip, Jupyter)
# Works on macOS (Homebrew) and Debian/Ubuntu Linux (apt).
#
# Usage:
#   ./env_install.sh             install everything
#   ./env_install.sh --dry-run   only show what would be done
#   ./env_install.sh --verbose   print every command before running it
#   ./env_install.sh --quiet     only print warnings and errors
#   ./env_install.sh --uninstall remove Jupyter again

# Strict mode: stop on the first error (-e), treat unset variables as errors (-u),
# and make a pipeline fail if any command inside it fails (pipefail).
set -euo pipefail

LOG_FILE="${HOME}/env_install.log"
DRY_RUN=false
VERBOSE=false
QUIET=false
UNINSTALL=false

# ---------------------------------------------------------------- colours ---
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

# ---------------------------------------------------------------- helpers ---

# Feature 1: pretty printing. A blank line before and after makes each step
# easy to spot in a long output. printf is used because echo behaves
# differently across shells (-e, escape sequences...).
pretty_print() {
    local message="$1"
    local colour="${2:-$GREEN}"
    if [ "$QUIET" = false ] || [ "$colour" != "$GREEN" ]; then
        printf "\n${colour}%s${RESET}\n\n" "$message"
    fi
    log "$message"
}

warn()  { pretty_print "WARNING: $1" "$YELLOW"; }
error() { pretty_print "ERROR: $1" "$RED"; }

# Logging: every action goes to a file with a timestamp, so a failed
# installation can be debugged afterwards.
log() {
    printf "[%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "$LOG_FILE"
}

# Run a command, or only show it in dry-run mode. Records success or failure.
run() {
    if [ "$VERBOSE" = true ] || [ "$DRY_RUN" = true ]; then
        printf "  \$ %s\n" "$*"
    fi
    log "RUN: $*"
    if [ "$DRY_RUN" = true ]; then
        return 0
    fi
    if "$@"; then
        log "OK: $*"
    else
        log "FAILED: $*"
        error "Command failed: $*"
        return 1
    fi
}

# ------------------------------------------------------- argument parsing ---
for arg in "$@"; do
    case "$arg" in
        --dry-run)   DRY_RUN=true ;;
        --verbose)   VERBOSE=true ;;
        --quiet)     QUIET=true ;;
        --uninstall) UNINSTALL=true ;;
        -h|--help)
            sed -n '2,12p' "$0"
            exit 0 ;;
        *)
            error "Unknown option: $arg (use --help)"
            exit 1 ;;
    esac
done

# --------------------------------------------- Feature 2: OS detection ---
# $OSTYPE is set by bash itself: "darwin..." on macOS, "linux-gnu" on Linux.
detect_os() {
    case "$OSTYPE" in
        darwin*)    OS="macos" ;;
        linux-gnu*) OS="linux" ;;
        *)
            error "Unsupported operating system: $OSTYPE"
            exit 1 ;;
    esac
    pretty_print "Detected operating system: $OS"
}

# ------------------------------------------ Feature 3: Python 3 check ---
install_python() {
    if command -v python3 > /dev/null 2>&1; then
        pretty_print "Python is already installed: $(python3 --version)"
        return
    fi
    warn "python3 not found, installing it"
    if [ "$OS" = "macos" ]; then
        if ! command -v brew > /dev/null 2>&1; then
            error "Homebrew is required on macOS: https://brew.sh"
            exit 1
        fi
        run brew install python
    else
        run sudo apt-get update
        run sudo apt-get install -y python3 python3-pip python3-venv
    fi
    if [ "$DRY_RUN" = false ]; then
        pretty_print "Installed: $(python3 --version)"
    fi
}

# --------------------------------------------- Feature 4: pip check ---
check_pip() {
    if python3 -m pip --version > /dev/null 2>&1; then
        pretty_print "pip is available: $(python3 -m pip --version)"
    else
        warn "pip not found, installing it"
        if [ "$OS" = "linux" ]; then
            run sudo apt-get install -y python3-pip
        else
            run python3 -m ensurepip --upgrade
        fi
    fi
}

# ------------------------------------- Feature 5: Jupyter installation ---
install_jupyter() {
    if command -v jupyter > /dev/null 2>&1; then
        pretty_print "Jupyter is already installed: $(jupyter --version | head -n 1)"
        return
    fi
    pretty_print "Installing Jupyter Notebook"
    if [ "$OS" = "macos" ]; then
        run brew install jupyterlab
    else
        # --user avoids touching system packages; recent Debian/Ubuntu also need
        # --break-system-packages, so fall back to apt if pip refuses.
        run python3 -m pip install --user notebook || run sudo apt-get install -y jupyter-notebook
    fi
}

# ---------------------------------- Feature 6: macOS health check ---
macos_health_check() {
    if [ "$OS" = "macos" ]; then
        pretty_print "Running brew doctor (package manager health check)"
        run brew doctor || warn "brew doctor reported issues, read the output above"
    fi
}

uninstall() {
    pretty_print "Removing Jupyter" "$YELLOW"
    if [ "$OS" = "macos" ]; then
        run brew uninstall jupyterlab || warn "jupyterlab was not installed with brew"
    else
        run python3 -m pip uninstall -y notebook || warn "notebook was not installed with pip"
    fi
    pretty_print "Uninstall complete (Python itself is kept)"
}

# ------------------------------------------------------------ main logic ---
main() {
    log "=== env_install.sh started (dry-run=$DRY_RUN) ==="
    detect_os
    if [ "$UNINSTALL" = true ]; then
        uninstall
        exit 0
    fi
    install_python
    check_pip
    install_jupyter
    macos_health_check
    pretty_print "Environment ready. Log written to $LOG_FILE"
}

main
