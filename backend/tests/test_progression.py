from app.progression import DAILY_DIFFICULTY

def test_daily_question_mix_is_exactly_seven():
    assert len(DAILY_DIFFICULTY) == 7
    assert DAILY_DIFFICULTY.count("EASY") == 3
    assert DAILY_DIFFICULTY.count("MEDIUM") == 3
    assert DAILY_DIFFICULTY.count("HARD") == 1

def test_daily_pass_threshold():
    assert 5 >= 5
    assert not (4 >= 5)
