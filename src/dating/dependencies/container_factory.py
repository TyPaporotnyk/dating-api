from dishka import make_async_container

from dating.dependencies.base import BaseAppProvider
from dating.dependencies.interactors import InteractorsProvider
from dating.dependencies.repositories import RepositoriesProvider


def make_base_providers():
    return [
        BaseAppProvider(),
        RepositoriesProvider(),
        InteractorsProvider(),
    ]


def make_base_container():
    return make_async_container(*make_base_providers())
