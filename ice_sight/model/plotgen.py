import xarray as xr 
import s3fs
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from PIL import Image

bucket_name = "noaa-goes17"
product_name = "ABI-L2-MCMIPC"
year = 2021
day_of_year = 0
hour = 0
band = 5

def generate_plot_images():

    pngs = ["ice_sight/model/1.png", "ice_sight/model/2.png", "ice_sight/model/3.png", "ice_sight/model/4.png", "ice_sight/model/5.png", "ice_sight/model/6.png", "ice_sight/model/7.png", "ice_sight/model/8.png", "ice_sight/model/9.png", "ice_sight/model/10.png"]
    # i = 2

    # ncArray = [
    #     "ABI-L2-TPWC/2023/001/10/OR_ABI-L2-TPWC-M6_G17_s20230011001176_e20230011003549_c20230011005402.nc",
    #     "ABI-L2-TPWC/2023/001/11/OR_ABI-L2-TPWC-M6_G17_s20230011101176_e20230011103549_c20230011105379.nc",
    #     "ABI-L2-TPWC/2023/001/12/OR_ABI-L2-TPWC-M6_G17_s20230011201176_e20230011203549_c20230011205477.nc",
    #     "ABI-L2-TPWC/2023/001/13/OR_ABI-L2-TPWC-M6_G17_s20230011301176_e20230011303549_c20230011305509.nc",
    #     "ABI-L2-TPWC/2023/001/14/OR_ABI-L2-TPWC-M6_G17_s20230011401177_e20230011403550_c20230011405529.nc",
    #     "ABI-L2-TPWC/2023/001/15/OR_ABI-L2-TPWC-M6_G17_s20230011501177_e20230011503550_c20230011505431.nc",
    #     "ABI-L2-TPWC/2023/001/16/OR_ABI-L2-TPWC-M6_G17_s20230011601177_e20230011603550_c20230011605435.nc",
    #     "ABI-L2-TPWC/2023/001/17/OR_ABI-L2-TPWC-M6_G17_s20230011701177_e20230011703550_c20230011705480.nc",
    #     "ABI-L2-TPWC/2023/001/18/OR_ABI-L2-TPWC-M6_G17_s20230011801177_e20230011803550_c20230011805591.nc",
    #     "ABI-L2-TPWC/2023/001/19/OR_ABI-L2-TPWC-M6_G17_s20230011901177_e20230011903550_c20230011906022.nc",
    # ]

    # fs = s3fs.S3FileSystem(anon=True)
    # shapefile_path = "ice_sight\model\sigmets_202301010000_202302010000.dbf"
    # arrayOften = np.empty(10, dtype=object)

    # # Assuming you have already run the previous code snippet to create the filtered_subset plot
    # import geopandas as gpd

    # # do this ten times
    # # shapefile_path = "jan12023/sigmets_202301010000_202302010000.shp"
    # gdf = gpd.read_file(shapefile_path)
    # gdf = gdf.sort_values(by="ISSUE")

    # from matplotlib.colors import LinearSegmentedColormap

    # # Create a colormap that goes from transparent to red
    # colors = [(1, 0, 0, 0), (1, 0, 0, 1)]  # R -> G -> B -> Alpha
    # cmap_name = 'transparent_to_red'
    # cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

    # arrayOften2 = [None] * 10  # Initialize an array of size ten

    # for i in range(0, 10):

    #     f = fs.open("s3://noaa-goes17/{f}".format(f=ncArray[i]))
    #     ds = xr.open_dataset(f)
    #     ds = calc_latlon(ds)
    #     lats = (30, 55)
    #     lons = (-152, -112)

    #     ((x1, x2), (y1, y2)) = get_xy_from_latlon(ds, lats, lons)
    #     subset = ds.sel(x=slice(x1, x2), y=slice(y2, y1))

    #     fig = plt.figure(figsize=(8, 5))  # Create a new figure for each index

    #     # Define the variable
    #     variable = "TPW"

    #     # Find the 50th percentile value
    #     quantile_value = subset[variable].quantile(0.50)

    #     # Filter the data to only include values larger than the 50th percentile
    #     filtered_subset = subset[variable].where(subset[variable] > quantile_value)

    #     p = filtered_subset.plot(
    #         x="lon",
    #         y="lat",
    #         subplot_kws={"projection": ccrs.Orthographic(-119.4179, 36.7783)},
    #         # subplot_kws={'projection': ccrs.AlbersEqualArea(central_longitude=-96, central_latitude=37.5)},
    #         transform=ccrs.PlateCarree(),
    #         cmap=cm,  # Use the custom colormap
    #     )

    #     # Get the current issue time (replace 'frame' with the appropriate value)
    #     current_issue = gdf.iloc[i]["ISSUE"]

    #     # Filter the GeoDataFrame to include only the shapes active at the current issue time
    #     current_shapes = gdf[
    #         (gdf["ISSUE"] <= current_issue) & (gdf["EXPIRE"] > current_issue)
    #     ]

    #     # Add the current shapes to the existing plot
    #     # current_shapes.plot(ax=p.axes, markersize=5, color='blue')
    #     # Add the current shapes to the existing plot with 50% opacity
    #     current_shapes.plot(
    #         ax=p.axes, markersize=5, color="blue", alpha=0.5, transform=ccrs.PlateCarree()
    #     )
    #     # Update the plot title to include the current issue time
    #     p.axes.set_title(f"Filtered Subset and Shapefile Data\nIssue: {current_issue}")

    #     p.axes.set_extent(
    #         [-125, -114, 32, 42], ccrs.Geodetic()
    #     )  # Approximate coordinates of California
    #     # p.axes.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())  # Approximate extent of the continental US

    #     p.axes.add_feature(cfeature.COASTLINE)
    #     p.axes.add_feature(cfeature.STATES)
    #     p.axes.add_feature(cfeature.BORDERS, linestyle=":")
    #     # p.axes.add_feature(cfeature.LAKES, alpha=0.5)
    #     # p.axes.add_feature(cfeature.RIVERS)
    #     # Display the updated plot
    #     # plt.tight_layout()
    #     plt.show()
    #     arrayOften[i] = p

    images = [] 

    for p in pngs:
        with Image.open(p) as img:
            # Save the image to a BytesIO object in PNG format
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Encode the image data in base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Append the base64 string to the list, formatted as a data URL
            images.append(f"data:image/png;base64,{image_base64}")

    # for j in range(1, len(arrayOften)):

    #     # Save to BytesIO object and encode in base64
    #     buffer = BytesIO()
    #     arrayOften[j].savefig(buffer, format="png")
    #     plt.close(arrayOften[j])
    #     buffer.seek(0)
    #     image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    #     images.append(f"data:image/png;base64,{image_base64}")
    return images


def calc_latlon(ds):
    # The math for this function was taken from
    # https://makersportal.com/blog/2018/11/25/goes-r-satellite-latitude-and-longitude-grid-projection-algorithm

    x = ds.x
    y = ds.y
    goes_imager_projection = ds.goes_imager_projection

    x, y = np.meshgrid(x, y)

    r_eq = goes_imager_projection.attrs["semi_major_axis"]
    r_pol = goes_imager_projection.attrs["semi_minor_axis"]
    l_0 = goes_imager_projection.attrs["longitude_of_projection_origin"] * (np.pi / 180)
    h_sat = goes_imager_projection.attrs["perspective_point_height"]
    H = r_eq + h_sat

    a = np.sin(x) ** 2 + (
        np.cos(x) ** 2 * (np.cos(y) ** 2 + (r_eq**2 / r_pol**2) * np.sin(y) ** 2)
    )
    b = -2 * H * np.cos(x) * np.cos(y)
    c = H**2 - r_eq**2

    r_s = (-b - np.sqrt(b**2 - 4 * a * c)) / (2 * a)

    s_x = r_s * np.cos(x) * np.cos(y)
    s_y = -r_s * np.sin(x)
    s_z = r_s * np.cos(x) * np.sin(y)

    lat = np.arctan(
        (r_eq**2 / r_pol**2) * (s_z / np.sqrt((H - s_x) ** 2 + s_y**2))
    ) * (180 / np.pi)
    lon = (l_0 - np.arctan(s_y / (H - s_x))) * (180 / np.pi)

    ds = ds.assign_coords({"lat": (["y", "x"], lat), "lon": (["y", "x"], lon)})
    ds.lat.attrs["units"] = "degrees_north"
    ds.lon.attrs["units"] = "degrees_east"

    return ds


def get_xy_from_latlon(ds, lats, lons):
    lat1, lat2 = lats
    lon1, lon2 = lons

    lat = ds.lat.data
    lon = ds.lon.data

    x = ds.x.data
    y = ds.y.data

    x, y = np.meshgrid(x, y)

    x = x[(lat >= lat1) & (lat <= lat2) & (lon >= lon1) & (lon <= lon2)]
    y = y[(lat >= lat1) & (lat <= lat2) & (lon >= lon1) & (lon <= lon2)]

    return ((min(x), max(x)), (min(y), max(y)))
