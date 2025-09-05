from openerp.osv import osv, fields

class Grade(osv.osv):
    _name = "odooeduconnect_grade"
    _description = "Grade"
    
    _columns = {
        "score": fields.integer("Score", required=True), 
        "student_id": fields.many2one('odooeduconnect_student', 'Student', required=True),
        "subject_id": fields.many2one('odooeduconnect_subject', 'Subject', required=True),
    }
