import os
import logging
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import urlparse
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup database base class
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///research_platform.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)

# Add custom Jinja filters
@app.template_filter('nl2br')
def nl2br(value):
    """Convert newlines to HTML line breaks."""
    if value:
        return value.replace('\n', '<br>')

# Import models and forms after db is initialized to avoid circular imports
from models import User, Profile, StudentProfile, PIProfile, IndustryProfile, VendorProfile, Opportunity, Message, Application, Notification
from forms import LoginForm, RegistrationForm, StudentProfileForm, PIProfileForm, IndustryProfileForm, VendorProfileForm, OpportunityForm, MessageForm, SearchForm

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Routes
@app.route('/')
def index():
    featured_opportunities = Opportunity.query.filter_by(status='Active').order_by(Opportunity.created_at.desc()).limit(3).all()
    featured_profiles = Profile.query.order_by(db.func.random()).limit(4).all()
    return render_template('index.html', 
                          opportunities=featured_opportunities, 
                          profiles=featured_profiles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        
        flash('Login successful!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            user_type=form.user_type.data,
            account_status='Active',
            verification_status='Pending',
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        user.password_hash = generate_password_hash(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Create profile based on user type
        profile = Profile(
            user_id=user.id,
            profile_type=form.user_type.data,
            profile_completeness=0,
            visibility_settings="Public",
            last_updated=datetime.utcnow()
        )
        db.session.add(profile)
        db.session.commit()
        
        # Create specific profile type
        if form.user_type.data == 'Student':
            student_profile = StudentProfile(profile_id=profile.id)
            db.session.add(student_profile)
        elif form.user_type.data == 'PI':
            pi_profile = PIProfile(profile_id=profile.id)
            db.session.add(pi_profile)
        elif form.user_type.data == 'Industry':
            industry_profile = IndustryProfile(profile_id=profile.id)
            db.session.add(industry_profile)
        elif form.user_type.data == 'Vendor':
            vendor_profile = VendorProfile(profile_id=profile.id)
            db.session.add(vendor_profile)
            
        db.session.commit()
        
        flash('Congratulations, you are now registered! Please complete your profile.', 'success')
        login_user(user)
        return redirect(url_for('edit_profile'))
    
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    try:
        profile = Profile.query.filter_by(user_id=current_user.id).first_or_404()
        
        if profile.profile_type == 'Student':
            form = StudentProfileForm()
            specific_profile = StudentProfile.query.filter_by(profile_id=profile.id).first_or_404()
        elif profile.profile_type == 'PI':
            form = PIProfileForm()
            specific_profile = PIProfile.query.filter_by(profile_id=profile.id).first_or_404()
        elif profile.profile_type == 'Industry':
            form = IndustryProfileForm()
            specific_profile = IndustryProfile.query.filter_by(profile_id=profile.id).first_or_404()
        elif profile.profile_type == 'Vendor':
            form = VendorProfileForm()
            specific_profile = VendorProfile.query.filter_by(profile_id=profile.id).first_or_404()
        else:
            flash('Invalid profile type', 'danger')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error loading profile for editing: {str(e)}")
        flash('There was an error loading your profile. Please try again later.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        # Populate form with existing data
        if profile.profile_type == 'Student' and specific_profile.name:
            form.name.data = specific_profile.name
            form.affiliation.data = specific_profile.affiliation
            form.contact_email.data = specific_profile.contact_email
            form.contact_phone.data = specific_profile.contact_phone
            form.gender.data = specific_profile.gender
            form.address.data = specific_profile.address
            form.research_interests.data = specific_profile.research_interests
            form.why_me.data = specific_profile.why_me
            form.current_status.data = specific_profile.current_status
        elif profile.profile_type == 'PI' and specific_profile.name:
            form.name.data = specific_profile.name
            form.department.data = specific_profile.department
            form.affiliation.data = specific_profile.affiliation
            form.gender.data = specific_profile.gender
            form.current_designation.data = specific_profile.current_designation
            form.email.data = specific_profile.email
            form.contact_phone.data = specific_profile.contact_phone
            form.address.data = specific_profile.address
            form.current_message.data = specific_profile.current_message
            form.current_focus.data = specific_profile.current_focus
            form.expectations_from_students.data = specific_profile.expectations_from_students
            form.why_join_lab.data = specific_profile.why_join_lab
        elif profile.profile_type == 'Industry' and specific_profile.company_name:
            form.company_name.data = specific_profile.company_name
            form.contact_person.data = specific_profile.contact_person
            form.email.data = specific_profile.email
            form.contact_phone.data = specific_profile.contact_phone
            form.gst.data = specific_profile.gst
            form.pan.data = specific_profile.pan
            form.address.data = specific_profile.address
            form.vision.data = specific_profile.vision
            form.sector.data = specific_profile.sector
            form.team_size.data = specific_profile.team_size
            form.annual_turnover.data = specific_profile.annual_turnover
        elif profile.profile_type == 'Vendor' and specific_profile.company_name:
            form.company_name.data = specific_profile.company_name
            form.contact_person.data = specific_profile.contact_person
            form.dealing_categories.data = specific_profile.dealing_categories
            form.email.data = specific_profile.email
            form.contact_phone.data = specific_profile.contact_phone
            form.gst.data = specific_profile.gst
            form.pan.data = specific_profile.pan
            form.address.data = specific_profile.address
            form.product_categories.data = specific_profile.product_categories
            form.why_me.data = specific_profile.why_me
            form.region.data = specific_profile.region
    
    if form.validate_on_submit():
        # Update specific profile based on user type
        completeness = 0
        
        if profile.profile_type == 'Student':
            specific_profile.name = form.name.data
            specific_profile.affiliation = form.affiliation.data
            specific_profile.contact_email = form.contact_email.data
            specific_profile.contact_phone = form.contact_phone.data
            specific_profile.gender = form.gender.data
            specific_profile.address = form.address.data
            specific_profile.research_interests = form.research_interests.data
            specific_profile.why_me = form.why_me.data
            specific_profile.current_status = form.current_status.data
            
            # Calculate profile completeness
            fields = [form.name.data, form.affiliation.data, form.contact_email.data,
                      form.gender.data, form.research_interests.data, form.current_status.data]
            completeness = sum(1 for field in fields if field) / len(fields) * 100
            
        elif profile.profile_type == 'PI':
            specific_profile.name = form.name.data
            specific_profile.department = form.department.data
            specific_profile.affiliation = form.affiliation.data
            specific_profile.gender = form.gender.data
            specific_profile.current_designation = form.current_designation.data
            specific_profile.email = form.email.data
            specific_profile.contact_phone = form.contact_phone.data
            specific_profile.address = form.address.data
            specific_profile.current_message = form.current_message.data
            specific_profile.current_focus = form.current_focus.data
            specific_profile.expectations_from_students = form.expectations_from_students.data
            specific_profile.why_join_lab = form.why_join_lab.data
            
            # Calculate profile completeness
            fields = [form.name.data, form.department.data, form.affiliation.data,
                      form.current_designation.data, form.email.data, form.current_focus.data]
            completeness = sum(1 for field in fields if field) / len(fields) * 100
            
        elif profile.profile_type == 'Industry':
            specific_profile.company_name = form.company_name.data
            specific_profile.contact_person = form.contact_person.data
            specific_profile.email = form.email.data
            specific_profile.contact_phone = form.contact_phone.data
            specific_profile.gst = form.gst.data
            specific_profile.pan = form.pan.data
            specific_profile.address = form.address.data
            specific_profile.vision = form.vision.data
            specific_profile.sector = form.sector.data
            specific_profile.team_size = form.team_size.data
            specific_profile.annual_turnover = form.annual_turnover.data
            
            # Calculate profile completeness
            fields = [form.company_name.data, form.contact_person.data, form.email.data,
                      form.sector.data, form.vision.data]
            completeness = sum(1 for field in fields if field) / len(fields) * 100
            
        elif profile.profile_type == 'Vendor':
            specific_profile.company_name = form.company_name.data
            specific_profile.contact_person = form.contact_person.data
            specific_profile.dealing_categories = form.dealing_categories.data
            specific_profile.email = form.email.data
            specific_profile.contact_phone = form.contact_phone.data
            specific_profile.gst = form.gst.data
            specific_profile.pan = form.pan.data
            specific_profile.address = form.address.data
            specific_profile.product_categories = form.product_categories.data
            specific_profile.why_me = form.why_me.data
            specific_profile.region = form.region.data
            
            # Calculate profile completeness
            fields = [form.company_name.data, form.contact_person.data, form.email.data,
                      form.dealing_categories.data, form.product_categories.data]
            completeness = sum(1 for field in fields if field) / len(fields) * 100
        
        # Update profile completeness and last updated
        profile.profile_completeness = int(completeness)
        profile.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('view_profile', user_id=current_user.id))
    
    return render_template('profile/edit.html', title='Edit Profile', form=form, profile_type=profile.profile_type)

@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    try:
        user = User.query.get_or_404(user_id)
        profile = Profile.query.filter_by(user_id=user_id).first_or_404()
        
        if profile.profile_type == 'Student':
            specific_profile = StudentProfile.query.filter_by(profile_id=profile.id).first_or_404()
            template = 'profile/student.html'
        elif profile.profile_type == 'PI':
            specific_profile = PIProfile.query.filter_by(profile_id=profile.id).first_or_404()
            template = 'profile/pi.html'
        elif profile.profile_type == 'Industry':
            specific_profile = IndustryProfile.query.filter_by(profile_id=profile.id).first_or_404()
            template = 'profile/industry.html'
        elif profile.profile_type == 'Vendor':
            specific_profile = VendorProfile.query.filter_by(profile_id=profile.id).first_or_404()
            template = 'profile/vendor.html'
        else:
            flash('Invalid profile type', 'danger')
            return redirect(url_for('index'))
        
        return render_template(template, user=user, profile=profile, specific_profile=specific_profile)
    except Exception as e:
        logger.error(f"Error viewing profile: {str(e)}")
        flash('There was an error loading the profile. Please try again later.', 'danger')
        return redirect(url_for('index'))

@app.route('/opportunities', methods=['GET'])
def list_opportunities():
    page = request.args.get('page', 1, type=int)
    type_filter = request.args.get('type', None)
    
    if type_filter:
        opportunities = Opportunity.query.filter_by(
            type=type_filter, 
            status='Active'
        ).order_by(Opportunity.created_at.desc()).paginate(page=page, per_page=10)
    else:
        opportunities = Opportunity.query.filter_by(
            status='Active'
        ).order_by(Opportunity.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('opportunities/list.html', 
                          title='Research Opportunities',
                          opportunities=opportunities)

@app.route('/opportunities/create', methods=['GET', 'POST'])
@login_required
def create_opportunity():
    # Check if user is a PI or Industry
    user_profile = Profile.query.filter_by(user_id=current_user.id).first()
    if user_profile.profile_type not in ['PI', 'Industry']:
        flash('Only PIs and Industry partners can post opportunities', 'danger')
        return redirect(url_for('index'))
    
    form = OpportunityForm()
    
    if form.validate_on_submit():
        opportunity = Opportunity(
            creator_profile_id=user_profile.id,
            type=form.type.data,
            title=form.title.data,
            domain=form.domain.data,
            eligibility=form.eligibility.data,
            deadline=form.deadline.data,
            description=form.description.data,
            location=form.location.data,
            duration=form.duration.data,
            compensation=form.compensation.data,
            keywords=form.keywords.data,
            status='Active',
            created_at=datetime.utcnow()
        )
        
        db.session.add(opportunity)
        db.session.commit()
        
        flash('Your opportunity has been posted!', 'success')
        return redirect(url_for('view_opportunity', opportunity_id=opportunity.id))
    
    return render_template('opportunities/create.html', 
                          title='Post Opportunity',
                          form=form)

@app.route('/opportunities/<int:opportunity_id>')
def view_opportunity(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    creator_profile = Profile.query.get_or_404(opportunity.creator_profile_id)
    creator_user = User.query.get_or_404(creator_profile.user_id)
    
    has_applied = False
    if current_user.is_authenticated:
        user_profile = Profile.query.filter_by(user_id=current_user.id).first()
        if user_profile:
            application = Application.query.filter_by(
                opportunity_id=opportunity.id,
                applicant_user_id=current_user.id
            ).first()
            has_applied = application is not None
    
    return render_template('opportunities/view.html',
                          title=opportunity.title,
                          opportunity=opportunity,
                          creator_profile=creator_profile,
                          creator_user=creator_user,
                          has_applied=has_applied)

@app.route('/opportunities/<int:opportunity_id>/apply', methods=['POST'])
@login_required
def apply_opportunity(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    
    # Check if user already applied
    existing_application = Application.query.filter_by(
        opportunity_id=opportunity.id,
        applicant_user_id=current_user.id
    ).first()
    
    if existing_application:
        flash('You have already applied for this opportunity', 'warning')
        return redirect(url_for('view_opportunity', opportunity_id=opportunity.id))
    
    # Create new application
    application = Application(
        opportunity_id=opportunity.id,
        applicant_user_id=current_user.id,
        application_date=datetime.utcnow(),
        status='Pending'
    )
    
    db.session.add(application)
    db.session.commit()
    
    # Create notification for opportunity creator
    creator_profile = Profile.query.get_or_404(opportunity.creator_profile_id)
    notification = Notification(
        user_id=creator_profile.user_id,
        type='application',
        reference_id=application.id,
        message=f'New application received for {opportunity.title}',
        created_at=datetime.utcnow(),
        read_status=False
    )
    
    db.session.add(notification)
    db.session.commit()
    
    flash('Your application has been submitted!', 'success')
    return redirect(url_for('view_opportunity', opportunity_id=opportunity.id))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    
    if form.validate_on_submit() or request.args.get('query'):
        query = form.query.data if form.validate_on_submit() else request.args.get('query')
        category = form.category.data if form.validate_on_submit() else request.args.get('category', 'all')
        
        if category == 'opportunities' or category == 'all':
            opportunities = Opportunity.query.filter(
                Opportunity.status == 'Active',
                (Opportunity.title.ilike(f'%{query}%') |
                 Opportunity.description.ilike(f'%{query}%') |
                 Opportunity.domain.ilike(f'%{query}%') |
                 Opportunity.keywords.ilike(f'%{query}%'))
            ).all()
        else:
            opportunities = []
            
        if category == 'profiles' or category == 'all':
            # Get student profiles
            student_profiles = db.session.query(Profile, StudentProfile, User).join(
                StudentProfile, Profile.id == StudentProfile.profile_id
            ).join(
                User, Profile.user_id == User.id
            ).filter(
                (StudentProfile.name.ilike(f'%{query}%') |
                 StudentProfile.research_interests.ilike(f'%{query}%'))
            ).all()
            
            # Get PI profiles
            pi_profiles = db.session.query(Profile, PIProfile, User).join(
                PIProfile, Profile.id == PIProfile.profile_id
            ).join(
                User, Profile.user_id == User.id
            ).filter(
                (PIProfile.name.ilike(f'%{query}%') |
                 PIProfile.current_focus.ilike(f'%{query}%') |
                 PIProfile.department.ilike(f'%{query}%'))
            ).all()
            
            # Get industry profiles
            industry_profiles = db.session.query(Profile, IndustryProfile, User).join(
                IndustryProfile, Profile.id == IndustryProfile.profile_id
            ).join(
                User, Profile.user_id == User.id
            ).filter(
                (IndustryProfile.company_name.ilike(f'%{query}%') |
                 IndustryProfile.sector.ilike(f'%{query}%') |
                 IndustryProfile.vision.ilike(f'%{query}%'))
            ).all()
            
            # Get vendor profiles
            vendor_profiles = db.session.query(Profile, VendorProfile, User).join(
                VendorProfile, Profile.id == VendorProfile.profile_id
            ).join(
                User, Profile.user_id == User.id
            ).filter(
                (VendorProfile.company_name.ilike(f'%{query}%') |
                 VendorProfile.dealing_categories.ilike(f'%{query}%') |
                 VendorProfile.product_categories.ilike(f'%{query}%'))
            ).all()
            
            # Combine all profiles
            profiles = {
                'student': student_profiles,
                'pi': pi_profiles,
                'industry': industry_profiles,
                'vendor': vendor_profiles
            }
        else:
            profiles = {'student': [], 'pi': [], 'industry': [], 'vendor': []}
            
        return render_template('search/results.html',
                              title='Search Results',
                              query=query,
                              category=category,
                              opportunities=opportunities,
                              profiles=profiles)
    
    return render_template('search/results.html', 
                          title='Search',
                          form=form,
                          opportunities=[],
                          profiles={'student': [], 'pi': [], 'industry': [], 'vendor': []})

@app.route('/messages')
@login_required
def messages():
    conversations = db.session.query(
        Message.sender_user_id,
        Message.receiver_user_id,
        db.func.max(Message.sent_time).label('last_message_time')
    ).filter(
        (Message.sender_user_id == current_user.id) | 
        (Message.receiver_user_id == current_user.id)
    ).group_by(
        Message.sender_user_id,
        Message.receiver_user_id
    ).order_by(
        db.desc('last_message_time')
    ).all()
    
    # Process conversations to get details
    conversation_details = []
    for sender_id, receiver_id, last_time in conversations:
        # Determine the other user
        other_user_id = sender_id if receiver_id == current_user.id else receiver_id
        other_user = User.query.get(other_user_id)
        
        # Get unread count
        unread_count = Message.query.filter_by(
            sender_user_id=other_user_id,
            receiver_user_id=current_user.id,
            read_status=False
        ).count()
        
        # Get last message
        last_message = Message.query.filter(
            ((Message.sender_user_id == current_user.id) & 
             (Message.receiver_user_id == other_user_id)) |
            ((Message.sender_user_id == other_user_id) & 
             (Message.receiver_user_id == current_user.id))
        ).order_by(Message.sent_time.desc()).first()
        
        conversation_details.append({
            'user': other_user,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    return render_template('messages/inbox.html',
                          title='Messages',
                          conversations=conversation_details)

@app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    
    # Get messages between current user and other user
    messages = Message.query.filter(
        ((Message.sender_user_id == current_user.id) & 
         (Message.receiver_user_id == user_id)) |
        ((Message.sender_user_id == user_id) & 
         (Message.receiver_user_id == current_user.id))
    ).order_by(Message.sent_time).all()
    
    # Mark unread messages as read
    unread_messages = Message.query.filter_by(
        sender_user_id=user_id,
        receiver_user_id=current_user.id,
        read_status=False
    ).all()
    
    for msg in unread_messages:
        msg.read_status = True
    
    db.session.commit()
    
    # Handle new message submission
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            sender_user_id=current_user.id,
            receiver_user_id=user_id,
            content=form.content.data,
            sent_time=datetime.utcnow(),
            read_status=False
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Create notification for message receiver
        notification = Notification(
            user_id=user_id,
            type='message',
            reference_id=message.id,
            message=f'New message from {current_user.email}',
            created_at=datetime.utcnow(),
            read_status=False
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return redirect(url_for('conversation', user_id=user_id))
    
    return render_template('messages/conversation.html',
                          title=f'Conversation with {other_user.email}',
                          other_user=other_user,
                          messages=messages,
                          form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Check if user is admin
    if current_user.user_type != 'Admin':
        abort(403)
    
    # Get basic statistics
    stats = {
        'total_users': User.query.count(),
        'students': User.query.filter_by(user_type='Student').count(),
        'pis': User.query.filter_by(user_type='PI').count(),
        'industry': User.query.filter_by(user_type='Industry').count(),
        'vendors': User.query.filter_by(user_type='Vendor').count(),
        'opportunities': Opportunity.query.count(),
        'active_opportunities': Opportunity.query.filter_by(status='Active').count(),
        'applications': Application.query.count()
    }
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Recent opportunities
    recent_opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                          title='Admin Dashboard',
                          stats=stats,
                          recent_users=recent_users,
                          recent_opportunities=recent_opportunities)

# Initialize database
with app.app_context():
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            user_type='Admin',
            account_status='Active',
            verification_status='Verified',
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        admin.password_hash = generate_password_hash('adminpassword')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
