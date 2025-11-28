from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-super-segura-cambiar-en-produccion'


RDS_USERNAME = 'admin'  
RDS_PASSWORD = 'cristhian3738'  
RDS_ENDPOINT = 'contactos.cjuwydxejd04.us-east-1.rds.amazonaws.com' 
RDS_PORT = '3306'  # Puerto de MySQL (por defecto 3306)
RDS_DB_NAME = 'leads_db'  # Nombre de tu base de datos

# Usa RDS si está configurado, sino usa SQLite local
if RDS_ENDPOINT != 'tu-rds-endpoint.region.rds.amazonaws.com':
    # Primero intentamos crear la base de datos si no existe
    import pymysql
    try:
        print(f"📊 Conectando a AWS RDS: {RDS_ENDPOINT}")
        print(f"👤 Usuario: {RDS_USERNAME}")
        print(f"🌐 Tu IP detectada intentando conectar...")
        
        # Conectar sin especificar base de datos para crearla
        connection = pymysql.connect(
            host=RDS_ENDPOINT,
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            port=int(RDS_PORT)
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {RDS_DB_NAME}")
        cursor.execute(f"USE {RDS_DB_NAME}")
        print(f"✅ Base de datos '{RDS_DB_NAME}' lista")
        cursor.close()
        connection.close()
    except pymysql.err.OperationalError as e:
        if '1045' in str(e):
            print("\n❌ ERROR DE AUTENTICACIÓN:")
            print("   1. Verifica que la contraseña sea correcta")
            print("   2. Configura el Security Group en AWS:")
            print("      → AWS Console → RDS → contactos → Security")
            print("      → Click en el Security Group")
            print("      → Edit inbound rules → Add rule")
            print("      → Type: MYSQL/Aurora, Source: My IP")
            ip_info = str(e).split('@')[1].split("'")[0] if '@' in str(e) else 'desconocida'
            print(f"      → Tu IP actual: {ip_info}")
            print("\n")
            raise
    except Exception as e:
        print(f"⚠️ Error conectando a RDS: {e}")
        raise
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DB_NAME}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
    print("📊 Usando SQLite local para desarrollo")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================
# MODELO DE BASE DE DATOS
# ============================================

class Lead(db.Model):
    """Modelo para almacenar información de leads"""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    interes_servicio = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lead {self.nombre_completo}>'


# ============================================
# RUTAS
# ============================================

@app.route('/')
def index():
    """Página principal con formulario de registro"""
    return render_template('index.html')


@app.route('/registro', methods=['POST'])
def registro():
    """Procesar registro de nuevo lead"""
    try:
        nombre = request.form.get('nombre_completo')
        correo = request.form.get('correo_electronico')
        telefono = request.form.get('telefono')
        interes = request.form.get('interes_servicio')
        
        # Validar que todos los campos estén presentes
        if not all([nombre, correo, telefono, interes]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('index'))
        
        # Verificar si el correo ya existe
        lead_existente = Lead.query.filter_by(correo_electronico=correo).first()
        if lead_existente:
            flash('Este correo electrónico ya está registrado', 'error')
            return redirect(url_for('index'))
        
        # Crear nuevo lead
        nuevo_lead = Lead(
            nombre_completo=nombre,
            correo_electronico=correo,
            telefono=telefono,
            interes_servicio=interes
        )
        
        db.session.add(nuevo_lead)
        db.session.commit()
        
        flash('¡Lead registrado exitosamente!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar el lead: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/leads')
def listar_leads():
    """Listar todos los leads"""
    leads = Lead.query.order_by(Lead.fecha_registro.desc()).all()
    return render_template('leads.html', leads=leads)


@app.route('/lead/<int:id>')
def detalle_lead(id):
    """Ver detalles de un lead específico"""
    lead = Lead.query.get_or_404(id)
    return render_template('detalle_lead.html', lead=lead)


@app.route('/lead/<int:id>/editar', methods=['GET', 'POST'])
def editar_lead(id):
    """Editar información de un lead"""
    lead = Lead.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            lead.nombre_completo = request.form.get('nombre_completo')
            lead.correo_electronico = request.form.get('correo_electronico')
            lead.telefono = request.form.get('telefono')
            lead.interes_servicio = request.form.get('interes_servicio')
            
            db.session.commit()
            flash('¡Lead actualizado exitosamente!', 'success')
            return redirect(url_for('detalle_lead', id=lead.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el lead: {str(e)}', 'error')
    
    return render_template('editar_lead.html', lead=lead)


@app.route('/lead/<int:id>/eliminar', methods=['POST'])
def eliminar_lead(id):
    """Eliminar un lead"""
    try:
        lead = Lead.query.get_or_404(id)
        db.session.delete(lead)
        db.session.commit()
        flash('Lead eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el lead: {str(e)}', 'error')
    
    return redirect(url_for('listar_leads'))


# ============================================
# INICIALIZACIÓN
# ============================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
        print("🚀 Servidor iniciado en http://0.0.0.0:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

