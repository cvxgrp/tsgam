# Release process

TSGAM uses Git tags for releases. The tag should match the version declared in
`pyproject.toml`. The runtime `tsgam.__version__` comes from the installed
package metadata.

## Prepare a release

1. Update `version` in `pyproject.toml`.
2. Install and test with the locked environment:

   ```bash
   uv sync --frozen --group dev
   uv run ty check
   uv run pytest
   ```

3. Build and check the distributions:

   ```bash
   uv build
   uv run python scripts/check_package_contents.py
   uv run --with twine twine check dist/*
   ```

4. Once the release changes are on `main`, tag the release commit and push the tag:

   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

Pushing a tag matching `v*.*.*` runs the **Release** workflow. After the checks
pass, you can download the wheel and source distribution from the
`distributions` artifact on the workflow run.
