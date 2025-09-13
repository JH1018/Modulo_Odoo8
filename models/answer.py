from openerp.osv import osv, fields

class Answer(osv.osv):
    _name = "odooeduconnect_answer"
    _description = "Answer"
    _rec_name = "text"


    _columns = {
        "text": fields.char("Answer Text", required=True),
        "is_correct": fields.boolean("Is Correct"),
        "question_id": fields.many2one(
            "odooeduconnect_question", 
            "Question", 
            required=True, 
            ondelete="cascade"
        )
    }
