# -*- coding: utf-8 -*-
{
    'name': "Real-Estate",

    'summary': """Real-Estate Module Assigment""",

    'sequence': '-300',

    'description': """Real-Estate Module Assigment""",

    'author': "Muhammmad Usman Nazir",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menu.xml',
        'views/estate_property.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        # 'views/res_user.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
