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

        logging.debug(f"Authorized webhook request from {client_ip}")

        event = request.json
        event_type = event.get("event_type", "")
        ticket = event.get("ticket")
        if not ticket:
            logging.debug(f"Webhook request rejected (missing ticket) from {client_ip}")
            return jsonify({"error": "No ticket found"}), 400

        ticket_number = str(ticket["id"])
        subject = ticket["subject"]
        status = ticket["status"].lower()
        assignee_id = ticket.get("assignee_id")
        tags = ticket.get("tags", [])

        logging.debug(f"Processing ticket {ticket_number} with status: {status}")

        task_id = zendesk.get_ticket_task_id(ticket, config)

        if not "teamwork_task" in tags:
            logging.info(f"Ticket {ticket_number} does not have teamwork_task tag. Ignoring.")
            return jsonify({"skipped": "no tag"}), 200

        logging.debug(f"Ticket {ticket_number} has teamwork_task tag. Proceeding with processing.")

        teamwork_user_id = None
        if assignee_id:
            logging.debug(f"Ticket has an assignee, fetching Teamwork user ID")
            teamwork_user_id = zendesk.get_teamwork_user_id(assignee_id, config)
            logging.debug(f"Found Teamwork user ID: {teamwork_user_id}")

        if not task_id:
            logging.debug(f"Creating new Teamwork task for ticket {ticket_number}")
            task_id = teamwork.create_task(subject, ticket_number, teamwork_user_id, config)
            zendesk.set_ticket_task_id(ticket_number, task_id, config)
            logging.info(f"Created Teamwork task {task_id} for ticket {ticket_number}")
        else:
            # handle status updates
            logging.debug(f"Updating Teamwork task {task_id} for ticket {ticket_number} with status: {status}")
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

        logging.debug(f"Processing completed for ticket {ticket_number}")
        return jsonify({"ok": True}), 200

    return app
