# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class DuplicateExamWizard(osv.osv_memory):
    _name = 'duplicate_exam_wizard'
    _description = 'Wizard para duplicar examen'

    _columns = {
        'exam_id': fields.many2one('odooeduconnect_exam', 'Examen', required=True, ondelete='cascade'),
        'new_name': fields.char('Nuevo nombre', required=True),
        'new_date': fields.date('Nueva fecha', required=True),
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        
        res = super(DuplicateExamWizard, self).default_get(cr, uid, fields, context=context)
        
        exam_id = context.get('active_id')
        if exam_id:
            exam_obj = self.pool.get('odooeduconnect_exam')
            exam = exam_obj.browse(cr, uid, exam_id, context=context)

            user_obj = self.pool.get('res.users')
            user = user_obj.browse(cr, uid, uid, context=context)
            user_name = user.name.replace(' ', '_') 

            res.update({
                'exam_id': exam_id,
                'new_name': "%s - %s" % (exam.name, user_name),
                'new_date': exam.date,
            })
        
        return res

    def confirm_duplicate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        wizard = self.browse(cr, uid, ids[0], context=context)
        exam_obj = self.pool.get('odooeduconnect_exam')
        question_obj = self.pool.get('odooeduconnect_question')
        answer_obj = self.pool.get('odooeduconnect_answer')
        
        try:
            new_exam_id = exam_obj.create(cr, uid, {
                'name': wizard.new_name,
                'date': wizard.new_date,
                'subject_id': wizard.exam_id.subject_id.id,
            }, context=context)
            
            for question in wizard.exam_id.question_ids:
                new_question_id = question_obj.create(cr, uid, {
                    'text': question.text,
                    'exam_id': new_exam_id,
                    'correct_answer': question.correct_answer,
                }, context=context)
                
                for answer in question.answer_ids:
                    answer_obj.create(cr, uid, {
                        'text': answer.text,
                        'is_correct': answer.is_correct,
                        'question_id': new_question_id,
                    }, context=context)
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'odooeduconnect_exam',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': new_exam_id,
                'target': 'current',
            }
            
        except Exception as e:
            raise osv.except_osv('Error', 'No se pudo duplicar el examen: %s' % str(e))
