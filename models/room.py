# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class Room(osv.osv):
    _name = "odooeduconnect_room"
    _description = "Room"
    
    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "capacity": fields.integer("Capacity", required=True),
        "students": fields.many2many(
            'odooeduconnect_student',   
            'room_student_rel',         
            'room_id',                  
            'student_id',               
            'Students'               
        ),
        "subject_id": fields.one2many(
            'odooeduconnect_subject',  
            'room_id',                  
            'Subjects',
        ),
    }

    def write(self, cr, uid, ids, vals, context=None):
        if context and context.get('install_mode'):
            return super(Room, self).write(cr, uid, ids, vals, context=context)
            
        if 'students' in vals:
            room = self.browse(cr, uid, ids[0], context=context)
            current_student_ids = set(s.id for s in room.students)

            for command in vals['students']:
                try:
                    cmd_type = command[0]
                    if cmd_type == 4:  
                        current_student_ids.add(command[1])
                    elif cmd_type == 6:  
                        ids_list = command[2] if len(command) >= 3 and isinstance(command[2], (list, tuple)) else []
                        current_student_ids = set(ids_list)
                    elif cmd_type == 3:  
                        current_student_ids.discard(command[1])
                    elif cmd_type == 5:  
                        current_student_ids = set()
                    elif cmd_type == 0:  
                        current_student_ids.add(len(current_student_ids) + 1)
                except (IndexError, TypeError):
                    continue

            if len(current_student_ids) > room.capacity:
                raise osv.except_osv(_('Error!'), _('No se puede agregar: la sala ya alcanzó su capacidad.'))
        return super(Room, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        capacity = vals.get('capacity', 0)
        student_commands = vals.get('students', [])

        student_count = 0
        for cmd in student_commands:
            try:
                cmd_type = cmd[0]
                if cmd_type == 0:   
                    student_count += 1
                elif cmd_type == 4:  
                    student_count += 1
                elif cmd_type == 6:
                    ids_list = cmd[2] if len(cmd) >= 3 and isinstance(cmd[2], (list, tuple)) else []
                    student_count = len(ids_list)
            except (IndexError, TypeError):
                continue

        if student_count > capacity:
            raise osv.except_osv(_('Error!'), _('No se puede crear la sala: supera la capacidad'))

        return super(Room, self).create(cr, uid, vals, context=context)
