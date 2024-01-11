from odoo import models, fields, api


class SvisContratRenewer(models.Model):
    _name = 'svis.contrat.renewer'

    #flang gauche
    date = fields.Date(string='Renewal Date', required=True)

    #flang  droit
    contract = fields.Many2one('svis.contrat',string = 'Contract')
    customer = fields.Many2one('res.partner', string = 'Custumer', related='contract.customer', readonly=True)
    contrat_t = fields.Char(string = 'Contract Template', related='contract.contrat_t', readonly=True)
    date_start = fields.Date(string = 'Contract Start Date', related='contract.date_start', readonly=True)
    date_end = fields.Date(string = 'Contract End Date', related='contract.date_end', readonly=True)
    date_invoice = fields.Date(string = 'Date of Next Invoice', related='contract.date_invoice', readonly=True)

    #flang gauche 2
    #renewer part
    renewer_star = fields.Date(string='New Start Date', required=True)
    renewer_end = fields.Date(string='New End Date', required=True)
    renewer_invoice = fields.Date(string = 'Contract Invoce Date')
    renewal_reason = fields.Text(string='Renewal Reason')



    ############################################################################
    
    def perform_contract_renewal(self):
        # Vérifiez si le contrat d'origine est expiré
        if self.contract_id.state != 'expired':
            raise exceptions.UserError("Cannot renew the contract. The original contract is not expired.")

        # Mettez ici la logique pour le renouvellement du contrat.
        # Vous pouvez créer un nouveau contrat ou mettre à jour l'ancien contrat.

        # Vous pouvez également ajouter d'autres vérifications et validations ici.

        return True
