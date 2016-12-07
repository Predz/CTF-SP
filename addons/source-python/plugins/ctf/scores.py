'''

    Game score entity manager. Causes the
    game score entity to update whenever
    it tries to reset itself.

'''

## =============== ALL DECLARTION ===================

__all__ = (
    'Manager'
)

## =================== IMPORTS ======================

from filters.entities import EntityIter

## ============== SCORE DECLARTION ==================

class Manager:
    """
    Game score (cs_team_manager) entity wrapper.
    Allows you to manipulate the team scores easily.

    :param str team:
    """

    def __init__(self, team):
        self._team = team
        self._score = 0

        for entity in EntityIter('cs_team_manager'):
            if entity.get_property_string('m_szTeamname') == team:
                self.manager = entity
                break

    @property
    def team(self):
        return self._team

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.manager.set_property_int('m_scoreTotal', value)