from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..models import db, Schedule, Event
from marshmallow import Schema, fields

blp = Blueprint(
    "Schedules", "schedules", url_prefix="/api/schedules", description="Schedule endpoints"
)

class ScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    event_id = fields.Int(required=True)
    title = fields.Str(required=True)
    start_time = fields.DateTime(allow_none=True)
    end_time = fields.DateTime(allow_none=True)
    description = fields.Str()

class ScheduleCreateSchema(Schema):
    event_id = fields.Int(required=True)
    title = fields.Str(required=True)
    start_time = fields.DateTime(allow_none=True)
    end_time = fields.DateTime(allow_none=True)
    description = fields.Str()

# PUBLIC_INTERFACE
@blp.route("/")
class ScheduleList(MethodView):
    """List and create schedules"""

    @blp.response(200, ScheduleSchema(many=True))
    def get(self):
        return Schedule.query.all()

    @blp.arguments(ScheduleCreateSchema)
    @blp.response(201, ScheduleSchema)
    def post(self, new_data):
        if not Event.query.get(new_data["event_id"]):
            abort(404, message="Event not found.")
        schedule = Schedule(
            event_id=new_data["event_id"],
            title=new_data["title"],
            start_time=new_data.get("start_time"),
            end_time=new_data.get("end_time"),
            description=new_data.get("description"),
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule

@blp.route("/<int:schedule_id>")
class ScheduleDetail(MethodView):
    """Get or delete schedule"""

    @blp.response(200, ScheduleSchema)
    def get(self, schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            abort(404, message="Schedule not found.")
        return schedule

    def delete(self, schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            abort(404, message="Schedule not found.")
        db.session.delete(schedule)
        db.session.commit()
        return {"message": "Deleted"}
