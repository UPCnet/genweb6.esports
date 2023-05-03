# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import genweb6.esports


class Genweb6EsportsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=genweb6.esports)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'genweb6.esports:default')


GENWEB6_ESPORTS_FIXTURE = Genweb6EsportsLayer()


GENWEB6_ESPORTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEB6_ESPORTS_FIXTURE,),
    name='Genweb6EsportsLayer:IntegrationTesting',
)


GENWEB6_ESPORTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEB6_ESPORTS_FIXTURE,),
    name='Genweb6EsportsLayer:FunctionalTesting',
)


GENWEB6_ESPORTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        GENWEB6_ESPORTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='Genweb6EsportsLayer:AcceptanceTesting',
)
