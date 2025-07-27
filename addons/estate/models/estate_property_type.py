from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The type name must be unique.'),
    ]

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            domain = [('name', '=', record.name)]
            if record.id:
                domain.append(('id', '!=', record.id))
            if self.search_count(domain):
                raise ValidationError("The type name must be unique.")