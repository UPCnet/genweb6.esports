from plone import api
from plone.app.contentmenu.interfaces import IActionsMenu, IActionsSubMenuItem
from plone.app.contentmenu.menu import BrowserMenu, BrowserSubMenuItem
from zope.interface import implementer
from zope.security import checkPermission
from genweb6.esports.utils import query_catalog


@implementer(IActionsSubMenuItem)
class SyncContentSubMenuItem(BrowserSubMenuItem):

    title = 'Gestió de continguts'
    submenuId = 'sync_content_menu'

    # HTML attrs
    extra = {
        'id': 'toolbar-sync-content-menu',
    }

    order = 70

    @property
    def action(self):
        return 'placeholderurl'

    def available(self):
        if checkPermission('cmf.ModifyPortalContent', self.context):
            return True
        return False

    def selected(self):
        return False


@implementer(IActionsMenu)
class SyncContentMenu(BrowserMenu):

    def getMenuItems(self, context, request):

        url = context.absolute_url()
        menu = []

        # Obtain SyncFolders. 1 SyncFolder - 1  Submenu Item
        sync_folders = query_catalog('SyncFolder')
        for s_folder in sync_folders:
            menu.append({
                'title': s_folder.title,
                'description': '',
                'action': f'{s_folder.absolute_url()}/folder_contents',
                'selected': False,
                'extra': {
                    'separator': None,
                    'class': 'toolbar-sync-content-item'
                }
            })

        # Append Sync Content Button
        menu.append({
            'title': 'Sincronitzar continguts',
            'description': '',
            'action': f'{url}/sync_all_content',
            'selected': False,
            'extra': {
                'separator': None,
                'class': 'btn-primary'  # Not working
            }
        })

        return menu
