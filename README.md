This repo aims to solve case given by Thermondo. Request details can be seen [here](case_definition.md).

## Setup
You can use [poetry](https://python-poetry.org/) or docker for local development. 
For a list of instructions, see [Makefile](./Makefile)


## TODOS

Below is the list of subjects I would do better if I had time

**App**

 - Cover requests in [case_definition](./case_definition.md)

**Tests**
 
 - Extend fixtures & cases
 - Add integration tests

**Admin Panel**

 - Use [django grappelli](https://grappelliproject.com/)

**Docker**
 
 - [x] Use multi-stage builds
 - [ ] Publish custom docker image(s)
 - [ ] Add pg_ready check for database status before making a call
 
**Deployments**

 - Publish as pypi package
 - Prepare k8s resources for deployment  