{
    'name': 'OdooEduConnect',
    'version': '1.0.1',
    'category': 'Tools',
    'summary': 'Módulo de gestión educativa',
    'description': 'Módulo que proporciona herramientas para la gestión de una institución educativa para Odoo',
    'author': 'Javier Herrera',
    'website': 'https://github.com/JH1018/Modulo_Odoo8',
    'depends': ['base'],
    'data': [
        'views/room/tree_room.xml',
        'views/room/registerRoomView.xml',
        'views/students/tree_student.xml',
        'views/students/registerView.xml',
        'views/menu.xml'
    ],
    'installable': True,
    'auto_install': False,
}