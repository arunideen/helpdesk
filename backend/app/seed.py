"""Seed script: create default users, SLA policies, settings, and test data."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import User, SLAPolicy, Setting
from app.models.user import UserRole
from app.models.ticket import Ticket, TicketCategory, TicketPriority, TicketStatus
from app.models.ticket_comment import TicketComment, CommentSource
from app.models.ticket_assignment import TicketAssignment
from app.utils.auth import hash_password
from app.config import settings as app_settings


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ── Users ──────────────────────────────────────
    default_users = [
        ("Admin", "admin@company.com", "admin123", UserRole.ADMIN, "Engineering"),
        ("Sarah Manager", "manager@company.com", "manager123", UserRole.MANAGER, "Support"),
        ("Support Agent", "agent@company.com", "agent123", UserRole.AGENT, "Support"),
        ("DevOps Agent", "devops@company.com", "agent123", UserRole.AGENT, "Infrastructure"),
        ("QA Agent", "qa@company.com", "agent123", UserRole.AGENT, "Quality"),
        ("John Client", "john@client.com", "client123", UserRole.CLIENT, None),
        ("Jane Client", "jane@client.com", "client123", UserRole.CLIENT, None),
        ("Bob Client", "bob@client.com", "client123", UserRole.CLIENT, None),
    ]

    users_created = 0
    user_map = {}
    for name, email, pwd, role, team in default_users:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                name=name,
                email=email,
                hashed_password=hash_password(pwd),
                role=role,
                team=team,
            )
            db.add(user)
            db.flush()
            users_created += 1
            print(f"Created {role.value} user: {email} / {pwd}")
        user_map[email] = user

    if users_created:
        print(f"Total users created: {users_created}")

    # Create SLA policies
    sla_defaults = [
        (TicketPriority.LOW, 24, 72),
        (TicketPriority.MEDIUM, 8, 48),
        (TicketPriority.HIGH, 4, 24),
        (TicketPriority.CRITICAL, 1, 8),
    ]
    for priority, response_hours, resolution_hours in sla_defaults:
        existing = db.query(SLAPolicy).filter(SLAPolicy.priority == priority).first()
        if not existing:
            db.add(SLAPolicy(
                priority=priority,
                max_response_hours=response_hours,
                max_resolution_hours=resolution_hours,
            ))
            print(f"Created SLA policy: {priority.value} ({response_hours}h response, {resolution_hours}h resolution)")

    # Seed application settings
    default_settings = [
        # Email - IMAP
        ("IMAP_HOST", app_settings.IMAP_HOST, "email", "IMAP Host", "IMAP server hostname", "string"),
        ("IMAP_PORT", str(app_settings.IMAP_PORT), "email", "IMAP Port", "IMAP server port", "int"),
        ("IMAP_USER", app_settings.IMAP_USER, "email", "IMAP Username", "Email account username", "string"),
        ("IMAP_PASSWORD", app_settings.IMAP_PASSWORD, "email", "IMAP Password", "Email account password", "password"),
        ("IMAP_USE_SSL", str(app_settings.IMAP_USE_SSL), "email", "IMAP Use SSL", "Enable SSL for IMAP connection", "bool"),
        ("IMAP_POLL_INTERVAL_SECONDS", str(app_settings.IMAP_POLL_INTERVAL_SECONDS), "email", "Poll Interval (seconds)", "How often to check for new emails", "int"),
        # Email - SMTP
        ("SMTP_HOST", app_settings.SMTP_HOST, "email", "SMTP Host", "SMTP server hostname", "string"),
        ("SMTP_PORT", str(app_settings.SMTP_PORT), "email", "SMTP Port", "SMTP server port", "int"),
        ("SMTP_USER", app_settings.SMTP_USER, "email", "SMTP Username", "SMTP account username", "string"),
        ("SMTP_PASSWORD", app_settings.SMTP_PASSWORD, "email", "SMTP Password", "SMTP account password", "password"),
        ("SMTP_USE_TLS", str(app_settings.SMTP_USE_TLS), "email", "SMTP Use TLS", "Enable TLS for SMTP connection", "bool"),
        ("SMTP_FROM_EMAIL", app_settings.SMTP_FROM_EMAIL, "email", "From Email", "Sender email address for outgoing mail", "string"),
        ("SMTP_FROM_NAME", app_settings.SMTP_FROM_NAME, "email", "From Name", "Sender display name", "string"),
        # Attachments
        ("MAX_ATTACHMENT_SIZE_MB", str(app_settings.MAX_ATTACHMENT_SIZE_MB), "attachments", "Max File Size (MB)", "Maximum size per attachment in MB", "int"),
        ("MAX_TOTAL_ATTACHMENT_SIZE_MB", str(app_settings.MAX_TOTAL_ATTACHMENT_SIZE_MB), "attachments", "Max Total Size (MB)", "Maximum total attachment size per email in MB", "int"),
        ("ALLOWED_EXTENSIONS", app_settings.ALLOWED_EXTENSIONS, "attachments", "Allowed Extensions", "Comma-separated list of allowed file extensions", "string"),
        # Auto-reply
        ("AUTO_REPLY_COOLDOWN_SECONDS", str(app_settings.AUTO_REPLY_COOLDOWN_SECONDS), "auto_reply", "Cooldown (seconds)", "Minimum seconds between auto-replies to the same sender", "int"),
        # General
        ("APP_NAME", app_settings.APP_NAME, "general", "Application Name", "Name displayed in the UI and emails", "string"),
        ("ACCESS_TOKEN_EXPIRE_MINUTES", str(app_settings.ACCESS_TOKEN_EXPIRE_MINUTES), "general", "Session Timeout (minutes)", "JWT token expiration time in minutes", "int"),
    ]

    settings_created = 0
    for key, value, category, label, description, value_type in default_settings:
        existing = db.query(Setting).filter(Setting.key == key).first()
        if not existing:
            db.add(Setting(
                key=key,
                value=value,
                category=category,
                label=label,
                description=description,
                value_type=value_type,
            ))
            settings_created += 1
    if settings_created:
        print(f"Created {settings_created} default settings")

    # ── Test Tickets ──────────────────────────────────
    existing_tickets = db.query(Ticket).count()
    if existing_tickets == 0:
        john = user_map.get("john@client.com")
        jane = user_map.get("jane@client.com")
        bob = user_map.get("bob@client.com")
        agent = user_map.get("agent@company.com")
        devops = user_map.get("devops@company.com")
        qa = user_map.get("qa@company.com")

        test_tickets = [
            # (subject, category, project, priority, status, description, reporter_email, reporter_id)
            (
                "Login page returns 500 error after password reset",
                TicketCategory.BUG, "Web Portal", TicketPriority.HIGH, TicketStatus.IN_PROGRESS,
                "After resetting my password via the forgot password link, trying to log in with the new password returns a 500 Internal Server Error. The reset email was received and the link worked fine. This started happening today after the latest deploy.",
                "john@client.com", john,
            ),
            (
                "Add dark mode support to dashboard",
                TicketCategory.FEATURE, "Web Portal", TicketPriority.MEDIUM, TicketStatus.OPEN,
                "It would be great to have a dark mode toggle in the user settings. Many users work late hours and the bright white background is straining on the eyes. Could support both system-preference detection and manual toggle.",
                "jane@client.com", jane,
            ),
            (
                "Cannot access shared drive after VPN update",
                TicketCategory.ACCESS, "Internal Tools", TicketPriority.HIGH, TicketStatus.OPEN,
                "Since the VPN client was updated to v3.2, I can no longer access the shared drive at \\\\fileserver\\shared. Other network resources work fine. I've tried reconnecting the VPN and restarting my machine.",
                "bob@client.com", bob,
            ),
            (
                "Production server CPU at 98% - needs investigation",
                TicketCategory.INFRA, "Cloud Platform", TicketPriority.CRITICAL, TicketStatus.IN_PROGRESS,
                "Monitoring alerts show prod-web-03 has been at 98% CPU for the last 30 minutes. Response times are degraded. Need immediate investigation. Possibly related to the cron job that runs at midnight.",
                "john@client.com", john,
            ),
            (
                "Update company logo in email templates",
                TicketCategory.GENERAL, "Marketing Site", TicketPriority.LOW, TicketStatus.OPEN,
                "We've rebranded and the old logo is still showing in all automated email templates (welcome email, password reset, notifications). Please update to the new logo. I'll attach the new logo files.",
                "jane@client.com", jane,
            ),
            (
                "Database migration failing on staging",
                TicketCategory.BUG, "Cloud Platform", TicketPriority.HIGH, TicketStatus.RESOLVED,
                "Alembic migration 'add_user_preferences' fails on staging with: 'relation user_preferences already exists'. Looks like a partial migration from a previous failed attempt. Need to clean up the state.",
                "bob@client.com", bob,
            ),
            (
                "Implement SSO with Google Workspace",
                TicketCategory.FEATURE, "Web Portal", TicketPriority.MEDIUM, TicketStatus.OPEN,
                "We'd like to enable Single Sign-On using our Google Workspace accounts. This would simplify onboarding and improve security by centralizing authentication. Should support both web and mobile apps.",
                "john@client.com", john,
            ),
            (
                "Urgent: Payment processing down",
                TicketCategory.URGENT, "Payment System", TicketPriority.CRITICAL, TicketStatus.RESOLVED,
                "No payments have been processed since 2:00 AM. The payment gateway returns timeout errors. This is affecting all customers. Revenue impact is significant. Need immediate resolution.",
                "jane@client.com", jane,
            ),
            (
                "New employee needs access to Jira and Confluence",
                TicketCategory.ACCESS, "Internal Tools", TicketPriority.MEDIUM, TicketStatus.CLOSED,
                "New team member Sarah Johnson (sarah.j@company.com) starting Monday needs: Jira project access (WEBPORTAL, CLOUD), Confluence spaces (Engineering, Product), and Slack channels (#dev, #deployments).",
                "bob@client.com", bob,
            ),
            (
                "Kubernetes cluster autoscaling not working",
                TicketCategory.INFRA, "Cloud Platform", TicketPriority.HIGH, TicketStatus.IN_PROGRESS,
                "The k8s cluster autoscaler hasn't scaled up despite pods being in Pending state for 20+ minutes. HPA metrics look correct. Suspect the cluster autoscaler config was overwritten during the last Terraform apply.",
                "john@client.com", john,
            ),
            (
                "Export reports to PDF not formatting correctly",
                TicketCategory.BUG, "Web Portal", TicketPriority.LOW, TicketStatus.OPEN,
                "When exporting monthly reports to PDF, the charts are overlapping with the text and page breaks are in odd places. The CSV export works fine. This affects all report types.",
                "jane@client.com", jane,
            ),
            (
                "Set up monitoring for new microservice",
                TicketCategory.INFRA, "Cloud Platform", TicketPriority.MEDIUM, TicketStatus.OPEN,
                "The new notifications-service has been deployed but lacks monitoring. Need: Prometheus metrics endpoint, Grafana dashboard, PagerDuty alerting rules for error rate > 1% and p99 latency > 500ms.",
                "bob@client.com", bob,
            ),
        ]

        tickets_created = []
        for subject, cat, project, priority, status, desc, reporter_email, reporter in test_tickets:
            ticket = Ticket(
                subject=subject,
                category=cat,
                project=project,
                priority=priority,
                status=status,
                description=desc,
                reporter_email=reporter_email,
                reporter_id=reporter.id if reporter else None,
            )
            db.add(ticket)
            db.flush()
            tickets_created.append(ticket)

        print(f"Created {len(tickets_created)} test tickets")

        # ── Assignments ──────────────────────────────────
        assignments = [
            (tickets_created[0], agent),    # Login bug -> Support Agent
            (tickets_created[3], devops),   # CPU issue -> DevOps Agent
            (tickets_created[5], agent),    # DB migration -> Support Agent
            (tickets_created[7], agent),    # Payment down -> Support Agent
            (tickets_created[8], devops),   # Jira access -> DevOps Agent
            (tickets_created[9], devops),   # K8s autoscaling -> DevOps Agent
        ]
        for ticket, assigned_agent in assignments:
            db.add(TicketAssignment(ticket_id=ticket.id, agent_id=assigned_agent.id))
        print(f"Created {len(assignments)} ticket assignments")

        # ── Comments ──────────────────────────────────
        test_comments = [
            # Login bug
            (tickets_created[0], agent, "I can reproduce this. The password reset flow generates a hash with the new bcrypt version but the login check uses the old verifier. Looking into it now."),
            (tickets_created[0], john, "Thanks for the quick response. Is there a workaround in the meantime?"),
            (tickets_created[0], agent, "As a workaround, you can use the 'Sign in with Google' option. I'm deploying a fix to staging now."),
            # CPU issue
            (tickets_created[3], devops, "Identified the issue - the midnight cron job is running a full table scan on the analytics table which has grown to 50M rows. Killing the query now and will optimize it."),
            (tickets_created[3], john, "Thanks! Response times are back to normal now."),
            # DB migration
            (tickets_created[5], agent, "Fixed by dropping the partial migration and re-running. Added a check to the CI pipeline to prevent this in future."),
            (tickets_created[5], bob, "Confirmed staging is working now. Thanks!"),
            # Payment down
            (tickets_created[7], agent, "Payment gateway provider confirmed an outage on their end. They've restored service. All queued payments are now processing."),
            (tickets_created[7], jane, "I can confirm payments are going through again. Thank you for the fast resolution."),
            # K8s autoscaling
            (tickets_created[9], devops, "Confirmed - the cluster autoscaler config was overwritten. The max node count was set to the current count, preventing scale-up. Restoring the correct config now."),
        ]

        for ticket, author, body in test_comments:
            db.add(TicketComment(
                ticket_id=ticket.id,
                author_id=author.id if author else None,
                author_email=author.email if author else None,
                body=body,
                source=CommentSource.WEB,
            ))
        print(f"Created {len(test_comments)} test comments")

    db.commit()
    db.close()
    print("Seed complete.")


if __name__ == "__main__":
    seed()
