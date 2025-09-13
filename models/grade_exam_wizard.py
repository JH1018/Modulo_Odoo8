from openerp.osv import osv, fields
from datetime import date

class GradeExamWizard(osv.osv_memory):
    _name = "grade.exam.wizard"
    _description = "Wizard para Calificar Examen"

    _columns = {
        "exam_id": fields.many2one("odooeduconnect_exam", "Examen", required=True),
        "student_id": fields.many2one("odooeduconnect_student", "Estudiante", required=True),
        "questions": fields.integer("Numero de preguntas", readonly=True),
        "score": fields.integer("Puntuacion obtenida", readonly=True),
        "max_score": fields.integer("Puntuacion maxima", readonly=True),
        "percentage": fields.float("Porcentaje", readonly=True),
        "date": fields.date("Fecha de calificacion"),
        "calculation_detail": fields.text("Detalle del calculo", readonly=True),
    }

    def default_get(self, cr, uid, field_list, context=None):
        if context is None:
            context = {}

        res = super(GradeExamWizard, self).default_get(cr, uid, field_list, context=context)

        exam_id = context.get('active_id')
        if exam_id:
            res.update({
                'exam_id': exam_id,
                'date': date.today().strftime('%Y-%m-%d'),
                'questions': 0,
                'score': 0,
                'max_score': 0,
                'percentage': 0.0,
            })
        return res

    def action_calculate_score(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wizard = self.browse(cr, uid, ids[0], context=context)
        exam = wizard.exam_id
        student = wizard.student_id

        total_score = 0
        max_score = 0
        questions = 0

        for question in exam.question_ids:
            questions += 1
            max_score += 1
            
            correct_answer_text = question.correct_answer or ""
            question_correct = False
            
            if question.answer_ids:
                for answer in question.answer_ids:
                    answer_text = (answer.text or "").strip().lower()
                    correct_text = correct_answer_text.strip().lower()
                    
                    if answer.is_correct and answer_text == correct_text:
                        total_score += 1
                        question_correct = True
                        break
                
                if not question_correct:
                    for answer in question.answer_ids:
                        if answer.is_correct:
                            answer_text = (answer.text or "").strip().lower()
                            correct_text = correct_answer_text.strip().lower()
                            if correct_text in answer_text or answer_text in correct_text:
                                total_score += 1
                                question_correct = True
                                break

        percentage = (total_score * 100.0 / max_score) if max_score > 0 else 0.0
        
        final_detail = "RESUMEN FINAL:\n"
        final_detail += "Total de preguntas: %d\n" % questions
        final_detail += "Respuestas correctas: %d\n" % total_score
        final_detail += "Puntuacion maxima: %d\n" % max_score
        final_detail += "Porcentaje: %.2f%%" % percentage

        self.write(cr, uid, ids, {
            "score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "questions": questions,
            "calculation_detail": final_detail,
        }, context=context)

        grade_vals = {
            "score": percentage,
            "student_id": student.id,
            "subject_id": exam.subject_id.id,
            "date": wizard.date,
        }
        self.pool.get("odooeduconnect_grade").create(cr, uid, grade_vals, context=context)

        return {
            "type": "ir.actions.act_window",
            "res_model": "grade.exam.wizard",
            "view_mode": "form",
            "view_type": "form",
            "res_id": wizard.id,
            "target": "new",
        }
