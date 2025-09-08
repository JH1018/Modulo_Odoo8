from openerp.osv import osv, fields

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
            'Students',
            ondelete='set null'                  
        ),
        "subject_id": fields.one2many(
            'odooeduconnect_subject',  
            'room_id',                  
            'Subjects',
        ),
        
    }
