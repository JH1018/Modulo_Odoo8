from openerp.osv import osv, fields

class Student(osv.osv):
    _name = "odooEduConnect.student"
    _description = "Student"

    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "age": fields.integer("Age", required=True),
        "address": fields.char("Address", size=256),
        "section": fields.char("Section", required=True, size=1),
        "grade": fields.integer("Grade", required=True),
        "email": fields.char("Email", required=True, size=128),
        "phone": fields.char("Phone", required=True, size=8),
        "student_card": fields.char("ID Card", required=True, size=10),
        "subjects": fields.many2many('odooEduConnect.subject', string='Subjects'),
        "room_id": fields.many2one('odooEduConnect.room', 'Room', required=True)
    }
