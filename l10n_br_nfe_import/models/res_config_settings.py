from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Sequência para código de produto",
        config_parameter="l10n_br_nfe_import.product_sequence",
    )
