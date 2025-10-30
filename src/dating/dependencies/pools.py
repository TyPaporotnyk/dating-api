from dishka import Provider, Scope, provide

from dating.candidates.pools import CandidatePool


class PoolProvider(Provider):
    scope = Scope.APP

    get_candidate_pool = provide(CandidatePool)
