from dishka import Provider, Scope, provide

from dating.notifications.workers.email import EmailWorker


class WorkersProvider(Provider):
    scope = Scope.REQUEST

    get_email_worker = provide(EmailWorker)
