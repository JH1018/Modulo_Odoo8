from openerp.osv import osv, fields

class Grade(osv.osv):
    _name = "odooeduconnect_grade"
    _description = "Grade"
    
    _columns = {
        "score": fields.integer("Score", required=True), 
        "student_id": fields.many2one('odooeduconnect_student', 'Student', required=True, ondelete='cascade'),
        "subject_id": fields.many2one('odooeduconnect_subject', 'Subject', required=True, ondelete='cascade'),
    }

    def create(self, cr, uid, vals, context=None):
        grade_id = super(Grade, self).create(cr, uid, vals, context=context)
        student_id = vals.get('student_id')
        if student_id:
            student_obj = self.pool.get('odooeduconnect_student')
            student_obj.write(cr, uid, [student_id], {'grades_ids': [(4, grade_id)]}, context=context)
        return grade_id
