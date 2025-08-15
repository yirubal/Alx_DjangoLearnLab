## Documentation
- **Authentication Guide:** [docs/authentication.md](docs/authentication.md)
- Here’s the requested documentation for the authentication system.

Authentication Documentation

1) Overview
- The application uses Django’s built-in authentication (session-based) for login/logout and a custom registration/profile update flow.
- Key features:
  - Registration with username, password, and email (with uniqueness validation).
  - Login and logout using Django’s built-in views.
  - Authenticated profile update for first_name, last_name, and email.
  - Flash messages for user feedback (e.g., “Account created…”, “Profile updated.”).
  - Namespaced URLs (blog:...) to keep routes unambiguous.

2) Components

- URLs
  - Project-level URLconf includes the blog app’s URLconf at the root path.
  - App-level URLconf exposes:
    - '' → Home page
    - 'login/' → Login
    - 'logout/' → Logout
    - 'register/' → Registration
    - 'profile/' → Profile update (requires authentication)
  - Use namespaced reverses like 'blog:login' and 'blog:profile'.

- Views
  - Registration: A CreateView backed by a CustomUserCreationForm. On success, redirects to login and shows a success message.
  - Login: Django’s built-in LoginView renders the login template, authenticates on POST, and creates a session on success. Respects ?next= for redirects.
  - Logout: Django’s built-in LogoutView ends the session and renders the logged out template (or redirects per settings).
  - Profile: An UpdateView with LoginRequiredMixin that edits the current logged-in user instance and shows a success message on save.
  - Home: A simple TemplateView for the landing page.

- Forms
  - CustomUserCreationForm: Extends Django’s user creation to include email validation (ensuring uniqueness). Passwords are validated and hashed by Django.
  - ProfileUpdateForm: A ModelForm for the user model to edit first_name, last_name, and email. Email uniqueness is enforced via clean_email; when editing, it excludes the current user’s record.

- Templates
  - registration/login.html: Login form (username/password) with CSRF protection and message display.
  - registration/logged_out.html: Logout confirmation with a link back to login.
  - registration/register.html: Registration form with CSRF protection, field errors, and non-field errors.
  - blog/pages/profile.html: Profile update form for first_name, last_name, and email with CSRF protection.
  - blog/pages/home.html and base.html: Layout and navigation; ensure links use namespaced URL tags (e.g., {% url 'blog:login' %}).

- Flash messages
  - Uses django.contrib.messages to show success notifications after registration and profile updates.
  - Ensure the base template renders messages (loop through messages).

- Access control and sessions
  - LoginRequiredMixin on the profile view restricts access to authenticated users.
  - Unauthenticated access to profile triggers a redirect to login with a next parameter.
  - Successful login establishes a session; logout clears it.

- Important setup note
  - reverse_lazy should be imported from Django’s URL utilities. Ensure:
    - Import reverse_lazy from django.urls, not from any other package.

3) User Flows

- Registration
  - User opens the registration page.
  - Submits username, password (with confirmation), and email.
  - If valid and email is unique, the user is created, a success message is shown, and the user is redirected to the login page.
  - On validation error, field-specific errors and non-field errors are displayed.

- Login
  - User opens the login page.
  - Submits username and password.
  - On success, an authenticated session is created. If a next parameter is present, user is redirected there; otherwise to the default.
  - On failure, the form is re-rendered with errors.

- Logout
  - User triggers logout.
  - Session is cleared and the logged out template is displayed (or redirect, depending on configuration).

- Profile Update
  - Authenticated user navigates to the profile page.
  - Form is pre-filled with current first_name, last_name, and email.
  - User updates fields and submits.
  - If valid (including unique email), changes are saved; a success message is displayed; the user remains on profile.
  - If invalid, errors are displayed inline.

4) Setup and Configuration

- Ensure the app is in INSTALLED_APPS:
  - django.contrib.auth
  - django.contrib.contenttypes
  - django.contrib.sessions
  - django.contrib.messages
  - django.contrib.staticfiles
  - blog

- Middleware must include:
  - AuthenticationMiddleware
  - SessionMiddleware
  - MessageMiddleware
  - CSRF-related middleware

- Template configuration:
  - DIRS includes your templates directory.
  - context processors include messages and request.

- URLs:
  - Project URLconf includes the blog URLs at root.

- reverse_lazy import:
  - Ensure reverse_lazy is imported from django.urls.

- Database:
  - Run migrations before use:
    - python manage.py migrate

- Superuser (optional for admin access):
  - python manage.py createsuperuser

- Run server:
  - python manage.py runserver

5) How to Test (Manual)

- Registration
  - Navigate to the registration page.
  - Submit valid username, strong password (twice), and a unique email.
  - Expected: Redirect to login; success message shown.
  - Negative tests:
    - Reuse an existing email → Expect “email already in use” error.
    - Password mismatch → Expect form error.
    - Missing required fields → Expect field errors.

- Login
  - Use correct credentials for an existing user.
  - Expected: Authenticated session; redirect to next if provided or to default.
  - Negative tests:
    - Wrong password → Expect form error and stay on login.
    - Inactive user (if applicable) → Expect login failure.

- Logout
  - While logged in, log out.
  - Expected: Session cleared; logged out page displayed.

- Profile Update
  - Visit the profile page while logged in.
  - Expected: first_name, last_name, and email fields are pre-populated with current values.
  - Change first_name/last_name and save → Expect success message and updated data persisted.
  - Change email to an email owned by another user → Expect “email already in use” error.
  - Access profile while logged out → Expect redirect to login with next parameter.

- Navigation and messages
  - Verify navbar links for login/logout/register/profile point to namespaced URLs and render correctly.
  - Ensure flash messages display in the base template.

6) How to Test (Automated)

- Unit/integration tests to cover:
  - Registration success and validation failures (duplicate email, weak password, mismatch).
  - Login success, invalid password, and next parameter redirect.
  - Logout clears the session.
  - Profile view requires login and redirects when anonymous.
  - Profile update persists changes and enforces email uniqueness.
  - Templates render expected forms and include CSRF token.



7) Deliverables

- Code Files (authentication-related)
  - blog/views.py: RegisterView (registration), ProfileView (profile edit), HomeView (home). Login/Logout are provided by Django’s auth views and are wired via URLs.
  - blog/forms.py: CustomUserCreationForm (registration), ProfileUpdateForm (profile editing with clean_email uniqueness).
  - blog/urls.py: Routes for home, login, logout, register, profile (namespaced under app_name).
  - django_blog/urls.py: Includes blog URLs at root.

- Template Files
  - templates/registration/login.html
  - templates/registration/register.html
  - templates/registration/logged_out.html
  - templates/blog/pages/profile.html
  - templates/blog/pages/home.html
  - templates/base.html (renders messages and navigation)

- Documentation
  - This document: Explains the architecture, setup, and user flows, and provides testing instructions (manual and automated).

8) Troubleshooting and Tips

- reverse_lazy import error
  - Ensure reverse_lazy comes from django.urls. If imported elsewhere, update the import.

- Email uniqueness during profile edit
  - clean_email must exclude the current instance to avoid false positives.

- Form fields not pre-populating
  - Ensure the profile view binds the instance to the form (the UpdateView with get_object returning request.user handles this).
  - Avoid redefining model fields on ModelForms unless you set initial values accordingly.

- NoReverseMatch errors in templates
  - Always use named URL patterns (namespaced) in templates: {% url 'blog:login' %}, {% url 'blog:profile' %}.

- Messages not appearing
  - Verify MessageMiddleware is enabled and the base template renders messages.

If you want me to generate example tests tailored to your exact form field names or to review your forms for first_name/last_name pre-population, let me know and I can adapt the examples precisely.