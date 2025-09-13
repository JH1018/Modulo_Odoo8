from openerp.osv import osv, fields

class Question(osv.osv):
    _name = "odooeduconnect_question"
    _description = "Question"
    _rec_name = "text"

    _columns = {
        "text": fields.char("Question Text", required=True),
        "correct_answer": fields.char("Correct Answer", required=True),
        "exam_id": fields.many2one(
            "odooeduconnect_exam", 
            "Exam", 
            required=True, 
            ondelete="cascade"
        ),
        "answer_ids": fields.one2many(
            "odooeduconnect_answer", 
            "question_id", 
            "Possible Answers"
        ),
    }
