# SpaceXplore

A smart, real-time room and lab availability tracking system for educational institutions.

## 1. Project Overview

* **Project Title**: spaceXplore
* **Problem Statement**: In large universities and institutions, students often struggle to find vacant classrooms, laboratories, or study spaces. Checking rooms manually is time-consuming and inefficient.
* **Objective**: To provide a centralized platform where students can view real-time room availability, and faculty can manage room statuses efficiently.
* **Target Users**: Students (viewers) and Faculty / Class Representatives (administrators).
* **Real-world Use Case**: University campuses where students need to find a place to study between classes, or faculty need an ad-hoc room for an extra lecture or meeting.

## 2. Features & Functionalities

* **Core Features**:
  * Role-based access control (Student vs Faculty/Admin).
  * Real-time room availability dashboard.
  * Faculty override module to manually mark rooms as occupied or available.
  * Next available time prediction based on the current timetable.
* **Advanced Features**:
  * **Camera Density Simulation**: Simulates integration with CCTV/Cameras to show how crowded an available room currently is.
  * **Dynamic Time Machine**: Allows users to input a 'demo time' to view what the availability will be at a specific time of day.
* **Future Scope**:
  * Integration with actual IoT sensors / Camera feeds for real physical occupancy detection.
  * Sync with institutional Timetable APIs instead of local generation.

## 3. Technical Stack

* **Frontend**: HTML5, CSS3, Jinja2 Templating
* **Backend**: Python 3, Flask
* **Database**: Firebase Firestore (NoSQL)
* **Libraries / Frameworks**: `Flask`, `firebase-admin`, `gunicorn`
* **Tools & Platforms Used**: Git, Python Virtual Environment, Google Cloud Firebase Console

## 4. System Architecture

* **High-level Architecture Explanation**: 
  The project follows a Client-Server architecture where the browser acts as the client, Flask serves as the controller and view-renderer (using Jinja templates), and Firebase acts as the database layer.
* **Data Flow Description**:
  1. User authenticates via the `/login` route.
  2. Flask validates the credentials against Firebase (`faculties` collection).
  3. Dashboard requests fetch all rooms from Firestore.
  4. The `availability_engine` cross-references room timetables and custom overrides to output a final availability status.
  5. The rendered HTML is returned to the user.
* **Component Breakdown**:
  * **Auth Component**: Manages session state and role (Student/Faculty).
  * **Room Engine**: Fetches static room capacity and type.
  * **Availability Engine**: Calculates if a room is free based on current time vs timetable and faculty overrides.
  * **Timetable Generator**: Generates base logical occupancy logic for testing.

## 5. Folder & File Structure

* `app.py`: The main entry point for the Flask application containing all route definitions and session management.
* `requirements.txt`: Python package dependencies needed to run the application.
* `serviceAccountKey.json`: Firebase Admin SDK certification keys (ensure this is kept secure).
* `services/`: Contains backend core logic.
  * `firebase_config.py`: Initializes the Firebase app and Firestore client.
  * `availability_engine.py`: Contains the `get_status` function which calculates room status with a 5-minute buffer time.
  * `timetable_generator.py`: Mocks a daily class timetable schedule.
* `templates/`: Contains Jinja2 HTML templates.
  * `login.html`: User authentication page.
  * `dashboard.html`: Main student view.
  * `admin.html`: Faculty view with override controls.
* `static/`: Contains static assets like CSS (`style.css`) and images (`favicon.png`).

## 6. Setup & Installation Guide

* **Prerequisites**:
  * Python 3.8+
  * Firebase Project with Firestore Database initialized
  * A valid `serviceAccountKey.json` from the Firebase Console

* **Step-by-step Setup Instructions**:
  1. **Clone the Repository**:
     ```bash
     git clone <repo_url>
     cd spaceXplore
     ```
  2. **Create a Virtual Environment**:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
  3. **Install Dependencies**:
     ```bash
     pip install -r requirements.txt
     ```
  4. **Firebase Configuration**:
     * Place your Firebase Admin SDK file inside the root directory and name it `serviceAccountKey.json`.

* **How to run the project locally**:
  Execute the following command in your terminal:
  ```bash
  python app.py
  ```
  The application will run by default on `http://localhost:8080`.

## 7. API / Routing Documentation

Since this is a Server-Side Rendered (SSR) Application, these are the primary HTTP routes utilized:

* `GET /`
  * **Description**: Renders the landing/login page.
* `POST /login`
  * **Request Format**: Form Data (`user_type`, and if faculty: `reg_id`, `access_code`)
  * **Response**: Redirects to `/dashboard` (student) or `/admin` (faculty).
* `GET /dashboard`
  * **Description**: Retrieves the student view. Requires `demo_time` query param.
  * **Response**: HTML rendered template `dashboard.html` with room objects.
* `GET /admin`
  * **Description**: Retrieves the faculty view.
  * **Response**: HTML rendered template `admin.html` with room objects.
* `POST /admin`
  * **Request Format**: Form Data (`room_id`, `action`, `till_time`)
  * **Description**: Creates a new room override in Firestore.
  * **Response**: Redirects to `GET /admin`.

## 8. Feasibility Analysis

* **Technical Feasibility**: Highly feasible. Using Flask allows rapid development, while Firebase handles real-time data sync without complex backend infrastructure.
* **Economic Feasibility**: Very feasible. Firebase offers a generous free tier which is more than enough for initial institutional deployment. Hosting Flask is also inexpensive.
* **Operational Feasibility**: The simple UI ensures that students require zero training to use the system, and faculty can override room limits intuitively.

## 9. Advantages & Limitations

* **Advantages**:
  * Reduces time wasted searching for empty study spaces.
  * Helps institutions optimize room utility.
  * Easy scaling capabilities via Firebase.
* **Limitations**:
  * Currently relies on subjective faculty overrides if the static timetable changes.
  * Camera density is currently mocked and requires actual hardware API integration for production.

## 10. Future Improvements

* Integrate hardware IoT sensors (PIR motion trackers or CCTV density estimators) for completely autonomous occupancy tracking.
* Expand the dashboard to include a booking/reservation system for study rooms.
* Migrate to a fully decoupled architecture (e.g., React.js front-end and a REST/GraphQL API back-end).

## 11. Conclusion

spaceXplore is a highly practical and scalable solution to a common university problem. By leveraging a serverless database and a lightweight web framework, the application delivers real-time visibility into campus infrastructure and optimizes the utilization of institutional spaces.

## 12. Demo Login Credentials

You can test the faculty functionalities using the following demo credentials:
* **Faculty / CR registration id**: `CR001`
* **Access code**: `CR001A`
