from openerp.osv import osv, fields

class Subject(osv.osv):
    _name = "odooEduConnect.subject"
    _description = "Subject"

    _columns = {
        "name": fields.char("Name", required=True, size=64),
        "code": fields.char("Code", required=True, size=10),
        "description": fields.text("Description"),
        "credits": fields.integer("Credits", required=True),
        "room_id": fields.many2one('odooEduConnect.room', 'Room', required=True),
        "students": fields.many2many('odooEduConnect.student', string='Students'),
    }
