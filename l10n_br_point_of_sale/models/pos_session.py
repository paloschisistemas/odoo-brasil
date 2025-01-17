# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import RedirectWarning


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            config_id = vals.get("config_id") or self.env.context.get("default_config_id")
            pos_config = self.env["pos.config"].browse(config_id)

            msg = "Configurar posições fiscais"
            if not pos_config.default_fiscal_position_id:
                raise RedirectWarning(
                    "Configure uma posição fiscal padrão para o POS",
                    self.env.ref("point_of_sale.action_pos_configuration").id,
                    msg,
                )

            if not pos_config.company_id.l10n_br_nfe_sequence:
                raise RedirectWarning(
                    "Configure uma sequência de nota de produto para esta empresa",
                    self.env.ref("account.action_account_config").id,
                    "Configurar Sequência",
                )
        return super(PosSession, self).create(vals_list)
