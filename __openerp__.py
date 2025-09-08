{
    'name': 'OdooEduConnect',
    'version': '1.0.1',
    'category': 'Tools',
    'summary': 'Módulo de gestión educativa',
    'author': 'Javier Herrera',
    'website': 'https://github.com/JH1018/Modulo_Odoo8',
    'depends': ['base'],
    'data': [
        'views/students/searchView.xml',
        'views/students/tree_student.xml',
        'views/students/registerView.xml',
        'views/grades/tree_grades.xml',
        'views/grades/registerGradesView.xml',
        'views/subject/tree_subject.xml',
        'views/subject/registerSubjectView.xml',
        'views/room/tree_room.xml',
        'views/room/registerRoomView.xml',
        'views/menu.xml'
    ],
    'installable': True,
    'auto_install': False,
}
