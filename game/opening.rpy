# The opening contains only monochrome, unoccupied scenery.
label splashscreen:
    if renpy.loadable("movies/opening.webm"):
        $ renpy.movie_cutscene("movies/opening.webm")
    return

label opening_replay:
    if renpy.loadable("movies/opening.webm"):
        $ renpy.movie_cutscene("movies/opening.webm")
    $ renpy.end_replay()
    return
