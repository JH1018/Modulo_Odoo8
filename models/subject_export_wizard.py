from openerp.osv import osv, fields
import base64
from reportlab.pdfgen import canvas
from cStringIO import StringIO

class SubjectExportWizard(osv.osv_memory):
    _name = 'subject.export.wizard'
    _description = 'Wizard para exportar materias'

    _columns = {
        'dummy': fields.char('Campo Temporal'),
        'file_data': fields.binary('Archivo PDF'),
        'file_name': fields.char('Nombre de archivo'),
    }

    def action_export_pdf(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        try:
            subject_obj = self.pool.get('odooeduconnect_subject')
            subject_ids = subject_obj.search(cr, uid, [], context=context)
            
            if not subject_ids:
                raise Exception("No se encontraron materias en la base de datos")
                
            subjects = subject_obj.browse(cr, uid, subject_ids, context=context)

            buffer = StringIO()
            pdf = canvas.Canvas(buffer)
            pdf.setTitle("Reporte de Materias")
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
            pdf.drawString(100, y, "Reporte de Materias")
            y -= 30
            pdf.setFont("Helvetica", 10)
            pdf.drawString(100, y, "Generado con ReportLab - Total: {} materias".format(len(subjects)))
            y -= 40

            for i, subject in enumerate(subjects):
                if y < 150:
                    pdf.showPage()
                    y = 800

                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, y, "Informacion de Materia #{}".format(i + 1))
                y -= 25

                pdf.setFont("Helvetica", 12)
                
                info_data = [
                    ("Nombre", safe_get(subject, 'name')),
                    ("Codigo", safe_get(subject, 'code')),
                    ("Descripcion", safe_get(subject, 'description')),
                ]

                for label, value in info_data:
                    pdf.drawString(100, y, "{}: {}".format(label, value))
                    y -= 15

                try:
                    if hasattr(subject, 'teacher_id') and subject.teacher_id:
                        teacher_name = subject.teacher_id.name if subject.teacher_id.name else "Sin nombre"
                        pdf.drawString(100, y, "Maestro: {}".format(teacher_name))
                    else:
                        pdf.drawString(100, y, "Maestro: No asignado")
                    y -= 15
                except:
                    pdf.drawString(100, y, "Maestro: Error al obtener informacion")
                    y -= 15

                try:
                    if hasattr(subject, 'room_id') and subject.room_id:
                        room_name = subject.room_id.name if subject.room_id.name else "Sin nombre"
                        pdf.drawString(100, y, "Salon: {}".format(room_name))
                    else:
                        pdf.drawString(100, y, "Salon: No asignado")
                    y -= 20
                except:
                    pdf.drawString(100, y, "Salon: Error al obtener informacion")
                    y -= 20

                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(100, y, "Estudiantes inscritos:")
                y -= 15
                pdf.setFont("Helvetica", 12)
                
                try:
                    if hasattr(subject, 'students') and subject.students:
                        for student in subject.students:
                            student_name = student.name if student.name else "Estudiante sin nombre"
                            pdf.drawString(120, y, "- {}".format(student_name))
                            y -= 12
                    else:
                        pdf.drawString(120, y, "- No hay estudiantes inscritos")
                        y -= 12
                except Exception as e:
                    pdf.drawString(120, y, "- Error al obtener estudiantes: {}".format(str(e)))
                    y -= 12

                pdf.setStrokeGray(0.5)
                pdf.line(100, y-5, 500, y-5)
                y -= 25

            pdf.showPage()
            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()

            pdf_base64 = base64.b64encode(pdf_data)

            self.write(cr, uid, ids, {
                'file_data': pdf_base64,
                'file_name': 'Reporte_Materias.pdf'
            }, context=context)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'subject.export.wizard',
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
            pdf.drawString(100, 750, "Error al generar reporte de materias")
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 720, "Error: {}".format(str(e)))
            pdf.showPage()
            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()
            
            pdf_base64 = base64.b64encode(pdf_data)
            self.write(cr, uid, ids, {
                'file_data': pdf_base64,
                'file_name': 'Error_Reporte_Materias.pdf'
            }, context=context)
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'subject.export.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': ids[0],
                'target': 'new',
            }
