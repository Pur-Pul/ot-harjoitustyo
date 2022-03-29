# Requirement Specification

## The Purpose of The Application
The application will use simulated physics to generate pixelart clouds. Said clouds will be animated and can be exported as a spritesheet. Specific values can be controlled to alter the appearance and behaviour of the clouds.

## User types
There is only one type of user, which is normal user. There is no need for other user types, as the program will not feature a user hierarchy.

## User interface
The user interface will feature two different pages. One for project creation and on for the work environment. 

In the project creation page the user is prompted to either open a project or create a new one. After selecting either the work environment is loaded in.
The work environment consists of a sprite viewer, and a settings tab. Exporting a project opens up the filebrowser, which prompts the user to select folder to save in.
### Drafts:
![Draft of creation page](https://github.com/Pur-Pul/ot-harjoitustyo/blob/master/dokumentaatio/cloudpage1draft.png)
![Draft of work environment](https://github.com/Pur-Pul/ot-harjoitustyo/blob/master/dokumentaatio/cloudpage2draft.png)
## Functionality
### Project Creation
New projects can be created from scratch or from a template. Creating from template effectively means assigning the same basevalues to the new project as an old one. During the creation the user is also prompted to select a project name, which has to be unique. The left tab of the creation page lists all the previous projects. These can be opened by selecting them. Opening an old project or creating a new one loads in said project to the work environment.  

### Work environment
In the work environment attributes can be changed by typing new values into the textboxes. The attributes affect the appearance and animated behaviour of the cloud. The sprite viewer shows the current state of the cloud sprite being worked at. If FPS is not set to 0 the viewer will be animated, otherwise it will only show the first frame. The settings tab consists of the editable attributes and the export button. The export button converts the cloud into an animated sprite sheet, which the user is then prompted to save using the computers filebrowser.

### Cloud generation algorithm
Clouds are generated based on the set values for *Length* and *Height*. Because all clouds are unique, randomness will also be implemented into the algorithm. Each pixel will have a random chance to generate a neighboring pixel. Altough the clod will always reach the specified *Length* and *Height*.

### Wind simulation
The basic idea is that each pixel in the cloud is a node. Each node can have up to 4 bonds, which are the adjecent pixels. These bonds act as friction on the nodes, and the more bonds a node has, the more force is required to move them (With 4 bonds the pixel is fixed). Wind acts as a force on the nodes and will push them either left or right, depending on its value. The density attribute will affect the nodes windresistance. Less dense nodes are affected more by wind than the more dense ones.

## Ideas for future implementation
- Manual drawing of clouds and a zooming feature in the sprite viewer.
- Allow importating projects.
- Allow removal of old projects.
- Allow selection colors by their hexvalues.
- Allow transparent backgrounds.
- Allow jumping between frames in the sprite viewer when FPS is set to 0.
