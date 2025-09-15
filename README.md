# 🎓 OdooEduConnect

**Sistema Integral de Gestión Educativa para Odoo 8**

Un módulo completo y profesional diseñado para revolucionar la administración educativa, ofreciendo una solución centralizada, intuitiva y robusta para instituciones educativas de cualquier tamaño.

---

## 📋 Características Principales

### 🎯 **Gestión Completa de Entidades Educativas**
- **👥 Estudiantes**: Registro completo con prefijos, carnets automáticos y gestión de credenciales
- **👨‍🏫 Profesores**: Administración integral de docentes con asignación de materias
- **🏫 Salones**: Control de capacidad y asignación inteligente de espacios
- **📚 Materias**: Gestión de cursos con códigos únicos y descripciones detalladas

### 📊 **Sistema de Evaluación Avanzado**
- **📝 Exámenes**: Creación de evaluaciones con preguntas de opción múltiple
- **🎯 Calificaciones**: Sistema automatizado con cálculo de porcentajes y estadísticas
- **📈 Reportes**: Exportación de datos en PDF con gráficos y análisis detallados
- **🔄 Duplicación**: Wizards para reutilizar exámenes existentes

### 🛡️ **Seguridad y Control de Acceso**
- **👤 Roles Diferenciados**: Administrador, Profesor, Estudiante
- **🔐 Credenciales Automáticas**: Generación segura de usuarios y contraseñas
- **📱 Interfaz Adaptable**: Optimizada para diferentes tipos de usuario

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| **Framework** | Odoo | 8+ |
| **Base de Datos** | PostgreSQL | 9.4+ |
| **Lenguaje Backend** | Python | 2.7 |
| **Lenguaje Frontend** | XML/JavaScript | - |
| **Reportes PDF** | ReportLab | 3.0+ |
| **Arquitectura** | MVC Pattern | - |

---

## 🚀 Instalación y Configuración

### 📋 **Prerrequisitos**
- Instancia de Odoo 8 funcionando
- PostgreSQL configurado
- Permisos de administrador en Odoo

### 🔧 **Proceso de Instalación**

#### **Paso 1: Clonar el Repositorio**
```bash
# Navegar al directorio de addons de tu instancia Odoo
cd /path/to/odoo/addons

# Clonar el repositorio
git clone https://github.com/JH1018/Modulo_Odoo8.git -b 2.0
```

#### **Paso 2: Activar el Módulo**
1. **Acceder a Odoo**: Inicia sesión como administrador
2. **Navegación**: `Configuración > Módulos Locales`
3. **Actualizar Lista**: Haz clic en "Actualizar Lista de Módulos"
4. **Buscar**: Escribe "OdooEduConnect" en la barra de búsqueda
5. **Instalar**: Haz clic en "Instalar"

#### **Paso 3: Configuración Inicial**
1. **Acceso**: Ve al menú "Administración" en el navbar principal
2. **Demo Data**: El módulo incluye datos de prueba listos para usar
3. **Permisos**: Configura los grupos de usuarios según tu estructura organizacional

---

## 📚 Guía de Usuario

### 👥 **Gestión de Estudiantes**

#### **Crear Nuevo Estudiante**
1. **Navegación**: `Administración > Gestión de Estudiantes`
2. **Formulario**: Completa la información personal
3. **Prefijo**: Ingresa 3 letras (se convertirán automáticamente a mayúsculas)
4. **Carnet**: Se genera automáticamente con secuencia única

> [!NOTE]
> **Credenciales Automáticas**: El email será el usuario y se generará una contraseña automática que se mostrará al guardar.

#### **Campos Requeridos**
- ✅ Nombre completo
- ✅ Email (será el usuario de acceso)
- ✅ Prefijo (3 caracteres)
- ⚪ Teléfono (opcional)
- ⚪ Información académica (se puede llenar después)

### 👨‍🏫 **Gestión de Profesores**

#### **Registrar Nuevo Profesor**
1. **Navegación**: `Administración > Gestión de Profesores`
2. **Información Personal**: Completa todos los datos del docente
3. **Credenciales**: El email será tanto usuario como contraseña inicial

> [!IMPORTANT]
> **Seguridad**: Recuerda que el profesor debe cambiar su contraseña en el primer acceso.

#### **Asignación de Materias**
- Las materias se pueden asignar durante la creación o posteriormente
- Un profesor puede impartir múltiples materias
- Las asignaciones se reflejan automáticamente en los reportes

### 🏫 **Configuración de Salones**

#### **Crear Salón con Control de Capacidad**
1. **Información Básica**:
   - Nombre del salón
   - Capacidad máxima
   - Descripción (opcional)

2. **Asignación de Estudiantes**:
   - Después de crear el salón, editarlo
   - Agregar estudiantes respetando la capacidad máxima
   - El sistema previene sobrecupo automáticamente

> [!WARNING]
> **Control de Capacidad**: Siempre respeta la capacidad máxima para evitar conflictos en el sistema.

### 📚 **Gestión de Materias**

#### **Configurar Nueva Materia**
1. **Datos Básicos**:
   - Nombre de la materia
   - Código único
   - Descripción detallada

2. **Asignaciones**:
   - Profesor responsable
   - Salón donde se imparte
   - Estudiantes inscritos


### 📚 **Gestión de Exámenes**

#### **Configurar Nuevo Examen**
1. **Datos Básicos**:
   - Nombre del Examen
   - Fecha del examen

2. **Asignaciones**:
   - Asignaturas

3. **Preguntas**:
   - Para agregar preguntas dar click en el menú central, luego rellenar los campos
   - Rellenar Pregunta, respuesta correcta (Se calificará el texto asi que tiene que estar bien escrito) y preguntas
   - Para resolver el examen el alumno debe darle en iniciar el examen realizara una copia del examen base
   - El alumno deberá buscar el examen para resolver en la lista con estos parametros "nombre del examen - nombre alumno"
   - Para responder el alumno debera de editar el examen y dar click en cada pregunta, y marcar en el checkbox de la respuesta correcta

---

## 📊 **Sistema de Evaluaciones**

### 📝 **Crear Exámenes**
- **Preguntas de Opción Múltiple**: Hasta 4 opciones por pregunta
- **Respuestas Correctas**: Marcación clara de la opción correcta
- **Fechas de Aplicación**: Programación automática

### 🎯 **Calificación Automática**
- **Cálculo Automático**: Porcentajes basados en respuestas correctas
- **Reportes Detallados**: Análisis completo de rendimiento

### 📈 **Exportación de Reportes**
- **Formato PDF**: Reportes profesionales con gráficos
- **Múltiples Vistas**: Por estudiante, profesor, materia o salón

--

## 📄 **Licencia y Derechos**

**Licencia**: MIT License
**Autor**: JH1018
**Versión**: 2.0
**Última Actualización**: Septiembre 2025
