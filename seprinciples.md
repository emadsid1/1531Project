Rigidity- Incorporated more components to classes such that we edit classes and not add random things
Fragility- ???
Immobility- Changed to have a route handler isolated and then functions in different files, makes it easier to extract functions for us to use in different projects
Opacity- Convetion in variable names, and better variable names, comments and helper functions
Needless complexity- Removed a few for loops

DRY Implemented more helper functions and improved them in the separate helper_functiosn file
Found that when someone else needed a certain function, if we checked there more often than not someone else already wrote it
KISS Changed to have a route handler isolated and then functions in different files, makes it easier to extract functions for us to use in different projects
Also removed a few global variables, such as list of admins, owners etc, instead used flags

YAGNI at no point did we start building lower level functions until we fully understood the purpose and began writing the higher level function
    Minimised waste of time