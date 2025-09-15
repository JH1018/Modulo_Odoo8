# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import base64
from reportlab.pdfgen import canvas
from cStringIO import StringIO

class GradeExportWizard(osv.osv_memory):
    _name = 'grade.export.wizard'
    _description = 'Wizard para exportar calificaciones'

    _columns = {
        'dummy': fields.char('Campo Temporal'),
        'file_data': fields.binary('Archivo PDF'),
        'file_name': fields.char('Nombre de archivo'),
    }

    def action_export_pdf(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        try:
            grade_obj = self.pool.get('odooeduconnect_grade')
            grade_ids = grade_obj.search(cr, uid, [], context=context)
            
            if not grade_ids:
                raise Exception("No se encontraron calificaciones en la base de datos")
                
            grades = grade_obj.browse(cr, uid, grade_ids, context=context)

            buffer = StringIO()
            pdf = canvas.Canvas(buffer)
            pdf.setTitle("Reporte de Calificaciones")
            y = 800 
            
            def safe_get(obj, field, default="N/A"):
                try:
                    value = getattr(obj, field, None)
                    if value is None or str(value).strip() == '' or str(value) == 'False':
                        return default
                    return str(value)
                except:
                    return default

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(100, y, "Reporte de Calificaciones")
            y -= 30
            pdf.setFont("Helvetica", 10)
            pdf.drawString(100, y, "Generado con ReportLab - Total: {} calificaciones".format(len(grades)))
            y -= 40

            for i, grade in enumerate(grades):
                if y < 150:
                    pdf.showPage()
                    y = 800

                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, y, "Calificacion #{}".format(i + 1))
                y -= 25

                pdf.setFont("Helvetica", 12)
                
                info_data = [
                    ("Puntuacion", safe_get(grade, 'score')),
                    ("Fecha", safe_get(grade, 'date')),
                ]

                for label, value in info_data:
                    pdf.drawString(100, y, "{}: {}".format(label, value))
                    y -= 15

                try:
                    if hasattr(grade, 'student_id') and grade.student_id:
                        student_name = grade.student_id.name if grade.student_id.name else "Sin nombre"
                        pdf.drawString(100, y, "Estudiante: {}".format(student_name))
                    else:
                        pdf.drawString(100, y, "Estudiante: No asignado")
                    y -= 15
                except:
                    pdf.drawString(100, y, "Estudiante: Error al obtener información")
                    y -= 15

                try:
                    if hasattr(grade, 'subject_id') and grade.subject_id:
                        subject_name = grade.subject_id.name if grade.subject_id.name else "Sin nombre"
                        subject_code = grade.subject_id.code if grade.subject_id.code else "Sin código"
                        pdf.drawString(100, y, "Materia: {} ({})".format(subject_name, subject_code))
                    else:
                        pdf.drawString(100, y, "Materia: No asignada")
                    y -= 15
                except:
                    pdf.drawString(100, y, "Materia: Error al obtener información")
                    y -= 15

                try:
                    if hasattr(grade, 'subject_id') and grade.subject_id and hasattr(grade.subject_id, 'teacher_id') and grade.subject_id.teacher_id:
                        teacher_name = grade.subject_id.teacher_id.name if grade.subject_id.teacher_id.name else "Sin nombre"
                        pdf.drawString(100, y, "Maestro: {}".format(teacher_name))
                    else:
                        pdf.drawString(100, y, "Maestro: No disponible")
                    y -= 15
                except:
                    pdf.drawString(100, y, "Maestro: Error al obtener información")
                    y -= 15

                try:
                    score_value = float(safe_get(grade, 'score', '0'))
                    if score_value >= 70: 
                        status = "APROBADO"
                        status_color = "green"
                    else:
                        status = "REPROBADO"
                        status_color = "red"
                    
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.drawString(100, y, "Estado: {}".format(status))
                    y -= 15
                    pdf.setFont("Helvetica", 12)
                except:
                    pdf.drawString(100, y, "Estado: Error al calcular")
                    y -= 15

                try:
                    if hasattr(grade, 'notes') and grade.notes:
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(100, y, "Comentarios:")
                        y -= 12
                        pdf.setFont("Helvetica", 12)
                        notes = safe_get(grade, 'notes')
                        if len(notes) > 60:
                            lines = [notes[j:j+60] for j in range(0, len(notes), 60)]
                            for line in lines:
                                pdf.drawString(120, y, line)
                                y -= 12
                        else:
                            pdf.drawString(120, y, notes)
                            y -= 12
                    y -= 5
                except:
                    pass

                pdf.setStrokeGray(0.5)
                pdf.line(100, y-5, 500, y-5)
                y -= 25

            if len(grades) > 0:
                pdf.showPage()
                y = 800
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(100, y, "Estadísticas Generales")
                y -= 30
                
                try:
                    total_grades = len(grades)
                    scores = []
                    approved = 0
                    failed = 0
                    
                    for grade in grades:
                        try:
                            score = float(safe_get(grade, 'score', '0'))
                            scores.append(score)
                            if score >= 70:
                                approved += 1
                            else:
                                failed += 1
                        except:
                            continue
                    
                    if scores:
                        avg_score = sum(scores) / len(scores)
                        max_score = max(scores)
                        min_score = min(scores)
                        
                        pdf.setFont("Helvetica", 12)
                        stats_data = [
                            ("Total de calificaciones", str(total_grades)),
                            ("Promedio general", "{:.2f}".format(avg_score)),
                            ("Calificacion mas alta", "{:.2f}".format(max_score)),
                            ("Calificacion mas baja", "{:.2f}".format(min_score)),
                            ("Estudiantes aprobados", str(approved)),
                            ("Estudiantes reprobados", str(failed)),
                            ("Porcentaje de aprobacion", "{:.1f}%".format((approved/total_grades)*100 if total_grades > 0 else 0))
                        ]
                        
                        for label, value in stats_data:
                            pdf.drawString(100, y, "{}: {}".format(label, value))
                            y -= 15
                except Exception as e:
                    pdf.drawString(100, y, "Error al calcular estadísticas: {}".format(str(e)))

            pdf.showPage()
            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()

            pdf_base64 = base64.b64encode(pdf_data)

            self.write(cr, uid, ids, {
                'file_data': pdf_base64,
                'file_name': 'Reporte_Calificaciones.pdf'
            }, context=context)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'grade.export.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': ids[0],
                'target': 'new',
            }

        except Exception as e:
            buffer = StringIO()
            pdf = canvas.Canvas(buffer)
            pdf.setTitle("Error en Reporte")
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(100, 750, "Error al generar reporte de calificaciones")
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 720, "Error: {}".format(str(e)))
            pdf.showPage()
            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()
            
            pdf_base64 = base64.b64encode(pdf_data)
            self.write(cr, uid, ids, {
                'file_data': pdf_base64,
                'file_name': 'Error_Reporte_Calificaciones.pdf'
            }, context=context)
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'grade.export.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': ids[0],
                'target': 'new',
            }
