from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
contacts = []
@app.route('/')
def index():
    return render_template('hello.html', contacts=contacts)
@app.route('/add', methods=['POST'])
def add_contact():
    ime = request.form['ime']
    prezime = request.form['prezime']
    email = request.form['email']
    new_contact = {'ime': ime, 'prezime': prezime, 'email': email}
    contacts.append(new_contact)
    return redirect(url_for('index'))
@app.route('/edit/<email>', methods=['GET', 'POST'])
def edit_contact(email):
    contact_to_edit = next((contact for contact in contacts if contact['email'] == email), None)
    if contact_to_edit is None:
        return "Contact not found"
    if request.method == 'POST':
        contact_to_edit['ime'] = request.form['ime']
        contact_to_edit['prezime'] = request.form['prezime']
        contact_to_edit['email'] = request.form['email']
        return redirect(url_for('index'))
    return render_template('edit.html', contact=contact_to_edit)
@app.route('/delete/<email>', methods=['POST'])
def delete_contact(email):
    global contacts
    contacts = [contact for contact in contacts if contact['email'] != email]
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)