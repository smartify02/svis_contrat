from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import math
import logging

class SvisContrat(models.Model):
    _name = 'svis.contrat'



    #up there
    contract_name = fields.Char(string = 'Contract Name', required = 'True')
    invoice_id = fields.Many2one('account.move', string = 'Invoice')
    quotation_id = fields.Many2one('sale.order', string = 'Quotation')

    #signature et vehicle
    vehicles = fields.Many2many('svis.vehicle', string = 'Vehicles')
    services = fields.Many2many('svis.vehicle.log.services', string = 'Services')

    #flant gauche
    customer = fields.Many2one('res.partner', string = 'Custumer')
    pricelist = fields.Integer(string = 'Pricelist')
    payments_terms = fields.Char(string = 'Payements Terms')
    responsable = fields.Many2one('hr.employee', string = 'Responsible')


    #flant droit
    contrat_t = fields.Char(string = 'Contract Template')
    fiscal_p = fields.Char(string = 'Fiscal Position')
    journal = fields.Char(string = 'Journal')

    #deuxieme flant gauche
    invoice_every = fields.Selection([('un','1 Months'),('trois','3 Month')], string = 'Invoice Every')
    invoice_type = fields.Selection([('pre','Pre-paid'),('pais','Paid')], string = 'Invoice Type')

    #deuxieme flant droit
    date_start = fields.Date(string = 'Date Star')
    date_end = fields.Date(string = 'Date End')
    date_invoice = fields.Date(string = 'Date of Next Invoice')


    ## amount and other
    amount = fields.Integer(string = 'Amount')
    renewal_amount = fields.Integer(string = 'Renewal Amount')

    ##signature
    signature = fields.Binary(string='Signature')


    #troisieme flant gauche
    generation = fields.Char(string = 'Generation Type')

    #relation 
    contract = fields.One2many('svis.contrat.follow','contrat_follow', string = 'contract Follow')
    renewal_invoice_id = fields.Many2one('svis.contrat.follow', string='Renewal Invoice', copy=False, readonly=True)
    state = fields.Selection(
        [('futur', 'Incoming'),
         ('open', 'In Progress'),
         ('expired', 'Expired'),
         ('closed', 'Closed')
        ], 'Status', default='open', readonly=True,
        help='Choose whether the contract is still valid or not',
        tracking=True, copy=False)

    notes = fields.Html('Terms and Conditions', help='Write here all supplementary information relative to this contract', copy=False)
    cost_generated = fields.Integer('Recurring Cost', tracking=True)
    cost_frequency = fields.Selection([
        ('no', 'No'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
        ], 'Recurring Cost Frequency', default='monthly', required=True)   

    #count
    renewer_count = fields.Integer(compute="_compute_count_renewer", string='renewer')
     


    ###############################################################################

    def generate(self):
        # Définissez vos critères pour sélectionner les contrats éligibles au renouvellement.
        eligible_contracts = self.search([
            ('date_end', '<=', fields.Date.today()),  # Contrats dont la date de fin est passée.
            # Ajoutez d'autres critères de sélection si nécessaire.
        ])

        for contrat in eligible_contracts:
            # Vérifiez si une facture de renouvellement existe déjà pour ce contrat.
            if contrat.renewal_invoice_id:
                # Une facture de renouvellement existe déjà pour ce contrat, passez au suivant.
                continue

            # Créez une facture de renouvellement en utilisant le modèle de facture de renouvellement.
            renewal_invoice = self.env['svis.contrat.follow'].create({
                'name': 'Numéro de Facture de Renouvellement',  # Personnalisez cela en fonction de votre modèle de facture.
                # Ajoutez d'autres champs de facture de renouvellement ici.
            })

            # Liez la facture de renouvellement au contrat en utilisant le champ renewal_invoice_id.
            contrat.renewal_invoice_id = renewal_invoice.id

            
    def generate_pdf(self):
        return

    def schedule_renewal_invoice_generation(self):
        # Appelez la méthode de génération de factures de renouvellement.
        self.generate()


    def open_renewer(self):
        renewer = self.env['svis.contrat.renewer'].search([('contract', '=', self.id)])
        action = self.env.ref('svis_contrat.action_svis_contrat_renewer')  # Remplacez 'your_module_name' par le nom de votre module.
        
        if renewer:
            action = action.read()[0]
            action['domain'] = [('id', 'in', renewer.ids)]
            return action
        else:
            # Gérez le cas où il n'y a pas de renouvellement à afficher.
            # Vous pouvez afficher un avertissement ou effectuer d'autres actions ici.
            return {'type': 'ir.actions.act_window_close'}


    @api.depends('contract')
    def _compute_count_renewer(self):
        for contrat in self:
            contrat.renewer_count = self.env['svis.contrat.renewer'].search_count([('contract', '=', contrat.id)])
    

    @api.depends('date_start', 'date_end')
    def _compute_contract_state(self):
        today = fields.Date.today()
        for contrat in self:
            if contrat.date_end and contrat.date_end < today:
                contrat.state = 'expired'
            elif contrat.date_start and contrat.date_start <= today <= contrat.date_end:
                contrat.state = 'in_progress'
            else:
                contrat.state = 'incoming'