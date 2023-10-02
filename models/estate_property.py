from dateutil import relativedelta

from odoo import fields, models , api
from datetime import datetime, date
from datetime import timedelta
from odoo.exceptions import UserError




class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(string='Name', required=True)
    property_type = fields.Many2one('estate.property.type', string="Property Type")
    property_tag = fields.Many2one('estate.property.tag', string="Tag")
    description = fields.Text(string='Description')
    post_code = fields.Char(string='Post Code')
    date_availability = fields.Date(string='Available Form')
    expected_price = fields.Float(string='Expected Price',required=True)
    best_offer = fields.Float(string='Best Offer',compute="_compute_best_offer")
    selling_price = fields.Float(string='Selling Price')
    bedroom = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garden = fields.Boolean(string='Garden')
    garage = fields.Boolean(string='Garage')
    garden_area = fields.Integer(string='Garden Area(sqm)')
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')], string='Garden Orientation')
    status = fields.Selection([('new', 'New'), ('cancel', 'Cancel')], string='Status', default='new')
    sale_man = fields.Many2one('res.users', string='Salesman')
    buyer = fields.Many2one('res.partner', string='Buyer')
    house_offer = fields.One2many('house.offer', 'estate_property', string='Offer lIne')
    total = fields.Float(string='Total', compute="_compute_total")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >=0)', 'The expected price must a positive number.'),
        ('check_selling_price', 'CHECK(selling_price >=0 OR selling_price=null)',
         'The selling price must a positive number.'),
    ]


    @api.depends("house_offer")
    def _compute_best_offer(self):
        for record in self:
            try:
                record.best_offer = max(record.house_offer.mapped("price"))
            except ValueError:
                record.best_offer = 0


    @api.onchange('garden_area','living_area')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.living_area + rec.garden_area

    def action_done(self):
        for rec in self:
            if rec.status == 'cancel':
                raise UserError("Cancelled Properties Cannot be sold")

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancel'


class Offer(models.Model):
    _name = 'house.offer'
    _description = "Create a line in house offers"

    price = fields.Float(string="Price")
    partner = fields.Many2one('res.partner', string="Partner")
    status12 = fields.Selection([('accept', 'Accept'), ('refused', 'Refused')], string='Status')
    validity = fields.Integer(string="Validity(days)",defuslt=7)
    deadline = fields.Date(string="Deadline",default=datetime.today() , inverse="_inverse_deadline")
    estate_property = fields.Many2one('estate.property', string='Estate Property')


    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must a positive number.'),
    ]

    @api.onchange('validity')
    def change_date(self):
        for rec in self:
            if rec.validity:
                if rec.deadline:
                    rec.deadline = rec.deadline + timedelta(days=rec.validity)
                else:
                    print("Heloo")

            else:
                rec.validity = 7

    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                record.validity = (record.deadline - record.create_date.date()).days



    def refused_action(self):
        for rec in self:
            rec.status12 = 'refused'

    def accept_action(self):
        for rec in self:
            rec.status12 = 'accept'
            rec.estate_property.selling_price = rec.estate_property.best_offer
            rec.estate_property.buyer = rec.partner
