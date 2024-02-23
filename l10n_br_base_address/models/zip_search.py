import re
import logging
import requests

from odoo import models

_logger = logging.getLogger(__name__)


class ZipSearchMixin(models.AbstractModel):
    _name = "zip.search.mixin"
    _description = "Pesquisa de CEP"

    def search_address_by_zip(self, zip_code):
        zip_code = re.sub("[^0-9]", "", zip_code or "")
        res = requests.request("GET", f"http://viacep.com.br/ws/{zip_code}/json/")
        if res.ok and not res.json().get('erro'):
            vals = res.json()
            state = (
                self.env["res.country.state"]
                .search(
                    [
                        ("country_id.code", "=", "BR"),
                        ("code", "=", vals["uf"]),
                    ]
                )
            )

            city = (
                self.env["res.city"]
                .search(
                    [
                        ("name", "=ilike", vals["localidade"]),
                        ("state_id", "=", state.id),
                    ]
                )
            )

            if vals["logradouro"] is None:
                vals["logradouro"] = ""
            if vals["bairro"] is None:
                vals["bairro"] = ""
            return {
                "zip": zip_code,
                "street": vals["logradouro"],
                "l10n_br_district": vals["bairro"],
                "country_id": state.country_id.id,
                "state_id": state.id,
                "city_id": city.id,
            }
        return {}
