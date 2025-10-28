from dishka import Provider, Scope, provide

from dating.auth.interactors.create_user import CreateUserInteractor
from dating.auth.interactors.login import LoginUserInteractor
from dating.photos.interactors.create import CreateProfilePhotoInteractor
from dating.photos.interactors.delete import DeleteProfilePhotoInteractor
from dating.photos.interactors.get_all import GetAllProfilePhotoInteractor
from dating.profiles.interactors.create import CreateProfileInteractor
from dating.profiles.interactors.update import UpdateProfileInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    get_user_interactor = provide(CreateUserInteractor)
    login_user_interactor = provide(LoginUserInteractor)

    create_profile_interactor = provide(CreateProfileInteractor)
    update_prodile_interactor = provide(UpdateProfileInteractor)

    create_profile_photo_interactor = provide(CreateProfilePhotoInteractor)
    get_all_profile_photo_interactor = provide(GetAllProfilePhotoInteractor)
    delete_profile_photo_interactor = provide(DeleteProfilePhotoInteractor)
