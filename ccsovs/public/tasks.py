from background_task import background

@background(schedule=2)
def count_vote_end(election):
    