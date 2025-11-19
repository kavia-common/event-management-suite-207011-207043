from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..models import db, Ticket, Event, Attendee
from marshmallow import Schema, fields

blp = Blueprint(
    "Tickets", "tickets", url_prefix="/api/tickets", description="Ticket endpoints"
)

class TicketSchema(Schema):
    id = fields.Int(dump_only=True)
    attendee_id = fields.Int(required=True)
    event_id = fields.Int(required=True)
    type = fields.Str()
    price = fields.Float()

class TicketCreateSchema(Schema):
    attendee_id = fields.Int(required=True)
    event_id = fields.Int(required=True)
    type = fields.Str()
    price = fields.Float()

# PUBLIC_INTERFACE
@blp.route("/")
class TicketList(MethodView):
    """List & assign tickets"""

    @blp.response(200, TicketSchema(many=True))
    def get(self):
        return Ticket.query.all()

    @blp.arguments(TicketCreateSchema)
    @blp.response(201, TicketSchema)
    def post(self, new_data):
        if not Event.query.get(new_data["event_id"]):
            abort(404, message="Event not found.")
        if not Attendee.query.get(new_data["attendee_id"]):
            abort(404, message="Attendee not found.")
        ticket = Ticket(
            attendee_id=new_data["attendee_id"],
            event_id=new_data["event_id"],
            type=new_data.get("type"),
            price=new_data.get("price"),
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket

@blp.route("/<int:ticket_id>")
class TicketDetail(MethodView):
    """View or delete single ticket"""

    @blp.response(200, TicketSchema)
    def get(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            abort(404, message="Ticket not found.")
        return ticket

    def delete(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            abort(404, message="Ticket not found.")
        db.session.delete(ticket)
        db.session.commit()
        return {"message": "Deleted"}
