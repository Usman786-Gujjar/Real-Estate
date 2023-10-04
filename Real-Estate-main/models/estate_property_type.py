from odoo import fields, models

class EstatePropertiesType(models.Model):
    _name = "estate.property.type"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(string='Name', required=True)
