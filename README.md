![CI Status](https://github.com/YasinZabun/aircraft_production/actions/workflows/ci.yaml/badge.svg)

# Aircraft Production System

## Overview

The Aircraft Production System is a web-based application designed to facilitate the management of aircraft, parts, teams, and assembly processes. This application provides tools for administrators and users to track and manage various components effectively.

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [Folder Structure](#folder-structure)
7. [Usage](#usage)
8. [Application Screens and Example Usages](#application-screens-and-example-usages)
9. [Api References via Swagger](#api-references-via-swagger)
10. [Admin Dashboard](#admin-dashboard)

---

## Project Architecture

The project follows the **Django Framework** architecture and is organized into multiple apps, each handling specific features and functionality. The main components include:

1. **accounts**: Manages user authentication and profiles.
2. **aircraft**: Handles aircraft data.
3. **assembly**: Manages assembly processes.
4. **common**: Contains reusable utilities like permissions.
5. **parts**: Handles information about aircraft parts.
6. **teams**: Manages team-related data.

Additional components include templates, static files, and configurations for Docker and Nginx.

---

## Features

- **User Authentication**: Secure login system for administrators and users.

- **Aircraft Management**: Add, edit, and view aircraft details.

- **Parts Management**: Track and manage aircraft parts.

- **Team Management**: Assign teams to specific tasks or parts.

- **Assembly Tracking**: Monitor the assembly of aircraft components.

- **Responsive Design**: Frontend templates designed for desktop and mobile users.

---

## Requirements

To run the application, ensure the following dependencies are installed:

- Python 3.11 or later
- Django 5.1.4
- PostgreSQL
- Docker & Docker Compose
- Nginx
  
Python dependencies are listed in `requirements.txt`.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YasinZabun/aircraft_production
   cd aircraft-production
   ```

2. Set up a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Load initial data (optional):

   ```bash
   python manage.py loaddata initial_data.json
   ```

---

## Running the Application

### Local Development

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`.

### Docker

1. Build and run the Docker container:

   ```bash
   docker-compose up -d --build
   ```

2. Access the application at `http://localhost:8000/`.

---

## Folder Structure

```
src
├─ aircraft_app
│  ├─ apps
│  │  ├─ accounts
│  │  │  ├─ tests
│  │  ├─ aircraft
│  │  │  ├─ tests
│  │  ├─ assembly
│  │  │  ├─ tests
│  │  ├─ common
│  │  │  ├─ tests
│  │  ├─ parts
│  │  │  ├─ tests
│  │  └─ teams
│  │      ├─ tests
├─ static
├─ templates
├─ docker-compose.yaml
├─ Dockerfile
├─ manage.py
├─ init.sh                                                                                       
├─ initial_data.json                                                                             
├─ manage.py                                                                                     
├─ nginx.conf                                                                                    
└─ requirements.txt  
```

### Key Folders and Files

- `src/aircraft_app/apps`: Contains Django apps for different modules.
- `src/aircraft_app/apps/<one_of_the_apps>`: Contains unit testing files for models, serializers and views. 
- `templates`: Contains shared HTML templates.
- `static`: Stores static files like CSS.
- `Dockerfile` & `docker-compose.yaml`: Docker configuration files.
- `init.sh`: Contains some initialization commands that it will used by Docker and creates admin.
- `initial_data.json`: Contains initialization records. (The password of all these users is **pass123pass**)
- `nginx.conf`: It is important for issuing static css,js and etc files by nginx on Docker.
- `requirements.txt`: Python dependencies are listed in it.

---

## Usage

### Authentication

- Navigate to `/accounts/login/` or `/` to log in.

### Managing Aircraft

- Use the dashboard to add, update, and view aircraft information.

### Managing Parts

- Navigate to `/parts/` to manage parts.

### Teams and Assembly

- Assign teams and track assembly progress from the respective modules.

---

## Application Screens and Example Usages

### Entry and Authentication

- Navigate `/` to log in.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/1.1_login.png

### Dashboard

- Use the dashboard to go related sections.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/1.2_dashboard.png
- Use the dashboard as assembly team member to go related sections.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/2.2_dashboard_as_assembly_member.png
  
### Part Logic

- Use the parts section to add, update, and view parts information.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/1.3_part_list.png
- Use the parts create button to add new part information.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/1.4_part_creating_modal.png
- Use the recycle button to delete a part information.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/1.5_part_recyling.png

### Assemble Logic

- Use assemble section to assembling aircraft.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/2.3_assemble_aircraft_selection.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/2.4_assemble_aircraft.png
- Use Produced Aircraft section to list assembled aircrafts
- https://github.com/YasinZabun/aircraft_production/blob/main/images/2.6_aircraft_assembling_list.png

---
## Api References via Swagger

### Entry and Authentication

- Navigate `/swagger` to log in and see api endpoints.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/3.1_swagger.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/3.2_swagger_aircraft_listing.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/3.3_swagger_assemble_posting.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/3.4_swagger_part_listing.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/3.5_swagger_part_posting.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/3.6_swagger_part_recyling.png

---
## Admin Dashboard

### Dashboard


- Navigate `/admin` to log in and use the dashboard to manage everything.
- https://github.com/YasinZabun/aircraft_production/blob/main/images/4.1_admin_objects.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/4.2_admin_profiles.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/4.3_admin_teams.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/4.4_admin_users.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/4.5_admin_parts.png
- https://github.com/YasinZabun/aircraft_production/blob/main/images/4.6_admin_aircrafts.png

---  
