Powerglove
=============

Powerglove is a daemon that wraps up the data output by the CurrentCost power monitoring  devices in a 
lovely HTTP API. So lovely it's practically made of cotton wool and kittens. Kittens that died so you 
can save money on your energy bill. I hope you're happy now.

In it's simplest form it obediently slurps in the data the CurrentCost meter is shoving down the serial
cable and logs it in an RRD file for you to do as you please. But it does a lot more.

So we all like graphs, right? Yeaaah, go graphs. Let's get a graph of the energy usage for the last 
hour in our house:

    http://192.168.0.1:8080/Graph

But wait, I want the last DAY damnit!

    http://192.168.0.1:8080/Graph?back=86400

?back= allows us to specify a time period to look at before now, it's specified in seconds.

There's a bump in that graph though, I think it might be the electric heater turning on. Let's see
if it was:

    http://192.168.0.1:8080/Graph?back=86400&type=temp

And now we have a graph of the temperature in the room that the CurrentCost meter lives in over
the last day.

You can specify various options for the graphs, like &title=name, &width=px and &height=px.

That's all very nice, but we're developers here, we want the damn DATA, screw the graphs.

    $ lynx -dump http://192.168.0.1:8080/Json?back=60

    {start: 1267912620, end: 1267912686, step: 6, data: [
    {timestamp: 1267912620, watts: 572.000000, temp: 20.200000},
    {timestamp: 1267912626, watts: 565.000000, temp: 20.150000},
    {timestamp: 1267912632, watts: 558.000000, temp: 20.100000},
    {timestamp: 1267912638, watts: 558.000000, temp: 20.150000},
    {timestamp: 1267912644, watts: 555.000000, temp: 20.200000},
    {timestamp: 1267912650, watts: 555.000000, temp: 20.200000},
    {timestamp: 1267912656, watts: 548.750000, temp: 20.200000},
    {timestamp: 1267912662, watts: 548.750000, temp: 20.200000},
    {timestamp: 1267912668, watts: 547.000000, temp: 20.200000},
    {timestamp: 1267912674, watts: 550.000000, temp: 20.200000},
    {timestamp: 1267912680, watts: 0.000000, temp: 0.000000}
    ]}

Hurrah for JSON! The start and end times are the period this is over, the step is the resolution of the
data (6 second increments for recent data). Let's get some data from a few hours ago and see what that's
like shall we:

    $ lynx -dump http://192.168.0.1:8080/Json?start=1267894740&end=1267895040

    {start: 1267894740, end: 1267895070, step: 30, data: [
    {timestamp: 1267894740, watts: 339.000000, temp: 20.700000},
    {timestamp: 1267894770, watts: 345.481481, temp: 20.792593},
    {timestamp: 1267894800, watts: 345.238519, temp: 20.776741},
    {timestamp: 1267894830, watts: 343.420639, temp: 20.730484},
    {timestamp: 1267894860, watts: 340.036530, temp: 20.799087},
    {timestamp: 1267894890, watts: 340.036530, temp: 20.799087},
    {timestamp: 1267894920, watts: 340.036530, temp: 20.799087},
    {timestamp: 1267894950, watts: 340.036530, temp: 20.799087},
    {timestamp: 1267894980, watts: 340.036530, temp: 20.799087},
    {timestamp: 1267895010, watts: 340.036530, temp: 20.799087},
    {timestamp: 1267895040, watts: 340.036530, temp: 20.799087}
    ]}

You'll notice that the step has increased to 30 seconds now, indicating that these values are averaged over
30 seconds. Also notice that you specify unix timestamps for a time range to view.

If you want to write webapps with this data, you need to get it into the browser... let's see what JSONP looks like.

    $ lynx -dump http://192.168.0.1:8080/Json?back=10&jsonp=callbackMethod

    callbackMethod(
    {start: 1267913082, end: 1267913100, step: 6, data: [
    {timestamp: 1267913082, watts: 480.666667, temp: 20.500000},
    {timestamp: 1267913088, watts: 0.000000, temp: 0.000000},
    {timestamp: 1267913094, watts: 0.000000, temp: 0.000000}
    ]}
    );

But lets say you want an excuse to play in excel (Yay pivot tables!). Lets see what the powerglove can do for you:

    $ lynx -dump http://192.168.0.1:8080/Tsv?back=60

    Timestamp   Watts   Temp
    1267911936  465.000000  20.300000
    1267911942  464.333333  20.300000
    1267911948  461.000000  20.300000
    1267911954  462.000000  20.300000
    1267911960  464.666667  20.233333
    1267911966  464.666667  20.233333
    1267911972  466.333333  20.200000
    1267911978  467.333333  20.200000
    1267911984  465.333333  20.233333

Mmmm, lovely Tab-seperated-values.

And that's about it so far. All the output formats are plugins, it's simple to add new ones.


Publishers
----------

Based on the original work I (ka2er) have added initial support to add external plotting hosting solution.

In order to activate them you need to add a section in the config file with the publisher name
and a key "Enabled" valued to true.

Examples :

    [plotwatt]
    enabled = True

    [echo]
    enabled = True

    [myenersave]
    enabled = True

You can add other externals solutions.
The refresh rate must be set in the plugin and must be expressed in seconds.

Current plugins are :

- echo : just echo the reading
- plotwatt : send to your plotwatt.com account
- myenersave : send to your myenersave.com account

Don't hesitate to fork, develop your own plugin and pull request to get it merged !


Example Apps
------------
I've shoved a few quick example apps in /examples/

1. powergraphs.html is a page of graphs generated by Powerglove showing your power usage over various time periods.

2. powermeter.html is a page that live-updates your current watt-usage every 30 seconds using the JSON data.

3. googlechart.html is an example of using the JSON history data with google graphs instead of the internal graphing.


Running Powerglove
------------------
Powerglove was intentionally written to use as few non-standard modules as possible, the only one you'll need is the
python RRDTool bindings - it's packaged for most systems.


I love the Powerglove
---------------------
It's so bad. Yes this was mostly an excuse to validly call something Powerglove.

(If you have no idea what I'm talking about: http://www.youtube.com/watch?v=Ya0F83Bmbl4 )
