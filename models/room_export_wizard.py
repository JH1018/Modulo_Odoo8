# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import base64
from reportlab.pdfgen import canvas
from cStringIO import StringIO

class RoomExportWizard(osv.osv_memory):
    _name = 'room.export.wizard'
    _description = 'Wizard para exportar salones'

    _columns = {
        'dummy': fields.char('Campo Temporal'),
        'file_data': fields.binary('Archivo PDF'),
        'file_name': fields.char('Nombre de archivo'),
    }

    def action_export_pdf(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        try:
            room_obj = self.pool.get('odooeduconnect_room')
            room_ids = room_obj.search(cr, uid, [], context=context)
            
            if not room_ids:
                raise Exception("No se encontraron salones en la base de datos")
                
            rooms = room_obj.browse(cr, uid, room_ids, context=context)

            buffer = StringIO()
            pdf = canvas.Canvas(buffer)
            pdf.setTitle("Reporte de Salones")
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
            pdf.drawString(100, y, "Reporte de Salones")
            y -= 30
            pdf.setFont("Helvetica", 10)
            pdf.drawString(100, y, "Generado con ReportLab - Total: {} salones".format(len(rooms)))
            y -= 40

            for i, room in enumerate(rooms):
                if y < 150:
                    pdf.showPage()
                    y = 800

                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, y, "Información de Salón #{}".format(i + 1))
                y -= 25

                pdf.setFont("Helvetica", 12)
                
                info_data = [
                    ("Nombre", safe_get(room, 'name')),
                    ("Número", safe_get(room, 'number')),
                    ("Capacidad", safe_get(room, 'capacity')),
                ]

                for label, value in info_data:
                    pdf.drawString(100, y, "{}: {}".format(label, value))
                    y -= 15

                try:
                    if hasattr(room, 'description') and room.description:
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(100, y, "Descripción:")
                        y -= 12
                        pdf.setFont("Helvetica", 12)
                        description = safe_get(room, 'description')
                        if len(description) > 60:
                            lines = [description[j:j+60] for j in range(0, len(description), 60)]
                            for line in lines:
                                pdf.drawString(120, y, line)
                                y -= 12
                        else:
                            pdf.drawString(120, y, description)
                            y -= 12
                    y -= 5
                except:
                    pass

                try:
                    if hasattr(room, 'location') and room.location:
                        location = safe_get(room, 'location')
                        pdf.drawString(100, y, "Ubicacion: {}".format(location))
                        y -= 15
                except:
                    pass

                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(100, y, "Estado y uso del salón:")
                y -= 15
                pdf.setFont("Helvetica", 12)

                try:
                    subject_obj = self.pool.get('odooeduconnect_subject')
                    subject_ids = subject_obj.search(cr, uid, [('room_id', '=', room.id)], context=context)
                    
                    if subject_ids:
                        subjects = subject_obj.browse(cr, uid, subject_ids, context=context)
                        pdf.drawString(120, y, "Materias asignadas:")
                        y -= 12
                        
                        for subject in subjects:
                            subject_name = subject.name if subject.name else "Materia sin nombre"
                            subject_code = subject.code if subject.code else "Sin código"
                            
                            teacher_name = "Sin maestro"
                            if hasattr(subject, 'teacher_id') and subject.teacher_id:
                                teacher_name = subject.teacher_id.name if subject.teacher_id.name else "Sin nombre"
                            
                            pdf.drawString(140, y, "{} ({}) - Maestro: {}".format(subject_name, subject_code, teacher_name))
                            y -= 12
                        
                        total_students = 0
                        for subject in subjects:
                            if hasattr(subject, 'students') and subject.students:
                                total_students += len(subject.students)
                        
                        try:
                            capacity = int(safe_get(room, 'capacity', '0'))
                            if capacity > 0:
                                occupancy_rate = (total_students / capacity) * 100
                                pdf.drawString(120, y, "Estudiantes totales: {} de {} ({:.1f}% ocupacion)".format(
                                    total_students, capacity, occupancy_rate))
                            else:
                                pdf.drawString(120, y, "Estudiantes totales: {} (capacidad no definida)".format(total_students))
                            y -= 15
                        except:
                            pdf.drawString(120, y, "Estudiantes totales: {} (error al calcular ocupacion)".format(total_students))
                            y -= 15
                            
                    else:
                        pdf.drawString(120, y, "Estado: DISPONIBLE (sin materias asignadas)")
                        y -= 15
                        
                except Exception as e:
                    pdf.drawString(120, y, "Error al obtener información de uso: {}".format(str(e)))
                    y -= 15

                try:
                    if hasattr(room, 'equipment') and room.equipment:
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(100, y, "Equipamiento:")
                        y -= 12
                        pdf.setFont("Helvetica", 12)
                        equipment = safe_get(room, 'equipment')
                        pdf.drawString(120, y, equipment)
                        y -= 15
                except:
                    pass

                pdf.setStrokeGray(0.5)
                pdf.line(100, y-5, 500, y-5)
                y -= 25

            if len(rooms) > 0:
                pdf.showPage()
                y = 800
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(100, y, "Estadísticas de Salones")
                y -= 30
                
                try:
                    total_rooms = len(rooms)
                    total_capacity = 0
                    occupied_rooms = 0
                    available_rooms = 0
                    
                    for room in rooms:
                        try:
                            capacity = int(safe_get(room, 'capacity', '0'))
                            total_capacity += capacity
                            
                            subject_obj = self.pool.get('odooeduconnect_subject')
                            subject_ids = subject_obj.search(cr, uid, [('room_id', '=', room.id)], context=context)
                            
                            if subject_ids:
                                occupied_rooms += 1
                            else:
                                available_rooms += 1
                        except:
                            continue
                    
                    pdf.setFont("Helvetica", 12)
                    stats_data = [
                        ("Total de salones", str(total_rooms)),
                        ("Capacidad total", str(total_capacity)),
                        ("Salones ocupados", str(occupied_rooms)),
                        ("Salones disponibles", str(available_rooms)),
                        ("Porcentaje de ocupacion", "{:.1f}%".format((occupied_rooms/total_rooms)*100 if total_rooms > 0 else 0)),
                        ("Capacidad promedio", "{:.1f}".format(total_capacity/total_rooms if total_rooms > 0 else 0))
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
                'file_name': 'Reporte_Salones.pdf'
            }, context=context)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'room.export.wizard',
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
            pdf.drawString(100, 750, "Error al generar reporte de salones")
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 720, "Error: {}".format(str(e)))
            pdf.showPage()
            pdf.save()
            pdf_data = buffer.getvalue()
            buffer.close()
            
            pdf_base64 = base64.b64encode(pdf_data)
            self.write(cr, uid, ids, {
                'file_data': pdf_base64,
                'file_name': 'Error_Reporte_Salones.pdf'
            }, context=context)
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'room.export.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': ids[0],
                'target': 'new',
            }
