# How to contribute to the project

## Feedback

The report of issues and the proposal of new features is very welcome.
Please use the bitbucket issue page for this.

## Contributing code

Code contributions to the signac-flow open-source project are welcomed via pull requests on bitbucket.
Prior any work you should contact the signac-flow developers to ensure that the planned development meshes well with the directions and standards of the project.
All contributors must agree to the Contributor Agreement ([ContributorAgreement.md](ContributorAgreement.md)) before their pull request can be merged.

General guidelines:

  * The signac-flow development is based on the [git flow model][gitflow], which means new features should be developed within a feature branch based off the 'develop' branch.
  * If external library depedencies cannot be avoided, they must be added as *soft depedencies*.
  * All contributed code should pass `flake8` checks as specified in the tox.ini configuration file.
  * All new features require unit tests.

[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
