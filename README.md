# Grid-search method for STA/LTA parameters selection
This **repository** contains the codes for a **Grid-search** methodology to automatically select the **parameters** of the **STA/LTA (Allen, 1978)**, for the purpose of **selecting significative events** from raw signals relative to Stromboli Volcano. This method is applicable to every seismo-volcanic signal, improving the selection of significative events in raw signal.

--------------
## Prerequisites
To run the code in this repository, you need:

*	Python 3.9 or higher
*	ObsPy 1.4.0 or higher

--------------

## Installation
1.	Clone this repository to your local machine
2.	Build your own environment with **pip** or **conda**. <br>
    Using pip
    ```
      python3 -m venv <environment_name>
    ```
    Using conda
    ```
      conda create --name <environment_name> --file requirements.txt
    ```
3. After creating your own environment, install the dependecies using **requirements.txt** file present in repository. <br>
    Using pip
    ```
      pip install -r requirements.txt
    ```
    Using conda
    ```
      conda install -r requirements.txt
    ```
--------------

## Usage
1.	You can use the config_file.json to set the parameters of the quadruple: sta, lta, trigger on and trigger off. These parameters will be used for the Training Phase.
2. Run ‘python training_phase.py’. In this phase, by default, the training_set inside 'data' folder will be used to execute the training phase.
3.	After the execution of the previous script, a training_results file inside 'results' folder will be created. This file contains the array calculated from the training phase containing the qni's value resulted from every quadruple combination.
4.	You can run ‘python plot_results.py’ to show a plot of the quintuples (sta, lta, trigger on, trigger off, qni) extracted from training phase providing training_results file.
5.	Run ‘python testing_phase.py’. In this phase, by default the testing_set inside 'data' folder will be used to execute the testing phase. You have to provide training_results file from which the Testing Phase start.
6.	After the execution of the previous script, a testing_results file inside 'results' folder will be created. This file contains the array calculated from the testing phase.
7. Again, you can run ‘python plot_results.py’ to show a plot of the quintuples (sta, lta, trigger on, trigger off, qni) extracted from testing phase providing testing_results file.
--------------

## Contact
For any questions, please contact Andrea Di Benedetto at andrea.dibenedetto@unipa.it (or andrea.dibenedetto@ingv.it), Giosue' Lo Bosco at giosue.lobosco@unipa.it.

--------------
## Acknowledgments
The authors would like to acknowledge Dario Delle Donne from Istituto Nazionale di Geofisica e Vulcanologica - Osservatorio Vesuviano (INGV-OV), for helping us to extract the data from STRA seismic station.
