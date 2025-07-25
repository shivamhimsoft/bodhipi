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



class Register(db.Model):
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256))  # 🔐 New column
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Register {self.email} - {self.user_type}>'



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

    # ➕ New Relationship: Education
    educations = db.relationship('Education', backref='profile', lazy='dynamic', cascade='all, delete-orphan')
    
    # Relationships - created content
    created_opportunities = db.relationship('Opportunity', backref='creator', lazy='dynamic', 
                                           foreign_keys='Opportunity.creator_profile_id', cascade="all, delete-orphan")

    # Add this relationship
    experiences = db.relationship('Experience', backref='profile', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profile {self.id} - {self.profile_type}>'



class PIProfile(db.Model):
    __tablename__ = 'pi_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False, unique=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    affiliation = db.Column(db.Text)  # changed
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    current_designation = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    profile_picture = db.Column(db.String(200))
    current_message = db.Column(db.Text)  # changed
    current_focus = db.Column(db.Text)
    expectations_from_students = db.Column(db.Text)
    why_join_lab = db.Column(db.Text)

     # New columns added below
    profile_url = db.Column(db.String(255))  # New: Profile URL
    affiliation_short = db.Column(db.String(100))  # New: Affiliation (Short Form)
    location = db.Column(db.String(100))  # New: Location (City)
    education_summary = db.Column(db.Text)  # New: Education
    research_interest = db.Column(db.Text)  # New: Research Interest
    papers_published = db.Column(db.Integer)  # New: Papers
    total_citations = db.Column(db.Integer)  # New: Citations
    research_experience_years = db.Column(db.Integer)  # New: Research experience (Number of years)
    h_index = db.Column(db.Integer)  # New: h-index
    last_updated = db.Column(db.DateTime)  # New: Last updated date
    
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
    sop_file = db.Column(db.String(255))
    equipment_type = db.Column(db.String(20))  # Major/Minor
    
    def __repr__(self):
        return f'<ResearchFacility {self.equipment_name}>'

# class ResearchFacility(db.Model):
#     __tablename__ = 'research_facilities'
    
#     id = db.Column(db.Integer, primary_key=True)
#     profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
#     equipment_name = db.Column(db.String(100), nullable=False)
#     make = db.Column(db.String(100), nullable=False)
#     model = db.Column(db.String(100), nullable=False)
#     working_status = db.Column(db.String(20), nullable=False)
#     sop_file = db.Column(db.String(200), nullable=False)
#     equipment_type = db.Column(db.String(20), nullable=False)

#     profile = db.relationship('Profile', backref='research_facilities')

#     def __repr__(self):
#         return f'<ResearchFacility {self.equipment_name}>'


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

# class TeamMember(db.Model):
#     __tablename__ = 'team_members'
    
#     id = db.Column(db.Integer, primary_key=True)
#     pi_profile_id = db.Column(db.Integer, db.ForeignKey('pi_profiles.id'), nullable=False)
#     student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'))
#     name = db.Column(db.String(100))  # For external members
#     position = db.Column(db.String(50))
#     status = db.Column(db.String(20))  # Current/Former
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
    
#     # Relationship
#     student = db.relationship('StudentProfile', backref='team_memberships')
    
#     def __repr__(self):
#         return f'<TeamMember {self.name or self.student.name}>'


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
    
    # ✅ Add this relationship
    pi_profile = db.relationship('PIProfile', backref='team_members_direct')
    # Relationships
    student = db.relationship('StudentProfile', backref='team_memberships')
    
    def __repr__(self):
        return f'<TeamMember {self.name or (self.student.name if self.student else "Unnamed")}>'



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


class Institute(db.Model):
    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    centers = db.Column(db.String(255))
    lab_sector = db.Column(db.Text)
    focus_area = db.Column(db.Text)
    key_resources = db.Column(db.Text)
    researchers = db.Column(db.String(255))
    director = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    link = db.Column(db.String(500))
    ownership = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Institute {self.name}>'


department_institute = db.Table('department_institute',
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id')),
    db.Column('institute_id', db.Integer, db.ForeignKey('institutes.id'))
)

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Many-to-many relationship
    institutes = db.relationship('Institute', secondary=department_institute, backref='departments')

    def __repr__(self):
        return f'<Department {self.name}>'


class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    degree_name = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(150), nullable=False)
    university = db.Column(db.String(150), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer)
    currently_pursuing = db.Column(db.Boolean, default=False)
    university_address = db.Column(db.String(255))

    def __repr__(self):
        return f"<Education {self.degree_name} at {self.college}>"


class Experience(db.Model):
    __tablename__ = 'experience'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    project_title = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    pi = db.Column(db.String(100))
    pi_affiliation = db.Column(db.String(150))
    college = db.Column(db.String(150))
    university_or_industry = db.Column(db.String(150))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    currently_working = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Experience {self.project_title} - {self.position}>"
        
class Publication(db.Model):
    __tablename__ = 'publications'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.Text, nullable=False)
    journal_or_conference = db.Column(db.String(255))
    year = db.Column(db.Integer, nullable=False)
    doi = db.Column(db.String(100))
    citation = db.Column(db.Text)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.Text)

    profile = db.relationship('Profile', backref='publications')

    def __repr__(self):
        return f"<Publication {self.title} ({self.year})>"


# class ResearchFacility(db.Model):
#     __tablename__ = 'research_facilities'

#     id = db.Column(db.Integer, primary_key=True)
#     pi_profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
#     equipment_name = db.Column(db.String(100), nullable=False)
#     make = db.Column(db.String(100), nullable=False)
#     model = db.Column(db.String(100), nullable=False)
#     working_status = db.Column(db.String(50), nullable=False)
#     sop_file = db.Column(db.String(255), nullable=False)
#     equipment_type = db.Column(db.String(20), nullable=False)  # Major/Minor

#     pi_profile = db.relationship('Profile', backref='research_facilities')

#     def __repr__(self):
#         return f"<ResearchFacility {self.equipment_name} ({self.equipment_type})>"

class Technology(db.Model):
    __tablename__ = 'technologies'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    keywords = db.Column(db.String(200))
    trl = db.Column(db.Integer)  # Technology Readiness Level (1-9)
    usp = db.Column(db.Text)  # Unique Selling Proposition
    target_industries = db.Column(db.String(200))
    ip_status = db.Column(db.String(50))  # Patent Pending, Patented, Trade Secret, etc.
    licensing_intent = db.Column(db.String(50))  # Available for License, Seeking Partners, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    creator = db.relationship('Profile', backref='technologies')
    
    def __repr__(self):
        return f'<Technology {self.title}>'


class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    skill_type = db.Column(db.String(50), nullable=False)  # Software, Instrument, Data Analysis, Specific
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(50))  # Beginner, Intermediate, Advanced, Expert
    
    # Relationship
    profile = db.relationship('Profile', backref='skills')
    
    def __repr__(self):
        return f'<Skill {self.skill_name} ({self.skill_type})>'


class Award(db.Model):
    __tablename__ = 'awards'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    issuing_organization = db.Column(db.String(200))
    
    # Relationship
    profile = db.relationship('Profile', backref='awards')
    
    def __repr__(self):
        return f'<Award {self.title} ({self.date.year})>'



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




# STUDENTS MODELS : =============>

# class StudentProfile(db.Model):
#     __tablename__ = 'student_profiles'

#     id = db.Column(db.Integer, primary_key=True)  # StudentProfileID
#     profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
#     name = db.Column(db.String(120), nullable=False)
#     affiliation = db.Column(db.String(120))
#     contact_email = db.Column(db.String(120))
#     contact_phone = db.Column(db.String(20))
#     dob = db.Column(db.Date)
#     gender = db.Column(db.String(10))
#     address = db.Column(db.Text)
#     profile_picture = db.Column(db.String(200))  # path to image
#     research_interests = db.Column(db.Text)
#     why_me = db.Column(db.Text)
#     current_status = db.Column(db.String(120))

#     profile = db.relationship('Profile', backref='student_profile', uselist=False)






class SponsorRequest(db.Model):
    __tablename__ = 'sponsor_requests'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('pi_profiles.id'), nullable=False)

    event_specifications = db.Column(db.Text, nullable=False)
    target_amount = db.Column(db.Numeric(12, 2), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to PI
    pi = db.relationship('PIProfile', backref='sponsor_requests')

    def __repr__(self):
        return f"<SponsorRequest for PI {self.profile_id}>"

