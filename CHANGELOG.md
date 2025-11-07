# CHANGELOG

<!-- version list -->

## v1.4.1 (2025-11-07)

### Bug Fixes

- Lower required Python version to 3.10 in pyproject.toml
  ([`0458633`](https://github.com/you-n-g/toolbox/commit/045863339f6d4c5112edfb2f55c9fd2754380b07))


## v1.4.0 (2025-11-07)

### Build System

- Add optional crawl dependency group to pyproject.toml
  ([`af15f18`](https://github.com/you-n-g/toolbox/commit/af15f18c71810a58d59158245cb5895673713108))

### Features

- Add TmuxPane wrapper and T function using libtmux
  ([`526a419`](https://github.com/you-n-g/toolbox/commit/526a4196d4afc0b85a84938b7be12dcc461d47ff))


## v1.3.1 (2025-10-25)

### Bug Fixes

- Handle Selenium server connection errors and update endpoint path
  ([`23b66b6`](https://github.com/you-n-g/toolbox/commit/23b66b6e124f60a8377c245f6e18eff242860b68))


## v1.3.0 (2025-10-25)

### Features

- Add selenium-based crawler for WeChat article content extraction
  ([`e288479`](https://github.com/you-n-g/toolbox/commit/e28847902b461495ed24f34ef2771f783d394605))


## v1.2.1 (2025-10-13)

### Bug Fixes

- Resolve file path issues in get_changed_files for git diff
  ([`279d54a`](https://github.com/you-n-g/toolbox/commit/279d54a4f712c963294b1d37771b0696a5334630))


## v1.2.0 (2025-06-28)

### Chores

- Update project description with GitHub URL
  ([`488dd90`](https://github.com/you-n-g/toolbox/commit/488dd908cd4ce1f95d825dc9901759c65af0727a))

### Documentation

- Update README and pyproject metadata
  ([`0df7965`](https://github.com/you-n-g/toolbox/commit/0df79652e8d9adf4503f38bcb12d868f0a1bc5f8))

### Features

- Add design feedback
  ([`124f780`](https://github.com/you-n-g/toolbox/commit/124f780b073137b2c04d66ab7e874ad4789d7a5e))


## v1.1.0 (2025-06-28)

### Build System

- Add uv publish step to release target
  ([`9868264`](https://github.com/you-n-g/toolbox/commit/9868264fc2e76a6de3bf088d723116b527b60f13))

- Switch to setuptools-scm and update build targets
  ([`d157100`](https://github.com/you-n-g/toolbox/commit/d1571007d0c16cb15b6fea8474b543cf8a9bc401))

### Chores

- Use uvx for build/release, ignore .uv, enable dynamic version
  ([`713ba4f`](https://github.com/you-n-g/toolbox/commit/713ba4fdc73a05dac14ca268f9345bfd78287cc2))

### Features

- Add xytb code review CLI and update project dependencies
  ([`cc6bc3a`](https://github.com/you-n-g/toolbox/commit/cc6bc3a26c2c7d1db277a2f3da8f1daec4c65851))


## v1.0.0 (2025-06-28)

- Initial Release
