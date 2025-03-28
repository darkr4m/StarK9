# StarK9 - Canine Training Progress Tracking and CRM

## Phase I
### Technology Setup & Project Structure:
#### Backend (Django)
- Install Python and pip
- Create a virtual environment
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- Install Django
  ```
  pip install django
  ```
- Install psycopg
  ```
  pip install "psycopg[binary]"
  ```
- Instal dot env for storing and utilizing app secrets
  ```
  pip install python-dotenv
  ```
- Install Django REST Framework (for APIs)
  ```
  pip install djangorestframework
  ```
- Install CORS headers middleware - for React frontend communication
  ```
  pip install django-cors-headers
  ```
- Create Django project
  ```
  django-admin startproject backend
  ```
- Create Django apps within the project
  ```
  python manage.py startapp training_tracker_app
  ```
- Configure settings.py:
  - Add `rest_framework`, `corsheaders`, and `training_tracker_app` app to `INSTALLED_APPS`
  - Configure `CORS_ALLOWED_ORIGINS` (start with http://localhost:3000 for React development)
  - Add `corsheaders.middleware.CorsMiddleware` to `MIDDLEWARE`
#### Frontend (React)
- Install Node.js and npm
- Use Vite to bootstrap frontend project:
  ```
  npm create vite frontend .
  ```
- `cd frontend` and run `npm install`
- Install `axios` for making API requests
  ```
  npm install axios
  ```
- Install `react-router-dom` for navigation
  ```
  npm install react-router-dom
  ```
### Key Entities
- Dogs
- Owners (Clients)
- Trainers (Maybe? Or is it just the user? Assume one trainer/user initially for simplicity, but keep scalability in mind).
- Training Plans (A set of goals or modules for a dog)
- Training Sessions/Appointments (Specific scheduled events)
- Progress Notes/Updates (Linked to sessions or skills)
- Skills/Behaviors (Specific things being taught, e.g., "Sit", "Stay", "Leash Walking")
### Core Features (MVP - Minimum Viable Product)
- **CRUD for Clients:** Add, View, Edit, Delete client information (Name, Contact Info)
- **CRUD for Dogs:** Add, View, Edit, Delete dog information (Name, Breed, Age, associated Client).
- **CRUD for Training Plans:** Create template plans (e.g., "Puppy Basics", "Advanced Obedience") with defined goals or steps.
- **CRUD for Skills/Behaviors:** Add, View, Edit, Delete (Specific things being taught, e.g., "Sit", "Stay", "Leash Walking)
- **Assign Plans to Dogs:** Link a specific dog to a training plan.
- **CRUD for Appointments:** Schedule, View, Edit, Delete training appointments (linking Dog, Date/Time, Location, maybe associated Plan).
- **Record Progress:** Add notes to appointments or directly to a dog's profile regarding specific skills or plan progress.
- **View Dog Progress:** See a history of appointments and notes for a specific dog.
- View upcoming/past appointments (calendar/list view)
## Phase II 
### Backend Development (Django)
Focus on getting the data structure and API endpoints ready.
#### Data Modeling (training_tracker/models.py): 
Define database tables as Django models
- `Client`: Fields like `name`, `email`, `phone`.
- `Dog`: Fields like `name`, `breed`, `age`, `client` (ForeignKey to `Client`), `notes` (TextField, optional)
- `Trainer`
- `TrainingPlan`: Fields like `name`, `description`, `goals` (TextField).
- `DogTrainingPlan` (Intermediate Model or logic):\Need a way to track which dog is on which plan and their progress within it. Maybe a `current_plan` (ForeignKey to `TrainingPlan` on `Dog` model, nullable=True) and `plan_progress_notes` (TextField on `Dog` or a separate `ProgressNote` model).
- `Skill`: Fields like name, description. Could link skills to TrainingPlan (ManyToMany) or track progress per skill.
- `Appointment`: Fields like dog (ForeignKey to Dog), date_time, duration, location, notes (TextField), completed (BooleanField).
- `ProgressNote`: Fields like dog (ForeignKey), appointment (ForeignKey, nullable=True), skill (ForeignKey, nullable=True), note_text, date_recorded (auto_now_add=True). This offers more granular tracking than just notes on appointments.
#### Migrations
Run `python manage.py makemigrations training_tracker`
Run `python manage.py migrate` to apply the changes to database
#### Admin Interface 
`training_tracker/admin.py`
- Register models to easily add/edit data via the Django admin panel (`/admin/`)
- Create a superuser: `python manage.py createsuperuser`
#### API Development (Django REST Framework):
- Serializers (`training_tracker/serializers.py`): Define how models are converted to/from JSON. Create serializers for `Client`, `Dog`, `Appointment`, `TrainingPlan`, `ProgressNote`, etc. Use `ModelSerializer`.
- Views (`training_tracker/views.py`): Create API views. Use DRF's `ModelViewSet` for quick CRUD endpoints for each model. These handle GET (list, detail), POST, PUT/PATCH, DELETE requests.
- URLs (`training_tracker/urls.py` and `backend/urls.py`):
  - In `training_tracker/urls.py`, use DRF's `DefaultRouter` to automatically generate URLs for your ViewSets.
  - In `backend/urls.py`, include the URLs from your `training_tracker` app under a base path like `/api/`.
#### Testing: 
Use the Django admin and Postman to test API endpoints before building the frontend.
