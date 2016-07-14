from mpl_toolkits.basemap import Basemap

def plotCoors(coor_list):
    lats, longs = [x[0] for x in coor_list], [x[1] for x in coor_list]
    m = Basemap(projection='merc', llcrnrlat=33.8, urcrnrlat=37, llcrnrlon=-85,
                urcrnrlon=-75, lat_ts=20, resolution='l')
    m.drawcoastlines()
    m.drawstates()
    x,y = m(longs, lats)
    m.drawmapboundary()
    m.scatter(x,y)