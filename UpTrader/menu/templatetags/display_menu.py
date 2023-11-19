from django import template
from menu import models

register = template.Library()


class TreeMenuItem:
    def __init__(
            self,
            pk: int,
            name: str,
            menu_id: int,
            parent_id: int,
            has_children: int,
    ):
        self.id = pk
        self.name = name
        self.menu_id = menu_id
        self.parent_id = parent_id
        self.has_children = True if has_children else False
        self.children = []


def get_tree_menu_items(items: list):
    storage = {item.pk: TreeMenuItem(
            item.pk,
            item.name,
            item.menu_id,
            item.parent_id,
            item.has_children if hasattr(item, 'has_children') else True,
        ) for item in items}
    result: list[TreeMenuItem] = []
    for item in items:

        if item.parent_id is None:
            result.append(storage[item.pk])
        else:
            storage[item.parent_id].children.append(storage[item.pk])

    return result


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, name):
    selected_item = context['selected_item']
    if selected_item is None:
        menu_items = list(
            models.MenuItem.objects.filter(menu__name=name)
            .filter(parent=None)
        )
    else:
        menu_items = list(models.MenuItem.objects.raw(
            """
            WITH RecTree(id, name, menu_id, parent_id, has_children) AS (  
            
                SELECT item.id, item.name, item.menu_id, item.parent_id, 
                        CASE
                            WHEN EXISTS (SELECT 1 FROM menu_menuitem ch WHERE ch.parent_id = item.id) 
                                THEN 1
                                ELSE 0
                        END
                FROM menu_menuitem item  
                JOIN menu_menu ON menu_menu.id = item.menu_id  
                WHERE menu_menu.name = %(menu)s AND item.parent_id = %(item)s
                
                UNION ALL
                
                SELECT item3.id, item3.name, item3.menu_id, item3.parent_id, 
                        CASE
                            WHEN EXISTS (SELECT 1 FROM menu_menuitem ch WHERE ch.parent_id = item3.id) 
                                THEN 1
                                ELSE 0
                        END  
                FROM RecTree rec  
                JOIN menu_menuitem item2 ON rec.parent_id = item2.id  
                JOIN menu_menuitem item3 ON item3.parent_id = item2.parent_id 
                    OR item3.parent_id is null
                JOIN menu_menu ON menu_menu.id = item3.menu_id
                WHERE menu_menu.name = %(menu)s
            )  
            SELECT DISTINCT * FROM RecTree
            """,
            {"menu": name, "item": context['selected_item']},
        ))

    tree_items = get_tree_menu_items(menu_items)

    return {"menu_items": tree_items}
