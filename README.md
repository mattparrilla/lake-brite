#Lake Brite

Creating visualizations using the 7,500 node LED matrix at Burlington's [ECHO Center](http://www.echovermont.org/).

##Lake Brite Animation Generator

Generate animations for Lake Brite with [this web application](https://lake-brite.herokuapp.com/)

![LakeBrite display](/static/lb.gif)

##About The Display

The LED matrix is approximately 24ft wide by 9ft tall by 5ft deep. In terms of LED nodes, this translates to 50x15x10.

![LakeBrite display schematics](http://i.imgur.com/oMijoMz.png)

Each node is capable of being programmed to display 8-bit RGB colors.

##Programming The Display

The LED matrix expects a series of GIFs as its input. Each GIF contains the entire state of the matrix at any given time and the display is animated by looping through a series of GIFs.

This is a bit contrary to how we normally think of GIFs (as containing a complete animation). Instead, each GIF is basically a frame of the 3D display.

Each individual GIF must be 50x15 in size and contain 10 frames. The first frame represents the front 50x15 slice of the display, the second from is the slice behind that, and so on.

![LakeBrite interface design](http://i.imgur.com/LkX8dku.png)

In order to animate the display, a series of GIFs of these dimensions and frame length must be passed along.

##Low-Res Lake Champlain

Not necessarily going to get to use, but here's a super low-res (50x10) image of Lake Champlain I whipped up!

![Low Resolution Lake Champlain](http://i.imgur.com/imHm5dR.png)
