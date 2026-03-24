# Client User Manual

## Overview

As a **Client**, you can submit support tickets, track their progress, communicate with the support team through comments, and upload file attachments. You can only see your own tickets — not tickets from other users.

---

## Table of Contents

- [Logging In](#logging-in)
- [Dashboard — My Tickets](#dashboard--my-tickets)
- [Creating a Ticket](#creating-a-ticket)
- [Viewing Ticket Details](#viewing-ticket-details)
- [Communicating with Support](#communicating-with-support)
- [Logging Out](#logging-out)
- [Submitting via Email](#submitting-via-email)

---

## Logging In

1. Open the application at **http://localhost:5173**
2. Enter your email and password:
   - Default test accounts:
     - `john@client.com` / `client123`
     - `jane@client.com` / `client123`
     - `bob@client.com` / `client123`
3. Click **Sign in**
4. You will be taken to your ticket dashboard

---

## Dashboard — My Tickets

After logging in, you see the **Tickets** page showing only your tickets.

### What You See
- A table listing all tickets you have submitted
- Each row shows: **Subject**, **Category**, **Priority**, **Status**, **Date**
- Status badges tell you where your ticket stands:
  - **Blue (Open)** — Your ticket has been received and is waiting to be picked up
  - **Yellow (In Progress)** — A support agent is actively working on your issue
  - **Green (Resolved)** — The issue has been fixed; review and confirm
  - **Gray (Closed)** — The ticket is complete, no further action needed

### Filtering Your Tickets
Use the filter controls at the top to find specific tickets:
- **Status** — Show only Open, In Progress, Resolved, or Closed tickets
- **Priority** — Filter by priority level
- **Category** — Filter by ticket category

### Opening a Ticket
Click any ticket row to see full details and the conversation history.

---

## Creating a Ticket

This is how you submit a new support request.

### Step 1: Open the Form
Click **New Ticket** in the left sidebar.

### Step 2: Fill In the Details

| Field | Description | Required |
|-------|------------|----------|
| **Subject** | A brief summary of your issue (e.g., "Cannot log into portal") | Yes |
| **Category** | The type of issue — choose the most appropriate: | Yes |
| | - **Bug** — Something is broken or not working correctly | |
| | - **Feature** — A request for new functionality | |
| | - **Access** — Permission or account access issues | |
| | - **Infra** — Server, network, or infrastructure problems | |
| | - **General** — Questions or general requests | |
| | - **Urgent** — Time-sensitive critical issues | |
| **Priority** | How urgent is this? | Yes |
| | - **Low** — Minor issue, no rush | |
| | - **Medium** — Normal priority (default) | |
| | - **High** — Important, needs attention soon | |
| | - **Critical** — Severe impact, needs immediate help | |
| **Project** | The name of the project or product this relates to | Yes |
| **Description** | A detailed explanation of your issue. Include: | Yes |
| | - What you were trying to do | |
| | - What happened instead | |
| | - Steps to reproduce (if applicable) | |
| | - Any error messages you saw | |

### Step 3: Attach Files (Optional)

If you have screenshots, logs, or documents to share:

1. **Click** the dashed upload area, or **drag & drop** files onto it
2. You'll see each file listed with:
   - File type icon (image, document, spreadsheet, archive)
   - Filename
   - File size
   - **X** button to remove it
3. A summary shows the total number of files and combined size

**File limits:**
- Maximum **10MB** per individual file
- Maximum **25MB** total across all files
- Supported formats: PNG, JPG, GIF, PDF, DOC, DOCX, XLS, XLSX, CSV, TXT, ZIP, TAR.GZ, LOG

### Step 4: Submit
Click **Create Ticket**. You'll be taken to your new ticket's detail page.

---

## Viewing Ticket Details

Click on any ticket from your dashboard to see its full details.

### Ticket Header
- **Ticket ID** — A unique number (e.g., #15) for reference
- **Subject** — Your ticket summary
- **Status badge** — Current status (color-coded)

### Description
The full description you provided when creating the ticket.

### Attachments
If you attached files, they appear here:
- Each file shows its name, size, and type
- **Preview** — Click to open images or PDFs in a new browser tab
- **Download** — Click to save the file to your computer

### Comments
The conversation history between you and the support team:
- Each comment shows the author's email, timestamp, and whether it came from web or email
- Comments are listed chronologically (oldest first)

### Details Sidebar (right side)
- **Category** — Bug, Feature, etc.
- **Project** — Which project the ticket is for
- **Priority** — Low, Medium, High, Critical
- **Reporter** — Your email address
- **Created** — When the ticket was submitted
- **SLA Deadline** — When the support team should respond/resolve by (based on priority)

---

## Communicating with Support

### Adding a Comment

1. Open your ticket
2. Scroll to the bottom of the page
3. Type your message in the **Add a comment** text box
4. Click **Send**
5. Your comment appears immediately in the thread

### When to Comment
- **Provide additional information** — Share details the support team requested
- **Confirm resolution** — Let the team know if the fix worked
- **Report changes** — If the issue changed or you found new information
- **Ask for updates** — If your ticket hasn't been addressed within the expected timeframe

### Tips for Effective Communication
- Be specific — include exact error messages, URLs, or screenshots
- If the issue is resolved, say so clearly so the ticket can be closed
- If the fix didn't work, explain what still isn't working

---

## Logging Out

1. Click **Logout** at the bottom of the left sidebar
2. Your session is cleared and you return to the login page

---

## Submitting via Email

You can also create tickets by sending an email to the helpdesk email address (configured by your admin).

### Email Format

**Subject line:**
```
[Category] Brief summary
```
Example: `[Bug] Login page shows 500 error`

**Email body:**
```
Project: Web Portal
Priority: High
Description:
After resetting my password, the login page returns a 500 error.
The reset email was received and the link worked fine.
```

**Attachments:** You can attach files to your email. Same limits apply (10MB per file, 25MB total).

### How It Works
1. Your email is automatically parsed and converted into a ticket
2. If the format doesn't match, you'll receive an auto-reply with the correct template
3. Replies to ticket notification emails are threaded as comments on the existing ticket

---

## Navigation

Your sidebar contains:
- **Tickets** — View your ticket list
- **New Ticket** — Create a new support request

You do **not** see Users or Settings pages — those are for admin staff only.

---

## Permissions Summary

| Action | Client |
|--------|--------|
| View own tickets | Yes |
| View other users' tickets | No |
| Create tickets | Yes |
| Update ticket status | No |
| Assign agents | No |
| Add comments (own tickets) | Yes |
| Upload attachments | Yes |
| Download attachments (own tickets) | Yes |
| View users | No |
| View settings | No |

---

## Need Help?

If you're unable to log in or access the system, contact your company's IT administrator directly. They can reset your password or verify your account status.
