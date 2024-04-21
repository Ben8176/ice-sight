# Ice Sight

## Inspiration
In 1994, an ATR-72 holding in icing conditions crashed near Roselawn, Indiana resulting in the deaths of all 68 people on board. More recently, a pilot near Los Angeles died last week when icing caused him to lose control of his aircraft. 

The weight of the accumulated ice disrupts the airflow around the wings and tail surfaces. The ice changes the airfoil cross section and destroys lift, increases drag and raises the stalling speed.

Tragically, in both cases, no icing Inflight Weather Advisories were in place for the region.

This begs the question - how can we better predict and warn pilots of dangerous icing conditions to prevent more needless deaths? IceSight is our answer. By leveraging satellite imagery and machine learning, we aim to provide high-fidelity, localized, predictive icing condition forecasts to give pilots advanced warning of hazardous airspace.

## What it does
IceSight ingests near real-time multispectral imagery from NOAA's GOES-R geostationary satellites. By applying carefully tuned weightings to the satellite's 16 sensor bands, we identify the locations and altitudes of clouds most likely to pose an icing risk. Key parameters include the Advanced Baseline Imager's cloud top temperature, cloud particle size, and total precipitable water products.

To provide localized context, IceSight fuses the satellite data with readings from a distributed network of FAA weather stations. An unsupervised learning model, trained on historical data from a dozen California weather stations, learns the regional patterns preceding icing events. The result is a icing risk heatmap, offering much finer spatial granularity than today's advisories.

## Why it's a game-changer 
Currently, pilots rely on icing SIGMETs (Significant Meteorological Information notices) to avoid dangerous conditions. However, these warnings have critical limitations:

Updated only once every 6 hours
Spans at least 3,000 square miles
Provides only binary risk indication
Issued on a national vs local level
Reactive rather than predictive

In contrast, IceSight updates every 5 minutes with the latest satellite data. It provides neighborhood-level resolution, with risk levels expressed as a continuous gradient. The ML model learns from local weather patterns to predict conditions in advance. Most importantly, it aims to highlight dangerous icing that current systems miss.

## How we built it
The key steps of the IceSight data pipeline are:

Ingest raw data from GOES-R imagery hosted on AWS S3 using the S3FS library
Extract the spatial area of interest and calculate a latitude/longitude grid using Numpy and Xarray
Apply weightings to relevant sensor bands - cloud top temperature, particle size, precipitable water vapor
Combine with data from local weather stations and feed into an unsupervised anomaly detection model
Render the model's risk gradient output as a heatmap layer using Matplotlib and Cartopy
To validate the system, we compared IceSight's historical predictions to actual icing-related aviation incidents that occurred outside of SIGMET advisory zones. Our goal was to "light up" hazardous conditions that current systems fail to catch.

## Challenges we ran into
Obtaining "ground truth" for training and validation was a key challenge. Aviation incident reports often lack the full meteorological context needed to correlate them with our predictors. We ultimately relied on a set of NTSB accident investigation reports that contained detailed icing data.

The other challenge was avoiding alert fatigue. If IceSight is overly sensitive, it will inundate pilots with false alarms that are ultimately ignored. We had to carefully tune the model to find the optimal balance between hit rate and false alarm rate.

## Accomplishments that we're proud of
Figuring out how to tap into the firehose of GOES-R data and wrangle it for our purposes felt like a major accomplishment. The satellites collect over a terabyte per day! Being able to query the exact datasets we needed and feed them into our model pipeline was a huge win.

The other exciting milestone was when we were first able to overlay IceSight's risk gradient on a map and compare it to historical SIGMET polygons. Seeing the system highlight hazardous conditions missed by current advisories was a very rewarding "aha" moment.

## What we learned

We talked to an engineer for fixed wing aircraft and he helped us identify the three largest contributors to icing dangers. From a meteorological perspective, we learned that icing risk is highest when supercooled liquid water and droplets larger than ~50 micrometers are present, typically below 12,000 ft in "layer type" clouds. This helped inform the features and weightings fed into our model.

On the technical side, we gained experience working with xarray, numpy, and matplotlib to process complex multidimensional scientific data. Fusing the various data sources required careful geospatial data alignment.

## What's next for IceSight
The natural next step is to validate IceSight against a larger historical dataset in partnership with the FAA. This will allow us to further refine the model weightings for optimal performance.

Ultimately, we envision IceSight being made available as an advisory tool for air traffic controllers, who can use it to supplement existing flight safety systems. It could also be delivered as a mobile app for pilots to check conditions at a glance before takeoff. By providing a clearer picture of icing risks, we hope to make aviation safer for all who travel by air.
