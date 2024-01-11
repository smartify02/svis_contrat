from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import math
import logging

class SvisContratTemplate(models.Model):
    _name = 'svis.contrat.template'

    name = fields.Char(string = 'Name')
    cag = fields.Char(string = 'categories')