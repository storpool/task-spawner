import logging
from flask import Flask, request, jsonify
import teamwork

def create_app(config, redis_client):
    app = Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def handle_ticket_event():
        event = request.json
        ticket = event.get("ticket")

        if not ticket:
            logging.warning("Webhook received without a ticket payload")
            return jsonify({"error": "Invalid payload"}), 400

        ticket_id = str(ticket["id"])
        subject = ticket["subject"]
        status = ticket["status"]
        assignee_id = ticket.get("assignee_id")
        event_type = event.get("event_type", "")

        teamwork_user_id = None
        if assignee_id:
            teamwork_user_id = redis_client.get_teamwork_user(str(assignee_id))
            if not teamwork_user_id:
                logging.warning(f"No mapping found for Zendesk user {assignee_id}. Assigning to Anyone.")

        task_id = redis_client.get_task_by_ticket(ticket_id)

        if not task_id:
            task_id = teamwork.create_task(subject, teamwork_user_id, config)
            redis_client.map_ticket_to_task(ticket_id, task_id)
            logging.info(f"Created Teamwork task {task_id} for Zendesk ticket {ticket_id}")
            return jsonify({"message": f"Created task {task_id}"}), 201

        if status == "solved":
            teamwork.update_task_status(task_id, completed=True, config=config)
        elif status == "open":
            teamwork.update_task_status(task_id, completed=False, config=config)
        elif status == "closed":
            teamwork.delete_task(task_id, config=config)
            redis_client.delete_ticket_task(ticket_id)
        elif event_type == "deleted":
            teamwork.delete_task(task_id, config=config)
            redis_client.delete_ticket_task(ticket_id)
        elif event_type == "merged":
            teamwork.update_task_status(task_id, completed=True, config=config)

        logging.info(f"Processed update for ticket {ticket_id}")
        return jsonify({"message": "Handled"}), 200

    @app.route("/healthz", methods=["GET"])
    def health_check():
        try:
            # Check Redis connection
            redis_client.client.ping()
            return "ok", 200
        except Exception as e:
            logging.warning(f"Health check failed: Redis not available - {e}")
            return "Redis unavailable", 503

    return app
