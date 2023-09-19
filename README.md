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
1.	Load the dataset (REQUIRED_DATA.mat) into MATLAB (onshore_height.mat is additional data if tsunami wave height is interested)
2.	Open the ‘short_code.m’ file in MATLAB
3.	Set the option for response variable (1 for tsunami height and 2 for tsunami loss), number of offshore sensors (1 for 99 sensors and 2 for 6 sensors), and waiting time
4.	The input features are maximum wave amplitude from each offshore sensors and earthquake information, including magnitude, longitude, and latitude. The main response variable is tsunami loss.
5.	Run the ‘short_code.m’ file in MATLAB
6.	The results, including mean squared error and scatter plot for comparing model performance will be displayed in the MATLAB console

--------------

## Contact
For any questions, please contact Andrea Di Benedetto at andrea.dibenedetto@unipa.it (or andrea.dibenedetto@ingv.it), Giosué Lo Bosco at giosue.lobosco@unipa.it.
