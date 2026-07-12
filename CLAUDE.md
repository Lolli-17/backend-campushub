# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Django REST Framework backend for **CampusHub**, a student-housing / campus management app. It's deployed on PythonAnywhere (see `ALLOWED_HOSTS`, `DATABASES`, static files via Whitenoise in `backend_def/settings.py`) and serves at least two frontends (CORS is opened for `localhost:3000` and two hosted frontend origins).

The user working on this repo was new to Django when it was built, so treat the code as a learning project with real inconsistencies rather than an intentional design — see "Known issues" below before trusting migrations, permissions, or model relationships at face value.

## Commands

```bash
# install deps (mysqlclient needs the MySQL client headers installed on the host OS)
pip install -r requirements.txt

# run the dev server
python manage.py runserver

# migrations
python manage.py makemigrations
python manage.py migrate

# create an admin user
python manage.py createsuperuser

# tests (campus_management/tests.py is currently empty boilerplate — no real tests exist yet)
python manage.py test

# Celery worker / beat (only meaningful once a real broker URL is configured, see Known issues)
celery -A backend_def worker -l info
celery -A backend_def beat -l info
```

There is no linter/formatter configured (no flake8/black/ruff/isort config anywhere in the repo).

## Architecture

- **`backend_def/`** — the Django project: settings, root `urls.py`, WSGI/ASGI, Celery app bootstrap (`celery.py`), and a shared `models.py` containing `BaseModel`, an abstract base (UUID primary key + `created_at`/`updated_at`) that every model in the app inherits from.
- **`campus_management/`** — the single Django app holding the entire domain: `models.py`, `serializers.py`, `views.py`, `urls.py`, `choices.py` (all `TextChoices` enums in one place), `signal.py`, `tasks.py` (Celery tasks), and `mixin.py` (an unused-looking generic `ChoiceFieldMixin` — check before assuming any model actually uses it).

### Domain model

`Campus` → `Apartment` → `CustomUser` (a resident, via `apartment` FK). Feature models hang off a resident + apartment pair:
- `Guest` — visitor tracking with check-in/status workflow (`IN_ARRIVO` / `IN_HOUSE` / `OFF_HOUSE`) and a computed "time in house".
- `Package` — delivery tracking.
- `CommonAreaReservation`, `CleaningReservation`, `FaultReport` — booking/maintenance requests.
- `ElectricityReading` — utility meter readings per resident; the latest value is also denormalized onto `CustomUser.lastElectricityReading`.
- `GlobalNotifications` (per campus) / `UserNotifications` (per resident) — scheduled announcements with `PROGRAMMATA`/`INVIATA` status.

### Auth

- `CustomUser` (`AUTH_USER_MODEL`) extends `AbstractUser` + `BaseModel`, adding a `role` field (`RoleChoices`: Resident Manager, Front Office(+Manager), Community Ambassador, Marketing, Hotel, Student).
- Three DRF authentication classes are all enabled simultaneously: Basic, Session, and SimpleJWT (`DEFAULT_AUTHENTICATION_CLASSES` in settings). A DRF authtoken is also auto-created for every user via a `post_save` signal (`signal.py`), though nothing currently seems to consume it over Basic/Session/JWT.
- Login is custom: `MyTokenObtainPairSerializer` (`serializers.py`) overrides SimpleJWT to authenticate by **`first_name` + `last_name` + `password`**, not username — a deliberate but non-standard choice, exposed at `POST /user/login`.
- Auth endpoints (`/user/login`, `/user/logout`, `/user/register`, `/user/token/refresh`, `/user/get-current`) are declared directly in `backend_def/urls.py`; all other resources are routed through a DRF `DefaultRouter` in `campus_management/urls.py` under `/api/`.
- Permissions mostly rely on Django's built-in group/model-permission system via `DjangoModelPermissions` per viewset — `role` is **not** wired into a permission class anywhere, so it's informational unless permissions are separately assigned per group in the admin. The one exception is ad hoc role checks inside `GuestViewSet.perform_update` / `GuestSerializer` (only Student/Hotel roles with an assigned apartment can be set as a `Guest.resident`).

## Known issues (read before changing related code)

- **`CustomUserViewSet` has no `permission_classes`**, unlike every other viewset — it falls back to the global default (`IsAuthenticated` only, no `DjangoModelPermissions`). Any authenticated user, regardless of role, can currently list/create/edit/delete any other user through `/api/custom-users/`.
- **Migrations are out of sync with `models.py`.** E.g. migration `0003` defines `resident` on `Guest`/`Package`/`CleaningReservation`/`CommonAreaReservation`/`FaultReport` as `OneToOneField`, but `models.py` currently defines them as `ForeignKey`; the initial migration also still references a `Room`/`ElectricityMeter` model that no longer exists under those names. Don't assume either migrations or `models.py` reflect the real deployed schema — check with the actual database, and run `makemigrations` to see the true pending diff, before making schema changes.
- `CustomUser.campus` is a `OneToOneField`, meaning at most one user can ever be linked to a given campus directly — this looks like it should be a `ForeignKey` given the `Campus → Apartment → many residents` model, but hasn't been fixed.
- `ElectricityReading.__str__` references `self.meter.room.number`, an attribute that doesn't exist on the model (the model has no `meter` field) — calling `str()` on this model will raise `AttributeError`.
- `choices.py` defines `StatusChoices`, `CleaningTypeChoices`, and `FaultTypeChoices`, but the corresponding model fields (`CleaningReservation.cleaningType`, `FaultReport.faultType`, various `status` fields) are plain `CharField`s without `choices=` wired up — these enums are currently dead/aspirational.
- **Celery is not actually functional as configured.** `backend_def/celery.py` and `tasks.py` define a beat schedule (`update_guest_nights` daily, `activate_scheduled_notifications` every minute), but `CELERY_BROKER_URL`/`CELERY_RESULT_BACKEND` are commented out in `settings.py` (a Redis Cloud instance was intentionally disabled to avoid cost). `campus_management/commands/process_daily_tasks.py` duplicates the same logic as a management command intended to be cron'd instead — **but it lives in `campus_management/commands/`, not `campus_management/management/commands/`**, so Django does not register it; `python manage.py process_daily_tasks` will fail with "Unknown command" until it's moved into a proper `management/commands` package.
- `GlobalNotifications.sendingTime` defaults to `timezone.now()` called at import/class-definition time (not `timezone.now`, a callable) — every instance without an explicit value gets the timestamp of when the server process started, not creation time.
- `settings.py` has `SECRET_KEY`, the MySQL password, and `DEBUG = True` hardcoded and committed — there's no environment-based config split between dev/prod. Be careful not to further entrench this if adding config, and flag it if asked about production readiness.
