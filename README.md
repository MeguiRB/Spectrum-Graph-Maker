# Spectrum Graph Maker
## GUI that plots Transmittance, Reflectance, Absorption and Absorbance graphs
### Make a Plot from scratch
You can pick a folder with all the csv files. With the folder and optical parameter selected, you can click on submit to show the corresponding files in the list box.
From these, you can pick which you want to use to make a graph. A new plot window is then created. 

#### Examples
<img src = "/images/transmittance_plot.png" width ="250" /> <img src = "/images/reflectance_plot.png" width ="250" /> <img src = "/images/absorption_plot.png" width ="250" />

You have to take into account that the file name identifies which property (transmittance, reflectance, absorption or absorbance) its values corresponds to. For example, if it has 'TT' in it, it corresponds to a transmittance file (e.g., '### TT.csv').
Moreover, in the case of absorption, because it's calculated using transmittance and reflectance values, to properly pair the files, the name of these without the optical property (TT, R) should be the same (e.g., 'S001 TT.csv' and 'S001 R.csv').
* Transmittance - TT, 
* Reflectance - R,
* Absorption - TT, R. 
  * The absorption is calculated with the following formula:  Absorption(%) = 100 - Transmittance(%) - Reflectance (%)
* Absorbance - Abs 

You can edit the plot. In the first tab, it's possible to set the title and the axis range.
The second tab is to edit the plot lines (color, width, style) and the legend (text, font size, position, framing and number of columns).

There is also an option to save the data. Just input the file name (extension not needed) and the graph is saved in png and pickle formats.

<img src = "/images/GUI_tab1.png" width ="400" /> <img src = "/images/GUI_tab2.png" width ="400" />

### Open a pickle file
The pickle files allow to edit the plot later on. In the menu, there is the option 'Open pickle file'. 
Click on it to choose the file and the plot window will open.