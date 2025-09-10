from openerp.osv import osv, fields

class Teacher(osv.osv):
    _name = "odooeduconnect_teacher"
    _description = "Teacher"
    
    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "profile_picture": fields.binary("Profile Picture"),
        "age": fields.integer("Age", required=True),
        "address": fields.char("Address", size=256),
        "email": fields.char("Email", required=True, size=128),
        "phone": fields.char("Phone", required=True, size=8),
        "subject_ids": fields.one2many('odooeduconnect_subject', 'teacher_id', 'Subjects'),
    }