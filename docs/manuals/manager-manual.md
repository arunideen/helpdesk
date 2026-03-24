# Manager User Manual

## Overview

As a **Manager**, you have oversight of tickets and team members. You can view all tickets, assign agents, change ticket statuses, manage comments, and view users and system settings. You cannot create or edit users or modify settings.

---

## Table of Contents

- [Logging In](#logging-in)
- [Dashboard — Ticket List](#dashboard--ticket-list)
- [Creating a Ticket](#creating-a-ticket)
- [Viewing Ticket Details](#viewing-ticket-details)
- [Viewing Users](#viewing-users)
- [Viewing Settings](#viewing-settings)
- [Logging Out](#logging-out)

---

## Logging In

1. Open the application at **http://localhost:5173**
2. Enter your credentials:
   - Default: `manager@company.com` / `manager123`
3. Click **Sign in**

---

## Dashboard — Ticket List

The **Tickets** page is your main workspace.

### What You See
- A table showing all tickets across the system
- Each row displays: **Subject**, **Category**, **Priority**, **Status**, **Reporter**, **Date**
- Color-coded status badges:
  - **Blue** — Open
  - **Yellow** — In Progress
  - **Green** — Resolved
  - **Gray** — Closed

### Filtering Tickets
Use the filter controls to focus on specific tickets:
- **Status** — Open, In Progress, Resolved, Closed
- **Priority** — Low, Medium, High, Critical
- **Category** — Bug, Feature, Access, Infra, General, Urgent

### Opening a Ticket
Click any ticket row to view its full details.

---

## Creating a Ticket

1. Click **New Ticket** in the left sidebar
2. Fill in the form:
   - **Subject** — Brief summary (required)
   - **Category** — Bug, Feature, Access, Infra, General, or Urgent
   - **Priority** — Low, Medium, High, or Critical
   - **Project** — Project name (required)
   - **Description** — Detailed description (required)
3. **Attachments** (optional):
   - Click the upload area or drag & drop files onto it
   - Supported: png, jpg, pdf, doc, xls, csv, txt, zip, and more
   - Max 10MB per file, 25MB total
   - Remove unwanted files by clicking the **X** button next to each
4. Click **Create Ticket**

---

## Viewing Ticket Details

### Main Area (left side)
- **Ticket header** — Ticket ID number, subject, and status badge
- **Description** — The full issue description
- **Attachments** — Files attached to the ticket
  - Click **Preview** to open images/PDFs in a new tab
  - Click **Download** to save any file
- **Comments** — Conversation history with author, timestamp, and source
- **Add Comment** — Type in the text box and click **Send** to add your comment

### Sidebar (right side)
- **Details** — Category, Project, Priority, Reporter, Created date, SLA Deadline
- **Actions**:
  - **Status** — Change the ticket status using the dropdown
  - **Assign to Agent** — Select an agent and click the assign button

### Changing Ticket Status
1. Use the **Status** dropdown in the Actions section
2. Select the new status — the change saves immediately

### Assigning an Agent
1. Select an agent from the **Assign to Agent** dropdown
2. Click the assign button (person+ icon)
3. The ticket is now assigned and the page refreshes

---

## Viewing Users

Click **Users** in the left sidebar (under ADMIN section).

### What You Can Do
- View the complete list of all users
- See each user's **Name**, **Email**, **Role**, **Team**, and **Status**
- Filter by role using the dropdown

### What You Cannot Do
- Create new users (Admin only)
- Edit existing users (Admin only)
- Toggle user status (Admin only)

---

## Viewing Settings

Click **Settings** in the left sidebar (under ADMIN section).

### What You Can Do
- View all system configuration settings
- See settings grouped by category: General, Email, Attachments, Auto-Reply

### What You Cannot Do
- Edit or save settings (Admin only)

---

## Logging Out

1. Click **Logout** at the bottom of the left sidebar
2. You are returned to the login page

---

## Permissions Summary

| Action | Manager |
|--------|---------|
| View all tickets | Yes |
| Create tickets | Yes |
| Update ticket status | Yes |
| Assign agents | Yes |
| Add comments | Yes |
| Upload attachments | Yes |
| Download attachments | Yes |
| View all users | Yes |
| Create users | No |
| Edit users | No |
| Toggle user status | No |
| View settings | Yes |
| Edit settings | No |
