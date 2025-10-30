from dating.candidates.entities import Candidate
from dating.pools.redis import RedisPool


class CandidatePool(RedisPool[Candidate]):
    pool_obj_type = Candidate
