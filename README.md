# Coding Challenge: Simple Restaurant Booking System

## User Story ##
As a restaurant owner I want a system for making and tracking reservations which
can interact with other services so that reservations can be handled by third party services.

The system provides REST API with endpoints:
* To make reservations
* To check how many seats are available at a certain point of time
* To get an overview of the booked tables per restaurant (this endpoint will have two possible outputs: the regular JSON, and HTML so the owner can use as it a report)

Besides, the system offers a Back office where the restaurant staff can easily manage reservations (you can use Django Admin for this).

**Considerations**
* A reservation is for a name (any string) and for a certain amount of time
* The system can be used by multiple restaurants
* Those restaurants can be in different parts of the world
* When possible, use third-party packages
* Include an example of each endpoint so the person that reviews the code doesn't miss anything. A Postman collection (or similar) is also fine.

**Out of the scope of this task**

To keep the coding challenge as short as possible, the following tasks are not required:

* User filtering: we assume that all the restaurants belong to the same person/company
* Design/Styling
* Localization

## Provided Environment ##
A basic environment will be provided, containing:
* Docker container with volumes for code and database
* Django environment with some modules pre-installed and with scaffolding for an app (Restaurant model, ...)

## Submitting your solution
* Compress the repository's root folder and send it to tech-challenge@orderbird.com
* Do not remove the git information, so we can easily review your changes
* Do not fork the repository or upload it to a public repository, just submit it to us by email
