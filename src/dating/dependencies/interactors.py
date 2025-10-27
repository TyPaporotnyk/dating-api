from dishka import Provider, Scope, provide

from dating.users.interactors.create_user import CreateUserInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    get_user_interactor = provide(CreateUserInteractor)
