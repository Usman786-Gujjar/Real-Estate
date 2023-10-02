from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Realestate Property Tags"
    _order = "name asc"

    name = fields.Char('Property Tags', required=True)
    color = fields.Integer('Tag Color')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('unique_tags', 'unique(name)', "Tag already exists.")
    ]
