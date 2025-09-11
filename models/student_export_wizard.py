from openerp.osv import osv, fields
import base64
from reportlab.pdfgen import canvas
from cStringIO import StringIO

class StudentExportWizard(osv.osv_memory):
    _name = 'student.export.wizard'
    _description = 'Wizard para exportar estudiantes'

    _columns = {
        'dummy': fields.char('Campo Temporal'),
        'file_data': fields.binary('Archivo PDF'),
        'file_name': fields.char('Nombre de archivo'),
    }

    def action_export_pdf(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        student_obj = self.pool.get('odooeduconnect_student')
        student_ids = student_obj.search(cr, uid, [], context=context)
        students = student_obj.browse(cr, uid, student_ids, context=context)

        buffer = StringIO()
        pdf = canvas.Canvas(buffer)
        pdf.setTitle("Reporte de Estudiantes")
        y = 800 
        
        for student in students:
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(100, y, "Ficha del Estudiante")
            y -= 20
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, y, "Nombre: {}".format(student.name or ''))
            y -= 15
            pdf.drawString(100, y, "Edad: {}".format(student.age or ''))
            y -= 15
            pdf.drawString(100, y, "Seccion: {}".format(student.section or ''))
            y -= 15
            pdf.drawString(100, y, "Grado: {}".format(student.grade or ''))
            y -= 15
            pdf.drawString(100, y, "Email: {}".format(student.email or ''))
            y -= 15
            pdf.drawString(100, y, "Telefono: {}".format(student.phone or ''))
            y -= 15
            pdf.drawString(100, y, "Prefijo: {}".format(student.prefix or ''))
            y -= 15
            pdf.drawString(100, y, "Carnet: {}".format(student.student_card or ''))
            y -= 15
            pdf.drawString(100, y, "Salon: {}".format(student.room_id.name or ''))
            y -= 20

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(100, y, "Materias:")
            y -= 15
            pdf.setFont("Helvetica", 12)
            for subj in student.subjects:
                pdf.drawString(120, y, "- {}".format(subj.name))
                y -= 15

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(100, y, "Notas:")
            y -= 15
            pdf.setFont("Helvetica", 12)
            for grade in student.grades_ids:
                pdf.drawString(120, y, "{}: {}".format(grade.subject_id.name, grade.score))
                y -= 15

            if y < 100:
                pdf.showPage()
                y = 800
            else:
                y -= 20

        pdf.showPage()
        pdf.save()
        pdf_data = buffer.getvalue()
        buffer.close()

        pdf_base64 = base64.b64encode(pdf_data)

        print("Cantidad de estudiantes:", len(students))
        for s in students:
            print("Nombre:", s.name, "Edad:", s.age)


        self.write(cr, uid, ids, {
            'file_data': pdf_base64,
            'file_name': 'Reporte_Estudiantes.pdf'
        }, context=context)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'student.export.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': ids[0],
            'target': 'new',
        }
