from flask import Flask, request, jsonify, abort
import teamwork
import zendesk
import logging

def create_app(config):
    app = Flask(__name__)
    zendesk.ensure_custom_fields(config)
    webhook_secret = config["WEBHOOK_SECRET"]

    @app.route("/webhook", methods=["POST"])
    def webhook():
        received_secret = request.headers.get("X-Webhook-Secret")
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        if not received_secret:
            logging.warning(f"Webhook request rejected (missing secret) from {client_ip}")
            abort(403)

        if received_secret != webhook_secret:
            logging.warning(f"Webhook request rejected (invalid secret) from {client_ip}")
            abort(403)

        event = request.json
        ticket = event.get("ticket")
        if not ticket:
            return jsonify({"error": "No ticket found"}), 400

        ticket_id = str(ticket["id"])
        ticket_number = ticket.get("id")  # actual public ticket number
        subject = ticket["subject"]
        tags = ticket.get("tags", [])
        assignee_id = ticket.get("assignee_id")

        task_id = zendesk.get_ticket_task_id(ticket, config)

        teamwork_tagged = "teamwork_task" in tags

        if not teamwork_tagged:
            logging.info(f"Ticket {ticket_id} does not have teamwork_task tag. Ignoring.")
            return jsonify({"skipped": "no tag"}), 200

        teamwork_user_id = None
        if assignee_id:
            teamwork_user_id = zendesk.get_teamwork_user_id(assignee_id, config)

        if not task_id:
            task_id = teamwork.create_task(subject, ticket_number, teamwork_user_id, config)
            zendesk.set_ticket_task_id(ticket_id, task_id, config)
            logging.info(f"Created Teamwork task {task_id} for ticket {ticket_number}")
        else:
            # handle status updates
            status = ticket["status"]
            event_type = event.get("event_type", "")

            if status == "solved":
                teamwork.complete_task(task_id, config)
            elif status in ("open", "reopened"):
                teamwork.reopen_task(task_id, config)
            elif status == "closed" or event_type == "deleted":
                teamwork.delete_task(task_id, config)
            elif event_type == "merged":
                merged_into = event.get("merged_into_ticket_id", "unknown")
                teamwork.append_to_task_description(task_id, f"Merged into ticket {merged_into}", config)
                teamwork.complete_task(task_id, config)

        return jsonify({"ok": True}), 200

    return app
