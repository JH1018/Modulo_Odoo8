from openerp.osv import osv, fields
import base64
from reportlab.pdfgen import canvas
from cStringIO import StringIO

class TeacherExportWizard(osv.osv_memory):
    _name = 'teacher.export.wizard'
    _description = 'Wizard para exportar maestros'

    _columns = {
        'dummy': fields.char('Campo Temporal'),
        'file_data': fields.binary('Archivo PDF'),
        'file_name': fields.char('Nombre de archivo'),
    }

    def action_export_pdf(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        try:
            teacher_obj = self.pool.get('odooeduconnect_teacher')
            teacher_ids = teacher_obj.search(cr, uid, [], context=context)
            
            if not teacher_ids:
                raise Exception("No se encontraron maestros en la base de datos")
                
            teachers = teacher_obj.browse(cr, uid, teacher_ids, context=context)

            buffer = StringIO()
            pdf = canvas.Canvas(buffer)
            pdf.setTitle("Reporte de Maestros")
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
            pdf.drawString(100, y, "Reporte de Maestros")
            y -= 30
            pdf.setFont("Helvetica", 10)
            pdf.drawString(100, y, "Generado con ReportLab - Total: {} maestros".format(len(teachers)))
            y -= 40

            for i, teacher in enumerate(teachers):
                if y < 150:
                    pdf.showPage()
                    y = 800

                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, y, "Ficha del Maestro #{}".format(i + 1))
                y -= 25

                pdf.setFont("Helvetica", 12)
                
                info_data = [
                    ("Nombre", safe_get(teacher, 'name')),
                    ("Edad", safe_get(teacher, 'age')),
                    ("Email", safe_get(teacher, 'email')),
                    ("Telefono", safe_get(teacher, 'phone')),
                    ("Direccion", safe_get(teacher, 'address')),
                ]

                for label, value in info_data:
                    pdf.drawString(100, y, "{}: {}".format(label, value))
                    y -= 15

                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(100, y, "Materias que imparte:")
                y -= 15
                pdf.setFont("Helvetica", 12)
                
                try:
                    if hasattr(teacher, 'subject_ids') and teacher.subject_ids:
                        for subj in teacher.subject_ids:
                            subject_name = subj.name if subj.name else "Materia sin nombre"
                            pdf.drawString(120, y, "- {}".format(subject_name))
                            y -= 15
                    else:
                        pdf.drawString(120, y, "- No tiene materias asignadas")
                        y -= 15
                except Exception as e:
                    pdf.drawString(120, y, "- Error al obtener materias: {}".format(str(e)))
                    y -= 15

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
                'file_name': 'Reporte_Maestros.pdf'
            }, context=context)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'teacher.export.wizard',
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
            pdf.drawString(100, 750, "Error al generar reporte de maestros")
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 720, "Error: {}".format(str(e)))
            pdf.showPage()
            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()
            
            pdf_base64 = base64.b64encode(pdf_data)
            self.write(cr, uid, ids, {
                'file_data': pdf_base64,
                'file_name': 'Error_Reporte_Maestros.pdf'
            }, context=context)
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'teacher.export.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': ids[0],
                'target': 'new',
            }
