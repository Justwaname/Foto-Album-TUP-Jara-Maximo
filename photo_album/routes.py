from flask import Blueprint, render_template, redirect, url_for, request, flash
from app_init import db
from models import Foto
from forms import FotoForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    fotos = Foto.query.all()
    return render_template('index.html', photos=fotos)

@main.route('/agregar', methods=['GET', 'POST'])
def agregar_foto():
    form = FotoForm()
    if form.validate_on_submit():
        
        if form.image_url.data:  
            ruta_imagen = form.image_url.data  
        else:
            flash('Por favor, proporciona una URL de la imagen.', 'danger')
            return redirect(url_for('main.agregar_foto'))

        
        nueva_foto = Foto(
            title=form.title.data,
            description=form.description.data,
            image=ruta_imagen  
        )
        db.session.add(nueva_foto)
        db.session.commit()
        
        return redirect(url_for('main.index'))  
    
    return render_template('photo_form.html', form=form)  

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_foto(id):
    foto = Foto.query.get_or_404(id)
    form = FotoForm(obj=foto)

    
    if not form.image_url.data:
        form.image_url.data = foto.image  

    if form.validate_on_submit():
        
        foto.title = form.title.data
        foto.description = form.description.data

        if form.image_url.data and form.image_url.data != foto.image:
            foto.image = form.image_url.data

        db.session.commit()
       
        return redirect(url_for('main.index'))

    return render_template('photo_form.html', form=form, foto=foto)

@main.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_foto(id):
    foto = Foto.query.get_or_404(id)
    db.session.delete(foto)
    db.session.commit()
   
    return redirect(url_for('main.index'))
