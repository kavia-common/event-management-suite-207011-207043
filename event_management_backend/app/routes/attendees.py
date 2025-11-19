from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..models import db, Attendee, Event
from marshmallow import Schema, fields

blp = Blueprint(
    "Attendees", "attendees", url_prefix="/api/attendees", description="Attendee endpoints"
)

class AttendeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    event_id = fields.Int(required=True)

class AttendeeCreateSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    event_id = fields.Int(required=True)

# PUBLIC_INTERFACE
@blp.route("/")
class AttendeeList(MethodView):
    """List and register attendees"""

    @blp.response(200, AttendeeSchema(many=True))
    def get(self):
        return Attendee.query.all()

    @blp.arguments(AttendeeCreateSchema)
    @blp.response(201, AttendeeSchema)
    def post(self, new_data):
        if not Event.query.get(new_data["event_id"]):
            abort(404, message="Event not found.")
        attendee = Attendee(
            name=new_data["name"],
            email=new_data["email"],
            event_id=new_data["event_id"],
        )
        db.session.add(attendee)
        db.session.commit()
        return attendee

@blp.route("/<int:attendee_id>")
class AttendeeDetail(MethodView):
    """Get or delete single attendee"""

    @blp.response(200, AttendeeSchema)
    def get(self, attendee_id):
        attendee = Attendee.query.get(attendee_id)
        if not attendee:
            abort(404, message="Attendee not found.")
        return attendee

    def delete(self, attendee_id):
        attendee = Attendee.query.get(attendee_id)
        if not attendee:
            abort(404, message="Attendee not found.")
        db.session.delete(attendee)
        db.session.commit()
        return {"message": "Deleted"}
