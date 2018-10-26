# ros-translator

Adds modules for NCATS Translator to the underlying Ros language.

Also implements prototype workflows to guide testing and expansion of the system.


This repository provides these Translator specific [Ros](https://github.com/NCATS-Tangerine/ros) modules via a Ros plugin: 
* **biothings**: BioThings modules. Currently modules 4 and 5 of workflow 1.
* **gamma**: Invokes the Gamma reasoner. The example below calls Gamma a few times with different machine questions. It will be updated to use the new Quick API for added flexibility.
* **xray**: XRay reasoner modules. Currently modules 1 and 2 of workflow 1.
* **bionames**: Naming resolver. Finds ontology identifiers for natural language names.
* **icees**: Aggregate clinical data outcome data service.
