# Choam

<a href="https://pepy.tech/project/choam"><img src="https://img.shields.io/pypi/dw/choam"></a>
<a href="https://pypi.org/project/choam"><img src="https://img.shields.io/pypi/v/choam"></a>
<a href="https://github.com/cowboycodr/choam"><img alt="LOC" src="https://shields.io/tokei/lines/github/cowboycodr/choam"></a>
<a href="https://github.com/cowboycodr/choam"><img src="https://img.shields.io/github/repo-size/cowboycodr/choam"></a>

Python enviroment manager based around making depedency management, and publication easier.

While Python is a simple langauge all-around, managing dependencies and publication aren't. However, Choam automates this, with easy configuration, and simple commands.

> Choam, automating the nooks and crannies of Python. 

## Warning
Choam is currently in beta. If you are not comfortable with this, then use a different dependency manager in the meantime like `poetry`.

## Installation
`$ pip install choam`

## Snippets
The most useful snippets of `Choam`

> Note: Depending on your system's configurations, Choam might have to be prefixed with `$ python3 -m` like this, `$ python3 -m choam <COMMAND>` 

#### To create a new project

`$ choam new <project_name>`

#### To initialize a project in the current directory
`$ choam init <optional: --adapt (adapts the current project to choam's standards)>`

#### Add required dependency
`$ choam add <dependency_name>`

#### Install required dependencies of an existing project
`$ choam install`

#### Find all required dependencies and update `Choam.toml` accordingly
`$ choam deps`

#### Convert `Choam.toml` requirements to `requirements.txt`
`$ choam reqs`

#### Setup config files for publication to PyPi according to `Choam.toml`
`$ choam setup`

#### Start publication to PyPi
`$ choam publish`

#### Run project entrypoint
`$ choam run <filepath_or_script> <optional: --file (to run files instead of scripts)>`
___

## `Choam.toml` quick start
```toml
# Choam.toml
[package]
name = "choam"
version = "0.0.0"
description = "Choam is a project manager"
repo = "https://github.com/cowboycodr/choam"
keywords = ["manager"]
```

So far we've described the package metadata. Including the package name, version, description, and other useful information. This will all be setup when you setup the project with Choam.

### Managing dependencies
Managing dependencies with Choam is just as easy as defining the package metadata.
```toml
# Choam.toml
[package]
...

[modules]
choam = "*"
```

The `*` means it will require the lastest version of the specified module. You can sepcify specific versions if you like: `choam = "0.1.18""`
___
Since Choam is in beta, it will sometimes capture unwanted depedencies. To by-pass this behavior define a `[modules-ignore]` section. Like so:
```toml
# Choam.toml
[package]
...

[modules]
...

[modules-ignore]
shutil = "*"
```
`toml` is a weird configuration langauge so make sure to include the ` = "*"` after the specified package.
___

### Choam's scripts

To add custom defined scripts to your project all that is required is `[script.<YOUR_SCRIPT_NAME>]` and a few other parameters. Let's make a format script with python's black, for example.
```toml
# Choam.toml
[package]
...

[modules]
...

[modules-ignore]
...

[script.format]
requires = ["black"]
perspective = "${PROJECT}"
command = "${PYTHON} -m black ."
```

The `requires` section defines what dependencies are used with the script.

The `perspective` parameter defines where the script will run relative to the project folder. The `${PROJECT}` will run in the project files directory instead of the overall project folder where the `Choam.toml`, `README.md` etc. are. 

> Note: notice how `${PROJECT}` is used? When a piece of text is wrapped like `${}` this means it is a script variable. Choam provides multiple script variables such as `${PYTHON}` to access the active python interpreter, `${CWD}` to access the current directory, and `${PROJECT}` which is the current working directory. With these script variables you can create very useful scripts that work on any machine.

The `perspective` parameter defines the actual command that will be run.

Combining all of these with script variables you can create dynmaic, cross-platform, useful, scripts available to anyone.

Running the script:

`$ choam run format`

In result this will format all of your project files

## `.choam` folder

The `.choam` folder is specifically for storing Choam related resources. For example: if you have a choam script, and you need to pull from a file, for example. You would put the resource in `.choam/scripts/<SCRIPT_NAME>/<FILE>`

### This project is structured with [Choam](https://github.com/cowboycodr/choam)
