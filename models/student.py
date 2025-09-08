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
            string='Subjects',
        ),
        "room_id": fields.many2one('odooeduconnect_room', 'Room', required=False, ondelete='set null'),
        "grades_ids": fields.one2many('odooeduconnect_grade', 'student_id', 'Grades', ondelete='cascade'),
    }
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for student in self.browse(cr, uid, ids, context=context):
            display_name = "%s - %s" % (student.name, student.student_card)
            res.append((student.id, display_name))
        return res
    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        grade_obj = self.pool.get('odooeduconnect_grade')
        
        for student_id in ids:
            grade_ids = grade_obj.search(cr, uid, [
                ('student_id', '=', student_id)
            ], context=context)
            
            if grade_ids:
                try:
                    grade_obj.unlink(cr, uid, grade_ids, context=context)
                except Exception as e:
                    raise osv.except_osv(('Error!'), 
                        ('No se pudieron eliminar las notas del estudiante. Error: %s' % str(e)))
                    
        return super(Student, self).unlink(cr, uid, ids, context)