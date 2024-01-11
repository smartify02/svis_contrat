from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import math
import logging

class SvisContratFollow(models.Model):
    _name = 'svis.contrat.follow'


    #flant gauche
    name = fields.Char(string='Invoice Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('svis.contrat.follow'))
    product = fields.Char(string = 'Product')
    description = fields.Char(string = 'Descriptions')
    analytic = fields.Char(string = 'Analyttic Terms')
    responsable = fields.Many2one('hr.employee', string = 'Responsible')


    #flant droit
    quantity = fields.Integer(string = 'Quantity')
    unit_of = fields.Char(string = 'Unit of Measurement')
    auto_price = fields.Char(string = 'Auto-Price')

    #deuxieme flant gauche
    unit_price = fields.Integer(string = 'Unit Price')
    sub_total = fields.Integer(string = 'Sub Total')
    end_date = fields.Date(string = 'End Date')

    #relation
    contrat_follow = fields.Many2one('svis.contrat', string = 'Contrat')

    ###############################################################

   