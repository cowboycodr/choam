# Choam
<a href="https://pypi.org/project/choam"><img src="https://img.shields.io/pypi/dw/choam"></a>
<a href="https://pypi.org/project/choam"><img src="https://img.shields.io/pypi/v/choam"></a>
<a href="https://github.com/cowboycodr/choam"><img src="https://shields.io/tokei/lines/github/cowboycodr/choam"></a>
<a href="https://github.com/cowboycodr/choam"><img src="https://img.shields.io/github/repo-size/cowboycodr/choam"></a>

Python enviroment manager based around making depedency management, and publication easier.

## Snippets
The most useful snippets of `Choam`

#### To create a new project
`$ choam new <project_name>`

#### To initialize a project in the current directory
`$ choam init <project_name>`

#### Add required dependency
`$ choam add <dependency_name>`

#### Install required dependencies of an existing project
`$ choam install`

#### Find all required dependencies and update `Choam.toml` accordingly
`$ choam deps`

#### Setup config files for publication to PyPi according to `Choam.toml`
`$ choam setup`

#### Start publication to PyPi
`$ choam publish`

#### Run project entrypoint
`$ choam run <optional:relative_path>`
___

### This project is structured with [Choam](https://github.com/cowboycodr/choam)
