from openerp.osv import osv, fields

class Exam(osv.osv):
    _name = "odooeduconnect_exam"
    _description = "Exam"
    
    _columns = {
        "name": fields.char("Name", required=True),
        "date": fields.date("Date", required=True),
        "subject_id": fields.many2one(
            "odooeduconnect_subject", 
            "Subject", 
            required=True, 
            ondelete="cascade"
        ),
        "question_ids": fields.one2many(
            "odooeduconnect_question", 
            "exam_id", 
            "Questions"
        )
    }

    def duplicate_exam(self, cr, uid, ids, context=None):
        """Método para duplicar examen (opcional, el wizard maneja la lógica)"""
        for exam in self.browse(cr, uid, ids, context=context):
            new_exam = self.copy(cr, uid, exam.id, context=context)
        return True
