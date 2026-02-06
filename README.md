# LEPT AI Reviewer (PH)

AI-Powered Reviewer for the Philippine Licensure Examination for Professional Teachers

## Features

- **AI-Generated Questions**: Practice with intelligently generated exam questions based on your reviewer materials
- **Upload Reviewers**: Use your own PDF and DOCX review materials for personalized practice
- **Multiple Exam Categories**: General Education, Professional Education, and various Specializations
- **Difficulty Levels**: Easy, Medium, and Hard questions
- **Usage Tracking**: Email + IP based tracking with anti-abuse measures
- **GCash Monetization**: PRO (₱99) and PREMIUM (₱499) plans with manual receipt validation
- **Admin Panel**: Full management of users, payments, and reviewer documents

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Secrets

Create or update `.streamlit/secrets.toml` with your credentials:

```toml
[snowflake]
account = "your_snowflake_account"
user = "your_username"
password = "your_password"
database = "LEPT_REVIEWER"
schema = "PUBLIC"
warehouse = "COMPUTE_WH"

[openai]
api_key = "sk-your-openai-api-key"

[admin]
password = "your_secure_admin_password"
```

### 3. Initialize Database

Run the app and access the Admin Panel to initialize the database tables:

1. Start the app: `streamlit run app.py`
2. Log in with any email
3. Use the Admin Access section in the sidebar
4. Go to Settings tab and click "Initialize Tables"

### 4. Run the Application

```bash
streamlit run app.py
```

## Project Structure

```
├── app.py                      # Main entry point
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── .streamlit/
│   └── secrets.toml           # Credentials (not in git)
├── config/
│   └── settings.py            # App configuration
├── database/
│   ├── connection.py          # Snowflake connection
│   ├── schema.py              # Table creation
│   └── queries.py             # Database queries
├── pages/
│   ├── home.py                # Home page
│   ├── upload_reviewer.py     # Document upload
│   ├── practice_exam.py       # Practice exams
│   ├── upgrade.py             # Payment/upgrade
│   └── admin_panel.py         # Admin interface
├── components/
│   ├── sidebar.py             # Navigation
│   ├── auth.py                # Authentication
│   ├── cards.py               # UI cards
│   └── alerts.py              # Notifications
├── services/
│   ├── ai_generator.py        # OpenAI integration
│   ├── document_processor.py  # PDF/DOCX processing
│   ├── usage_tracker.py       # Usage management
│   └── payment_handler.py     # Payment processing
├── utils/
│   ├── ip_utils.py            # IP detection
│   ├── file_utils.py          # File handling
│   └── validators.py          # Input validation
└── assets/
    └── style.css              # Custom CSS
```

## Pricing Plans

| Plan | Price | Features |
|------|-------|----------|
| FREE | Free | 10 questions, upload own reviewers |
| PRO | ₱99 | +75 questions (total 85), access to admin reviewers |
| PREMIUM | ₱499 | Unlimited questions for 30 days, all features |

## Payment Flow

1. User selects a plan on the Upgrade page
2. User sends payment via GCash to the displayed number
3. User uploads receipt and submits payment request
4. Admin reviews and approves/rejects in Admin Panel
5. On approval, user's plan is automatically upgraded

## Admin Features

- View and manage all users
- Approve/reject payment requests
- Upload admin reviewer documents
- Block/unblock users
- Adjust user quotas manually
- View audit logs

## Technology Stack

- **Frontend**: Streamlit
- **Database**: Snowflake
- **AI**: OpenAI GPT-3.5/GPT-4
- **Document Processing**: PyPDF2, python-docx
- **Authentication**: Email + IP based

## Security Notes

- Never share your `.streamlit/secrets.toml` file
- Admin password should be strong and unique
- User emails are tracked with IP addresses for anti-abuse
- Payment receipts are stored securely in the database

## Support

For issues or questions, please contact the administrator.

---

© 2024 LEPT AI Reviewer (PH). All rights reserved.
