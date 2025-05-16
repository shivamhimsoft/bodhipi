from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # Student, PI, Industry, Vendor, Admin, Guest
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    account_status = db.Column(db.String(20), default='Active')  # Active, Suspended, Deleted
    verification_status = db.Column(db.String(20), default='Pending')  # Pending, Verified, Rejected
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete-orphan")
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic', 
                                   foreign_keys='Message.sender_user_id', cascade="all, delete-orphan")
    received_messages = db.relationship('Message', backref='receiver', lazy='dynamic', 
                                       foreign_keys='Message.receiver_user_id', cascade="all, delete-orphan")
    applications = db.relationship('Application', backref='applicant', lazy='dynamic', 
                                  foreign_keys='Application.applicant_user_id', cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.email}>'

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    profile_type = db.Column(db.String(20), nullable=False)  # Student, PI, Industry, Vendor
    profile_completeness = db.Column(db.Integer, default=0)
    visibility_settings = db.Column(db.String(20), default='Public')  # Public, Private, Contacts-Only
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - specific profile types
    student_profile = db.relationship('StudentProfile', backref='profile', uselist=False, cascade="all, delete-orphan")
    pi_profile = db.relationship('PIProfile', backref='profile', uselist=False, cascade="all, delete-orphan")
    industry_profile = db.relationship('IndustryProfile', backref='profile', uselist=False, cascade="all, delete-orphan")
    vendor_profile = db.relationship('VendorProfile', backref='profile', uselist=False, cascade="all, delete-orphan")
    
    # Relationships - created content
    created_opportunities = db.relationship('Opportunity', backref='creator', lazy='dynamic', 
                                           foreign_keys='Opportunity.creator_profile_id', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Profile {self.id} - {self.profile_type}>'

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, unique=True)
    name = db.Column(db.String(100))
    affiliation = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    profile_picture = db.Column(db.String(200))
    research_interests = db.Column(db.Text)
    why_me = db.Column(db.Text)
    current_status = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<StudentProfile {self.name}>'

class PIProfile(db.Model):
    __tablename__ = 'pi_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, unique=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    affiliation = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    current_designation = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    profile_picture = db.Column(db.String(200))
    current_message = db.Column(db.Text)
    current_focus = db.Column(db.Text)
    expectations_from_students = db.Column(db.Text)
    why_join_lab = db.Column(db.Text)
    
    # Relationships
    research_facilities = db.relationship('ResearchFacility', backref='pi', lazy='dynamic', cascade="all, delete-orphan")
    projects = db.relationship('Project', backref='pi', lazy='dynamic', cascade="all, delete-orphan")
    team_members = db.relationship('TeamMember', backref='pi', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<PIProfile {self.name}>'

class IndustryProfile(db.Model):
    __tablename__ = 'industry_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(100))
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    gst = db.Column(db.String(20))
    pan = db.Column(db.String(20))
    address = db.Column(db.String(200))
    logo = db.Column(db.String(200))
    vision = db.Column(db.Text)
    sector = db.Column(db.String(100))
    team_size = db.Column(db.Integer)
    annual_turnover = db.Column(db.String(50))
    
    # Relationships
    csr_funds = db.relationship('CSRFund', backref='industry', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<IndustryProfile {self.company_name}>'

class VendorProfile(db.Model):
    __tablename__ = 'vendor_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(100))
    contact_person = db.Column(db.String(100))
    dealing_categories = db.Column(db.String(200))
    email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    gst = db.Column(db.String(20))
    pan = db.Column(db.String(20))
    address = db.Column(db.String(200))
    logo = db.Column(db.String(200))
    product_categories = db.Column(db.String(200))
    why_me = db.Column(db.Text)
    region = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<VendorProfile {self.company_name}>'

class ResearchFacility(db.Model):
    __tablename__ = 'research_facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    pi_profile_id = db.Column(db.Integer, db.ForeignKey('pi_profiles.id'), nullable=False)
    equipment_name = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    working_status = db.Column(db.String(20))
    sop_file = db.Column(db.String(200))
    equipment_type = db.Column(db.String(20))  # Major/Minor
    
    def __repr__(self):
        return f'<ResearchFacility {self.equipment_name}>'

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    pi_profile_id = db.Column(db.Integer, db.ForeignKey('pi_profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    funding_agency = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20))  # Active, Completed, Planned
    description = db.Column(db.Text)
    keywords = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Project {self.title}>'

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    pi_profile_id = db.Column(db.Integer, db.ForeignKey('pi_profiles.id'), nullable=False)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'))
    name = db.Column(db.String(100))  # For external members
    position = db.Column(db.String(50))
    status = db.Column(db.String(20))  # Current/Former
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Relationship
    student = db.relationship('StudentProfile', backref='team_memberships')
    
    def __repr__(self):
        return f'<TeamMember {self.name or self.student.name}>'

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Internship, PhD, Job, PostDoc, Project
    title = db.Column(db.String(200), nullable=False)
    domain = db.Column(db.String(100))
    eligibility = db.Column(db.Text)
    deadline = db.Column(db.Date)
    description = db.Column(db.Text)
    advertisement_link = db.Column(db.String(200))
    location = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    compensation = db.Column(db.String(100))
    keywords = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Active')  # Active, Closed, Filled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='opportunity', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    applicant_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected, Shortlisted
    resume = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)
    additional_documents = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Application {self.id}>'

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_time = db.Column(db.DateTime, default=datetime.utcnow)
    read_status = db.Column(db.Boolean, default=False)
    attachments = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Message {self.id}>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # message, application, etc.
    reference_id = db.Column(db.Integer)
    message = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_status = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Notification {self.id}>'

class CSRFund(db.Model):
    __tablename__ = 'csr_funds'
    
    id = db.Column(db.Integer, primary_key=True)
    industry_profile_id = db.Column(db.Integer, db.ForeignKey('industry_profiles.id'), nullable=False)
    amount = db.Column(db.Float)
    interest_areas = db.Column(db.String(200))
    availability = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<CSRFund {self.id}>'
