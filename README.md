# Conference Inclusion Pledge<br/>Compromiso de Inclusión en Conferencias

Now that video conferencing is widely available,
no one should be left out of a conference
because they cannot afford to travel,
are unable to obtain a visa,
have health concerns,
or need to look after family members.
We have therefore started a petition to pressure conference organizers
to support remote attendance.
This repository hosts a simple standalone web application for collecting signatures.

## Local Setup

1.  Install Python 3.10 (or create a virtual environment with Python 3.10).
2.  `pip install -r requirements.txt` to install dependencies.
3.  `make testdb` to create a test database.
4.  `make serve` to run a local server.
5.  Open <http://127.0.0.1:5000> in your browser.

## Workflow

1.  The home page shows who has signed so far.
2.  When you fill in the form,
    a temporary record is added to the database
    and you are sent an email message asking you to confirm your signature.
    **The email confirmation message has not yet been implemented.**
3.  When you click on the link in the email message,
    your signature is marked as having been validated
    and your name is then displayed in the list of signers.
4.  An error messge is displayed
    if you try to sign up again with the same email address.

## Internals

1.  All data is stored in a single SQLite database `cip.db`
    with these fields (see `sql/makedb.sql`):
    -   `hash`: identify this record
    -   `fullname`: the signer's full name
    -   `email`: the signer's email address
    -   `country`: what country they're in (optional)
    -   `affiliation`: their affiliation (optional)
    -   `created`: when the signing record was created
    -   `pending`: 1 if waiting for confirmation, 0 if confirmed
2.  The Flask application is in `cip.py`, which handles:
    -   `/`: home page with signup form and list of signers
    -   `/submission/`: submission of signup form
    -   `/confirmation/<id>/`: confirmation of signup
3.  The application uses embedded SQL statements
    rather than an object-relational mapper.
4.  The application's page templates are stored in `templates`.
    Inclusions use the `.inc` suffix instead of `.html`.
    -   `base.html`: base template from which others derive
    -   `confirmation.html`: confirmation page
    -   `error.html`: error page
    -   `index.html`: home page
    -   `submission.html`: signup acknowledgment
5.  Static assets are stored in `static`.
    -   `chairs.jpg`: splash image from <https://unsplash.com/photos/2xaF4TbjXT0>
    -   `cip.css`: page styles
    -   `cip.js`: JavaScript to handle tab display
    -   `favicon.ico`: favicon file
