from dataclasses import astuple, dataclass
from datetime import date


@dataclass(frozen=True)
class GameRow:
    player_id: int
    game_date: date
    matchup: str
    minutes: float
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    win_loss: str
    field_goal_made: int
    field_goal_attempted: int
    field_goal_three_made: int
    field_goal_three_attempted: int
    free_throw_made: int
    free_throw_attempted: int
    turn_over: int
    season: str

    def to_row(self) -> tuple:
        return (
            self.player_id,
            self.game_date.isoformat(),
            self.matchup,
            self.minutes,
            self.points,
            self.rebounds,
            self.assists,
            self.steals,
            self.blocks,
            self.win_loss,
            self.field_goal_made,
            self.field_goal_attempted,
            self.field_goal_three_made,
            self.field_goal_three_attempted,
            self.free_throw_made,
            self.free_throw_attempted,
            self.turn_over,
            self.season
        )
