# Change Log for Pushable Project

Following the style in https://keepachangelog.com/en/1.0.0/

## [0.2.0] Switch to uv and updated dependencies, drop Python 3.10/3.11, 2026-05-17

### Changed

- Switched from poetry to uv
- Updated dependencies
- Switched from CircleCI to GitHub CI workflow & added release workflow

## [0.1.8] Updating dependencies, 2024-08-13

### Changed

- poetry.lock due to dependabot alert.


## [0.1.6] Protecting against possible vulnerability

### Changed

- poetry.lock of sister project lazychains had vulnerability reported. This
  is a proactive update of poetry.lock.

## [0.1.5] Include type annotations, 2023-02-13

### Added

- Added py.typing so that type annotations can be type-checked when the pushable
  package is imported.


## [0.1.4] Fixes skipPopOr, 2023-02-13

### Added

- mypy added to continuous integration on CircleCI

### Fixed

- Typo in skipPopOr that preventing this method from working fixed.
  It went undetected due to lack of static type checking &
  code coverage. Added type checking and backfilled unit tests.
