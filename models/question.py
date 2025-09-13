from openerp.osv import osv, fields

class Question(osv.osv):
    _name = "odooeduconnect_question"
    _description = "Question"
    
    _columns = {
        "text": fields.text("Text", required=True),
        "answer_ids": fields.one2many('odooeduconnect_answer','question_id', 'Answers'),
        "exam_id": fields.many2one('odooeduconnect_exam', 'Exam', required=False, ondelete='cascade')
    }
