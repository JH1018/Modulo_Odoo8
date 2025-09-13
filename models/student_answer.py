from openerp.osv import osv, fields

class StudentAnswer(osv.osv):
    _name = "odooeduconnect_student_answer"
    _description = "Student Answer"
    
    _columns = {
        "student_id": fields.many2one('odooeduconnect_student', 'Student', required=True, ondelete='cascade'),
        "question_id": fields.many2one('odooeduconnect_question', 'Question', required=True, ondelete='cascade'),
        "answer_id": fields.many2one('odooeduconnect_answer', 'Answer', required=True, ondelete='cascade'),
        "exam_id": fields.many2one('odooeduconnect_exam', 'Exam', required=True, ondelete='cascade'),
        "is_correct": fields.boolean("Is Correct"),
    }
