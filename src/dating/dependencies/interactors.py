from dishka import Provider, Scope, provide

from dating.auth.interactors.create_user import CreateUserInteractor
from dating.auth.interactors.login import LoginUserInteractor
from dating.profiles.interactors.create import CreateProfileInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    get_user_interactor = provide(CreateUserInteractor)
    login_user_interactor = provide(LoginUserInteractor)
    create_user_interactor = provide(CreateProfileInteractor)
