# Coding Challenge: Simple Restaurant Booking System
## User Story ##
As a restaurant owner I want a system for making and tracking reservations which
can interact with other services so that reservations can be handled by third party services.
* The system can be used by multiple restaurants
* The system provides REST API endpoints:
    * To make reservations
    * To check if a number of seats is available at a certain time
* A reservation is for a name (any string) and for a certain amount of time
* The restaurant owner can get an overview over the booked tables as a HTML report

**Limitations**
* Authentication/Authorization isn't in the scope of this task
* No localization needed

**Hints**
* Use third-party packages where applicable!

## Provided Environment ##
A basic environment will be provided, containing:
* Docker container with volumes for code and database
* Django environment with some modules pre-installed and with scaffolding for an app (Restaurant model, ...)

## Submitting your solution
Please compress the repository's root folder and send it to us, so we can evaluate your changes.
Do not remove the git information, so we can easily find your changes.
