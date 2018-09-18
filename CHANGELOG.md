# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.3.0] - 2018-18-09
### Added
- Do not recommend pushes to `master` in `CONTRIBUTING.md`
- Documentation about how to set up the site and Postgres up locally using Docker and `pip`
- Healthchecks for the `app` container
- Require 100% code coverage in `CONTRIBUTING.md`
- Require `CHANGELOG.md` updates in `CONTRIBUTING.md`
- The `psmgr` console script as a shortcut to `python manage.py`
- This file

### Changed
- Improved build speed by not installing unneeded dependencies.
