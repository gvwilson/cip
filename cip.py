from datetime import datetime
import hashlib
import sys

from flask import Flask, render_template, request
import sqlite3
from wtforms import Form, StringField, validators

app = Flask(__name__)
DB = "cip.db"

class CIPError(Exception):
    def __init__(self, message):
        self.message = message

class SubmissionForm(Form):
    fullname = StringField("fullname", [validators.Length(min=1)])
    email = StringField("email", [validators.Length(min=3)])
    country = StringField("country")
    affiliation = StringField("affiliation")

# ----------------------------------------------------------------------

@app.route("/")
def homepage():
    """Handle request for site home page."""
    signers = _get_signers()
    return render_template("index.html", signers=signers)

@app.route("/submission/", methods=["POST"])
def submission():
    """Handle submission of signup form."""
    try:
        if not SubmissionForm(request.form).validate():
            raise CIPError("Error #3: invalid submission data.")
        data = _get_form_values(request.form)
        _add_pending(data)
        _send_confirmation_request(data)
        return render_template("submission.html")
    except CIPError as exc:
        return render_template("error.html", message=exc.message)

@app.route("/confirmation/<identifier>/")
def confirmation(identifier):
    """Handle click on confirmation link."""
    try:
        fullname = _confirm_signature(identifier)
        return render_template("confirmation.html", fullname=fullname)
    except CIPError as exc:
        return render_template("error.html", message=exc.message)

# ----------------------------------------------------------------------

# Check if an email address has already been registered.
Q_EMAIL_CHECK = """
select pending from signers
where email = ?
"""

# Insert someone who has asked to sign the pledge.
Q_INSERT_SIGNER = """
insert into signers(hash, fullname, email, country, affiliation, created, pending)
values(?, ?, ?, ?, ?, ?, 1)
"""

def _add_pending(data):
    """Add database records for pending signup."""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    _check_registration_status(cur, data["email"])
    values = (data["hash"], data["fullname"], data["email"], data["country"], data["affiliation"], _get_date())
    cur.execute(Q_INSERT_SIGNER, values)
    con.commit()
    con.close()

def _check_registration_status(cur, email):
    found = cur.execute(Q_EMAIL_CHECK, (email,)).fetchone()
    if not found:
        return
    pending = found[0]
    if pending:
        raise CIPError(f"Error #14: already waiting to confirm signature for {email}")
    else:
        raise CIPError(f"Error #15: have already confirmed signature for {email}")

# ----------------------------------------------------------------------

Q_UPDATE_SIGNER = """
update signers
set pending = 0
where hash = ?
"""

Q_GET_SIGNER_NAME = """
select fullname
from signers
where hash = ?
"""

def _confirm_signature(identifier):
    """Confirm a signature."""
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(Q_UPDATE_SIGNER, (identifier,))
    if cur.rowcount == 0:
        raise CIPError(f"Error #14: unknown identifier {identifier}")
    elif cur.rowcount > 1:
        raise CIPError(f"Error #9: multiple entries for identifier {identifier}")

    cur.execute(Q_GET_SIGNER_NAME, (identifier,))
    row = cur.fetchone()
    fullname = row[0]
    
    con.commit()
    con.close()
    return fullname

# ----------------------------------------------------------------------

# Get everyone who has signed.
Q_SIGNERS = """
select fullname, coalesce(country, ""), coalesce(affiliation, ""), created
from signers
where not pending
order by created
"""
Q_SIGNERS_KEYS = "fullname country affiliation created".split()

def _get_signers():
    """Get all signers (one dictionary per row)."""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(Q_SIGNERS)
    rows =  cur.fetchall()
    result = [{k:v for k,v in zip(Q_SIGNERS_KEYS, r)} for r in rows]
    con.close()
    return result

# ----------------------------------------------------------------------

def _get_date():
    """Get the date formatted as YYYY-MM-DD."""
    return datetime.today().strftime("%Y-%m-%d")

def _get_form_values(form):
    """Get values from submitted signup form."""
    data = {
        "fullname": form["fullname"].strip(),
        "email": form["email"].strip(),
        "country": form["country"].strip(),
        "affiliation": form["affiliation"].strip()
    }
    hasher = hashlib.sha1(bytes(form["email"], encoding="utf-8"))
    data["hash"] = hasher.hexdigest()
    return data

def _send_confirmation_request(data):
    print(f"/confirmation/{data['hash']}/", file=sys.stderr)
