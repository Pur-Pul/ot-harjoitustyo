# **Cloud Generator**

This application will allow the user to simulate pixel art clouds reacting to wind.  
This application requires python 3.8 to function.  
Application is still under developement.  

## Documentation  
[Työaikakirja](dokumentaatio/tyoaikakirja.md)  
[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)  
[Changelog](dokumentaatio/changelog.md)  

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
