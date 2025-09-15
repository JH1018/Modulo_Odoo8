# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class Student(osv.osv):
    _name = "odooeduconnect_student"
    _description = "Student"

    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "profile_picture": fields.binary("Profile Picture"),
        "age": fields.integer("Age", required=True),
        "address": fields.char("Address", size=256),
        "section": fields.char("Section", required=True, size=1),
        "grade": fields.integer("Grade", required=True),
        "email": fields.char("Email", required=True, size=128),
        "password": fields.char("Password", required=True, size=64),
        "phone": fields.integer("Phone", required=True, size=8),
        "prefix": fields.char("Prefijo", required=True, size=3),
        "student_card": fields.char("ID Card", readonly=True, size=10),
        "subjects": fields.many2many(
            'odooeduconnect_subject',
            'student_subject_rel',
            'student_id',
            'subject_id',
            string='Subjects',
        ),
        "room_id": fields.many2one('odooeduconnect_room', 'Room', ondelete='set null'),
        "grades_ids": fields.one2many('odooeduconnect_grade', 'student_id', 'Grades', ondelete='cascade'),
    }

    def create(self, cr, uid, vals, context=None):
        if 'prefix' in vals:
            prefix = vals['prefix'].upper()
            existing_ids = self.search(cr, uid, [('student_card', 'ilike', prefix + '%')], context=context)
            max_seq = 0
            for student in self.browse(cr, uid, existing_ids, context=context):
                num_part = str(student.student_card or '')[3:]
                if num_part.isdigit():
                    max_seq = max(max_seq, int(num_part))
            next_seq = max_seq + 1
            vals['student_card'] = prefix + str(next_seq).zfill(4)
            vals['password'] = vals['student_card']

        student_id = super(Student, self).create(cr, uid, vals, context=context)

        user_obj = self.pool.get('res.users')
        group_obj = self.pool.get('res.groups')
        group_ids = group_obj.search(cr, uid, [('name', '=', 'Estudiante')], context=context)

        user_vals = {
            'name': vals['name'],
            'login': vals['email'],
            'password': vals['password'],
            'groups_id': [(6, 0, group_ids)]
        }
        user_obj.create(cr, uid, user_vals, context=context)

        return student_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(Student, self).write(cr, uid, ids, vals, context=context)

        user_obj = self.pool.get('res.users')

        for student in self.browse(cr, uid, ids, context=context):
            user_ids = user_obj.search(cr, uid, [('login', '=', student.email)], context=context)
            if user_ids:
                user_vals = {}
                if 'email' in vals:
                    user_vals['login'] = vals['email']
                    user_vals['password'] = student.student_card
                if user_vals:
                    user_obj.write(cr, uid, user_ids, user_vals, context=context)

        return res
