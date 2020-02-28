# fsf_2020_screening_task

#### Details for Fossee Task Submission
    **Author**: Megha Kailash Sankhlecha
    **Username**: 17dcs056
    **Email**: 17dcs056@charusat.edu.in

This project done for the completion of screening task for python, FOSSEE 2020 Python Fellowship. 
The task requirement was to implement a fully functional GUI Spreadsheet Data Converter to work with data related to Civil/Structural engineering by using Python and PyQT as an open source project hosted on github.

<details>
<summary>Screening Task (Click to expand)</summary>

#### Technologies/Libraries to use:
   1. Python
   2. OOP
   3. GUI (PyQt5)
   4. Git
  
#### Instructions:

     1. Develop a desktop application that will take inputs for four different categories (modules).

     2. GUI shall have a spreadsheet, Load Inputs, Validate and Submit buttons, message box to display warning messages if the user gives a bad value.
   
     3. A spreadsheet of different modules should be opened in different tabs of the same window.

     4. Based on the selected module corresponding header row shall be displayed in spreadsheet GUI. Details of header rows, with sample input values for each module, are given in resources.
            1. For example You can develop UI with four tabs, one for each module, which has respective header rows. (Checkout QTableWidget, QStakedWidget, QTabWidget of PyQt5 for GUI design)

     5. “Load Inputs” button shall prompt for selecting CSV/xlxs file, which will populate the spreadsheet. Also, Users can fill data manually in each row.

     6. The clicking of the “Validate” button should validate the data and a suitable error message for bad values should be displayed in the message box.
            1. Required validators are:
            2. All cells other than headers should only take numerical inputs.
            3. Headers should not be editable.
            4. ID column shall be unique, i.e., ID number should not be repeated

     7. Once the user submits the data by clicking on the “Submit” button, it should create a new text file for each row. This text file shall be a dictionary with header value as key and cell value as value.
            1. Text files can be saved in the working folder or you can take folder location from the user.

     8. Text files shall be saved as Modulename_ID. For example, if the user submits fin plate inputs, the first row will be saved as FinPlate_1 automatically, i.e., the user does not have to specify the file name for each row.

     9. An easy to use, user-friendly and clean looking GUI application would help the user to quickly adapt to the application.

     10. Create an installer (Windows or Ubuntu) for your application.
</details>


<details>
<summary>Usage (Click to expand)</summary>

##### Install using Windows Installer - Download from here - [Download Link](dist/Spreadsheet_Data_Converter_Fossee_1.0_Setup.exe)

OR

1. Download the project from github or clone the repo to your machine using:

     ```
     git clone https://github.com/meghasankhlecha/fsf_2020_screening_task.git
  	```
2. Install the project requirements using pip:

	If on linux, type:
  ```pip3 install -r requirements.txt```
  <br>
  	If on windows type
    ```pip install -r requirements.txt```

4. To run the app, navigate to dataconverter folder in the terminal using ```cd dataconverter```
	<br>
    Now execute the app by:
    <br>
    ```python3 dataconverter``` if on Linux
    <br>
    ```python dataconverter``` if on Windows
 
</details>

<details>
<summary>Screenshots (Click to expand)</summary>

![Screenshot_1](https://i.postimg.cc/s2NHY2Sc/1.png "Home Screen")
![Screenshot_2](https://i.postimg.cc/ZnkfQDwv/2.png "Loading Inputs")
![Screenshot_3](https://i.postimg.cc/sD4nnm71/3.png "Select file for loading")
![Screenshot_4](https://i.postimg.cc/G3YgDdpF/4.png "Spreadsheet")
![Screenshot_5](https://i.postimg.cc/8chygBYK/5.png "Add/Edit Data")
![Screenshot_6](https://i.postimg.cc/3JTSCVyP/6.png "Rename Tabs")
![Screenshot_7](https://i.postimg.cc/0ytVvNts/7.png "Close tab prompt")
![Screenshot_8](https://i.postimg.cc/0y5VhS0n/8.png "Validation error - Duplicate ID")
![Screenshot_9](https://i.postimg.cc/BvXMnGy1/9.png "Validation error - Non numerical input")
![Screenshot_10](https://i.postimg.cc/rp3gdPXZ/10.png "Validation error - Empty input")
![Screenshot_11](https://i.postimg.cc/Qt7mcJj8/11.png "Save Data")
![Screenshot_12](https://i.postimg.cc/rsLJjRpS/12.png "Select folder for saving data")
![Screenshot_13](https://i.postimg.cc/PJzMRfL0/13.png "Quit prompt")
![Screenshot_14](https://i.postimg.cc/hGj3QmJv/14.png "Setup installer 1")
![Screenshot_15](https://i.postimg.cc/3R0SnHFH/15.png "Setup installer 2")

</details>











