# Delivery Management API
RESTful API made with Django and DRF

### Tech Stack
 - Django
 - Django-Rest-Framework (API endpoints)
 - Djoser (Authentication)
 - MySQL (Database)

### Features
This project implements ordering, filtering, searching, and pagination. In addition, certain endpoints require authentication and authorization before use. Anonymous users can only call API endpoints 10 times per minute, while authenticated users have an unreachable, but reasonable limit on the number of calls they can make.
