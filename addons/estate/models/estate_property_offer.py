from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

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
    property_state = fields.Selection(related="property_id.state", readonly=True)

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

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
            property = record.property_id

            if record.property_id == "sold":
                raise UserError("Cannot accept offer for a sold property.")
            
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

            if property.state == 'new' or property.state == 'offer_received':
                property.state = 'offer_accepted'

            return True
    
    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Cannot refuse offer for affter acceted")
            
            record.status = 'refused'
            return True
        
    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        new_price = vals.get("price")

        if not property_id or not new_price:
            raise UserError("Property ID and price are required.")
        
        # Ambil harga tertinggi dari offer yang sudah ada untuk property ini
        highest_offer = self.search([
            ('property_id', '=', property_id)
        ], order='price desc', limit=1)

        if highest_offer and new_price <= highest_offer.price:
            raise UserError(f"Offer must be higher than {highest_offer.price}")


        # existing_offers =  self.search([('property_id', '=', vals["property_id"])])
        
        # for offer in existing_offers:
        #     if vals["price"] <= offer.price:
        #         raise UserError("Offer must be higer than existin offers")
            
        property =  self.env['estate.property'].browse(vals['property_id'])
        if property.state == "new":
            property.state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals)


        # offer = super().create(vals)
        # property = offer.property_id
        # if property.state == 'new':
        #     property.state = 'offer_received'

        # return offer
