# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class Schedule(osv.osv):
    _name = "odooeduconnect_schedule"
    _description = "Schedule"
    
    _columns = {
        "description": fields.char("Description", required=True, size=128),
        "start_time": fields.datetime("Start Time", required=True),
        "end_time": fields.datetime("End Time", required=True),
        "subject_id": fields.many2one(
            'odooeduconnect_subject',
            'Subject',
            ondelete='cascade',
            required=True
        ),
    }
