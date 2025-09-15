# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class Teacher(osv.osv):
    _name = "odooeduconnect_teacher"
    _description = "Teacher"
    
    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "profile_picture": fields.binary("Profile Picture"),
        "age": fields.integer("Age", required=True),
        "address": fields.char("Address", size=256),
        "email": fields.char("Email", required=True, size=128),
        "password": fields.char("Password", required=True, size=64),
        "phone": fields.char("Phone", required=True, size=8),
        "subject_ids": fields.one2many('odooeduconnect_subject', 'teacher_id', 'Subjects'),
    }

    def create(self, cr, uid, vals, context=None):
        if 'email' in vals and not vals.get('password'):
            vals['password'] = vals['email']

        teacher_id = super(Teacher, self).create(cr, uid, vals, context=context)

        user_obj = self.pool.get('res.users')
        group_obj = self.pool.get('res.groups')
        group_ids = group_obj.search(cr, uid, [('name', '=', 'Profesor')], context=context)

        user_vals = {
            'name': vals['name'],
            'login': vals['email'],
            'password': vals['password'],
            'groups_id': [(6, 0, group_ids)]
        }
        user_obj.create(cr, uid, user_vals, context=context)

        return teacher_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(Teacher, self).write(cr, uid, ids, vals, context=context)

        user_obj = self.pool.get('res.users')

        for teacher in self.browse(cr, uid, ids, context=context):
            user_ids = user_obj.search(cr, uid, [('login', '=', teacher.email)], context=context)
            if user_ids:
                user_vals = {}
                if 'email' in vals:
                    user_vals['login'] = vals['email']
                    user_vals['password'] = vals['email']
                if user_vals:
                    user_obj.write(cr, uid, user_ids, user_vals, context=context)

        return res
