from flask_restplus import Namespace, Resource
from flask import abort, current_app

from gsrest.apis.common import label_response, tag_response, currency_parser, \
    category_response
import gsrest.service.general_service as generalDAO
import gsrest.service.labels_service as labelsDAO
from gsrest.util.checks import check_inputs
from gsrest.util.decorator import token_required

api = Namespace('labels',
                path='/labels',
                description='Operations related to labels')

# TODO: add /labels/ to get al list of all labels


@api.param('label', 'The label of an entity (e.g., Internet Archive)')
@api.route("/<label>")
class Label(Resource):
    @token_required
    @api.marshal_with(label_response)
    def get(self, label):
        """
        Returns details (address count) for a specific label
        """
        check_inputs(label=label)
        result = None
        address_count = 0
        currency_result = dict()
        for currency in current_app.config['MAPPING']:
            if currency != "tagpacks":
                currency_result[currency] = labelsDAO.get_label(label,
                                                                currency)
                if currency_result[currency] and \
                        'address_count' in currency_result[currency]:
                    result = currency_result[currency]
                    address_count += result['address_count']
        if address_count:
            result['address_count'] = address_count
            return result
        abort(404, "Label not found")


@api.param('label', 'The label of an entity (e.g., Internet Archive)')
@api.route("/<label>/tags")
class LabelTags(Resource):
    @token_required
    @api.doc(parser=currency_parser)
    @api.marshal_list_with(tag_response)
    def get(self, label):
        """
        Returns the tags associated with a given label
        """
        currency = currency_parser.parse_args()['currency']
        check_inputs(label=label, currency_optional=currency)
        if currency:
            result = labelsDAO.list_tags(label, currency)
        else:
            result = []
            for currency in current_app.config['MAPPING']:
                if currency != "tagpacks":
                    tags = labelsDAO.list_tags(label, currency)
                    if tags:
                        result += tags
        if result:
            return result
        abort(404, "Label not found")


@api.route("/categories")
class Categories(Resource):
    @token_required
    @api.marshal_list_with(category_response)
    def get(self):
        """
        Returns the supported entity categories
        """
        return generalDAO.list_categories()

# TODO: add call: from category to list of labels and #addresses
