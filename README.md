## An interactive plotting app for experiments

Mostly I don't like tensorflow, so this is what I use instead.


### Data structure

When running an experiment, I keep a dictionary of lists of stats I track at a
certain resolution (per epoch, per update, per every so many updates). In this
dictionary, I always have an entry called **step** to keep track of how many
steps have passed. So every list in a given dictionary has the same length.

### Starting the app

Typically I'll run the app on a remote machine, so first I connect with

`ssh 5000:127.0.0.1:5000 [host address]`

where 5000 is port that [Flask](https://flask.palletsprojects.com/en/1.1.x/) defaults to.

Then on the remote machine I'll run the command
`python app.py`
and navigate to the browser on my local machine (Firefox/Chrome work best).

### Using the app

The top field provides a field to enter paths of jsons to load on the remote
machine. It supports unix path expansion, and any environment variables you might
have defined on the remote machine. Click the top-right update to load the paths
you specify. If you specify multiple paths, it will collate all the json
dictionaries (in my case I use this for comparing different seeds/treatments).

The two dropdowns below the plotting area are for selecting X and Y axis. X axis
is a single option, but Y axis supports multiple selections from any of the keys
in the dictionary of saved stats. You can also use regexes to select many keys 
with the format
`r'[regex body to be filled in]'`

Any keys that the regex matches will be plotted, click the bottom-right update
button to apply any selections to the plot.

The interactive plot is a plotly html file, and there's a button to hide the 
legend (for very verbose legends). You can click on a trace to disable it on the
graph, and double-click on a trace to isolate it (toggle all others).
