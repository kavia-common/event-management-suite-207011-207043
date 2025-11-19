from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# PUBLIC_INTERFACE
class Event(db.Model):
    """Event model representing an event."""
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))

    attendees = db.relationship("Attendee", backref="event", cascade="all, delete-orphan")
    tickets = db.relationship("Ticket", backref="event", cascade="all, delete-orphan")
    schedules = db.relationship("Schedule", backref="event", cascade="all, delete-orphan")

# PUBLIC_INTERFACE
class Attendee(db.Model):
    """Attendee model representing an event attendee."""
    __tablename__ = "attendees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    tickets = db.relationship("Ticket", backref="attendee", cascade="all, delete-orphan")

# PUBLIC_INTERFACE
class Ticket(db.Model):
    """Ticket model representing a ticket for an event."""
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    attendee_id = db.Column(db.Integer, db.ForeignKey("attendees.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    type = db.Column(db.String(50))  # e.g., General, VIP
    price = db.Column(db.Float)

# PUBLIC_INTERFACE
class Schedule(db.Model):
    """Schedule model representing event scheduled activities."""
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.Text)
