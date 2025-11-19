from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..models import db, Event
from marshmallow import Schema, fields

blp = Blueprint(
    "Events", "events", url_prefix="/api/events", description="Event management endpoints"
)

# Marshmallow schemas
class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    date = fields.DateTime(required=True, format="iso")
    location = fields.Str()

class EventCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    date = fields.DateTime(required=True, format="iso")
    location = fields.Str()

# PUBLIC_INTERFACE
@blp.route("/")
class EventsList(MethodView):
    """Get all events / create an event"""

    @blp.response(200, EventSchema(many=True))
    def get(self):
        """List all events"""
        return Event.query.all()

    @blp.arguments(EventCreateSchema)
    @blp.response(201, EventSchema)
    def post(self, new_data):
        """Create an event"""
        try:
            event = Event(
                title=new_data["title"],
                description=new_data.get("description"),
                date=new_data["date"],
                location=new_data.get("location"),
            )
            db.session.add(event)
            db.session.commit()
            return event
        except Exception as e:
            abort(400, message=str(e))

@blp.route("/<int:event_id>")
class EventDetail(MethodView):
    """Get, update, or delete single event"""

    @blp.response(200, EventSchema)
    def get(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")
        return event

    @blp.arguments(EventCreateSchema)
    @blp.response(200, EventSchema)
    def put(self, update_data, event_id):
        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")
        event.title = update_data.get("title", event.title)
        event.description = update_data.get("description", event.description)
        event.date = update_data.get("date", event.date)
        event.location = update_data.get("location", event.location)
        db.session.commit()
        return event

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")
        db.session.delete(event)
        db.session.commit()
        return {"message": "Deleted"}
