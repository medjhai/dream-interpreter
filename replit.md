# Dream Interpreter Web App

## Overview

Dream Interpreter is a Flask-based web application that allows users to record their dreams and receive automated interpretations. The application provides a personal dream journal with intelligent analysis based on psychological symbolism and user-selected interpretation styles. Users can create accounts, log their dreams with mood and style preferences, and build a personal history of their dream interpretations over time.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (August 2025)

### Design System Overhaul
- **Date**: August 21, 2025
- **Changes**: Complete redesign from complex gradient-based design to clean minimal approach
- **Technical Details**: 
  - Replaced complex CSS with simplified CSS using CSS variables for easy maintenance
  - Created new minimal template system (_minimal.html versions) with fewer elements
  - Implemented mobile-first responsive design with hamburger navigation
  - Optimized for better adaptability across different screen resolutions
- **Files Updated**: All templates, static/minimal.css, app.py routes
- **Status**: Completed and tested - all functionality working correctly

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Authentication**: Flask-Login for user session management with secure password hashing
- **Database Schema**: Two main entities - Users and Dreams with one-to-many relationship
- **Dream Interpretation Engine**: Rule-based system using keyword matching and psychological symbol analysis
- **API Design**: RESTful endpoints for dream submission, interpretation, and CRUD operations

### Frontend Architecture
- **Template Engine**: Jinja2 for server-side rendering with minimal design system
- **Client-Side Logic**: Vanilla JavaScript for form handling and AJAX requests
- **UI Framework**: Custom minimal CSS with CSS variables for easy maintenance and theming
- **Design System**: Clean minimal approach with fewer elements for better responsiveness across all screen resolutions
- **Mobile Optimization**: Responsive navigation with hamburger menu for mobile devices
- **User Experience**: Simplified forms with mood selection, interpretation style preferences, and streamlined result display

### Data Storage
- **Database**: SQLAlchemy with support for multiple database backends (configured via DATABASE_URL environment variable)
- **User Model**: Stores authentication credentials, profile information, and account creation timestamps
- **Dream Model**: Records dream content, titles, moods, interpretation styles, generated interpretations, and timestamps
- **Relationships**: Foreign key constraints ensure data integrity between users and their dreams

### Authentication & Security
- **Password Security**: Werkzeug password hashing with salt for secure credential storage
- **Session Management**: Flask sessions with configurable secret keys for CSRF protection
- **User Authorization**: Login-required decorators protect sensitive routes and user-specific data
- **Data Privacy**: User dreams are isolated by user_id with proper access controls

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework for routing, templating, and request handling
- **Flask-SQLAlchemy**: Database ORM for model definitions and query operations
- **Flask-Login**: User authentication and session management
- **Werkzeug**: Password hashing utilities and WSGI middleware

### Frontend Dependencies
- **Bootstrap CSS**: UI framework delivered via CDN for responsive design
- **Font Awesome**: Icon library for enhanced visual elements
- **Custom CSS/JS**: Application-specific styling and client-side functionality

### Infrastructure Dependencies
- **Database**: Configurable via DATABASE_URL environment variable (supports PostgreSQL, SQLite, etc.)
- **Session Storage**: Environment-configurable secret key for secure session management
- **Deployment**: WSGI-compatible with proxy fix middleware for production deployment