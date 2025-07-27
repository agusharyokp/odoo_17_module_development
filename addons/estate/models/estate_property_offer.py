from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string="Validity (days)") 
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)',
         'The offer price must be strictly positive'),
    ]

    @api.constrains('price')
    def check_offer_price_positive(self):
        if self.price <= 0:
            raise ValidationError("The offer price must be strictly positive.")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days= record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days= record.validity)
    
    def _inverse_date_deadline(self):
         for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id == "sold":
                raise UserError("Cannot accept offer for a sold property.")
            
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            return True
    
    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Cannot refuse offer for affter acceted")
            
            record.status = 'refused'
            return True
