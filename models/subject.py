from openerp.osv import osv, fields

class Subject(osv.osv):
    _name = "odooeduconnect_subject"
    _description = "Subject"

    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "code": fields.char("Code", required=True, size=10),
        "description": fields.text("Description"),
        "room_id": fields.many2one('odooeduconnect_room', 'Room', required=False, ondelete='set null'),
        "students": fields.many2many(
            'odooeduconnect_student',
            'student_subject_rel',
            'subject_id',
            'student_id',
            string='Students',
        ),
        "teacher_id": fields.many2one(
            'odooeduconnect_teacher',
            'Teacher',
            ondelete='cascade'
        ),
    }
