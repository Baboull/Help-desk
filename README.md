# - Modern Django Ticketing System

A high-performance, role-based ticketing system built with **Django 5.1** and **Tailwind CSS**. Featuring a sleek **2026 Flat Design** with a **GitHub-inspired Dark Mode** aesthetic.

![SupportHub Preview](https://img.shields.io/badge/UI-GitHub_Dark-blue?style=for-the-badge&logo=github)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css)

## Features

- **Role-Based Access Control**: Separate dashboards and permissions for **Clients**, **Staff**, and **Admins**.
- **️ Ticket Lifecycle**: Create, claim, update status (Open, In Progress, Resolved, Closed), and manage internal notes.
- **Real-time Chat**: Integrated messaging system within each ticket for direct client-agent communication.
- **GitHub Dark Mode**: Premium UI/UX featuring deep navy canvases, subtle borders, and a modern sidebar navigation.
- **Public Resolved Archive**: Searchable archive of all past resolved issues, accessible to all authenticated users for knowledge sharing.
- **User Settings**: Update profile information (first name, last name, email) and change passwords directly from the dashboard.
- **Secure**: Built-in Django authentication with custom User models and role validation decorators.

## Quick Start

### 1. Clone & Set Up

```bash
git clone https://github.com/Dera2Salles/Help-desk.git
cd Help-desk
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Initialize

```bash
python manage.py migrate
python manage.py setup_defaults
```

**Default Demo Credentials:**
- **Admin**: `admin` / `admin123`
- **Staff**: `staff` / `staff123`
- **Client**: `client` / `client123`


### 4. Launch Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to get started.

## User Roles & Permissions

- **Client**: Can create tickets, view their own ticket history, and chat with agents.
- **Staff/Agent**: Can claim unassigned tickets, update statuses, add private internal notes, and manage the support queue.
- **Admin**: Full access to the support queue and the Django Admin panel at `/admin/`.

## Project Structure

```bash
├── chat/           # Messaging logic and models
├── core/           # Redirection and base views
├── departments/    # Support department management
├── tickets/        # Core ticket management, dashboards, and archive
├── users/          # Custom User models, auth, and profile settings
├── ticketing_system/ # Main configuration
├── templates/      # Global templates with 2026 Dark UI
└── manage.py
```

## ️ Tech Stack

- **Backend**: Python, Django 5.1 (SQLite as default)
- **Frontend**: HTML5, Vanilla CSS, Tailwind CSS (via CDN)
- **Typography**: Inter (Google Fonts)

---

_Built with ️ for 2026 Support Excellence._
