from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The tag name must be unique.'),
    ]

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            domain = [('name', '=', record.name)]
            if record.id:
                domain.append(('id', '!=', record.id))
            if self.search_count(domain):
                raise ValidationError("The tag name must be unique.")