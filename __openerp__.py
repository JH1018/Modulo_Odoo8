# -*- coding: utf-8 -*-
{
    'name': 'OdooEduConnect - Sistema de Gestión Educativa',
    'version': '1.0.1',
    'category': 'Education',
    'summary': 'Sistema integral de gestión educativa con exámenes, calificaciones y reportes',
    'description': """
Sistema Completo de Gestión Educativa
=====================================

Características Principales:
----------------------------
    * Gestión completa de estudiantes, maestros y materias
    * Sistema de exámenes con preguntas de opción múltiple  
    * Calificaciones automatizadas con estadísticas detalladas
    * Gestión de salones con control de capacidad
    * Exportación de reportes en PDF con ReportLab
    * Wizards de duplicación y calificación de exámenes
    * Seguridad por roles (Profesor, Estudiante, Administrador)

Módulos Incluidos:
------------------
    * Registro y gestión de estudiantes con prefijos y secciones
    * Administración de maestros con asignación de materias
    * Control de salones y capacidades
    * Sistema de exámenes interactivos
    * Calificaciones con cálculo automático de porcentajes
    * Reportes PDF exportables para todos los módulos

Funcionalidades Avanzadas:
--------------------------
    * Wizards para duplicar exámenes existentes
    * Calificación automática basada en respuestas correctas
    * Exportación masiva de datos en formato PDF
    * Demo data incluida para pruebas inmediatas
    * Interfaz intuitiva optimizada para Odoo 8

Desarrollado por:
----------------
    Javier Herrera

Soporte Técnico:
---------------
    https://github.com/JH1018/Modulo_Odoo8

Requisitos del Sistema:
----------------------
    * Odoo 8.0 o superior
    * ReportLab para generación de PDFs
    * Python 2.7 o superior
    """,
    'author': 'Javier Herrera',
    'maintainer': 'Javier Herrera',
    'website': 'https://github.com/JH1018/Modulo_Odoo8',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [ 'security/security.xml',
            'security/student_rules.xml', 
            'security/ir.model.access.csv',
            
            'views/students/studentGraph.xml',
            'views/exam/searchExam.xml', 
            'views/exam/registerExamView.xml', 
            'wizard/start_exam_wizard.xml', 
            'wizard/grade_exam_wizard.xml', 
            'views/exam/tree_exam.xml', 
            'views/teacher/searchRegisterView.xml', 
            'views/teacher/tree_teacher.xml', 
            'views/teacher/registerTeacherView.xml', 
            'views/students/searchView.xml', 
            'views/students/tree_student.xml', 
            'views/students/registerView.xml', 
            'views/grades/searchGradesView.xml', 
            'views/grades/tree_grades.xml', 
            'views/grades/registerGradesView.xml', 
            'views/subject/searchRegisterView.xml', 
            'views/subject/tree_subject.xml', 
            'views/subject/registerSubjectView.xml', 
            'views/room/searchRoomView.xml', 
            'views/room/tree_room.xml', 
            'views/room/registerRoomView.xml', 
            'views/menu.xml', 
            'views/exam/registerExamView.xml', 
            'wizard/student_export_wizard_view.xml', 
            'wizard/teacher_export_wizard_view.xml', 
            'wizard/subject_export_wizard_view.xml', 
            'wizard/grade_export_wizard_view.xml', 
            'wizard/room_export_wizard_view.xml', 
            'wizard/start_exam_wizard.xml', 
            
        ],
    'demo': [
        'data/demo_teachers.xml',
        'data/demo_students.xml',
        'data/demo_rooms.xml',
        'data/demo_subjects.xml',
        'data/demo_grades.xml',
        'data/demo_exams.xml',
        'data/demo_questions.xml',
        'data/demo_answers.xml',
        'data/demo_relations.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
    'images': ['static/description/icon.png'],
    'external_dependencies': {
        'python': ['reportlab'],
    },
    'price': 0.00,
    'currency': 'USD',
    'support': 'https://github.com/JH1018/Modulo_Odoo8/issues',
}
