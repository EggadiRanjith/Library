
# Library Management System

Welcome to the Library Management System project! This system automates library activities and provides students with access to check their ticket count. Additionally, it offers features such as accessing academic notes, journals, novels, and papers.

## Key Features

- **User Roles**: Admin & Students.
- **Student Registrations**: Managed by Admin (Librarian).
- **Book Management**: Admin can maintain the database of borrowed books by students, including lending, due dates, and tracking the number of books issued and returned.
- **Book Upload**: Admin can upload various types of books, including Journals, Novels, Papers, and Academic notes.
- **Student Access**: Students can log in to the website with their ID and password, check their ticket status, and access available books.

## Scope

Only registered students can access the system.

## Technologies Used

- **Django Framework**: A high-level Python web framework for rapid development and clean, pragmatic design.
- **HTML, CSS, JavaScript, Bootstrap**: Frontend technologies for building the user interface and enhancing user experience.
- **MySQL**: A relational database management system used for storing data related to users, books, and transactions.
- **Amazon S3**: Used for storing and serving static files such as book uploads.
- **SMTP Server**: Used for sending email notifications.

## Setting Up SMTP and Amazon S3

To set up SMTP and Amazon S3, follow these steps:

1. **SMTP Server**:
   - Host: [SMTP_HOST]
   - Port: [SMTP_PORT]
   - Username: [SMTP_USERNAME]
   - Password: [SMTP_PASSWORD]
   - Support Email: [support@example.com]

2. **Amazon S3**:
   - Access Key ID: [S3_ACCESS_KEY_ID]
   - Secret Access Key: [S3_SECRET_ACCESS_KEY]
   - Bucket Name: [S3_BUCKET_NAME]
   - Region: [S3_REGION]

## Installation and Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Set up Django backend:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

3. Access the application in your web browser.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit a pull request or open an issue.

## Support

For support or inquiries, please contact ranjitheggadi@gmail.com

## License

This project is licensed under the Licence.
