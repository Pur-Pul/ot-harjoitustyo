# **Cloud Generator**

This application will allow the user to simulate pixel art clouds reacting to wind.  
This application requires python 3.8 to function.  
Application is still under developement.  

## Documentation  
[Työaikakirja](dokumentaatio/tyoaikakirja.md)  
[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)  
[Changelog](dokumentaatio/changelog.md)  
[Architecture](dokumentaatio/arkkitehtuuri.md)

## Installation  
[Lastest Release](https://github.com/Pur-Pul/ot-harjoitustyo/releases/tag/first_release_v.0.1.0-alpha)  

Install requirements with:  
```bash
poetry install
```

Start the application with:  
```bash
poetry run invoke start
```
## Usage
The first window that opens up is where projects are created. To create a new project, simply write a project name into the entry field and click "create". After that the editor will show up, which is where the parameters can be changed and the cloud can be animated.

Parameters are changed by writing values in their respective entry fields. To generate a new cloud, click the "Generate a new cloud" button.  

To animate the cloud, increase the frames to a large value and click "Animate". The first time around the frames are generated, which means that it will not play at the specified FPS. Click again for the animation to play properly. Every time a setting is changed, the frames need to be generated again.  

To save the project, simply click "save project" and the next time the application is launched, it will be possible to open the same project again.  

To open a previously created project, click on it's name in the sidebar on the left, or create a project with the same name to load the same settings.

## Testing  
Run tests with:  
```bash
poetry run invoke test
```

The following commmand will generate a coverage report to the _htmlcov_ directory.  
```bash
poetry run invoke coverage-report
```

Run pylint with:
```bash
poetry run invoke lint
```
