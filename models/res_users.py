from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', inverse_name='salesperson',
                                   domain=lambda self: [('state', 'in', ('new', 'offer_received'))])
