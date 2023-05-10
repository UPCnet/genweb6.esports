from plone.app.contentmenu.interfaces import IActionsMenu
from plone.app.contentmenu.interfaces import IActionsSubMenuItem
from plone.app.contentmenu.menu import BrowserMenu
from plone.app.contentmenu.menu import BrowserSubMenuItem
from zope.interface import implementer
from zope.security import checkPermission
from plone import api



@implementer(IActionsSubMenuItem)
class SyncContentSubMenuItem(BrowserSubMenuItem):

    title = 'Content management'
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

        #Obtain SyncFolders. 1 SyncFolder - 1  Submenu Item
        sync_folders = self.query_catalog()
        for s_folder in sync_folders:
            menu.append({
                'title': s_folder.title,
                'description': '',
                'action': s_folder.absolute_url() + '/folder_contents',
                'selected': False,
                'extra': {
                    'separator': None,
                    'class': 'toolbar-sync-content-item'
                }
            })

        menu.append({
            'title': 'Sync Content',
            'description': '',
            'action': url + '/sync_all_content',
            'selected': False,
            'extra': {
                'separator': None,
                'class': 'toolbar-sync-content-item-button'
            }
        })

        """ 
        menu = [
            {
                'title': 'Installations',
                'description': '',
                'action': f'{url}/gestio/instalacions',
                'selected': False,
                'extra': {
                    'separator': None,
                    'class': 'toolbar-sync-content-item'
                }
            },
            {
                'title': 'Comeptitions',
                'description': '',
                'action': f'{url}/gestio/comepticions',
                'selected': False,
                'extra': {
                    'separator': None,
                    'class': 'toolbar-sync-content-item'
                }
            },
            {
                'title': 'Activities',
                'description': '',
                'action': f'{url}/gestio/activitats',
                'selected': False,
                'extra': {
                    'separator': None,
                    'class': 'toolbar-sync-content-item'
                }
            }
        ]
        """
        return menu
    
    def query_catalog(self):
        catalog = api.portal.get_tool('portal_catalog')
        params = {'portal_type': 'SyncFolder', 'review_state': 'published'}

        brains = catalog.searchResults(**params)
        return [brain.getObject() for brain in brains]
