# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class Subject(osv.osv):
    _name = "odooeduconnect_subject"
    _description = "Subject"

    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "code": fields.char("Code", required=True, size=10),
        "lesson_time": fields.char("Lesson Time", required=True),
        "description": fields.text("Description"),
        "room_id": fields.many2one(
            'odooeduconnect_room', 
            'Room', 
            required=False, 
            ondelete='set null'
        ),
        "students": fields.many2many(
            'odooeduconnect_student',
            'student_subject_rel',
            'subject_id',
            'student_id',
            string='Students',
            required=False
        ),
        "teacher_id": fields.many2one(
            'odooeduconnect_teacher',
            'Teacher',
            ondelete='set null',
            required=False
        ),
        "exam_ids": fields.one2many(
            'odooeduconnect_exam',
            'subject_id',
            'Exams'
        )
    }