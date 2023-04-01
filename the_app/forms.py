from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError


class ProductForm(FlaskForm):
    id = HiddenField("id")
    tipo_producto = StringField("Tipo de producto", validators=[DataRequired(), Length(min=3, message="Debe tener al menos 3 caracteres")])
    precio_unitario = FloatField("Precio unitario", validators=[DataRequired()])
    coste_unitario = FloatField("Coste unitario", validators=[DataRequired()])

    submit = SubmitField("Aceptar")

    def validate_coste_unitario(self, field):
        if field.data > self.precio_unitario.data:
            raise ValidationError("El coste unitario ha de ser menor o igual que el precio unitario")