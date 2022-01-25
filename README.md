# Choam
Choam is a project scaffolder and manager. Aiming to be like the NPM of Python. With easy
package managing, enviroment scaffolder, and especially an easier and more dynamic way of 
publishing to PyPi.

Install Choam via pi

```$ python3 -m pip install choam```

## Backstory
Etymology of ```choam```: The 'Combine Honnette Ober Advancer Mercantiles' or C.H.O.A.M. 
is the main source of control of all economic affairs in the book of Dune. The reasoning
behind this word is the smoothness of the word. 

I started Chaom when I was tired of two things. The first being project setup. I hate 
having to download Python projects and manually configure the whole project to be accurate
for my system. Secondly, publishing packages to PyPi is overally complicated and can 
be durastically simplified with the help of Python. 

## Snippets

To create a new Choam structured project

```$ python3 -m choam new <project_name>```

To initialize a pre-existing project with Choam

```$ choam init <project_name>```

To run a Choam project from default entry point in a pre-existing choam project

```$ python3 -m choam run```

To setup Choam for publication

```$ python3 -m choam setup```

To install Choam project dependencies

```$ python3 -m choam install```

## Goals
Easily scaffold/structure projects

- Install Choam projects from GitHub ```$ choam download cowboycodr/choam```
- Use ```choam``` as global executable
- Package projects to exe ```$ choam build```
- And more in the future...

#### This project is structured with [Choam](https://github.com/cowboycodr/choam)