import os
import sys
import textwrap

MODULE_TEMPLATE = {
    "__init__.py": "# -*- coding: utf-8 -*-\n\nfrom . import models\nfrom . import controllers\n",

    "__manifest__.py": textwrap.dedent('''# -*- coding: utf-8 -*-                                       
{{
    'name': "{module_name}",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': \"\"\"
Long description of module's purpose
    \"\"\",

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}}
                                       
    '''),

    "controllers/__init__.py": "# -*- coding: utf-8 -*-\n\nfrom . import controllers\n",

    "controllers/controllers.py": '''# -*- coding: utf-8 -*-
# from odoo import http


# class {camel_name}(http.Controller):
#     @http.route('/{module_name}/{module_name}', auth='public')
#     def index(self, **kw):
#         return "Hello, world!"

#     @http.route('/{module_name}/{module_name}/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('{module_name}.listing', {{
#             'root': '/{module_name}/{module_name}',
#             'objects': http.request.env['{module_name}.{module_name}'].search([]),
#         }})

#     @http.route('/{module_name}/{module_name}/objects/<model("{module_name}.{module_name}"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('{module_name}.object', {{
#             'object': obj
#         }})
 
    ''',

    "demo/demo.xml": '''<odoo>
    <data>
<!--
          <record id="object0" model="{module_name}.{module_name}">
            <field name="name">Object 0</field>
            <field name="value">0</field>
          </record>

          <record id="object1" model="{module_name}.{module_name}">
            <field name="name">Object 1</field>
            <field name="value">10</field>
          </record>

          <record id="object2" model="{module_name}.{module_name}">
            <field name="name">Object 2</field>
            <field name="value">20</field>
          </record>

          <record id="object3" model="{module_name}.{module_name}">
            <field name="name">Object 3</field>
            <field name="value">30</field>
          </record>

          <record id="object4" model="{module_name}.{module_name}">
            <field name="name">Object 4</field>
            <field name="value">40</field>
          </record>
-->
    </data>
</odoo>
    ''',

    "models/__init__.py": "# -*- coding: utf-8 -*-\n\nfrom . import models\n",

    "models/models.py": '''# -*- coding: utf-8 -*-
    
# from odoo import models, fields, api


# class {module_name}(models.Model):
#     _name = '{module_name}.{module_name}'
#     _description = '{module_name}.{module_name}'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    ''',

    "security/ir.model.access.csv": '''id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_{module_name}_{module_name},{module_name}.{module_name},model_{module_name}_{module_name},base.group_user,1,1,1,1
    ''',

    "views/templates.xml": '''<odoo>
    <data>
<!--
        <template id="listing">
          <ul>
            <li t-foreach="objects" t-as="object">
              <a t-attf-href="#{{ root }}/objects/#{{ object.id }}">
                <t t-esc="object.display_name"/>
              </a>
            </li>
          </ul>
        </template>
        <template id="object">
          <h1><t t-esc="object.display_name"/></h1>
          <dl>
            <t t-foreach="object._fields" t-as="field">
              <dt><t t-esc="field"/></dt>
              <dd><t t-esc="object[field]"/></dd>
            </t>
          </dl>
        </template>
-->
    </data>
</odoo>
    ''',  

    "views/views.xml": '''<odoo>
  <data>
    <!-- explicit list view definition -->
<!--
    <record model="ir.ui.view" id="{module_name}.list">
      <field name="name">{module_name}.list</field>
      <field name="model">{module_name}.{module_name}</field>
      <field name="arch" type="xml">
        <list>
          <field name="name"/>
          <field name="value"/>
          <field name="value2"/>
        </list>
      </field>
    </record>
-->

    <!-- actions opening views on models -->
<!--
    <record model="ir.actions.act_window" id="{module_name}.action_window">
      <field name="name">{module_name} window</field>
      <field name="res_model">{module_name}.{module_name}</field>
      <field name="view_mode">list,form</field>
    </record>
-->

    <!-- server action to the one above -->
<!--
    <record model="ir.actions.server" id="{module_name}.action_server">
      <field name="name">{module_name} server</field>
      <field name="model_id" ref="model_{module_name}_{module_name}"/>
      <field name="state">code</field>
      <field name="code">
        action = {{
          "type": "ir.actions.act_window",
          "view_mode": "list,form",
          "res_model": model._name,
        }}
      </field>
    </record>
-->

    <!-- Top menu item -->
<!--
    <menuitem name="{module_name}" id="{module_name}.menu_root"/>
-->
    <!-- menu categories -->
<!--
    <menuitem name="Menu 1" id="{module_name}.menu_1" parent="{module_name}.menu_root"/>
    <menuitem name="Menu 2" id="{module_name}.menu_2" parent="{module_name}.menu_root"/>
-->
    <!-- actions -->
<!--
    <menuitem name="List" id="{module_name}.menu_1_list" parent="{module_name}.menu_1"
              action="{module_name}.action_window"/>
    <menuitem name="Server to list" id="{module_name}" parent="{module_name}.menu_2"
              action="{module_name}.action_server"/>
-->
  </data>
</odoo>
''',    
}


def create_module(module_name, target_path):
    camel_name = ''.join(word.capitalize() for word in module_name.split('_'))
    module_path = os.path.join(target_path, module_name)
    if os.path.exists(module_path):
        print(f"❌ El módulo '{module_name}' ya existe en '{target_path}'")
        return

    os.makedirs(module_path)
    for relative_path, content in MODULE_TEMPLATE.items():
        file_path = os.path.join(module_path, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            try:
                f.write(content.format(module_name=module_name, camel_name=camel_name))
            except KeyError as e:
                print(f"❌ Error al procesar '{relative_path}': {e}")
                raise


    print(f"✅ Módulo '{module_name}' creado en: {module_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python odoo_scaffold.py nombre_modulo ruta_destino")
        sys.exit(1)

    module_name = sys.argv[1]
    if not module_name.isidentifier():
        print("❌ El nombre del módulo contiene caracteres no válidos.")
        sys.exit(1)
    target_path = os.path.abspath(sys.argv[2])
    create_module(module_name, target_path)
