# Admin User Manual

## Overview

As an **Admin**, you have full access to the Helpdesk system. You can manage all tickets, users, and system settings. This manual covers everything you need to know.

---

## Table of Contents

- [Logging In](#logging-in)
- [Dashboard — Ticket List](#dashboard--ticket-list)
- [Creating a Ticket](#creating-a-ticket)
- [Viewing Ticket Details](#viewing-ticket-details)
- [Managing Users](#managing-users)
- [System Settings](#system-settings)
- [Logging Out](#logging-out)

---

## Logging In

1. Open the application at **http://localhost:5173**
2. Enter your email and password:
   - Default: `admin@company.com` / `admin123`
3. Click **Sign in**
4. You will be redirected to the ticket dashboard

---

## Dashboard — Ticket List

After logging in, you see the **Tickets** page — the main dashboard.

### What You See
- A table of all tickets in the system
- Each row shows: **Subject**, **Category**, **Priority**, **Status**, **Reporter**, **Date**
- Status badges are color-coded:
  - **Blue** — Open
  - **Yellow** — In Progress
  - **Green** — Resolved
  - **Gray** — Closed

### Filtering Tickets
Use the filter controls at the top to narrow results:
- **Status** — Filter by Open, In Progress, Resolved, Closed
- **Priority** — Filter by Low, Medium, High, Critical
- **Category** — Filter by Bug, Feature, Access, Infra, General, Urgent

### Opening a Ticket
Click any ticket row to view its full details.

---

## Creating a Ticket

1. Click **New Ticket** in the left sidebar
2. Fill in the form:
   - **Subject** — Brief summary of the issue (required)
   - **Category** — Select from: Bug, Feature, Access, Infra, General, Urgent
   - **Priority** — Select from: Low, Medium, High, Critical
   - **Project** — Enter the project name (required)
   - **Description** — Detailed description of the issue (required)
3. **Attachments** (optional):
   - Click the upload area or drag & drop files
   - Supported formats: png, jpg, pdf, doc, xls, csv, txt, zip, and more
   - Max 10MB per file, 25MB total
   - You can remove files before submitting by clicking the **X** button
4. Click **Create Ticket**
5. You will be redirected to the new ticket's detail page

---

## Viewing Ticket Details

The ticket detail page has two sections:

### Main Area (left)
- **Ticket header** — ID, subject, status badge
- **Description** — Full ticket description
- **Attachments** — List of uploaded files with Preview (for images/PDFs) and Download links
- **Comments** — Full conversation thread with timestamps and source (web/email)
- **Add Comment** — Text box at the bottom to add a new comment

### Sidebar (right)
- **Details panel** — Category, Project, Priority, Reporter, Created date, SLA Deadline
- **Actions panel** (staff only):
  - **Status** — Change ticket status via dropdown (Open → In Progress → Resolved → Closed)
  - **Assign to Agent** — Select an agent from the dropdown and click the assign button

### Changing Ticket Status
1. In the sidebar **Actions** section, use the **Status** dropdown
2. Select the new status
3. The change is saved immediately

### Assigning an Agent
1. In the sidebar **Actions** section, use the **Assign to Agent** dropdown
2. Select an agent
3. Click the assign button (person+ icon)

---

## Managing Users

Click **Users** in the left sidebar (under ADMIN section).

### Viewing Users
- See all users in a table: **Name**, **Email**, **Role**, **Team**, **Status**, **Actions**
- Use the **role filter dropdown** to show only specific roles (Admin, Manager, Agent, Client)

### Creating a New User
1. Click the **Add User** button (top right)
2. Fill in the modal form:
   - **Name** — Full name (required)
   - **Email** — Valid email address (required, must be unique)
   - **Password** — Minimum 6 characters (required)
   - **Role** — Select: Admin, Manager, Agent, or Client
   - **Team** — Optional team name
3. Click **Create User**
4. The user list refreshes automatically

### Editing a User
1. Click **Edit** on any user row
2. Modify fields in the modal:
   - **Name** — Update the display name
   - **Email** — Shown but not editable (read-only)
   - **Role** — Change the user's role
   - **Team** — Update or clear the team
   - **Active toggle** — Enable or disable the user account
3. Click **Save Changes**

### Toggling User Status
- Click the **Active** or **Disabled** badge in the Status column to instantly toggle a user's account status
- Disabled users cannot log in

---

## System Settings

Click **Settings** in the left sidebar (under ADMIN section).

### Viewing Settings
Settings are organized into categories displayed as expandable sections:
- **General** — App name, session timeout
- **Email** — IMAP/SMTP server configuration, credentials, SSL/TLS toggles, poll interval
- **Attachments** — Max file size, max total size, allowed file extensions
- **Auto-Reply** — Cooldown period for auto-reply emails

### Editing Settings
1. Click on any setting value to edit it
2. Input types are automatic based on the setting:
   - **Text fields** — For strings like server addresses
   - **Number fields** — For numeric values like port numbers and timeouts
   - **Toggle switches** — For boolean values like SSL/TLS on/off
   - **Password fields** — For sensitive values like email passwords (with show/hide toggle)
3. A blue dot appears next to changed settings
4. The **Save Changes** and **Discard** buttons appear at the bottom when changes exist

### Saving Settings
1. Edit one or more settings
2. Click **Save Changes** to apply all modifications at once
3. A success message confirms the save
4. Click **Discard** to revert all unsaved changes

---

## Logging Out

1. Click the **Logout** button at the bottom of the left sidebar
2. You will be returned to the login page
3. Your session token is cleared

---

## Permissions Summary

| Action | Admin |
|--------|-------|
| View all tickets | Yes |
| Create tickets | Yes |
| Update ticket status | Yes |
| Assign agents | Yes |
| Add comments | Yes |
| Upload attachments | Yes |
| Download attachments | Yes |
| View all users | Yes |
| Create users | Yes |
| Edit users | Yes |
| Toggle user status | Yes |
| View settings | Yes |
| Edit settings | Yes |
