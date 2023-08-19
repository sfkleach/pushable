# Change Log for Pushable Project

Following the style in https://keepachangelog.com/en/1.0.0/

## [0.1.6] Protecting against possible vulnerability

## Changed

- poetry.lock of sister project lazychains had vulnerability reported. This
  is a proactive update of poetry.lock.

## Added

## [0.1.5] Include type annotations, 2023-02-13

## Added

- Added py.typing so that type annotations can be type-checked when the pushable
  package is imported.


## [0.1.4] Fixes skipPopOr, 2023-02-13

## Added

- mypy added to continuous integration on CircleCI

## Fixed

- Typo in skipPopOr that preventing this method from working fixed.
  It went undetected due to lack of static type checking &
  code coverage. Added type checking and backfilled unit tests.

