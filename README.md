# Choam
Choam is a project scaffolder and manager. Aiming to be like the NPM of Python. With easy
package managing, enviroment scaffolder, and especially an easier and more dynamic way of 
publishing to PyPi.

## Backstory
Etymology of ```choam```: The 'Combine Honnette Ober Advancer Mercantiles' or C.H.O.A.M. 
is the main source of control of all economic affairs in the book of Dune. The reasoning
behind this word is the smoothness of the word. 

## Snippets

To create a new Choam structured project

```$ choam new <project_name>```
___
To initialize a pre-existing project with Choam

```$ choam init <project_name>```
___
To run a Choam project from default entry point in a pre-existing choam project

```$ choam run```

## Goals
Easily scaffold/structure projects

- Manage ```choam``` configurations from a ```Choam.toml``` file
- Add dependencies to project ```$ choam add <dependency_name>```
- Install all project dependencies ```$ choam setup```
- Install Choam projects from GitHub ```$ choam install cowboycodr/choam```
- Use ```choam``` as global exe
- Package projects to exe ```$ choam build```
- And more...

#### This project is structured with [Choam](https://github.com/cowboycodr/choam)