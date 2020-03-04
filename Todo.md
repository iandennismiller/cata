# catalog

## Milestone 1

- [ ] create project: project-new catalog
- [ ] scaffold project: diamond --skel python scaffold
- [ ] create repository at https://github.com/new
    + [ ] set description
    + [ ] set documentation website
- [ ] enable continuous integration at https://travis-ci.org/profile/
- [ ] enable code coverage at https://coveralls.io/
- [ ] enable documentation at https://readthedocs.org/dashboard/import/
    + [ ] admin -- advanced settings -- requirements file -- ".readthedocs.txt"
- [ ] pypi (python setup.py register -r https://pypi.python.org/pypi)
- [ ] release to pypi (make release)
- [ ] install development environment (make dev test)
- [ ] install production environment

## Milestone 2

- add CSV_FILENAME PARAMS: copy a CSV file to the .cata folder and add an entry to the data catalog.  Also ensure CSV can be loaded as data frame.
- add DATA_FRAME PARAMS: serialize data frame to CSV and add to .cata
- get CHECKSUM: obtain a data frame
- get PARAMS_JSON INDEX: search catalog for parameters matching query and return first data frame that matches.  Or, return INDEX data frame if requested.
- ls: list entries in .cata
- find PARAMS_JSON: search catalog for parameters matching query
- delete CHECKSUM: delete a .cata entry and file

## Done
