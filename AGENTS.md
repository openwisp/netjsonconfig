# AGENTS.md

## Project Overview

`netjsonconfig` is the Python library used by OpenWISP to generate, validate, and parse network configuration data, especially NetJSON and OpenWrt configuration.

Core code lives in `netjsonconfig/`:

- `backends/` implements backend-specific configuration generation and parsing.
- `schema.py`, `channels.py`, `countries.py`, `exceptions.py`, and `utils.py` provide validation and shared helpers.
- Tests live in `tests/`.

## Source of Truth

- Use `README.rst` and `docs/` for setup, package usage, and baseline test commands.
- Use `.github/workflows/ci.yml` for CI-tested dependencies, QA/test commands, env vars, and supported Python versions.
- Use GitHub issue/PR templates when asked to open issues or PRs.

Follow the DRY principle: do not duplicate information or code across files.

If instructions conflict, repository config and CI workflows win first, docs next, and this file is supplemental.

## Development Notes

- Keep changes focused. Avoid unrelated refactors and formatting churn.
- Preserve public APIs, schema validation, backend output formats, and generated configuration compatibility unless explicitly required.
- Place imports at the top of the file. Only defer imports when necessary (e.g., Django model imports inside functions or methods where the app registry is not yet ready).
- Avoid unnecessary blank lines inside function and method bodies.
- Update docs when behavior, settings, public APIs, setup steps, or supported versions change.

## Testing and QA

- Add or update tests for every behavior change.
- For bug fixes, write the regression test first, run it against the unfixed code, confirm it fails for the expected reason, then implement the fix.
- Use targeted tests while iterating, then run the documented full test command before considering the change complete.
- Run `openwisp-qa-format` after editing when available.
- Run `./run-qa-checks` when present. Treat failures as blocking unless confirmed unrelated and reported.
- Prefer in-process tests so coverage tools can measure changed code.

## Security Notes

- Watch for invalid configuration output, unsafe paths, unsafe command strings, malformed network values, and secrets in generated configs.
- Preserve validation around interfaces, wireless settings, firewall rules, VPN settings, and backend-specific options.
- Write comments and docstrings only when they explain why code is shaped a certain way. Put comments before the relevant code block instead of scattering them inside it.

## Troubleshooting

- If setup, QA, or tests fail, check docs first, then compare with CI. If commands diverge, follow CI.
