# Agent User Manual

## Overview

As an **Agent**, you are the primary support responder. You handle tickets assigned to you, update their status, communicate with reporters through comments, and can assign tickets to other agents. You do not have access to the Users or Settings pages.

---

## Table of Contents

- [Logging In](#logging-in)
- [Dashboard — Ticket List](#dashboard--ticket-list)
- [Creating a Ticket](#creating-a-ticket)
- [Viewing Ticket Details](#viewing-ticket-details)
- [Working on Tickets](#working-on-tickets)
- [Logging Out](#logging-out)

---

## Logging In

1. Open the application at **http://localhost:5173**
2. Enter your credentials:
   - Default accounts:
     - `agent@company.com` / `agent123` (Support team)
     - `devops@company.com` / `agent123` (Infrastructure team)
     - `qa@company.com` / `agent123` (Quality team)
3. Click **Sign in**

---

## Dashboard — Ticket List

The **Tickets** page shows all tickets in the system.

### What You See
- A table of all tickets (not just yours)
- Each row shows: **Subject**, **Category**, **Priority**, **Status**, **Reporter**, **Date**
- Color-coded status badges:
  - **Blue** — Open (new, unhandled)
  - **Yellow** — In Progress (being worked on)
  - **Green** — Resolved (fix applied, awaiting confirmation)
  - **Gray** — Closed (completed)

### Filtering Tickets
Use the filter controls at the top:
- **Status** — Show only tickets in a specific state
- **Priority** — Focus on Critical or High priority tickets first
- **Category** — Filter by ticket type (Bug, Feature, Infra, etc.)

### Opening a Ticket
Click any row to open the ticket detail page.

---

## Creating a Ticket

Agents can create tickets on behalf of users or for internal issues.

1. Click **New Ticket** in the left sidebar
2. Fill in the required fields:
   - **Subject** — Brief summary of the issue
   - **Category** — Select the appropriate category
   - **Priority** — Set based on urgency and impact
   - **Project** — The project this relates to
   - **Description** — Provide a detailed description
3. **Attachments** (optional):
   - Click the dashed upload area or drag & drop files
   - You'll see each file listed with its name, size, and a remove button
   - Supported: images, documents, spreadsheets, archives, logs
   - Limits: 10MB per file, 25MB total
4. Click **Create Ticket**
5. You'll be taken to the new ticket's detail page

---

## Viewing Ticket Details

### Main Content (left)

**Ticket Header**
- Ticket ID (e.g., #15)
- Subject line
- Status badge (color-coded)

**Description**
- The full description of the issue as submitted

**Attachments Section**
- Shows all files attached to the ticket
- For each attachment: filename, size, content type
- **Preview** — Opens images and PDFs in a new browser tab
- **Download** — Saves the file to your computer

**Comments Section**
- Chronological list of all comments
- Each comment shows: author email, timestamp, source (web or email)
- Comment attachments appear as clickable chips below the comment text

**Add Comment**
- Type your message in the text area at the bottom
- Click **Send** to post your comment
- The comment appears immediately in the thread

### Sidebar (right)

**Details Panel**
- Category, Project, Priority, Reporter email
- Created date and SLA Deadline (if applicable)

**Actions Panel**
- **Status dropdown** — Change the ticket's status
- **Assign to Agent** — Reassign the ticket to another agent

---

## Working on Tickets

### Typical Workflow

1. **Pick up a ticket** — Find an Open ticket and change its status to **In Progress**
2. **Investigate** — Read the description and attachments
3. **Communicate** — Add comments to ask questions or provide updates
4. **Resolve** — Once fixed, change status to **Resolved**
5. **Close** — After confirmation, change status to **Closed** (or let the reporter/manager do this)

### Changing Ticket Status

1. Open the ticket detail page
2. In the sidebar **Actions** section, find the **Status** dropdown
3. Select the new status:
   - **open** — Ticket needs attention
   - **in_progress** — You are actively working on it
   - **resolved** — The issue has been fixed
   - **closed** — Ticket is complete, no further action needed
4. The status updates immediately

### Assigning to Another Agent

If a ticket should be handled by a different agent:
1. Open the ticket detail page
2. In the sidebar, use the **Assign to Agent** dropdown
3. Select the appropriate agent
4. Click the assign button (person+ icon)

### Adding Comments

1. Scroll to the bottom of the ticket detail page
2. Type your message in the comment box
3. Click **Send**
4. Your comment is visible to all users with access to the ticket

### Best Practices
- Always add a comment when changing status, explaining what was done
- Set tickets to **In Progress** as soon as you start working on them
- Include relevant details in comments (error messages, steps taken, solutions applied)
- If you can't handle a ticket, reassign it to the appropriate agent rather than leaving it

---

## Logging Out

1. Click **Logout** at the bottom of the left sidebar
2. Your session is cleared and you return to the login page

---

## Navigation

Your sidebar contains:
- **Tickets** — View all tickets
- **New Ticket** — Create a new ticket

You do **not** see the Users or Settings pages — those are for Admin and Manager roles only.

---

## Permissions Summary

| Action | Agent |
|--------|-------|
| View all tickets | Yes |
| Create tickets | Yes |
| Update ticket status | Yes |
| Assign agents | Yes |
| Add comments | Yes |
| Upload attachments | Yes |
| Download attachments | Yes |
| View users | No |
| Create/Edit users | No |
| View settings | No |
| Edit settings | No |
