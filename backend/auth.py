from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle both form and JSON requests
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')

        user = User.query.filter_by(email=email, role=role).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Logged in successfully!',
                    'user': {
                        'id': user.id,
                        'name': user.full_name,
                        'role': user.role
                    }
                })
            flash('Logged in successfully!', 'success')
            if user.role == 'manager':
                return redirect(url_for('manager.dashboard'))
            else:
                return redirect(url_for('speaker.dashboard'))
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid email or password'})
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle both form and JSON requests
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
        else:
            email = request.form.get('email')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Email already registered'})
            flash('Email already registered', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        if request.is_json:
            user = User(
                full_name=data.get('full_name'),
                email=email,
                password=generate_password_hash(data.get('password')),
                mobile=data.get('mobile'),
                role='speaker',
                track=data.get('track'),
                tshirt_size=data.get('tshirt_size'),
                food_choice=data.get('food_choice'),
                blood_group=data.get('blood_group'),
                emergency_contact_name=data.get('emergency_contact_name'),
                emergency_contact_number=data.get('emergency_contact_number'),
                linkedin_url=data.get('linkedin_url'),
                sap_community_url=data.get('sap_community_url'),
                speaker2_name=data.get('speaker2_name'),
                speaker2_email=data.get('speaker2_email'),
                speaker2_tshirt_size=data.get('speaker2_tshirt_size')
            )
        else:
            user = User(
                full_name=request.form.get('full_name'),
                email=email,
                password=generate_password_hash(request.form.get('password')),
                mobile=request.form.get('mobile'),
                role='speaker',
                track=request.form.get('track'),
                tshirt_size=request.form.get('tshirt_size'),
                food_choice=request.form.get('food_choice'),
                blood_group=request.form.get('blood_group'),
                emergency_contact_name=request.form.get('emergency_contact_name'),
                emergency_contact_number=request.form.get('emergency_contact_number'),
                linkedin_url=request.form.get('linkedin_url'),
                sap_community_url=request.form.get('sap_community_url'),
                speaker2_name=request.form.get('speaker2_name'),
                speaker2_email=request.form.get('speaker2_email'),
                speaker2_tshirt_size=request.form.get('speaker2_tshirt_size')
            )
        
        db.session.add(user)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.index'))