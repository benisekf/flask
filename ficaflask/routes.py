from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Contact
from . import db
bp = Blueprint('main', __name__)
@bp.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('hello.html', contacts=contacts)
@bp.route('/edit/<email>', methods=['GET', 'POST'])
def edit_contact(email):
    contact = Contact.query.filter_by(email=email).first()
    if request.method == 'POST':
        contact.ime = request.form['ime']
        contact.prezime = request.form['prezime']
        contact.email = request.form['email']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit.html', contact=contact)
@bp.route('/delete/<email>', methods=['POST'])
def delete_contact(email):
    contact = Contact.query.filter_by(email=email).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('main.index'))
@bp.route('/add', methods=['POST'])
def add_contact():
    ime = request.form['ime']
    prezime = request.form['prezime']
    email = request.form['email']
    if not ime or not prezime or not email:
        flash('All fields are required.')
        return redirect(url_for('main.index'))
    existing_contact = Contact.query.filter_by(email=email).first()
    if existing_contact:
        flash('A contact with this email already exists.')
        return redirect(url_for('main.index'))
    new_contact = Contact(ime=ime, prezime=prezime, email=email)
    db.session.add(new_contact)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the contact.')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))