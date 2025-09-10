from openerp.osv import osv, fields
from openerp.tools.translate import _

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
        "prefix": fields.char("Prefijo", required=True, size=3),
        "student_card": fields.char("ID Card", readonly=True, size=10),
        "subjects": fields.many2many(
            'odooeduconnect_subject',
            'student_subject_rel',
            'student_id',
            'subject_id',
            string='Subjects',
        ),
        "room_id": fields.many2one('odooeduconnect_room', 'Room', ondelete='set null'),
        "grades_ids": fields.one2many('odooeduconnect_grade', 'student_id', 'Grades', ondelete='cascade'),
    }

    def create(self, cr, uid, vals, context=None):
        if 'prefix' in vals:
            prefix = vals['prefix'].upper()
            existing_ids = self.search(cr, uid, [('student_card', 'ilike', prefix + '%')], context=context)
            max_seq = 0
            for student in self.browse(cr, uid, existing_ids, context=context):
                num_part = student.student_card[3:]
                if num_part.isdigit():
                    max_seq = max(max_seq, int(num_part))
            next_seq = max_seq + 1
            vals['student_card'] = prefix + str(next_seq).zfill(7)

        return super(Student, self).create(cr, uid, vals, context=context)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for student in self.browse(cr, uid, ids, context=context):
            res.append((student.id, "%s - %s" % (student.name, student.student_card)))
        return res
