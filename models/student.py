from openerp.osv import osv, fields

class Student(osv.osv):
    _name = "odooeduconnect_student"
    _description = "Student"

    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "profile_picture": fields.binary("Profile Picture"),
        "age": fields.integer("Age", required=True),
        "address": fields.char("Address", size=256),
        "section": fields.char("Section", required=True, size=1),
        "grade": fields.integer("Grade", required=True),
        "email": fields.char("Email", required=True, size=128),
        "phone": fields.char("Phone", required=True, size=8),
        "student_card": fields.char("ID Card", required=True, size=10),
        "subjects": fields.many2many(
            'odooeduconnect_subject',
            'student_subject_rel',
            'student_id',
            'subject_id',
            string='Subjects'
        ),
        "room_id": fields.many2one('odooeduconnect_room', 'Room', required=False),
        "grades_ids": fields.one2many('odooeduconnect_grade', 'student_id', 'Grades'),
    }