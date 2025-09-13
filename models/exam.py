from openerp.osv import osv, fields

class Exam(osv.osv):
    _name = "odooeduconnect_exam"
    _description = "Exam"
    
    _columns = {
        "name": fields.char("Name", required=True),
        "date": fields.date("Date", required=True),
        "question_ids": fields.one2many('odooeduconnect_question', 'exam_id', 'Questions'),
        "subject_id": fields.many2one('odooeduconnect_subject', 'Subject', required=True, ondelete='cascade'),
    }
