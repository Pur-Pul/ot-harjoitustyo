# Requirement Specification

## The Purpose of The Application
The application generates pixelart clouds based on user defined parameters. Said clouds can then be animated to experience a circular wind motion at the press of a button.

## User types "Done"
There is only one type of user, which is normal user. There is no need for other user types, as the program will not feature a user hierarchy.

## User interface "Done"
The user interface features two different pages. One for project creation and one for the work environment. 

In the project creation page the user is prompted to either open a project or create a new one. After selecting either the work environment is loaded in.
The work environment consists of a sprite viewer, a settings tab and a list of recently created projects.
### Drafts:
![Draft of creation page](https://github.com/Pur-Pul/ot-harjoitustyo/blob/master/dokumentaatio/cloudpage1draft.png)
![Draft of work environment](https://github.com/Pur-Pul/ot-harjoitustyo/blob/master/dokumentaatio/cloudpage2draft.png)
## Functionality
### Project Creation "Done"
New projects are created with certain predefined settings, that can be edited afterwards. During the creation the user is also prompted to select a project name, which has to be unique. If a name of an existing project is selected, said project will be opened instead. The left tab of the creation page lists recently created projects. These can be opened by clicking them or writing their name in the entry field. Opening an old project or creating a new one loads in said project to the work environment.  

### Work environment "Done"
In the work environment attributes can be changed by typing new values into the textboxes. The attributes affect the appearance and animated behaviour of the cloud. The sprite viewer shows the current state of the cloud sprite being worked at. If FPS is not set to 0 the viewer can be animated by pressing the animate button. Otherwise only the first frame is shown. The settings tab consists of the editable attributes as well as the animate and save buttons. The save button saves the project settings to the database, which can be loaded in again later to access the same cloud.

### Cloud generation algorithm "Done"
Clouds are generated based on the set values for *Length* and *Height*. Because all clouds are unique, randomness will also be implemented into the algorithm. Each pixel will have a random chance to generate a neighboring pixel. Altough the clod will always reach the specified *Length* and *Height*.

### Wind simulation "Done"
The basic idea is that each pixel in the cloud is a node. Each node can have up to 4 neighbors, which are the adjecent pixels. During the animation the nodes rotate around on the canvas in an orbit. This motion makes the cloud seem to rotate. The orbit shape is rectangular and the width and height is defined by the canvas width and height.
