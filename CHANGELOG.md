# Change Log for Pushable Project

Following the style in https://keepachangelog.com/en/1.0.0/

## [0.1.4] Fixes skipPopOr, 2023-02-13

## Added

- mypy added to continuous integration on CircleCI

## Fixed

- Typo in skipPopOr that preventing this method from working fixed.
  It went undetected due to lack of static type checking &
  code coverage. Added type checking and backfilled unit tests.

