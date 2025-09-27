# Speaker Persona App - Vibeathon Project

A comprehensive event management platform designed to streamline session management, speaker engagement, and event manager coordination for events like SIT/Vibeathon.

## 🚀 Features

### For Speakers
- **Session Management**: Submit, edit, and track session submissions
- **Document Upload**: Upload presentation materials and demo files
- **QR Code System**: Automated check-in and t-shirt collection QR codes
- **Agenda Access**: View published event agenda
- **Certificate Download**: Download speaker certificates post-event
- **Change Requests**: Request changes to session details
- **Notifications**: Email notifications for all updates

### For Event Managers
- **Session Review**: Review, approve, reject, or hold session submissions
- **Agenda Builder**: Dynamic agenda creation with drag-and-drop scheduling
- **Communication Tools**: Email templates and bulk notifications
- **Speaker Management**: Manage speaker information and requirements
- **Feedback System**: Collect and analyze session feedback
- **Certificate Generation**: Automated certificate creation and distribution
- **Analytics Dashboard**: Real-time event statistics and insights

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **Flask-Mail**: Email notifications
- **QRCode**: QR code generation
- **Pillow**: Image processing

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive dashboard functionality
- **Tailwind CSS**: Utility-first CSS framework
- **Bootstrap**: Component library
- **Font Awesome**: Icons

### Database
- **SQLite**: Development database
- **PostgreSQL**: Production ready (configurable)

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Vibeathon
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your_secret_key_here
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@vibeathon.com
```

### 5. Initialize Database
```bash
python app.py
```
This will create the database and all necessary tables.

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📱 Usage

### Speaker Registration
1. Navigate to the registration page
2. Fill in all required speaker information
3. Submit the registration form
4. Login with your credentials

### Speaker Dashboard
- **My Sessions**: View and manage your submitted sessions
- **Documents**: Upload presentation materials
- **Event Agenda**: View the published event schedule
- **QR Codes**: Download check-in and t-shirt collection QR codes
- **Certificates**: Download your speaker certificates

### Event Manager Dashboard
- **Submissions**: Review and manage session submissions
- **Agenda Builder**: Create and manage the event agenda
- **Communications**: Send emails and manage templates
- **Speakers**: View and manage speaker information
- **Feedback**: Collect and analyze session feedback
- **Certificates**: Generate and manage certificates

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - Register new speaker
- `POST /api/login` - User login
- `GET /auth/logout` - User logout

### Speaker Endpoints
- `GET /speaker/dashboard` - Speaker dashboard
- `POST /speaker/sessions/new` - Submit new session
- `PUT /speaker/sessions/<id>` - Update session
- `POST /speaker/sessions/<id>/confirm` - Confirm session participation
- `GET /speaker/qrcodes/<type>` - Get QR codes
- `POST /speaker/change-requests` - Submit change request

### Manager Endpoints
- `GET /manager/dashboard` - Manager dashboard
- `POST /manager/submissions/<id>/<action>` - Handle session submissions
- `POST /manager/agenda/update` - Update agenda
- `POST /manager/change-requests/<id>/<action>` - Handle change requests
- `POST /manager/certificates/generate` - Generate certificates
- `POST /manager/reminders/send` - Send reminders

## 🗄️ Database Schema

### Core Tables
- **users**: Speaker and manager information
- **sessions**: Session submissions and details
- **agenda**: Event schedule and timing
- **documents**: Uploaded files and materials
- **certificates**: Generated certificates
- **qr_codes**: QR code data and usage tracking
- **change_requests**: Session modification requests
- **notifications**: System notifications
- **email_templates**: Email template management
- **feedback**: Session feedback and ratings

## 🎨 UI/UX Features

- **Responsive Design**: Mobile-first approach
- **Modern Interface**: Clean and intuitive design
- **Real-time Updates**: Live data synchronization
- **Accessibility**: WCAG compliant design
- **Dark Mode**: Optional dark theme support
- **Animations**: Smooth transitions and effects

## 🔒 Security Features

- **Authentication**: Secure user login system
- **Authorization**: Role-based access control
- **Data Encryption**: Sensitive data protection
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Cross-site request forgery prevention

## 🚀 Deployment

### Production Setup
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Set up email service (SMTP)
4. Deploy using Gunicorn or similar WSGI server
5. Configure reverse proxy (Nginx)

### Docker Deployment
```bash
# Build the image
docker build -t speaker-persona .

# Run the container
docker run -p 5000:5000 speaker-persona
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎯 Future Enhancements

- **AI Integration**: Smart scheduling and recommendations
- **Mobile App**: Native mobile application
- **Advanced Analytics**: Detailed reporting and insights
- **Integration APIs**: Third-party service integrations
- **Multi-language Support**: Internationalization
- **Video Conferencing**: Built-in meeting capabilities

## 📊 Project Status

- ✅ Core functionality implemented
- ✅ User authentication and authorization
- ✅ Session management system
- ✅ QR code generation
- ✅ Email notification system
- ✅ Responsive UI/UX
- 🔄 Advanced features in development
- 🔄 AI-powered features planned

---

**Built with ❤️ for Vibeathon 2025**
